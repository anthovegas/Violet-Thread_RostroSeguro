import streamlit as st
import pandas as pd

def buscar(foto):
    """Revisa las paginas y devuelve una tabla de resultados.

    Por ahora devuelve datos FALSOS. Cuando motor.py y rastreador.py estén listos, aquí se conectan.
    """
    return pd.DataFrame(
            [
                {"Página": "Página de prueba 1", "Enlace": "http://localhost:8000/pagina1.html", "Coincidencias": 1},
                {"Página": "Página de prueba 2", "Enlace": "http://localhost:8000/pagina2.html", "Coincidencias": 0},
                {"Página": "Página de prueba 3", "Enlace": "http://localhost:8000/pagina3.html", "Coincidencias": 1}
            ]
    )

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
        st.write("Línea 100: [verificar número y horario en fuente oficial]")
        st.write("Denuncia: [verificar la vía en fuente oficial]")

