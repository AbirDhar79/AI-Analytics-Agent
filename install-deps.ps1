# Install dependencies into venv (run in a NEW terminal with Cursor/IDE closed if you get "file is being used" errors)
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$venvPy = Join-Path $root "venv\Scripts\python.exe"
$pip = Join-Path $root "venv\Scripts\pip.exe"

if (-not (Test-Path $venvPy)) {
    Write-Host "Creating venv..."
    python -m venv (Join-Path $root "venv")
}
Write-Host "Installing packages (streamlit, langchain, groq, etc.)..."
& $pip install streamlit python-dotenv langchain langchain-community langchain-groq SQLAlchemy mysql-connector-python
Write-Host "Done. Run the app with: .\run-app.ps1"
Write-Host "Or: .\venv\Scripts\python.exe -m streamlit run app.py"
