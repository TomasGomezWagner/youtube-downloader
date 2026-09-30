#!/usr/bin/env python3
"""
Script de prueba rápido para verificar que yt-dlp funciona correctamente.
Uso: python test_download.py
"""

import yt_dlp
import os
import tempfile


def test_download():
    """Prueba rápida de descarga"""

    # Video de prueba (Rick Astley - Never Gonna Give You Up)
    test_url = "https://www.youtube.com/live/b_pmWoQZPK8"

    output_path = os.path.join(tempfile.gettempdir(), "test_video.mp4")

    print("🧪 Probando descarga de YouTube...")
    print(f"📹 URL: {test_url}")
    print(f"💾 Destino: {output_path}\n")

    configs = [
        {
            "name": "iOS Client (bv*+ba/b)",
            "opts": {
                "format": "bv*+ba/b",
                "outtmpl": output_path,
                "quiet": False,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["ios"],
                    }
                },
            },
        },
        {
            "name": "Android Client (b)",
            "opts": {
                "format": "b",
                "outtmpl": output_path,
                "quiet": False,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android"],
                    }
                },
            },
        },
        {
            "name": "Web Client (best)",
            "opts": {
                "format": "best",
                "outtmpl": output_path,
                "quiet": False,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["web"],
                    }
                },
            },
        },
    ]

    for i, config in enumerate(configs, 1):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🔄 Intento {i}/3: {config['name']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        try:
            with yt_dlp.YoutubeDL(config["opts"]) as ydl:
                info = ydl.extract_info(test_url, download=True)
                title = info.get("title", "Desconocido")

            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                print(f"\n✅ ¡ÉXITO!")
                print(f"📝 Título: {title}")
                print(f"📦 Tamaño: {file_size:.2f} MB")
                print(f"📁 Archivo: {output_path}")

                # Limpiar
                # os.remove(output_path)
                # print("\n🧹 Archivo de prueba eliminado")
                print("\n🎉 ¡Todo funciona correctamente!")
                return True

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            if i < len(configs):
                print("\n⏭️  Intentando siguiente configuración...\n")
            continue

    print("\n❌ Todas las configuraciones fallaron")
    print("\n💡 Posibles soluciones:")
    print("1. Actualiza yt-dlp: pip install --upgrade yt-dlp")
    print("2. Verifica tu conexión a internet")
    print("3. Consulta SOLUCION_RAPIDA.md para usar cookies")
    return False


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("   YOUTUBE DOWNLOADER - TEST DE DESCARGA")
    print("=" * 50 + "\n")

    try:
        test_download()
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")

    print("\n" + "=" * 50 + "\n")
