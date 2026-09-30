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
        print(f"✅ Cookies decodificadas desde COOKIES_BASE64 → {COOKIES_FILE}")
        print(f"📦 Tamaño: {len(cookies_content)} bytes")
    except Exception as e:
        print(f"❌ Error decodificando cookies: {e}")

# También buscar cookies.txt en el directorio local
LOCAL_COOKIES = os.path.join(os.path.dirname(__file__), 'cookies.txt')
if os.path.exists(LOCAL_COOKIES) and not os.path.exists(COOKIES_FILE):
    import shutil
    shutil.copy(LOCAL_COOKIES, COOKIES_FILE)
    print(f"✅ Cookies copiadas desde {LOCAL_COOKIES} → {COOKIES_FILE}")

# Verificar si cookies están disponibles al iniciar
if os.path.exists(COOKIES_FILE):
    file_size = os.path.getsize(COOKIES_FILE)
    print(f"🍪 Archivo de cookies encontrado: {COOKIES_FILE} ({file_size} bytes)")
else:
    print(f"⚠️  No se encontró archivo de cookies. Algunas descargas pueden fallar.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list-formats')
def list_formats():
    """Lista formatos disponibles para un video (para debugging)"""
    url = request.args.get('url', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    try:
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],
                    'player_skip': ['webpage'],
                }
            },
        }
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                formats.append({
                    'format_id': f.get('format_id'),
                    'ext': f.get('ext'),
                    'resolution': f.get('resolution', 'audio only'),
                    'height': f.get('height'),
                    'vcodec': f.get('vcodec', 'none')[:20],
                    'acodec': f.get('acodec', 'none')[:20],
                })

            return jsonify({
                'title': info.get('title'),
                'duration': info.get('duration'),
                'formats_count': len(formats),
                'formats': formats,
                'has_format_18': any(f['format_id'] == '18' for f in formats),
            })
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc(),
            'cookies_loaded': os.path.exists(COOKIES_FILE)
        }), 500

@app.route('/debug')
def debug():
    """Endpoint de debug para verificar configuración"""
    debug_info = {
        'cookies_file_exists': os.path.exists(COOKIES_FILE),
        'cookies_file_path': COOKIES_FILE,
        'cookies_env_var_set': 'COOKIES_BASE64' in os.environ,
        'local_cookies_exists': os.path.exists(LOCAL_COOKIES),
    }

    if os.path.exists(COOKIES_FILE):
        debug_info['cookies_file_size'] = os.path.getsize(COOKIES_FILE)
        # Leer archivo completo para verificar formato
        try:
            with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Verificar header Netscape
            has_netscape = any('Netscape HTTP Cookie File' in line for line in lines[:5])

            # Verificar cookies de YouTube
            youtube_cookies = [l for l in lines if 'youtube.com' in l and not l.strip().startswith('#')]

            # Cookies importantes de YouTube
            important_cookies = ['CONSENT', 'VISITOR_INFO1_LIVE', 'PREF', '__Secure']
            has_important = any(any(cookie in line for cookie in important_cookies) for line in youtube_cookies)

            debug_info['has_netscape_header'] = has_netscape
            debug_info['youtube_cookie_count'] = len(youtube_cookies)
            debug_info['has_important_cookies'] = has_important
            debug_info['cookies_format_ok'] = has_netscape and len(youtube_cookies) > 0
            debug_info['total_lines'] = len(lines)
            debug_info['first_line'] = lines[0] if lines else 'empty'

            # Mostrar algunas cookies (sin valores sensibles)
            if youtube_cookies:
                cookie_names = []
                for line in youtube_cookies[:5]:
                    fields = line.split('\t')
                    if len(fields) >= 6:
                        cookie_names.append(fields[5])  # El nombre de la cookie
                debug_info['sample_cookie_names'] = cookie_names

        except UnicodeDecodeError:
            debug_info['cookies_read_error'] = 'UnicodeDecodeError - archivo no es UTF-8'
        except Exception as e:
            debug_info['cookies_read_error'] = str(e)

    return jsonify(debug_info)

def get_ydl_configs(output_path):
    """Retorna múltiples configuraciones para intentar en orden"""

    base_config = {
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }

    # TODAS las configuraciones DEBEN tener player_client para bypass

    # Configuración 1: iOS - Mejor disponible (sin especificar formato exacto)
    config1 = {
        **base_config,
        'format': 'best',
        'extractor_args': {
            'youtube': {
                'player_client': ['ios'],
                'player_skip': ['webpage'],
            }
        },
    }

    # Configuración 2: Android - Lo que sea
    config2 = {
        **base_config,
        'format': 'best',
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
                'player_skip': ['webpage'],
            }
        },
    }

    # Configuración 3: Android TV (otro bypass)
    config3 = {
        **base_config,
        'format': 'best',
        'extractor_args': {
            'youtube': {
                'player_client': ['android_embedded'],
            }
        },
    }

    # Configuración 4: iOS con merge si es necesario
    config4 = {
        **base_config,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'extractor_args': {
            'youtube': {
                'player_client': ['ios'],
            }
        },
    }

    # Configuración 5: Web client
    config5 = {
        **base_config,
        'format': 'best',
        'extractor_args': {
            'youtube': {
                'player_client': ['web'],
            }
        },
    }

    # Agregar cookies si existen
    configs = [config1, config2, config3, config4, config5]
    if os.path.exists(COOKIES_FILE):
        print(f"🍪 Agregando cookies desde: {COOKIES_FILE}")
        for config in configs:
            config['cookiefile'] = COOKIES_FILE
    else:
        print(f"⚠️  No hay cookies disponibles en: {COOKIES_FILE}")

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
                print(f"🔄 Intento {i+1}/{len(configs)}: player_client={ydl_opts.get('extractor_args', {}).get('youtube', {}).get('player_client', 'default')}")
                print(f"🍪 Usando cookies: {'cookiefile' in ydl_opts}")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'video')

                # Si llegamos aquí, la descarga fue exitosa
                if os.path.exists(output_path):
                    print(f"✅ Descarga exitosa con configuración {i+1}")
                    return send_file(
                        output_path,
                        as_attachment=True,
                        download_name=f'{title}.mp4',
                        mimetype='video/mp4'
                    )
            except Exception as e:
                last_error = str(e)
                print(f"❌ Intento {i+1} falló: {str(e)[:100]}")
                # Si no es el último intento, continuar con la siguiente configuración
                if i < len(configs) - 1:
                    continue
                # Si es el último intento, lanzar el error
                raise Exception(last_error)

        return jsonify({'error': 'No se pudo descargar el video'}), 500

    except Exception as e:
        error_msg = str(e)
        print(f"🔴 Error final: {error_msg}")

        # Mensajes de error más específicos
        if 'bot' in error_msg.lower() or 'sign in' in error_msg.lower():
            cookies_loaded = os.path.exists(COOKIES_FILE)
            if cookies_loaded:
                error_msg = f'Las cookies están cargadas pero YouTube sigue bloqueando. Posibles causas:\n1. Las cookies expiraron (exporta nuevas)\n2. El formato del archivo cookies.txt es incorrecto\n3. Verifica /debug para más información'
            else:
                error_msg = 'YouTube está bloqueando la descarga. Exporta tus cookies de YouTube (ver COOKIES_GUIDE.md o SOLUCION_RAPIDA.md)'
        elif 'format' in error_msg.lower():
            error_msg = f'Formato de video no disponible. Error: {error_msg[:200]}'

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
