import streamlit as st
import pandas as pd
from PIL import Image

# Si motor.py y rastreador.py existen, se usan. Si no, la app muestra datos de ejemplo.

try:
    import motor
    import rastreador
    HAY_MODULOS = True
except ImportError:
    HAY_MODULOS = False


def buscar(foto_subida):
    """Revisa las paginas y devuelve una tabla de resultados."""

    if not HAY_MODULOS:
        return pd.DataFrame(
                [
                    {"Página": "Página de prueba 1", "Enlace": "http://localhost:8000/pagina1.html", "Coincidencias": 1},
                    {"Página": "Página de prueba 2", "Enlace": "http://localhost:8000/pagina2.html", "Coincidencias": 0},
                    {"Página": "Página de prueba 3", "Enlace": "http://localhost:8000/pagina3.html", "Coincidencias": 1}
                ]
        )

    # Convertimos la foto subida en una imagen PIL, que es lo que pide motor.py
    foto_subida.seek(0)
    foto = Image.open(foto_subida)

    filas = []
    comparaciones = 0
    fallidas = 0

    for url in rastreador.leer_paginas():
        try:
            imagenes = rastreador.revisar_pagina(url)
        except Exception:
            filas.append({"Página":url, "Enalce": url, "Coincidencias": "No se pudo leer"})
            continue

        n = 0
        for imagen in imagenes:
            distancia = motor.comparar_rostro(foto, imagen)
            comparaciones = comparaciones + 1
            if distancia is None:
                fallidas = fallidas + 1
            elif distancia <= motor.UMBRAL:
                n = n + 1
        filas.append({"Página": url, "Enlace": url, "Coincidencias": n})

    # Si TODAS las comparaciones fallaron, lo más probable es que la foto no tenga un rostro claro
    if comparaciones > 0 and fallidas == comparaciones:
        st.warning("No pudimos encontrar un rostro claro en tu foto. Prueba con otra foto de frente y con buena luz.")

    return pd.DataFrame(filas)

st.title("RostroSeguro")
st.write("No estás sola. Esta herramienta te ayuda a revisar si tu rostro aparece sin tu consetimiento.")

st.info("Solo para revisar tu propio rostro. Tu foto se procesa y se descarta; no se guarda.")

acepta = st.checkbox("Confirmo que la foto es mía y acepto que se procese solo para esta revisión. ")

if not acepta:
    st.stop()

situacion = st.selectbox(
    "¿Cuál es tu situación?",
    [
        "Creo que hay una imagen mía íntima circulando",
        "Creo que hay un deepfake (imagen manipulada con IA) con mi rostro",
        "Me tomaron una foto sin permiso en la calle o el transporte",
    ],
)

archivo = st.file_uploader("Sube una foto tuya (JPG o PNG)", type=["jpg", "jpeg", "png"])

if archivo is None:
    st.stop()

st.image(archivo, caption="Tu foto (no se guarda)", width=200)

if st.button("Revisar páginas"):
    st.session_state["revisado"] = True

if st.session_state.get("revisado"):
    resultados = buscar(archivo)
    st.subheader("Resultados")
    st.dataframe(resultados)
    st.caption("Solo revisamos las paginas configuradas. No garantizamos encontrar todo internet. ")

    st.subheader("¿Qué puedes hacer ahora?")
    tab1, tab2, tab3 = st.tabs(["1. Guarda evidencia", "2. Pide el retiro", "3. Dónde pedir ayuda"])

    with tab1:
        st.write("- Haz capturas de pantalla donde se vea el enlace, la fecha y la hora.")
        st.write("- Copia y guarda las URLS.")
        st.write("- No borres mensaje ni conversaciones relacionadas.")

    with tab2:
        st.text_area(
            "Borrador de solicitud de retiro",
            "Hola, soy [nombre]. Solicito el retiro inmediato del contenido en [enlace], publicado sin mi consentimiento. Quedo atenta a su respuesta. ",
            height=160,
        )
    with tab3:
        st.write("**Línea 100 (gratis, 24 horas):** llama al **100** desde cualquier teléfono. Atiende en español, quechua y aimara, y es confidencial.")
        st.write("**Chat 100:** orientación en línea, 24 horas: https://chat100.warminan.gob.pe/")
        st.write("**Centros Emergencia Mujer (CEM):** atención gratuita. Los que están en comisarías atienden las 24 horas.")
        st.write("**Para denunciar:** en una comisaría, en la Fiscalía o en la DIVINDAT de la Policía Nacional (delitos de alta tecnología).")
        st.caption("Datos de gob.pe. Esta herramienta no reemplaza la asesoría legal.")

