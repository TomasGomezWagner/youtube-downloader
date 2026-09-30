# YouTube Video Downloader

Una aplicación web simple para descargar videos de YouTube con audio y video combinados.

## Características

- Interfaz limpia y moderna
- Descarga video + audio en formato MP4
- Funciona con cualquier URL de YouTube
- Gratis y sin límites para uso personal

## Tecnologías

- **Backend**: Flask + yt-dlp
- **Frontend**: HTML, CSS, JavaScript vanilla
- **Hosting**: Render (plan gratuito)

## Instalación Local

1. Clona o descarga este repositorio

2. **Instala FFmpeg** (requerido para fusionar video+audio):
   - **Windows**: Descarga de https://ffmpeg.org/download.html o usa `winget install ffmpeg`
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

3. Instala las dependencias Python:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
python app.py
```

5. Abre tu navegador en `http://localhost:5000`

## Despliegue en Render (GRATIS)

### Opción 1: Desde GitHub (Recomendada)

1. **Sube el código a GitHub**:
   - Crea un nuevo repositorio en GitHub
   - Sube todos los archivos de este proyecto

2. **Conecta con Render**:
   - Ve a [Render.com](https://render.com) y crea una cuenta
   - Click en "New +" → "Web Service"
   - Conecta tu cuenta de GitHub
   - Selecciona tu repositorio

3. **Configuración**:
   - **Name**: youtube-downloader (o el que prefieras)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. Click en "Create Web Service" y espera 5-10 minutos

5. Tu app estará disponible en: `https://tu-app.onrender.com`

### Opción 2: Despliegue Manual

Si no quieres usar GitHub:

1. Instala Render CLI:
```bash
pip install render
```

2. Inicia sesión:
```bash
render login
```

3. Despliega:
```bash
render deploy
```

## Uso

1. Copia la URL de cualquier video de YouTube
2. Pégala en el campo de entrada
3. Click en "Descargar"
4. Espera a que se procese (puede tardar 30 segundos - 2 minutos)
5. El video se descargará automáticamente

## Limitaciones del Plan Gratuito de Render

- El servicio se "duerme" después de 15 minutos de inactividad
- Primera carga después del "sueño" tarda ~30-60 segundos
- 750 horas de uso por mes (más que suficiente para 4 descargas/mes)
- Videos muy largos (>1 hora) pueden dar timeout

## Notas Importantes

- Solo para uso personal con contenido propio o con permiso
- Descargar contenido protegido por derechos de autor puede violar los términos de YouTube
- La primera descarga después de inactividad será más lenta (mientras el servidor despierta)

## Estructura del Proyecto

```
youtube_downloader/
├── app.py                 # Backend Flask
├── requirements.txt       # Dependencias Python
├── render.yaml           # Configuración Render
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Estilos
│   └── script.js         # Lógica del cliente
└── README.md             # Este archivo
```

## Solución de Problemas

**"Sign in to confirm you're not a bot"**:
Este es el error más común. Soluciones en orden:

1. **Actualizar yt-dlp** (prueba esto primero):
   ```bash
   pip install --upgrade yt-dlp
   pip freeze > requirements.txt
   ```

2. **Usar cookies de YouTube** (si el paso 1 no funciona):
   - Consulta el archivo `COOKIES_GUIDE.md` para instrucciones detalladas
   - Necesitarás exportar tus cookies de YouTube usando una extensión del navegador
   - Guarda el archivo `cookies.txt` en la raíz del proyecto

**El servicio está tardando mucho en responder**:
- El servidor puede estar "despertando". Espera 1 minuto y vuelve a intentar.

**Error al descargar**:
- Verifica que la URL sea válida
- Algunos videos con restricciones pueden fallar
- Videos privados no funcionarán

**El video se descarga sin audio**:
- Esto no debería pasar, la configuración usa `bestvideo+bestaudio`
- Si pasa, reporta el enlace del video

## Mantenimiento

El código es muy simple y no necesita mantenimiento regular. Solo actualiza `yt-dlp` si deja de funcionar:

```bash
pip install --upgrade yt-dlp
```

Luego actualiza `requirements.txt` con la nueva versión.
