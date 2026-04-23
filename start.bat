@echo off
chcp 65001
call venv\Script\activate
python clean.py
python code/15model.py

pause