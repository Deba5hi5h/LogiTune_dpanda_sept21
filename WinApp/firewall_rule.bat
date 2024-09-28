@echo on
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

set DFUPath="%~dp0"

::set ip_address1=%1
::set ip_address2=%2

::Firewall_Rule.vbs %ip_address1%,%ip_address2%

SET PARAMS=

:_PARAMS_LOOP

::There is a trailing space in the next line; it is there for formatting.
SET PARAMS=%PARAMS%%1,
ECHO %1
SHIFT

IF NOT "%1"=="" GOTO _PARAMS_LOOP

SET ip_addresses=%PARAMS:~0,-1%

firewall_rule.vbs %ip_addresses%

exit


