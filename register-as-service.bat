@echo off
echo Registering this application (QuicKCo) as a service
pause

sc create QuicKCo binPath= "%CD%\startscript.bat" start= auto

echo.
echo If it says "Access denied" above, run the script as Administrator.
echo If it says "SUCCESS" above, close the console or press any key to close it automatically
pause