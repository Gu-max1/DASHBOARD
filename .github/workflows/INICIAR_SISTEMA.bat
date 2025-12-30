@echo off
title Sistema de Inventario Launcher
echo ==========================================
echo   Iniciando Sistema de Control de Inventario
echo ==========================================

:: 1. Iniciar Backend (Python)
echo [1/3] Iniciando Servidor Backend...
start "Backend Server (NO CERRAR)" cmd /k "python server/main.py"

:: 2. Iniciar Frontend (React)
echo [2/3] Iniciando Interfaz Frontend...
:: Usamos call env_setup.bat para cargar el Node.js portable
start "Frontend Client (NO CERRAR)" cmd /k "call env_setup.bat && cd client && echo Iniciando Vite... && npm run dev"

:: 3. El navegador se abrirá automáticamente cuando el sistema esté listo.

echo.
echo ==========================================
echo   !Sistema Iniciado Correctamente!
echo ==========================================
echo.
echo  - Backend API: http://localhost:8001/docs
echo  - Frontend App: http://localhost:3000
echo.
echo NO CIERRES las ventanas negras que se abrieron.
echo Si las cierras, el sistema dejara de funcionar.
echo.
pause
