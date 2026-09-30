# Solución Rápida al Error "Failed to extract player response"

## El Problema
YouTube está bloqueando agresivamente las descargas. El código ahora intenta 3 estrategias diferentes automáticamente, pero probablemente necesites usar cookies de tu navegador.

## Solución (5 minutos)

### Paso 1: Exportar Cookies de YouTube

1. **Instala esta extensión en Chrome/Edge**:
   - https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

2. **Ve a YouTube e inicia sesión**:
   - https://www.youtube.com
   - Inicia sesión con tu cuenta de Google

3. **Exporta las cookies**:
   - Click en el icono de la extensión (mientras estás en YouTube)
   - Click en "Export"
   - Se descargará un archivo `youtube.com_cookies.txt`

### Paso 2: Subir a Render

**Opción A: Usando el script (recomendado)**
```bash
# Renombra el archivo si es necesario
mv youtube.com_cookies.txt cookies.txt

# Codifica las cookies
python encode_cookies.py cookies.txt

# Copia el texto que aparece
```

**Opción B: Manual en PowerShell (Windows)**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt"))
```

### Paso 3: Agregar a Render

1. Ve a https://dashboard.render.com
2. Selecciona tu servicio "youtube-downloader"
3. Click en **"Environment"** (menú izquierdo)
4. Click en **"Add Environment Variable"**
5. **Key**: `COOKIES_BASE64`
6. **Value**: Pega el texto base64 que copiaste
7. Click **"Save Changes"**
8. Espera 2-3 minutos a que redespliegue

### Paso 4: Probar

Vuelve a intentar descargar el video. Ahora debería funcionar.

## ¿Por qué pasa esto?

YouTube detecta requests automáticos y los bloquea. Al usar tus cookies:
- YouTube cree que eres tú navegando normalmente
- No te detecta como bot
- Las descargas funcionan

## Alternativa: Usar Localmente

Si no quieres configurar cookies en Render, puedes usar la app localmente:

```bash
# 1. Instala dependencias
pip install -r requirements.txt

# 2. Pon cookies.txt en la carpeta del proyecto

# 3. Corre la app
python app.py

# 4. Abre http://localhost:5000
```

## Las cookies expiran?

Sí, después de semanas o meses. Si vuelve a fallar:
1. Exporta cookies nuevamente
2. Actualiza la variable `COOKIES_BASE64` en Render
3. Listo

## Otros Errores Comunes

**"Video unavailable"**: El video es privado o fue eliminado
**Timeout**: Video muy largo (>1 hora). Usa localmente para videos largos
**"Sign in to confirm you're not a bot"**: Mismo problema, usa cookies

---

¿Necesitas ayuda? Revisa `COOKIES_GUIDE.md` para más detalles.
