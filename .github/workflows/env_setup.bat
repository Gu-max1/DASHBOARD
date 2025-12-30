@echo off
set "PROJECT_ROOT=%~dp0"
set "NODE_HOME=%PROJECT_ROOT%tools\node-v20.11.0-win-x64"
set "PATH=%NODE_HOME%;%PATH%"
echo Environment Configured. Node version:
node -v
echo NPM version:
npm -v
