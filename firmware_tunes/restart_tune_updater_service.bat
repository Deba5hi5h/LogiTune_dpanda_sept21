@echo off
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

echo Stopping the service...
sc stop "LogiTuneUpdaterService"

REM Wait until the service is stopped
:wait_for_stop
timeout /t 1 /nobreak > nul
sc query "LogiTuneUpdaterService" | find "STOPPED"
if errorlevel 1 goto wait_for_stop

echo Waiting for 5 seconds...
timeout /t 5 /nobreak > nul

echo Starting the service...
sc start "LogiTuneUpdaterService"

REM Wait until the service is started
:wait_for_start
timeout /t 1 /nobreak > nul
sc query "LogiTuneUpdaterService" | find "RUNNING"
if errorlevel 1 goto wait_for_start

echo Service restart completed.
exit