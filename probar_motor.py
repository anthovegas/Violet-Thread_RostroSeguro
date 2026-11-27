from PIL import Image
from motor import comparar_rostro, UMBRAL

foto = Image.open("foto1.jpg")

casos = {
    "misma persona": "foto2.jpg",
    "otra persona": "otra.jpg",
    "sin rostro": "paisaje.jpg",
    "varios rostros": "grupo.jpg",
}

for nombre, ruta in casos.items():
    d = comparar_rostro(foto, Image.open(ruta))
    if d is None:
        print(f"{nombre}: None (no se pudo comparar)")
    else:
        veredicto = "MISMA" if d <= UMBRAL else "DISTINTA"
        print(f"{nombre}: {d:.3f} -> {veredicto}")