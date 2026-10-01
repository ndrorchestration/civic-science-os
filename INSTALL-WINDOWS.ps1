$ErrorActionPreference = "Stop"
Write-Host "Civic Science Contribution OS v0.1.0 - Windows bootstrap"
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
  throw "Python launcher 'py' was not found. Install Python 3.10+ first."
}
$version = & py -3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "Python $version"
& py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e .
& .\.venv\Scripts\civic-science.exe init
Write-Host "Installed. Scientific classification remains HUMAN_ONLY."
Write-Host "Run .\\VERIFY-WINDOWS.ps1 to verify the local installation."
