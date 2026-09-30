#!/bin/bash
# Script de build para Render - instala FFmpeg y última versión de yt-dlp

# Instalar FFmpeg (necesario para fusionar video+audio)
apt-get update
apt-get install -y ffmpeg

# Instalar última versión de yt-dlp (importante para bypasses)
pip install --upgrade yt-dlp

# Instalar dependencias Python
pip install -r requirements.txt
