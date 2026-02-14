import streamlit as st
from converter import convert_word_to_html
import streamlit.components.v1 as components
import uuid
import base64

st.set_page_config(layout="wide")

st.title("Word → HTML Converter")

uploaded_file = st.file_uploader("Sube un archivo .doc o .docx", type=["doc", "docx"])

if uploaded_file:

    # Generar HTML inicial
    generated_html = convert_word_to_html(uploaded_file)

    col1, col2 = st.columns(2)

    # =========================
    # COLUMNA IZQUIERDA (EDITABLE)
    # =========================
    with col1:
        st.subheader("Código HTML (editable)")

        edited_html = st.text_area(
            "Modifica el HTML si lo necesitas",
            value=generated_html,
            height=600
        )

        # Botón copiar (versión segura con base64)
        encoded_html = base64.b64encode(edited_html.encode()).decode()
        unique_id_left = str(uuid.uuid4()).replace("-", "")

        copy_button_left = f"""
        <button onclick="copyLeft_{unique_id_left}()" 
        style="padding:8px 16px; background-color:#0a8f08; color:white; border:none; cursor:pointer;">
        Copiar HTML
        </button>

        <script>
        function copyLeft_{unique_id_left}() {{
            const decoded = atob("{encoded_html}");
            navigator.clipboard.writeText(decoded);
            alert("HTML copiado al portapapeles");
        }}
        </script>
        """

        components.html(copy_button_left, height=80)

    # =========================
    # COLUMNA DERECHA (PREVIEW DINÁMICA)
    # =========================
    with col2:
        st.subheader("Vista previa en tiempo real")

        components.html(
            edited_html,
            height=600,
            scrolling=True
        )

        # Botón copiar también en la derecha
        unique_id_right = str(uuid.uuid4()).replace("-", "")

        copy_button_right = f"""
        <button onclick="copyRight_{unique_id_right}()" 
        style="padding:8px 16px; background-color:#0a8f08; color:white; border:none; cursor:pointer;">
        Copiar HTML
        </button>

        <script>
        function copyRight_{unique_id_right}() {{
            const decoded = atob("{encoded_html}");
            navigator.clipboard.writeText(decoded);
            alert("HTML copiado al portapapeles");
        }}
        </script>
        """

        components.html(copy_button_right, height=80)
