import streamlit as st
from converter import convert_word_to_html
import streamlit.components.v1 as components
import base64

st.set_page_config(layout="wide")
st.title("Word → HTML Converter")

uploaded_file = st.file_uploader("Sube un archivo .doc o .docx", type=["doc", "docx"])

if uploaded_file:

    # Inicialización
    if "history" not in st.session_state:
        initial_html = convert_word_to_html(uploaded_file)
        st.session_state.history = [initial_html]
        st.session_state.history_index = 0

    current_html = st.session_state.history[st.session_state.history_index]

    col1, col2 = st.columns(2)

    # =========================
    # COLUMNA IZQUIERDA
    # =========================
    with col1:
        st.subheader("Código HTML (editable)")

        edited_html = st.text_area(
            "Modifica el HTML si lo necesitas. Para ver los cambios dale click en la ventana derecha",
            value=current_html,
            height=600,
            key="editor"
        )

        # Si cambia el contenido → guardar en historial
        if edited_html != current_html:
            # Cortar historial si estamos en medio
            st.session_state.history = st.session_state.history[:st.session_state.history_index + 1]
            st.session_state.history.append(edited_html)
            st.session_state.history_index += 1

        # -------- BOTONES --------
        col_undo, col_redo, col_copy = st.columns(3)

        with col_undo:
            if st.button("Deshacer"):
                if st.session_state.history_index > 0:
                    st.session_state.history_index -= 1
                    st.rerun()

        with col_redo:
            if st.button("Rehacer"):
                if st.session_state.history_index < len(st.session_state.history) - 1:
                    st.session_state.history_index += 1
                    st.rerun()

        with col_copy:
            encoded_html = base64.b64encode(
                st.session_state.history[st.session_state.history_index].encode()
            ).decode()

            copy_button = f"""
            <button onclick="copyToClipboard()" 
            style="padding:6px 12px; background-color:#0a8f08; color:white; border:none; cursor:pointer;">
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

            components.html(copy_button, height=60)

    # =========================
    # COLUMNA DERECHA
    # =========================
    with col2:
        st.subheader("Vista previa en tiempo real")

        components.html(
            st.session_state.history[st.session_state.history_index],
            height=600,
            scrolling=True
        )
