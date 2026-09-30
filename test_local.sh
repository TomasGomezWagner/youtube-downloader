#!/bin/bash
# Script para probar que yt-dlp funciona localmente

echo "======================================"
echo "PRUEBA LOCAL DE YT-DLP"
echo "======================================"
echo ""

# Verificar que yt-dlp está instalado
if ! command -v yt-dlp &> /dev/null; then
    echo "❌ yt-dlp no está instalado"
    echo "Instalando..."
    pip install yt-dlp
fi

echo "📦 Versión de yt-dlp:"
yt-dlp --version
echo ""

# Verificar cookies
if [ -f "cookies.txt" ]; then
    echo "🍪 Archivo cookies.txt encontrado"
    COOKIES_ARG="--cookies cookies.txt"
else
    echo "⚠️  No se encontró cookies.txt (se intentará sin cookies)"
    COOKIES_ARG=""
fi
echo ""

# Probar con video de prueba
TEST_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

echo "🧪 Probando extracción de información..."
echo "URL: $TEST_URL"
echo ""

# Intentar listar formatos
echo "📋 Listando formatos disponibles..."
yt-dlp $COOKIES_ARG --list-formats "$TEST_URL"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡ÉXITO! yt-dlp puede acceder a YouTube"
    echo ""
    echo "Esto confirma que:"
    echo "  1. yt-dlp funciona correctamente"
    echo "  2. Las cookies (si las usas) son válidas"
    echo "  3. Tu IP NO está bloqueada"
    echo ""
    echo "Conclusión: El problema es la IP de Render, no el código."
    echo ""
    echo "💡 Recomendación: Usa la app localmente"
    echo "   python app.py"
    echo "   Abre http://localhost:5000"
else
    echo ""
    echo "❌ ERROR: yt-dlp no puede acceder a YouTube"
    echo ""
    echo "Posibles causas:"
    echo "  1. Las cookies expiraron (re-expórtalas)"
    echo "  2. Tu IP está bloqueada (poco probable para IPs residenciales)"
    echo "  3. yt-dlp necesita actualización: pip install --upgrade yt-dlp"
fi

echo ""
echo "======================================"
