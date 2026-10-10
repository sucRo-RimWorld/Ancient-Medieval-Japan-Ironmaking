// Test-only Windows launcher: Unity still renders on a separate WinSta0 desktop.
// No visible fallback. If CreateDesktop/CreateProcess fails, return non-zero.
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Text;

internal static class IronmakingPrivateDesktop
{
    private const uint GENERIC_ALL = 0x10000000;
    private const uint CREATE_NO_WINDOW = 0x08000000;
    private const uint WAIT_OBJECT_0 = 0;
    private const uint WAIT_TIMEOUT = 258;

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    private struct StartupInfo
    {
        public int cb;
        public string reserved;
        public string desktop;
        public string title;
        public int x, y, width, height, charsX, charsY, fill, flags;
        public short show, reservedBytes;
        public IntPtr reservedPtr, input, output, error;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct ProcessInformation
    {
        public IntPtr process, thread;
        public uint pid, tid;
    }

    [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern IntPtr CreateDesktop(string name, IntPtr device,
        IntPtr mode, uint flags, uint access, IntPtr security);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool CloseDesktop(IntPtr desktop);

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true, EntryPoint = "CreateProcessW")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool CreateProcess(string application, StringBuilder command,
        IntPtr processAttributes, IntPtr threadAttributes, bool inheritHandles,
        uint creationFlags, IntPtr environment, string currentDirectory,
        ref StartupInfo startup, out ProcessInformation process);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern uint WaitForSingleObject(IntPtr process, uint milliseconds);

    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool GetExitCodeProcess(IntPtr process, out uint exitCode);

    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool TerminateProcess(IntPtr process, uint exitCode);

    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool CloseHandle(IntPtr handle);

    private static string Quote(string value)
    {
        // Windows CreateProcess command-line escaping for arguments.
        if (value.Length == 0) return "\"\"";
        if (value.IndexOfAny(new[] { ' ', '\t', '\n', '\v', '"' }) == -1)
            return value;
        var result = new StringBuilder("\"");
        int backslashes = 0;
        foreach (char character in value)
        {
            if (character == '\\') { backslashes++; continue; }
            if (character == '"')
            {
                result.Append('\\', backslashes * 2 + 1);
                result.Append('"');
                backslashes = 0;
                continue;
            }
            result.Append('\\', backslashes);
            backslashes = 0;
            result.Append(character);
        }
        result.Append('\\', backslashes * 2);
        result.Append('"');
        return result.ToString();
    }

    public static int Main(string[] args)
    {
        if (args.Length < 3)
        {
            Console.Error.WriteLine("Usage: launcher.exe GAME_EXE GAME_DIR TIMEOUT_SECONDS [GAME_ARGS...]");
            return 2;
        }

        int seconds;
        if (!Int32.TryParse(args[2], out seconds) || seconds < 1 || seconds > 3600)
        {
            Console.Error.WriteLine("Invalid hidden game timeout.");
            return 2;
        }
        string name = "AMJI-Pickle-" + Guid.NewGuid().ToString("N");
        IntPtr desktop = IntPtr.Zero;
        ProcessInformation child = new ProcessInformation();
        bool finished = false;
        try
        {
            desktop = CreateDesktop(name, IntPtr.Zero, IntPtr.Zero, 0,
                                    GENERIC_ALL, IntPtr.Zero);
            if (desktop == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error(),
                "Cannot create separate Windows desktop; visible fallback is forbidden");

            var startup = new StartupInfo();
            startup.cb = Marshal.SizeOf(typeof(StartupInfo));
            startup.desktop = "WinSta0\\" + name;

            var cmd = new StringBuilder(Quote(args[0]));
            for (int i = 3; i < args.Length; ++i) cmd.Append(" ").Append(Quote(args[i]));
            // Environment variables from Python (including selected profile and
            // source path) are inherited. No command shell and no focus stealing.
            bool started = CreateProcess(args[0], cmd, IntPtr.Zero, IntPtr.Zero,
                                         false, CREATE_NO_WINDOW, IntPtr.Zero, args[1],
                                         ref startup, out child);
            if (!started) throw new Win32Exception(Marshal.GetLastWin32Error(),
                "Cannot launch RimWorld on isolated desktop");

            Console.WriteLine("[PRIVATE_DESKTOP] RimWorld pid=" + child.pid +
                              "; graphics enabled; normal desktop unchanged");
            uint wait = WaitForSingleObject(child.process, (uint)seconds * 1000);
            if (wait == WAIT_TIMEOUT) throw new TimeoutException(
                "RimWorld Pickle exceeded hidden desktop timeout");
            if (wait != WAIT_OBJECT_0) throw new Win32Exception(
                Marshal.GetLastWin32Error(), "Failed to wait on hidden RimWorld process");

            finished = true;
            uint status;
            if (!GetExitCodeProcess(child.process, out status))
                throw new Win32Exception(Marshal.GetLastWin32Error(),
                    "Cannot read RimWorld exit code");
            return unchecked((int)status);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine("[PRIVATE_DESKTOP_FAIL] " + ex);
            return 1;
        }
        finally
        {
            if (child.process != IntPtr.Zero && !finished)
            {
                TerminateProcess(child.process, 1);
                WaitForSingleObject(child.process, 10000);
            }
            if (child.thread != IntPtr.Zero) CloseHandle(child.thread);
            if (child.process != IntPtr.Zero) CloseHandle(child.process);
            if (desktop != IntPtr.Zero) CloseDesktop(desktop);
        }
    }
}
