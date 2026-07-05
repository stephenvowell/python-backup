# Build PythonBackUp.exe and a customer-ready release zip.
#
#   pip install -r requirements-dev.txt
#   .\scripts\build-release.ps1
#
# Output:
#   dist\PythonBackUp.exe
#   dist\PythonBackUp-windows.zip

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$ReleaseDir = Join-Path $Root "release"
$Dist = Join-Path $Root "dist"
$Exe = Join-Path $Dist "PythonBackUp.exe"
$Zip = Join-Path $Dist "PythonBackUp-windows.zip"

Push-Location $Root
try {
    Write-Host "Running tests..."
    python -m pytest -q
    if ($LASTEXITCODE -ne 0) { throw "Tests failed" }

    & (Join-Path $Root "build_exe.ps1") -SkipDesktopCopy

    foreach ($name in @("SETUP.txt", "README.txt")) {
        $src = Join-Path $ReleaseDir $name
        if (-not (Test-Path $src)) {
            throw "Missing release file: $src"
        }
    }

    $license = Join-Path $Root "LICENSE"
    if (-not (Test-Path $license)) {
        throw "Missing LICENSE at repo root"
    }

    $Staging = Join-Path $Dist "PythonBackUp-windows"
    if (Test-Path $Staging) { Remove-Item -Recurse -Force $Staging }
    New-Item -ItemType Directory -Path $Staging -Force | Out-Null

    Copy-Item $Exe (Join-Path $Staging "PythonBackUp.exe")
    Copy-Item (Join-Path $ReleaseDir "SETUP.txt") $Staging
    Copy-Item (Join-Path $ReleaseDir "README.txt") $Staging
    Copy-Item (Join-Path $Root "LICENSE") (Join-Path $Staging "LICENSE.txt")

    if (Test-Path $Zip) { Remove-Item -Force $Zip }
    Compress-Archive -Path (Join-Path $Staging "*") -DestinationPath $Zip -Force
    Remove-Item -Recurse -Force $Staging

    Write-Host ""
    Write-Host "Release ready:"
    Write-Host "  $Exe"
    Write-Host "  $Zip"
}
finally {
    Pop-Location
}
