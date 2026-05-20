@echo off
set "BUNDLED_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

where python >nul 2>nul
if not errorlevel 1 goto use_python

where py >nul 2>nul
if not errorlevel 1 goto use_py

if exist "%BUNDLED_PYTHON%" goto use_bundled

echo Python was not found.
echo Install Python from https://www.python.org/downloads/ or add it to your PATH.
exit /b 1

:use_python
python banking_soc_lab.py %*
exit /b %errorlevel%

:use_py
py banking_soc_lab.py %*
exit /b %errorlevel%

:use_bundled
"%BUNDLED_PYTHON%" banking_soc_lab.py %*
exit /b %errorlevel%
