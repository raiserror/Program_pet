@echo off
chcp 65001 >nul
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║           Таймер обратного отсчета               ║
echo ╚══════════════════════════════════════════════════╝
echo.

echo 📦 Устанавливаем PyInstaller...
pip install pyinstaller

echo.
echo 🔨 Компилируем в EXE...
pyinstaller --name="ContdownTimer" ^
--onefile ^
--windowed ^
--add-data=".;." ^
contdown_timer.py

echo.
echo ✅ Готово! 
echo 📁 EXE файл находится в папке: dist\
echo.

pause