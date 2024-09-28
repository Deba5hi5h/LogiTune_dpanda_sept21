@echo off
title UninstallHelvellyn
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )


set DFUPath="%~dp0"

REM Create the logs directory if it doesn't exist
if not exist "logs\" mkdir "logs\"

for /F "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /F "tokens=1-2 delims=: " %%a in ("%time%") do (set mytime=%%a%%b)
msiexec /x%1 /quiet /qn /l*v logs/uninstall_logs_%mydate%_%mytime%.txt

exit