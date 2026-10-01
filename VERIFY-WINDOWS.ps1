$ErrorActionPreference = "Stop"
if (-not (Test-Path .\.venv\Scripts\python.exe)) { throw "Missing .venv; run INSTALL-WINDOWS.ps1 first." }
& .\.venv\Scripts\python.exe -m pip install pytest
& .\.venv\Scripts\python.exe -m pytest -q
& .\.venv\Scripts\civic-science.exe --help | Out-Null
Write-Host "PASS: logger tests and CLI availability verified."
Write-Host "This does not validate scientific classification accuracy or authorize classification automation."
