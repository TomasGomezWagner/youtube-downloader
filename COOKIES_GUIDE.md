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

1. **Exporta las cookies** usando el Método 1 (arriba)

2. **Codifica el archivo usando el script incluido**:
   ```bash
   python encode_cookies.py cookies.txt
   ```
   Esto mostrará el texto codificado en base64.

   **Alternativa manual**:
   ```bash
   # En Windows (PowerShell):
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt"))

   # En Mac/Linux:
   base64 cookies.txt
   ```

3. **Agrega como variable de entorno en Render**:
   - Ve a tu servicio en Render.com
   - Click en "Environment" en el menú izquierdo
   - Click en "Add Environment Variable"
   - **Key**: `COOKIES_BASE64`
   - **Value**: Pega el texto base64 completo
   - Click "Save Changes"
   - Espera a que el servicio se redespliegue automáticamente (~2 minutos)

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
