# Troubleshooting: "Las cookies están cargadas pero YouTube sigue bloqueando"

## Diagnóstico

Si ves este error, significa que:
- ✅ La variable `COOKIES_BASE64` está configurada en Render
- ✅ Las cookies se decodificaron correctamente
- ❌ Pero YouTube sigue detectándote como bot

## Paso 1: Verificar el estado actual

Ve a: `https://tu-app.onrender.com/debug`

Deberías ver algo como:
```json
{
  "cookies_file_exists": true,
  "cookies_file_path": "/tmp/cookies.txt",
  "cookies_env_var_set": true,
  "cookies_file_size": 12345,
  "cookies_format_ok": true
}
```

**Si `cookies_format_ok` es `false`**: El archivo no tiene el formato correcto (ver Paso 2)

**Si `cookies_file_exists` es `false`**: Las cookies no se están cargando (ver Paso 3)

## Paso 2: Verificar formato de cookies

El archivo **debe** estar en formato Netscape. Las extensiones normalmente lo exportan correctamente, pero verifica:

### Usar el script de verificación (local):

```bash
python verify_cookies.py cookies.txt
```

Esto te dirá si el formato es correcto.

### Formato correcto esperado:

```
# Netscape HTTP Cookie File
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1234567890	CONSENT	YES+...
.youtube.com	TRUE	/	TRUE	1234567890	VISITOR_INFO1_LIVE	xxx
...
```

**Características**:
- Primera línea debe contener "Netscape HTTP Cookie File"
- Cookies de `.youtube.com` o `youtube.com`
- 7 campos por línea separados por TABs (no espacios)

### Si el formato es incorrecto:

1. **Re-exporta las cookies** usando la extensión recomendada:
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **IMPORTANTE**: Asegúrate de:
   - Estar en `youtube.com` cuando exportas
   - Estar iniciado sesión
   - Usar modo "Export" o "Current site" (no "All sites")

## Paso 3: Las cookies expiraron

Las cookies de YouTube expiran después de semanas/meses. Si hace tiempo que las exportaste:

1. **Cierra sesión en YouTube** en tu navegador
2. **Inicia sesión nuevamente**
3. **Exporta cookies frescas** usando la extensión
4. **Re-codifica**:
   ```bash
   python encode_cookies.py cookies.txt
   ```
5. **Actualiza la variable en Render**:
   - Ve a Environment → COOKIES_BASE64
   - Reemplaza el valor con el nuevo
   - Save Changes

## Paso 4: Verificar los logs de Render

En Render, ve a "Logs" y busca estas líneas cuando la app inicia:

```
✅ Cookies decodificadas desde COOKIES_BASE64 → /tmp/cookies.txt
📦 Tamaño: 12345 bytes
🍪 Archivo de cookies encontrado: /tmp/cookies.txt (12345 bytes)
```

Cuando intentas descargar:

```
🍪 Agregando cookies desde: /tmp/cookies.txt
🔄 Intento 1/4: player_client=['ios']
🍪 Usando cookies: True
```

**Si ves `🍪 Usando cookies: False`**: Las cookies no se están pasando a yt-dlp

**Si ves `⚠️  No hay cookies disponibles`**: No se cargaron correctamente

## Paso 5: Probar localmente

Para aislar el problema, prueba localmente:

```bash
# 1. Pon cookies.txt en la carpeta del proyecto
cp youtube.com_cookies.txt cookies.txt

# 2. Verifica el formato
python verify_cookies.py cookies.txt

# 3. Corre la app
python app.py

# 4. Prueba descargar
# Ve a http://localhost:5000
```

Si funciona localmente pero no en Render:
- Verifica que la codificación base64 sea correcta
- Prueba re-encodear las cookies

## Paso 6: Alternativa - Probar con yt-dlp directamente

```bash
# Instala yt-dlp
pip install yt-dlp

# Prueba con tus cookies
yt-dlp --cookies cookies.txt https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Si funciona, el problema está en cómo la app usa las cookies
# Si falla, las cookies son inválidas
```

## Paso 7: Última opción - Cookies del navegador directo

En lugar de exportar a archivo, usa directamente las del navegador:

```bash
# Chrome
yt-dlp --cookies-from-browser chrome https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Si esto funciona, exporta:
yt-dlp --cookies-from-browser chrome --cookies cookies.txt https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Esto generará un `cookies.txt` válido garantizado.

## Checklist rápido

- [ ] ¿Las cookies tienen menos de 1 mes?
- [ ] ¿Exportadas desde youtube.com (no otra página)?
- [ ] ¿Formato Netscape correcto? (verificar con `verify_cookies.py`)
- [ ] ¿Variable `COOKIES_BASE64` actualizada en Render?
- [ ] ¿Los logs muestran "Usando cookies: True"?
- [ ] ¿Funciona con yt-dlp CLI directamente?

## Si nada funciona

Puede ser que YouTube haya endurecido las restricciones temporalmente. Opciones:

1. **Usa la app localmente** - Funcionará mejor porque usa tu IP residencial
2. **Espera unas horas** - A veces YouTube bloquea IPs de servidores temporalmente
3. **Prueba con otro video** - Algunos videos tienen más restricciones
4. **Verifica que el video sea público** - Videos privados/no listados requieren estar autenticado

## Contacto

Si después de todo esto sigue sin funcionar, revisa los logs completos de Render y comparte:

1. Salida de `/debug`
2. Salida de `verify_cookies.py`
3. Últimas 20 líneas de logs de Render
4. El error completo que recibes
