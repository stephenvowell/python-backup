# Build a standalone Windows executable for Python BackUp (backup_v2.py).
#
#   pip install -r requirements-dev.txt
#   .\build_exe.ps1
#
# Output: dist\PythonBackUp.exe (single-file, no console window).

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name PythonBackUp `
    backup_v2.py

Write-Host ""
Write-Host "Done. Executable is at: $(Join-Path $PSScriptRoot 'dist\PythonBackUp.exe')"
