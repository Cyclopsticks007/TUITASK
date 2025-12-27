if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python 3.10+ is required. Please install Python and retry."
    exit 1
}

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .

Write-Host ""
Write-Host "Install complete."
Write-Host "Run with: .\.venv\Scripts\Activate.ps1; tuitask"
