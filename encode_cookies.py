#!/usr/bin/env python3
"""
Script para codificar cookies.txt en base64 para usar en Render.
Uso: python encode_cookies.py cookies.txt
"""

import base64
import sys
import os

if len(sys.argv) != 2:
    print("Uso: python encode_cookies.py cookies.txt")
    sys.exit(1)

cookies_file = sys.argv[1]

if not os.path.exists(cookies_file):
    print(f"Error: No se encontró el archivo {cookies_file}")
    sys.exit(1)

with open(cookies_file, 'rb') as f:
    cookies_content = f.read()

encoded = base64.b64encode(cookies_content).decode('utf-8')

print("\n" + "="*80)
print("COOKIES EN BASE64 - Copia todo el texto de abajo:")
print("="*80)
print(encoded)
print("="*80)
print("\nInstrucciones:")
print("1. Ve a tu servicio en Render.com")
print("2. Ve a Environment → Add Environment Variable")
print("3. Nombre: COOKIES_BASE64")
print("4. Valor: Pega el texto de arriba")
print("5. Guarda y espera a que redeploy automático termine")
print("="*80)
