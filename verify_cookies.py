#!/usr/bin/env python3
"""
Script para verificar que el archivo cookies.txt tenga el formato correcto.
Uso: python verify_cookies.py cookies.txt
"""

import sys
import os

def verify_netscape_format(file_path):
    """Verifica que el archivo tenga formato Netscape"""
    if not os.path.exists(file_path):
        return False, f"❌ Archivo no encontrado: {file_path}"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            return False, "❌ Archivo vacío"

        # Verificar header Netscape
        has_netscape_header = any('Netscape HTTP Cookie File' in line for line in lines[:5])

        # Contar líneas de cookies (no comentarios ni vacías)
        cookie_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]

        # Verificar que tenga youtube.com
        has_youtube = any('youtube.com' in line or '.youtube.com' in line for line in cookie_lines)

        # Verificar formato de las líneas (deberían tener 7 campos separados por tabs)
        valid_format = []
        for line in cookie_lines[:5]:  # Verificar primeras 5 cookies
            fields = line.strip().split('\t')
            valid_format.append(len(fields) == 7)

        issues = []
        if not has_netscape_header:
            issues.append("⚠️  Falta el header '# Netscape HTTP Cookie File'")

        if not has_youtube:
            issues.append("❌ No se encontraron cookies de youtube.com")

        if cookie_lines and not any(valid_format):
            issues.append("❌ Formato incorrecto: las cookies deben tener 7 campos separados por TABs")

        if not cookie_lines:
            issues.append("❌ No hay cookies válidas en el archivo")

        if issues:
            return False, "\n".join(issues)

        return True, f"✅ Formato correcto\n📊 {len(cookie_lines)} cookies encontradas\n🎯 Cookies de YouTube: Sí"

    except UnicodeDecodeError:
        return False, "❌ Error de codificación. El archivo debe ser texto UTF-8"
    except Exception as e:
        return False, f"❌ Error al leer archivo: {e}"

def main():
    if len(sys.argv) != 2:
        print("Uso: python verify_cookies.py cookies.txt")
        print("\nBusca el archivo cookies.txt por defecto...")

        # Intentar buscar archivos comunes
        common_names = ['cookies.txt', 'youtube.com_cookies.txt', 'www.youtube.com_cookies.txt']
        for name in common_names:
            if os.path.exists(name):
                file_path = name
                print(f"✅ Encontrado: {name}\n")
                break
        else:
            print("❌ No se encontró cookies.txt")
            sys.exit(1)
    else:
        file_path = sys.argv[1]

    print("="*60)
    print(f"  VERIFICADOR DE COOKIES - {os.path.basename(file_path)}")
    print("="*60 + "\n")

    success, message = verify_netscape_format(file_path)

    print(message)
    print("\n" + "="*60)

    if success:
        print("\n✅ El archivo está listo para usar")
        print("\nPara Render:")
        print(f"  python encode_cookies.py {file_path}")
        print("\nPara local:")
        print(f"  cp {file_path} cookies.txt")
    else:
        print("\n❌ El archivo tiene problemas")
        print("\n💡 Solución:")
        print("1. Usa la extensión 'Get cookies.txt LOCALLY' en Chrome/Firefox")
        print("2. Ve a youtube.com e inicia sesión")
        print("3. Click en la extensión → Export")
        print("4. Guarda como cookies.txt")
        print("\nMás info: COOKIES_GUIDE.md")

    print("\n")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
