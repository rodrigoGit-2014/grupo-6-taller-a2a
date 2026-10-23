@echo off
setlocal EnableExtensions EnableDelayedExpansion

rem ---------------------------------------------------------------------------
rem Grupo 6 - Taller A2A
rem Genera un ZIP reproducible de entrega sin .env ni .venv.
rem Uso: scripts\empaquetar_entrega.bat
rem ---------------------------------------------------------------------------

for %%I in ("%~dp0..") do set "ROOT=%%~fI"
set "STAGE=%TEMP%\grupo-6-taller-a2a-entrega"
set "DIST=%ROOT%\dist"
set "ZIP=%DIST%\grupo-6-taller-a2a-entrega.zip"

echo.
echo [1/4] Preparando carpeta temporal...
if exist "%STAGE%" rmdir /s /q "%STAGE%"
mkdir "%STAGE%" || goto :error

echo [2/4] Copiando archivos permitidos...
robocopy "%ROOT%" "%STAGE%" /E ^
  /XD ".git" ".venv" ".langgraph_api" "__pycache__" ".pytest_cache" ".ipynb_checkpoints" "dist" ^
  /XF ".env" "*.pyc" ^
  /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 goto :error

rem Copia el blueprint de Paulina a la raíz del ZIP, ademas de su ubicacion original.
if not exist "%ROOT%\agente-paulina\blueprint.md" (
  echo ERROR: falta agente-paulina\blueprint.md
  goto :error
)
copy /Y "%ROOT%\agente-paulina\blueprint.md" "%STAGE%\blueprint.md" >nul || goto :error

rem Seguridad adicional: eliminar cualquier .env que hubiera quedado en el stage.
for /r "%STAGE%" %%F in (.env) do if exist "%%F" del /f /q "%%F"

echo [3/4] Creando ZIP...
if not exist "%DIST%" mkdir "%DIST%" || goto :error
if exist "%ZIP%" del /f /q "%ZIP%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "& { $ErrorActionPreference = 'Stop'; Add-Type -AssemblyName System.IO.Compression.FileSystem; $stage = '%STAGE%'; $zip = '%ZIP%'; Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel Optimal; $z = [System.IO.Compression.ZipFile]::OpenRead($zip); $bad = @($z.Entries | Where-Object { $_.FullName -match '(^|/)\.env$' -or $_.FullName -match '(^|/)\.venv/' }); $z.Dispose(); if ($bad.Count -gt 0) { $bad | ForEach-Object { Write-Error ('Archivo prohibido en el ZIP: ' + $_.FullName) }; exit 1 }; Write-Host ('ZIP creado: ' + $zip) }"
if errorlevel 1 goto :error

echo [4/4] Verificando contenido...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "& { Add-Type -AssemblyName System.IO.Compression.FileSystem; $z = [System.IO.Compression.ZipFile]::OpenRead('%ZIP%'); $n = $z.Entries.Count; $z.Dispose(); Write-Host ('Entradas en el ZIP: ' + $n) }"
if errorlevel 1 goto :error

for %%I in ("%ZIP%") do echo Tamano: %%~zI bytes
echo.
echo Listo: "%ZIP%"
echo.
exit /b 0

:error
echo.
echo ERROR: no se pudo generar el ZIP de entrega.
echo Revisa los mensajes anteriores y que no haya archivos bloqueados.
exit /b 1
