# Obtener la ruta del escritorio del usuario actual
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Ruta completa de la carpeta IAGen
$iaGenPath = Join-Path $desktopPath "IAGen"

# Crear la carpeta si no existe
if (-not (Test-Path $iaGenPath)) {
    New-Item -ItemType Directory -Path $iaGenPath
}

# Cambiar al directorio IAGen
Set-Location -Path $iaGenPath

# Ejecutar el comando para crear el entorno virtual con uv
uv venv --python=3.11