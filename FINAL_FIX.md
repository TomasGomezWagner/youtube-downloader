# FIX FINAL - Player Client en TODAS las configuraciones

## Problema detectado

El error "Requested format is not available" ocurre **incluso al listar formatos**.

Esto significa que YouTube bloquea la extracción de información, no solo la descarga.

## Root Cause

**Antes**: Solo algunas configuraciones tenían `player_client`
**Resultado**: Las primeras configuraciones fallaban porque YouTube detectaba el request como bot

## Solución implementada

### 1. TODAS las configuraciones ahora usan player_client

**Antes** (Config 1):
```python
config1 = {
    'format': '18',  # SIN player_client
}
```

**Ahora** (Config 1):
```python
config1 = {
    'format': 'best',
    'extractor_args': {
        'youtube': {
            'player_client': ['ios'],
            'player_skip': ['webpage'],
        }
    },
}
```

### 2. Orden de bypass optimizado

1. **iOS** - Player más confiable
2. **Android** - Alternativa rápida
3. **Android Embedded** - TV apps bypass
4. **iOS con merge** - Para videos que requieren fusión
5. **Web** - Último recurso

### 3. Build actualizado

`build.sh` ahora hace:
```bash
pip install --upgrade yt-dlp  # SIEMPRE la última versión
```

Esto asegura que tenemos los bypasses más recientes.

### 4. /list-formats mejorado

Ahora usa los mismos bypasses que la descarga, así que si `/list-formats` funciona, la descarga también funcionará.

## Desplegar

```bash
git add .
git commit -m "Final fix: player_client on ALL configs"
git push
```

**IMPORTANTE**: En Render, haz **"Clear build cache & deploy"** para forzar reinstalación de yt-dlp.

## Verificar

### 1. Verifica versión de yt-dlp en logs

Deberías ver durante el build:
```
Successfully installed yt-dlp-XXXX.XX.XX
```

### 2. Prueba /list-formats

`/list-formats?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ`

**Éxito**:
```json
{
  "title": "Rick Astley - Never Gonna Give You Up",
  "formats_count": 20+,
  "has_format_18": true
}
```

**Error**:
```json
{
  "error": "...",
  "traceback": "...",
  "cookies_loaded": true
}
```

Si sigue dando error, comparte el traceback completo.

### 3. Prueba descarga

Si `/list-formats` funciona, la descarga DEBE funcionar.

**Logs esperados**:
```
🍪 Agregando cookies desde: /tmp/cookies.txt
🔄 Intento 1/5: player_client=['ios']
🍪 Usando cookies: True
✅ Descarga exitosa con configuración 1
```

## Si TODAVÍA falla

Entonces el problema es uno de estos:

### A. YouTube bloqueó la IP de Render

**Síntoma**: Funciona localmente pero no en Render
**Solución**:
- Usa la app localmente
- O espera unas horas (los bloqueos de IP son temporales)

### B. Las cookies son inválidas

**Síntoma**: Mismo error con y sin cookies
**Prueba local**:
```bash
yt-dlp --cookies cookies.txt --list-formats https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Si falla localmente, las cookies son el problema:
1. Cierra sesión en YouTube
2. Borra cookies del navegador
3. Inicia sesión de nuevo
4. Re-exporta cookies

### C. yt-dlp necesita actualización más allá de la última release

**Síntoma**: Error persiste con última versión
**Solución**: Instalar desde git
```bash
pip install git+https://github.com/yt-dlp/yt-dlp.git
```

Actualiza `requirements.txt`:
```
git+https://github.com/yt-dlp/yt-dlp.git
```

## Archivos modificados

- ✅ `app.py` - Todas las configs con player_client
- ✅ `build.sh` - pip install --upgrade yt-dlp explícito
- ✅ `/list-formats` - Usa mismos bypasses que descarga

## Expectativa realista

Con estos cambios, **debería funcionar**.

Si no funciona:
1. Comparte el output completo de `/list-formats`
2. Prueba localmente con el mismo código
3. Si funciona local pero no en Render → IP bloqueada

## Próximos pasos

1. ✅ Despliega con "Clear build cache"
2. ⏳ Espera 5-7 minutos (build tarda más con cache limpio)
3. 🧪 Prueba `/list-formats` primero
4. 📊 Si funciona → Prueba descarga
5. 🎉 O 😢 Comparte resultados
