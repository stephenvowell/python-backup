# Build a standalone Windows executable for Python BackUp (backup_v2.py).
#
#   pip install -r requirements-dev.txt
#   .\build_exe.ps1
#
# Output: dist\PythonBackUp.exe (single-file, no console window).

param(
    [switch]$SkipDesktopCopy
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Get-Process -Name "PythonBackUp" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500

python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name PythonBackUp `
    --hidden-import backup_theme `
    backup_v2.py

$exe = Join-Path $PSScriptRoot "dist\PythonBackUp.exe"
if (-not (Test-Path $exe)) {
    throw "Build failed - $exe not found"
}

if (-not $SkipDesktopCopy) {
    $desktop = [Environment]::GetFolderPath("Desktop")
    $dest = Join-Path $desktop "PythonBackUp.exe"
    Copy-Item -Path $exe -Destination $dest -Force
    Write-Host "Copied to desktop:    $dest"
}

Write-Host ""
Write-Host "Done. Executable is at: $exe"
