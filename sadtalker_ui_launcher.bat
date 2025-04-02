@echo off
cd /d "%~dp0"
call sadtalker_env\Scripts\activate.bat
python sadtalker_ui.py
pause 