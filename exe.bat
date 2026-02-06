@echo off
setlocal
chcp 65001 >nul

echo ===========================================
echo   AntiYandex Build Script
echo ===========================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден! Установите Python с сайта python.org
    pause
    exit /b
)

echo [1/3] Проверка зависимостей (psutil, pyinstaller)...
python -m pip install --upgrade pip >nul
python -m pip install psutil pyinstaller >nul

echo [2/3] Сборка EXE...
python -m PyInstaller --onefile --windowed --hidden-import=psutil --icon=icon.ico main.py

if %errorlevel% equ 0 (
    echo ===========================================
    echo [3/3] Готово! Файл в папке dist
) else (
    echo [ERROR] Сборка завершилась с ошибкой.
)

pause