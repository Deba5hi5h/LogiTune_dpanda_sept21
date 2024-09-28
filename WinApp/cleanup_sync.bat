@echo off
set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )


set DFUPath="%~dp0"
del %DFUPath%\tmp_read.txt
echo start >> %DFUPath%\tmp_read.txt

net stop LogiSyncHandler
echo %errorlevel%
if !errorlevel! NEQ 0 (
	echo UNABLE TO STOP LogiSyncHandler SERVICE
) else (
	echo *** STOPPED LogiSyncHandler SERVICE ***
)
echo sleep for 5 seconds
ping 127.0.0.1 -n 5 -w 10000 >NUL

net stop LogiSyncMiddleware
echo %errorlevel%

if !errorlevel! NEQ 0 (
	echo UNABLE TO STOP LogiSyncMiddleware SERVICE
) else (
	echo *** STOPPED LogiSyncMiddleware SERVICE ***
)
echo sleep for 5 seconds
ping 127.0.0.1 -n 5 -w 10000 >NUL

net stop LogiSyncProxy
echo %errorlevel%
if !errorlevel! NEQ 0 (
	echo UNABLE TO STOP LogiSyncProxy SERVICE
) else (
	echo *** STOPPED LogiSyncProxy SERVICE ***
)
echo sleep for 5 seconds
ping 127.0.0.1 -n 5 -w 10000 >NUL

sc delete LogiSyncHandler
echo %errorlevel%
if !errorlevel! NEQ 0 (
	echo UNABLE TO DELETE LogiSyncHandler SERVICE
) else (
	echo *** DELETED LogiSyncHandler SERVICE ***
)
echo sleep for 5 seconds
ping 127.0.0.1 -n 5 -w 10000 >NUL

sc delete LogiSyncMiddleware
echo %errorlevel%
if !errorlevel! NEQ 0 (
	echo UNABLE TO DELETE LogiSyncMiddleware SERVICE
) else (
	echo *** DELETED LogiSyncMiddleware SERVICE ***
)
echo sleep for 5 seconds
ping 127.0.0.1 -n 5 -w 10000 >NUL

sc delete LogiSyncProxy
echo %errorlevel%
if !errorlevel! NEQ 0 (
	echo UNABLE TO DELETE LogiSyncProxy SERVICE
) else (
	echo *** DELETED LogiSyncProxy SERVICE ***
)
echo sleep for 5 seconds
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd C:\Program Files (x86)\Logitech\LogiSyncStub

.\LogiSyncStub.exe -remove

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd ..
echo %cd%
rmdir /s /q LogiSyncStub

echo %errorlevel%

if !errorlevel! NEQ 0 (
	echo UNABLE TO DELETE LOGISYNCSTUB FOLDER
) else (
	echo *** DELETED LOGISYNCSTUB FOLDER ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

set utemp=%userprofile%\AppData\Local\Temp
cd %utemp%
echo %cd%

rmdir /s /q LogiSync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE LOGISYNC FROM USER TEMP FOLDER
) else (
	echo *** DELETED LOGISYNC FROM USER TEMP FOLDER ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd %userprofile%\AppData\Roaming

echo %cd%

rmdir /s /q LogiSync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE LOGISYNC FROM ROAMING FOLDER
) else (
	echo *** DELETED LOGISYNC FROM ROAMING FOLDER ***
)

rmdir /s /q Sync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE SYNC FROM ROAMING FOLDER
) else (
	echo *** DELETED SYNC FROM ROAMING FOLDER ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL


cd C:\Windows\Temp
echo %cd%

rmdir /s /q LogiSync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE LOGISYNC FROM WINDOWS TEMP FOLDER
) else (
	echo *** DELETED LOGISYNC FROM WINDOWS TEMP FOLDER ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd C:\Windows\SysWOW64\config\systemprofile\AppData\Local\Logitech
echo %cd%

rmdir /s /q LogiSync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE LOGISYNC FROM WINDOWS SysWOW64 FOLDER
) else (
	echo *** DELETED LOGISYNC FROM WINDOWS SysWOW64 FOLDER ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd C:\Windows\ServiceProfiles\LocalService\AppData\Local\Temp
echo %cd%

rmdir /s /q LogiSync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE LOGISYNC FROM C:\Windows\ServiceProfiles\LocalService\AppData\Local\Temp
) else (
	echo *** DELETED LOGISYNC FROM C:\Windows\ServiceProfiles\LocalService\AppData\Local\Temp ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd C:\ProgramData\Logitech
echo %cd%

rmdir /s /q LogiSync

echo %errorlevel%

if %errorlevel% NEQ 0 (
	echo UNABLE TO DELETE LOGISYNC FROM C:\ProgramData\Logitech
) else (
	echo *** DELETED LOGISYNC FROM C:\ProgramData\Logitech ***
)

echo sleep for 5 seconds
REM timeout /t 5
ping 127.0.0.1 -n 5 -w 10000 >NUL

cd C:\Program Files (x86)\Logitech
echo %cd%

rmdir /s /q LogiSync


echo finish >> %DFUPath%\tmp_read.txt
exit