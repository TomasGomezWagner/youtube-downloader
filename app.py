from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import tempfile
import time
import base64
from pathlib import Path

app = Flask(__name__)

# Crear directorio temporal para descargas
DOWNLOAD_FOLDER = tempfile.gettempdir()

# Ruta al archivo de cookies (opcional)
COOKIES_FILE = os.path.join(DOWNLOAD_FOLDER, 'cookies.txt')

# Si hay cookies en variable de entorno (para Render), decodificarlas
if os.environ.get('COOKIES_BASE64'):
    try:
        cookies_content = base64.b64decode(os.environ['COOKIES_BASE64'])
        with open(COOKIES_FILE, 'wb') as f:
            f.write(cookies_content)
    except Exception as e:
        print(f"Error decodificando cookies: {e}")

# También buscar cookies.txt en el directorio local
LOCAL_COOKIES = os.path.join(os.path.dirname(__file__), 'cookies.txt')
if os.path.exists(LOCAL_COOKIES) and not os.path.exists(COOKIES_FILE):
    import shutil
    shutil.copy(LOCAL_COOKIES, COOKIES_FILE)

@app.route('/')
def index():
    return render_template('index.html')

def get_ydl_configs(output_path):
    """Retorna múltiples configuraciones para intentar en orden"""

    base_config = {
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    # Configuración 1: Mejor calidad, video+audio separados, muy flexible
    config1 = {
        **base_config,
        'format': 'bv*+ba/b',
        'extractor_args': {
            'youtube': {
                'player_client': ['ios'],
            }
        },
    }

    # Configuración 2: Lo mejor disponible en un solo archivo
    config2 = {
        **base_config,
        'format': 'b',
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
    }

    # Configuración 3: Web client, cualquier cosa
    config3 = {
        **base_config,
        'format': 'best/bestvideo+bestaudio/bestvideo',
        'extractor_args': {
            'youtube': {
                'player_client': ['web'],
            }
        },
    }

    # Configuración 4: Fallback absoluto - acepta lo que sea
    config4 = {
        **base_config,
        'format': 'worst',
    }

    # Agregar cookies si existen
    configs = [config1, config2, config3, config4]
    if os.path.exists(COOKIES_FILE):
        for config in configs:
            config['cookiefile'] = COOKIES_FILE

    return configs

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

        # Intentar con múltiples configuraciones
        configs = get_ydl_configs(output_path)
        last_error = None

        for i, ydl_opts in enumerate(configs):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'video')

                # Si llegamos aquí, la descarga fue exitosa
                if os.path.exists(output_path):
                    return send_file(
                        output_path,
                        as_attachment=True,
                        download_name=f'{title}.mp4',
                        mimetype='video/mp4'
                    )
            except Exception as e:
                last_error = str(e)
                # Si no es el último intento, continuar con la siguiente configuración
                if i < len(configs) - 1:
                    continue
                # Si es el último intento, lanzar el error
                raise Exception(last_error)

        return jsonify({'error': 'No se pudo descargar el video'}), 500

    except Exception as e:
        error_msg = str(e)
        if 'bot' in error_msg.lower():
            error_msg = 'YouTube está bloqueando la descarga. Por favor, exporta tus cookies de YouTube (ver COOKIES_GUIDE.md)'
        return jsonify({'error': error_msg}), 500

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
