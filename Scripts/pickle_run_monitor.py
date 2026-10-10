"""Observe a private-desktop RimWorld run, including silent game startup.

Heartbeats are diagnostics only. The caller validates the complete Pickle
summary and Player.log after an exit code of zero.
"""
from pathlib import Path
import os
import subprocess
import time


def _size(path):
    try:
        return path.stat().st_size
    except OSError:
        return None


def _status(report):
    log_bytes = _size(report / "Player.log")
    summary_bytes = _size(report / "summary.json")
    launcher_bytes = _size(report / "launcher.log")
    if log_bytes is None:
        message = "Player.log absent (game may still be starting)"
    else:
        message = "Player.log=" + str(log_bytes) + " bytes"
    if launcher_bytes is not None:
        message += "; launcher.log=" + str(launcher_bytes) + " bytes"
    if summary_bytes is not None:
        message += "; summary.json=" + str(summary_bytes) + " bytes (not yet validated)"
    return message


def _terminate_owned_tree(proc):
    """Stop only the launcher started by this run and its descendants."""
    if proc.poll() is not None:
        return
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=15, check=False,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except (OSError, subprocess.TimeoutExpired):
            pass
    if proc.poll() is None:
        proc.kill()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        raise RuntimeError("Owned private-desktop process could not be terminated")


def run_hidden_with_status(command, *, report, game, env, profile,
                           timeout, heartbeat=15, poll_seconds=1,
                           diagnostic_only=False):
    """Run hidden game and report status until exit or hard deadline.

    The C# launcher itself enforces timeout. This Python watchdog allows 30
    extra seconds for its cleanup, then terminates the owned process tree.
    """
    if not (1 <= timeout <= 3600) or heartbeat <= 0 or poll_seconds <= 0:
        raise ValueError("Invalid hidden-game timeout or heartbeat")
    report = Path(report)
    report.mkdir(parents=True, exist_ok=True)
    print(f"[E2E {profile}] Starting private-desktop RimWorld; "
          f"game timeout={timeout}s; report={report}", flush=True)
    started = time.monotonic()
    next_heartbeat = started + heartbeat
    old_status = None
    proc = None
    with (report / "launcher.log").open("w", encoding="utf-8") as output_log:
        try:
            proc = subprocess.Popen(command, cwd=game, env=env,
                                    stdout=output_log, stderr=subprocess.STDOUT)
            print(f"[E2E {profile}] Private-desktop controller pid={proc.pid}",
                  flush=True)
            deadline = started + timeout + 30
            while True:
                code = proc.poll()
                if code is not None:
                    next_action = ("startup observation ended; no Pickle pass inferred"
                                   if diagnostic_only
                                   else "validating full Pickle report next")
                    print(f"[E2E {profile}] Controller exited code={code} "
                          f"after {int(time.monotonic() - started)}s; "
                          f"{next_action}", flush=True)
                    return code
                now = time.monotonic()
                if now >= deadline:
                    raise TimeoutError(f"{profile}: no controller exit within "
                                       f"{timeout + 30}s; {_status(report)}; "
                                       "owned game/process tree will be stopped")
                if now >= next_heartbeat:
                    state = _status(report)
                    note = "log changed" if state != old_status else "no new log/report bytes"
                    print(f"[E2E {profile}] running {int(now - started)}s; "
                          f"{state}; {note}", flush=True)
                    old_status = state
                    next_heartbeat = now + heartbeat
                time.sleep(min(poll_seconds, max(0.05, deadline - now)))
        except BaseException:
            if proc is not None:
                _terminate_owned_tree(proc)
            raise


def diagnostic_tail(report, max_lines=8):
    """Human-readable source of failure; never interpret partial logs as success."""
    report = Path(report)
    outputs = []
    for name in ("launcher.log", "Player.log"):
        file = report / name
        if not file.is_file():
            outputs.append(name + ": absent")
            continue
        try:
            lines = file.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError as exc:
            outputs.append(name + ": unreadable (" + type(exc).__name__ + ")")
            continue
        # Keep diagnostics bounded even for large installed Mod sets.
        body = " | ".join(line.strip()[:300] for line in lines[-max_lines:])
        outputs.append(name + " (lines=" + str(len(lines)) + "): " + body[:1900])
    summary = report / "summary.json"
    outputs.append("Pickle summary: " + ("present (not validated)" if summary.is_file()
                                          else "absent (game did not finish Pickle)"))
    return "\n".join(outputs)
