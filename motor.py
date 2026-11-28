import numpy as np
import face_recognition
from PIL import Image, ImageOps

UMBRAL = 0.35          # distancia máxima para decir "es la misma persona"
TAMANO_MINIMO = 40    # imágenes más chicas que esto (en píxeles) no sirven
TAMANO_MAXIMO = 1600  # imágenes más grandes se reducen para ir más rápido


def _preparar(imagen_pil):
    """Convierte una imagen PIL en una matriz de números que face_recognition entiende."""
    imagen = ImageOps.exif_transpose(imagen_pil)  # endereza fotos de celular giradas
    imagen = imagen.convert("RGB")                # quita transparencia (RGBA) y grises

    ancho, alto = imagen.size
    if ancho < TAMANO_MINIMO or alto < TAMANO_MINIMO:
        return None                               # muy pequeña

    imagen.thumbnail((TAMANO_MAXIMO, TAMANO_MAXIMO))  # reduce solo si es grande
    return np.array(imagen)


def _area(ubicacion):
    """Área del rectángulo de un rostro. ubicacion = (arriba, derecha, abajo, izquierda)."""
    arriba, derecha, abajo, izquierda = ubicacion
    return (abajo - arriba) * (derecha - izquierda)


def comparar_rostro(foto, imagen):
    """Devuelve la distancia entre el rostro de 'foto' y el más parecido de 'imagen'.
    Menor = más parecido. Devuelve None si no se puede comparar."""
    try:
        matriz_foto = _preparar(foto)
        matriz_imagen = _preparar(imagen)
        if matriz_foto is None or matriz_imagen is None:
            return None

        # --- Rostro de la usuaria: si hay varios, el más grande ---
        ubicaciones = face_recognition.face_locations(matriz_foto)
        if len(ubicaciones) == 0:
            return None
        mas_grande = max(ubicaciones, key=_area)
        codigos_foto = face_recognition.face_encodings(
            matriz_foto, known_face_locations=[mas_grande]
        )
        if len(codigos_foto) == 0:
            return None
        codigo_usuaria = codigos_foto[0]

        # --- Rostros de la página: se comparan todos ---
        codigos_imagen = face_recognition.face_encodings(matriz_imagen)
        if len(codigos_imagen) == 0:
            return None

        distancias = face_recognition.face_distance(codigos_imagen, codigo_usuaria)
        return float(distancias.min())

    except Exception:
        # Imagen dañada, formato raro, etc.: no se cae el programa
        return None