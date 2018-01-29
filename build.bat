@echo off
cd /d "%~dp0"
if /i "%1"=="release" (
	transcrypt -b src\madmix.py
	if errorlevel 1 goto error
	if exist html\js rd /s /q html\js
	mkdir html\js
	copy /y src\__javascript__\madmix.min.js html\js\madmix.js
) else (
	transcrypt -n -m -dc -da src\madmix.py
	if errorlevel 1 goto error
	robocopy src\__javascript__ html\js /s /njh /njs
	if errorlevel 8 goto error
)

goto :eof
:error
pause
exit /b 1
