"""rastreador.py - Lee las págunas de la lista y baja sus imágenes.

Dos funciones, que usa app.py:
    leer_paginas()      -> lista de URLs (de config/paginas.txt)
    revisar_pagina(url) -> lista de imágenes (PIL.Image) de esa página
"""

from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from PIL import Image

ARCHIVO_PAGINAS = Path("config/paginas.txt")
TIMEOUT = 5 # segundos que esperamos antes de rendirnos

def leer_paginas():
    """Lee config/paginas.txt (una URL por línea).
    Ignora líneas vacías y las que empiezan con #."""
    if not ARCHIVO_PAGINAS.exists():
        return []
    urls = []
    #utf-8-sig quita el carácter invisible (BOM) que PowerShell agrega al inicio
    for linea in ARCHIVO_PAGINAS.read_text(encoding="utf-8-sig").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#"):
            urls.append(linea)
    return urls

def revisar_pagina(url):
    """Descarga la página y devuelve sus imágenes como lista de PIL.Image(RGB).
    - Imagen rota o que no abre: se salta.
    - Página caída o inexistente: lanza ConnectionError (app.py lo atrapa)."""
    try:
        respuesta = requests.get(url, timeout=TIMEOUT)
        respuesta.raise_for_status()
    except requests.RequestException as error:
        raise ConnectionError(f"No se pudo leer {url}: {error}")

    sopa = BeautifulSoup(respuesta.text, "html.parser")

    imagenes = []
    for etiqueta in sopa.find_all("img"):
        src = etiqueta.get("src")
        if not src:
            continue
        direccion = urljoin(url, src) # convierte "imagenes/a.jpg" en una URL completa
        try:
            r = requests.get(direccion, timeout=TIMEOUT)
            r.raise_for_status()
            imagenes.append(Image.open(BytesIO(r.content)).convert("RGB"))
        except Exception:
            continue # imagen rota: la saltamos
    return imagenes