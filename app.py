from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import tempfile
import time
from pathlib import Path

app = Flask(__name__)

# Crear directorio temporal para descargas
DOWNLOAD_FOLDER = tempfile.gettempdir()

# Ruta al archivo de cookies (opcional)
COOKIES_FILE = os.path.join(os.path.dirname(__file__), 'cookies.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400

        # Generar nombre de archivo único
        timestamp = int(time.time())
        output_path = os.path.join(DOWNLOAD_FOLDER, f'video_{timestamp}.mp4')

        # Configuración de yt-dlp con bypass de detección de bots
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
            # Configuraciones anti-bot
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
        }

        # Usar cookies si el archivo existe (ayuda con videos que requieren autenticación)
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE

        # Descargar video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')

        # Verificar que el archivo existe
        if not os.path.exists(output_path):
            return jsonify({'error': 'Error al descargar el video'}), 500

        # Enviar archivo y limpiarlo después
        return send_file(
            output_path,
            as_attachment=True,
            download_name=f'{title}.mp4',
            mimetype='video/mp4'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Endpoint para limpiar archivos temporales después de la descarga"""
    try:
        # Limpiar archivos antiguos (más de 1 hora)
        current_time = time.time()
        for file in Path(DOWNLOAD_FOLDER).glob('video_*.mp4'):
            if current_time - file.stat().st_mtime > 3600:
                file.unlink()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
