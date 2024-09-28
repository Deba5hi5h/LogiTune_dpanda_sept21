@echo off
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )


set DFUPath="%~dp0"
del %DFUPath%\tmp_read.txt
echo start >> %DFUPath%\tmp_read.txt
net stop LogiSyncHandler
net stop LogiSyncMiddleware
net stop LogiSyncProxy
net start LogiSyncHandler
net start LogiSyncMiddleware
net start LogiSyncProxy
echo finish >> %DFUPath%\tmp_read.txt
exit
