@echo off
call env_setup.bat
cd client
echo Installing dependencies (this may take a few minutes)...
call npm install
echo Starting Dev Server...
npm run dev
