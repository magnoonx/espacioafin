# Script de PowerShell para renderizar fácilmente las animaciones de Manim
param (
    [ValidateSet("l", "m", "h", "k")]
    [string]$Calidad = "l",

    # Modos disponibles:
    [ValidateSet("maestro", "pizarra_robotica", "sin_latex", "3d", "con_latex")]
    [string]$Modo = "maestro",

    # Factor de velocidad opcional para post-procesado con FFmpeg:
    # 0.5 = el doble de rápido, 1.5 = 50% más lento, 2.0 = el doble de lento
    [float]$Velocidad = 1.0
)

# 1. Asegurar activación del entorno virtual si existe
if ($env:VIRTUAL_ENV -eq $null -and (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "[INFO] Activando entorno virtual .venv..." -ForegroundColor Cyan
    & ".\.venv\Scripts\Activate.ps1"
}

# 2. Selección de archivo y escena según el modo
switch ($Modo) {
    "pizarra_robotica" {
        $Archivo = "transformacion_afin_pizarra.py"
        $Escena = "TransformacionAfinPizarra"
        Write-Host "[INFO] Modo: Ejercicio de Robótica en Pizarra Blanca con Marcador" -ForegroundColor Cyan
    }
    "maestro" {
        $Archivo = "plano_afin_sin_latex.py"
        $Escena = "PresentacionMaestraSinLatex"
        Write-Host "[INFO] Modo: Presentación Maestra Completa (Álgebra 2D + Modelo 3D + Resumen, ~2m 45s)" -ForegroundColor Green
    }
    "sin_latex" {
        $Archivo = "plano_afin_sin_latex.py"
        $Escena = "VideoCompletoSinLatex"
        Write-Host "[INFO] Modo: Solo Álgebra 2D (sin modelo 3D)" -ForegroundColor Green
    }
    "3d" {
        $Archivo = "plano_afin_sin_latex.py"
        $Escena = "Escena3D_SinLatex"
        Write-Host "[INFO] Modo: Solo Visualización Geométrica 3D con rotación orbital" -ForegroundColor Green
    }
    "con_latex" {
        $Archivo = "plano_afin_animacion.py"
        $Escena = "PresentacionMaestra3D"
        Write-Host "[INFO] Modo: Versión tipográfica formal con LaTeX (requiere MiKTeX)" -ForegroundColor Yellow
    }
}

Write-Host "[INFO] Renderizando escena '$Escena' en calidad -$Calidad..." -ForegroundColor Yellow
Write-Host "---------------------------------------------------------"

# 3. Ejecutar Manim
python -m manim "-pq$Calidad" $Archivo $Escena

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[OK] Video renderizado exitosamente." -ForegroundColor Green

    # 4. Ajuste automático de velocidad si se especificó un valor distinto de 1.0
    if ($Velocidad -ne 1.0) {
        Write-Host "[INFO] Aplicando ajuste de velocidad ($Velocidad x)..." -ForegroundColor Cyan
        $CalidadDir = switch ($Calidad) {
            "l" { "480p15" }
            "m" { "720p30" }
            "h" { "1080p60" }
            "k" { "2160p60" }
        }
        $NombreBase = [System.IO.Path]::GetFileNameWithoutExtension($Archivo)
        $VideoOriginal = ".\media\videos\$NombreBase\$CalidadDir\$Escena.mp4"
        $VideoAjustado = ".\media\videos\$NombreBase\$CalidadDir\${Escena}_velocidad_${Velocidad}.mp4"

        if (Test-Path $VideoOriginal) {
            $FiltroPTS = "setpts=" + (1.0 / $Velocidad).ToString([System.Globalization.CultureInfo]::InvariantCulture) + "*PTS"
            ffmpeg -y -i $VideoOriginal -filter:v $FiltroPTS -an $VideoAjustado
            Write-Host "[OK] Video con velocidad ajustada guardado en: $VideoAjustado" -ForegroundColor Green
        }
    }
} else {
    Write-Host "`n[ERROR] Ocurrió un problema durante el renderizado." -ForegroundColor Red
}
