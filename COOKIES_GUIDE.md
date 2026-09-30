# Guía para Exportar Cookies de YouTube

Si sigues recibiendo el error "Sign in to confirm you're not a bot", necesitas exportar tus cookies de YouTube.

## Método 1: Usando la extensión "Get cookies.txt LOCALLY" (Recomendado)

### Para Chrome/Edge:

1. **Instala la extensión**:
   - Ve a: https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   - Click en "Agregar a Chrome"

2. **Inicia sesión en YouTube**:
   - Ve a https://www.youtube.com
   - Inicia sesión con tu cuenta de Google

3. **Exporta las cookies**:
   - Mientras estés en YouTube, click en el icono de la extensión
   - Click en "Export" o "Copy to Clipboard"
   - Guarda el contenido en un archivo llamado `cookies.txt`

4. **Coloca el archivo**:
   - Guarda `cookies.txt` en la raíz del proyecto (al lado de app.py)

### Para Firefox:

1. **Instala la extensión**:
   - Ve a: https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/
   - Click en "Add to Firefox"

2. Sigue los pasos 2-4 del método de Chrome

## Método 2: Usando yt-dlp directamente

Si tienes yt-dlp instalado localmente:

```bash
# En tu navegador, inicia sesión en YouTube
# Luego ejecuta:
yt-dlp --cookies-from-browser chrome --cookies cookies.txt https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Cambia `chrome` por tu navegador: `firefox`, `edge`, `safari`, `opera`, etc.

## Para Render (Producción)

Si necesitas usar cookies en producción:

1. **Exporta las cookies** usando el Método 1

2. **Codifica el archivo en base64**:
   ```bash
   # En Windows (PowerShell):
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt")) | Out-File cookies_base64.txt

   # En Mac/Linux:
   base64 cookies.txt > cookies_base64.txt
   ```

3. **Agrega como variable de entorno en Render**:
   - En tu servicio de Render, ve a "Environment"
   - Agrega una nueva variable: `COOKIES_BASE64`
   - Pega el contenido del archivo `cookies_base64.txt`

4. **Actualiza app.py** para decodificar:
   ```python
   import base64

   # Al inicio de app.py, después de COOKIES_FILE:
   if os.environ.get('COOKIES_BASE64'):
       cookies_content = base64.b64decode(os.environ['COOKIES_BASE64'])
       with open(COOKIES_FILE, 'wb') as f:
           f.write(cookies_content)
   ```

## Notas Importantes

- Las cookies expiran. Si vuelves a tener problemas después de semanas/meses, repite el proceso
- NUNCA subas `cookies.txt` a GitHub (ya está en .gitignore)
- Las cookies contienen tu sesión de YouTube, mantenlas privadas
- Solo necesitas hacer esto si el error persiste después de actualizar yt-dlp

## Verificar que funciona

Después de agregar las cookies:

```bash
# Local:
python app.py

# Prueba descargar un video
```

Si aún tienes problemas, verifica que:
1. El archivo `cookies.txt` está en la carpeta correcta
2. Las cookies son recientes (menos de 1 mes)
3. Estás usando la última versión de yt-dlp: `pip install --upgrade yt-dlp`
