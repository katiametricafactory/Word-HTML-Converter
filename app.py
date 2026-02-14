import streamlit as st
from converter import convert_word_to_html
import streamlit.components.v1 as components
import uuid

st.set_page_config(layout="wide")

st.title("Word → HTML Converter")

uploaded_file = st.file_uploader("Sube un archivo .doc o .docx", type=["doc", "docx"])

if uploaded_file:
    html_output = convert_word_to_html(uploaded_file)

    # Generamos un ID único para evitar conflictos JS
    unique_id = str(uuid.uuid4()).replace("-", "")

    col1, col2 = st.columns(2)

    # =========================
    # COLUMNA IZQUIERDA (HTML)
    # =========================
    with col1:
        st.subheader("Código HTML")

        st.text_area(
            "HTML generado",
            html_output,
            height=600,
            key="html_area"
        )

        copy_button_html = f"""
        <button onclick="copyToClipboard_{unique_id}()" 
        style="padding:8px 16px; background-color:#0a8f08; color:white; border:none; cursor:pointer;">
        Copiar HTML
        </button>

        <script>
        function copyToClipboard_{unique_id}() {{
            navigator.clipboard.writeText(`{html_output}`);
            alert("HTML copiado al portapapeles");
        }}
        </script>
        """

        components.html(copy_button_html, height=80)

    # =========================
    # COLUMNA DERECHA (VISTA)
    # =========================
    with col2:
        st.subheader("Vista previa")

        st.components.v1.html(
            html_output,
            height=600,
            scrolling=True
        )

        copy_button_html_right = f"""
        <button onclick="copyToClipboardRight_{unique_id}()" 
        style="padding:8px 16px; background-color:#0a8f08; color:white; border:none; cursor:pointer;">
        Copiar HTML
        </button>

        <script>
        function copyToClipboardRight_{unique_id}() {{
            navigator.clipboard.writeText(`{html_output}`);
            alert("HTML copiado al portapapeles");
        }}
        </script>
        """

        components.html(copy_button_html_right, height=80)
