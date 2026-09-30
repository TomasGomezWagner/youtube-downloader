#!/bin/bash
# Script de build para Render - instala FFmpeg

# Instalar FFmpeg (necesario para fusionar video+audio)
apt-get update
apt-get install -y ffmpeg

# Instalar dependencias Python
pip install -r requirements.txt
