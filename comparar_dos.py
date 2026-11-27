import face_recognition

UMBRAL = 0.6

# 1. Cargar las imágenes 
imagen1 = face_recognition.load_image_file("foto1.jpg")
imagen2 = face_recognition.load_image_file("foto2.jpg")

# 2. Convertir cada rostro en su lista de 128 números
#    Devuelve una lista: un elemento por cada rostro encontrado
codigos1 = face_recognition.face_encodings(imagen1)
codigos2 = face_recognition.face_encodings(imagen2)

print("Rostros en foto1:", len(codigos1))
print("Rostros en foto2:", len(codigos2))

# 3. Si alguna no tiene rostro, avisa y termina
if len(codigos1) == 0 or len(codigos2) == 0:
    print("No se encontró rostro en una de las fotos.")
else:
    # 4. Medir la distancia entre el primer rostro de cada foto
    distancia = face_recognition.face_distance([codigos1[0]], codigos2[0])[0]
    print("Distancia:", round(float(distancia), 3))

    if distancia <= UMBRAL:
        print("Parece la MISMA persona")
    else:
        print("Parecen personas DISTINTAS")