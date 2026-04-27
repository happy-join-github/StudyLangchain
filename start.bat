@echo off
chcp 65001
call venv\Scripts\activate
python clean.py
python code/15model.py

pause