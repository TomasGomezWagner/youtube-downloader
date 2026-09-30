# Actualización Crítica - Arreglo de Timeout y Formatos

## Cambios implementados

### 1. Timeout de Gunicorn aumentado
- **Antes**: 30 segundos (default)
- **Ahora**: 300 segundos (5 minutos)
- **Por qué**: Las descargas necesitan más tiempo para procesar

### 2. Formatos optimizados para velocidad
**Cambios**:
- ✅ Prioriza formatos pre-merged (no requieren fusión)
- ✅ 5 estrategias en lugar de 4
- ✅ Incluye formato 18 (360p MP4) como fallback garantizado
- ✅ Límite de 1080p para evitar archivos enormes
- ✅ Removido post-procesador que causaba delays

**Nueva estrategia**:
1. iOS - Mejor calidad pre-merged
2. Android - Formato 18 (360p, siempre disponible)
3. iOS - Video+Audio merge solo si es necesario
4. Web - Mejor disponible
5. Fallback - Formato 18 directo

## Cómo desplegar esta actualización

### Si usas Git + Render:

```bash
git add .
git commit -m "Fix: timeout and format issues"
git push
```

Render redespliegará automáticamente en 3-5 minutos.

### Si subiste manualmente a Render:

1. Ve a tu servicio en Render
2. Sube los archivos actualizados:
   - `render.yaml` (timeout aumentado)
   - `app.py` (formatos optimizados)
3. Click "Manual Deploy" → "Deploy latest commit"

## Qué esperar después del despliegue

### Mejoras:
- ✅ No más "WORKER TIMEOUT"
- ✅ Descargas más rápidas (formatos pre-merged)
- ✅ Mayor tasa de éxito (5 estrategias)
- ✅ Siempre descarga algo (fallback a 360p)

### Calidad:
- **Videos normales**: 720p-1080p (mejor disponible)
- **Videos con restricciones**: Hasta 360p (formato 18)
- **Siempre**: Video + Audio juntos

## Verificación

Después de desplegar:

1. **Verifica el timeout en logs**:
   ```
   [INFO] Listening at: http://0.0.0.0:10000 (timeout: 300)
   ```

2. **Prueba descarga**:
   - URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Deberías ver en logs:
   ```
   🔄 Intento 1/5: player_client=['ios']
   🍪 Usando cookies: True
   ✅ Descarga exitosa con configuración 1
   ```

3. **Si falla el primer intento**, verás que prueba automáticamente:
   ```
   ❌ Intento 1 falló: ...
   🔄 Intento 2/5: player_client=['android']
   ✅ Descarga exitosa con configuración 2
   ```

## Tiempo estimado de descarga

| Calidad | Duración Video | Tiempo Estimado |
|---------|---------------|-----------------|
| 360p    | <5 min        | 10-20 seg       |
| 720p    | <5 min        | 20-40 seg       |
| 1080p   | <5 min        | 40-90 seg       |
| 360p    | 10-30 min     | 30-60 seg       |
| 720p    | 10-30 min     | 60-120 seg      |

## Troubleshooting

**Si sigue dando timeout**:
- Videos muy largos (>30 min) pueden tardar >5 minutos
- Solución: Usa la app localmente para videos largos

**Si la calidad es muy baja (siempre 360p)**:
- La app está cayendo al fallback (formato 18)
- Revisa los logs para ver por qué fallan los primeros intentos
- Puede ser que las cookies expiraron (re-exporta)

**"Requested format is not available"**:
- Esto ya no debería pasar (formato 18 siempre existe)
- Si pasa, comparte los logs completos

## Archivos modificados

- ✅ `render.yaml` - Timeout 300s, 1 worker
- ✅ `app.py` - 5 configuraciones optimizadas
- ✅ Este archivo `DEPLOY_UPDATE.md`

## Siguientes pasos

1. Despliega los cambios
2. Espera 3-5 minutos
3. Prueba una descarga
4. Comparte los resultados (éxito o logs si falla)
