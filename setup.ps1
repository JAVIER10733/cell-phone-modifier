Write-Host "=== Instalando CPM en Windows ===" -ForegroundColor Cyan

# Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -e ".[dev]"

Write-Host "=== ¡Instalación completada! ===" -ForegroundColor Green
Write-Host "Para empezar, ejecuta: python main.py web" -ForegroundColor Yellow