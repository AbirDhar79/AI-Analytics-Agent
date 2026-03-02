# Run the app (disables usage stats to avoid permission issues with .streamlit folder)
$env:STREAMLIT_BROWSER_GATHER_USAGE_STATS = "false"
$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    & $venvPython -m streamlit run app.py
} else {
    python -m streamlit run app.py
}
