import streamlit as st
from converter import convert_word_to_html
import streamlit.components.v1 as components
import base64

st.set_page_config(layout="wide")
st.title("Word → HTML Converter")

uploaded_file = st.file_uploader(
    "Sube un archivo .doc o .docx",
    type=["doc", "docx"]
)

if uploaded_file:

    # Generar HTML inicial solo una vez por archivo
    if "html_content" not in st.session_state:
        st.session_state.html_content = convert_word_to_html(uploaded_file)

    col1, col2 = st.columns(2)

    # =========================
    # COLUMNA IZQUIERDA (EDITOR)
    # =========================
    with col1:
        st.subheader("Código HTML (editable)")

        st.session_state.html_content = st.text_area(
            "Modifica el HTML si lo necesitas. Tienes que dar clic en la parte derecha para ver el cambio",
            value=st.session_state.html_content,
            height=600
        )

        # Botón copiar (seguro con base64)
        encoded_html = base64.b64encode(
            st.session_state.html_content.encode()
        ).decode()

        copy_button = f"""
        <button onclick="copyToClipboard()" 
        style="padding:8px 16px; background-color:#0a8f08; color:white; border:none; cursor:pointer;">
        Copiar HTML
        </button>

        <script>
        function copyToClipboard() {{
            const decoded = atob("{encoded_html}");
            navigator.clipboard.writeText(decoded);
            alert("HTML copiado al portapapeles");
        }}
        </script>
        """

        components.html(copy_button, height=80)

    # =========================
    # COLUMNA DERECHA (PREVIEW)
    # =========================
    with col2:
        st.subheader("Vista previa en tiempo real")

        components.html(
            st.session_state.html_content,
            height=600,
            scrolling=True
        )
