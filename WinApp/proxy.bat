@echo on
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

set DFUPath="%~dp0"
del %DFUPath%\tmp_read.txt
echo start >> %DFUPath%\tmp_read.txt

set setup=%1
set proxy=%2
set instance=%3

set ip_address="172.28.78.218"
set port="3128"
set singlepac="http://swqa-automation-mac.logitech.com/proxy.pac"
set multiplepac="http://swqa-automation-mac.logitech.com/multipleproxy.pac"

IF [%1]==[/?] GOTO :Help

if %setup%==set (call:Setup) else (call:Reset)
exit

:Setup
call:Reset
netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound
if %proxy%==ip (call:ProxyIP) else (call:ProxyPAC)
goto :eof

:Reset
netsh advfirewall set allprofiles firewallpolicy blockinbound,allowoutbound
netsh winhttp reset proxy
Reg Add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
::Reg Add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v AutoConfigURL /t REG_SZ /d %singlepac% /f
Reg Delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v AutoConfigURL /f
echo reset_success >> %DFUPath%\tmp_read.txt
goto :eof

::IP Proxy setup
:ProxyIP
netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound
Reg Add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
Reg Add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d %ip_address%:%port% /f
Reg Add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d <local> /f
netsh winhttp set proxy proxy-server="http=%ip_address%:%port%;https=%ip_address%:%port%"
echo ip_success >> %DFUPath%\tmp_read.txt
goto :eof

::PAC Proxy setup
:ProxyPAC
if %instance%==single (set pac=%singlepac%) else (set pac=%multiplepac%)
Reg Add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings" /v AutoConfigURL /t REG_SZ /d %pac% /f
echo pac_success >> %DFUPath%\tmp_read.txt
goto :eof

::Usage
:Help
echo USAGE: proxy.bat [set/reset] [ip/pac] [single/multiple]
