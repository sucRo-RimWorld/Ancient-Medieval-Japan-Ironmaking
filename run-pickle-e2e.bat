@echo off
setlocal
where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "%~dp0Scripts\run-pickle-e2e.py" %*
) else (
  python "%~dp0Scripts\run-pickle-e2e.py" %*
)
exit /b %ERRORLEVEL%
