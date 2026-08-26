@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "LM_STUDIO_URL=http://127.0.0.1:1234"
set "LM_STUDIO_MODEL=qwen/qwen3-vl-4b"
python scripts\lmstudio_operator.py
pause
