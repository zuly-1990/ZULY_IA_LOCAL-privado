@echo off
title ZULY IA - Telegram Listener
color 0A
echo Iniciando ZULY Telegram Listener...
set PYTHONPATH=%cd%
set PYTHONIOENCODING=utf-8
python core\external\telegram_listener.py
pause
