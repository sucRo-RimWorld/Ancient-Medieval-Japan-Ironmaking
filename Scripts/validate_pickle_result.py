#!/usr/bin/env python3
"""Fail-closed Pickle summary + RimWorld ERROR log checker."""
import argparse
import json
from pathlib import Path
import re
import sys

EXPECTED = {
    "Exact Ironmaking development source and profile are loaded",
    "Processing Defs and Vanilla or MO result resolve",
    "Native initial ironmaking research gate",
    "Loaded sand trade generators distinguish buying and selling",
    "Natural map creation produces finite iron sand",
    "Natural iron-sand deposit is actually mineable and finite",
    "Colonist mining job consumes finite deposit and yields sand",
    "Sand deposits survive real game save reload",
}
PRODUCTION = {
    "Exact Ironmaking development source and profile are loaded",
    "Loaded fuel component exclusivity",
    "Charcoal bill consumes wood and produces charcoal",
    "Smelting bill consumes sand and charcoal and produces bloom",
    "Optional MO coal fuel and Vanilla isolation",
    "Interrupted smelting conserves resources",
    "Forging bill consumes bloom and produces the profile metal",
}
ERRORS = re.compile(
    r"(?im)^.*(?:\[ERROR\]|Could not resolve cross-reference|XML error|"
    r"Exception during|Error in static constructor).*$"
)


def validate(report, suite="core"):
    expected = {"core": EXPECTED, "production": PRODUCTION}[suite]
    count = len(expected)
    summary_file = report / "summary.json"
    log_file = report / "Player.log"
    if not summary_file.is_file() or not log_file.is_file():
        raise ValueError("Fresh summary.json and Player.log are required in " + str(report))
    try:
        summary = json.loads(summary_file.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Invalid Pickle summary") from exc
    if summary.get("exitReason") != "passed":
        raise ValueError("Pickle exitReason=" + repr(summary.get("exitReason")))
    if any(summary.get(k, -1) != v for k, v in
           (("total", count), ("passed", count), ("failed", 0), ("skipped", 0))):
        raise ValueError("Pickle counts incomplete or failing: " + repr(summary))
    if summary.get("flaky", 0) != 0:
        raise ValueError("Pickle reported flaky scenarios")
    scenarios = summary.get("scenarios", [])
    names = [s.get("name") for s in scenarios if isinstance(s, dict)]
    if len(names) != len(expected) or set(names) != expected:
        raise ValueError("Pickle scenario identity mismatch: " + repr(names))
    if not all(s.get("outcome", "").lower() == "passed"
               for s in scenarios):
        raise ValueError("Pickle scenario outcomes include non-pass")
    log = log_file.read_text(encoding="utf-8-sig", errors="replace")
    matches = ERRORS.findall(log)
    if matches:
        raise ValueError("RimWorld runtime ERROR lines: " + repr(matches[:8]))
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--suite", choices=("core", "production"), default="core")
    args = parser.parse_args()
    try:
        n = validate(args.report, args.suite)
    except (ValueError, OSError) as exc:
        print("[FAIL]", exc, file=sys.stderr)
        raise SystemExit(1)
    print("[PASS]", n, "Pickle scenarios, 0 skipped/flaky/error logs")


if __name__ == "__main__":
    main()
