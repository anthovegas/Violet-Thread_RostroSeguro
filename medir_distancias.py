from pathlib import Path
from PIL import Image
import motor

foto = Image.open("pruebas_fotos/persona1.jpg")

for ruta in sorted(Path("sitio_prueba/imagenes").glob("*.jpg")):
    d = motor.comparar_rostro(foto, Image.open(ruta))
    texto = "no se pudo comparar" if d is None else f"{d:.3f}"
    print(f"{ruta.name:20} {texto}")