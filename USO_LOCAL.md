# Guía de Uso Local - YouTube Downloader

## Por qué usar localmente

YouTube bloquea las IPs de servidores cloud como Render. La app funciona **perfectamente** cuando la corres en tu computadora.

## Instalación (Una sola vez)

### Windows

```bash
# 1. Abre PowerShell o CMD en la carpeta del proyecto
cd C:\Users\Tom\Desktop\PROYECTOS\youtube_downloader

# 2. (Opcional) Crea un entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instala FFmpeg
winget install ffmpeg
# O descarga de: https://ffmpeg.org/download.html

# 4. Instala dependencias
pip install -r requirements.txt
```

### Mac/Linux

```bash
# 1. Navega a la carpeta
cd ~/youtube_downloader

# 2. (Opcional) Crea entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instala FFmpeg
# Mac:
brew install ffmpeg

# Linux:
sudo apt install ffmpeg

# 4. Instala dependencias
pip install -r requirements.txt
```

## Uso Diario

Cada vez que quieras descargar videos:

```bash
# 1. Abre terminal en la carpeta del proyecto

# 2. (Si usas venv) Activa el entorno
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Corre la app
python app.py

# 4. Verás algo como:
#    * Running on http://127.0.0.1:5000

# 5. Abre tu navegador en: http://localhost:5000
```

### Descargar Video

1. Copia la URL del video de YouTube
2. Pégala en el campo
3. Click "Descargar"
4. Espera 10-60 segundos (según el tamaño)
5. El video se descarga automáticamente

### Detener la App

En la terminal donde corre, presiona: **Ctrl + C**

## Uso con Cookies (Opcional)

Si algunos videos no se descargan (error de bot):

1. Exporta cookies de YouTube usando la extensión "Get cookies.txt LOCALLY"
2. Guarda el archivo como `cookies.txt` en la carpeta del proyecto
3. Reinicia la app

La app detectará las cookies automáticamente.

## Acceso desde Otros Dispositivos (Opcional)

Por defecto, solo puedes acceder desde tu PC. Para acceder desde tu teléfono/tablet en la misma red:

### Opción 1: IP Local

```python
# Edita app.py, última línea, cambia:
app.run(host='0.0.0.0', port=port)
```

Luego accede desde: `http://TU_IP_LOCAL:5000`

Para encontrar tu IP:
- Windows: `ipconfig` (busca IPv4)
- Mac/Linux: `ifconfig` (busca inet)

### Opción 2: Cloudflare Tunnel (Internet)

Para acceder desde cualquier lugar (incluso fuera de casa):

```bash
# 1. Instala cloudflared
# https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

# 2. Corre tu app
python app.py

# 3. En otra terminal:
cloudflared tunnel --url http://localhost:5000

# 4. Te dará una URL como: https://xxx.trycloudflare.com
# Comparte esa URL o úsala desde cualquier dispositivo
```

**IMPORTANTE**: La URL cambia cada vez. Para una URL fija necesitas cuenta de Cloudflare (gratis).

## Creación de Acceso Directo (Windows)

Para no tener que abrir terminal cada vez:

1. Crea un archivo `run.bat` en la carpeta del proyecto:

```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python app.py
pause
```

2. Doble click en `run.bat` para iniciar la app

## Ventajas de Uso Local

✅ **Siempre funciona** - Tu IP no está bloqueada por YouTube
✅ **Más rápido** - Sin latencia de servidor remoto
✅ **Sin límites** - No hay restricciones de Render
✅ **Mejor calidad** - Puede descargar hasta 4K
✅ **Privado** - Las cookies nunca salen de tu PC
✅ **Gratis** - Sin costos de hosting

## Desventajas

❌ Solo funciona cuando tu PC está prendida
❌ Solo tú puedes usarla (a menos que uses Cloudflare Tunnel)

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### "ERROR: ffmpeg not found"

Instala FFmpeg:
- Windows: `winget install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### "Address already in use"

Otro programa está usando el puerto 5000. Cambia el puerto:

```python
# En app.py, última línea:
port = int(os.environ.get('PORT', 5001))  # Cambia a 5001 o cualquier otro
```

### "yt-dlp error: Sign in to confirm you're not a bot"

Exporta cookies de YouTube (ver sección "Uso con Cookies" arriba).

### Video se descarga sin audio

Verifica que FFmpeg esté instalado: `ffmpeg -version`

## Alternativas

Si no quieres correr la app, puedes usar yt-dlp directamente:

```bash
# Instalar
pip install yt-dlp

# Descargar video
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# Con cookies
yt-dlp --cookies cookies.txt "URL"

# Especificar calidad
yt-dlp -f "best[height<=720]" "URL"
```

## Scripts de Ayuda

### test_local.sh
Prueba que yt-dlp funciona antes de usar la app.

```bash
bash test_local.sh
```

### verify_cookies.py
Verifica que tus cookies sean válidas.

```bash
python verify_cookies.py cookies.txt
```

## Conclusión

Para **4 descargas al mes**, usar la app localmente es la solución perfecta:

1. Una sola instalación
2. Cuando necesites: `python app.py`
3. Descargas lo que quieras
4. Ctrl+C para detener
5. Listo hasta la próxima vez

Simple, rápido y siempre funciona. 🎉
