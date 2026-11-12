@echo off
setlocal
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
title Ders Ciktisi Kalite Kontrolu - sunucu
echo.
echo  Ders ciktisi kalite kontrolu baslatiliyor.
echo  Modeller yukleniyor, birkac saniye surer...
echo  Tarayici otomatik acilacak: http://127.0.0.1:8765
echo.
echo  KAPATMAK ICIN: bu pencereyi kapatin (ya da Ctrl+C).
echo.
start "" /min cmd /c "timeout /t 8 /nobreak >nul & start http://127.0.0.1:8765"
"C:\Users\Alptekin Zengin\.venvs\yz-final\Scripts\python.exe" "%~dp0sunucu.py"
echo.
echo  Sunucu durdu. Bu pencereyi kapatabilirsiniz.
pause
