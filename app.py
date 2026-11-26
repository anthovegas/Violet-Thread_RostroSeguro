import streamlit as st
import pandas as pd

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
    resultados = pd.DataFrame(
        [
            {"Página": "Página de prueba 1", "Enlace": "http://localhost:8000/pagina1.html", "Coincidencias": 1},
            {"Página": "Página de prueba 2", "Enlace": "http://localhost:8000/pagina2.html", "Coincidencias": 0},
            {"Página": "Página de prueba 3", "Enlace": "http://localhost:8000/pagina3.html", "Coincidencias": 1}
        ]
    )
    st.subheader("Resultados")
    st.dataframe(resultados)
    st.caption("Solo revisamos las paginas configuradas. No garantizamos encontrar todo internet. ")