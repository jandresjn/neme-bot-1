import streamlit as st
from .faq import faqMD

def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True
    print('OPENAI API key is Configured Successfully!')

def sidebar():
    with st.sidebar:
        st.title("Instrucciones 🐹")
        st.subheader("1. Selección de modelo")
        model_option = st.sidebar.selectbox(
            "Elija el modelo:",
            ("Modelo OpenAI", "Modelo LLama 2 7B", "Modelo Hugging Open")
        )
        st.sidebar.subheader('2. ¡Sube un documento para interactuar!')
        uploaded_file = st.sidebar.file_uploader("Subir archivo", type=['txt', 'pdf'])
        
        if uploaded_file:
            st.write("Archivo subido con éxito.")
            st.write("¡**Ya puedes hablar con tu documento** :sunglasses:!")
            # Aquí puedes procesar el archivo según el modelo seleccionado, 
            # por ejemplo:
            # if model_option == "Modelo A":
            #     process_with_model_a(uploaded_file)
        st.sidebar.subheader('3. Configuración de Key')
        st.markdown(
            "Ingresa tu [OpenAI API key](https://platform.openai.com/account/api-keys)🔑\n"  # noqa: E501
        )
        open_api_key_input = st.text_input(
            "Openai API Key",
            type="password",
            placeholder="Paste your API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPEN_API_KEY", ""),
        )

        if open_api_key_input:
            # print(f'Entered API is {open_api_key_input}')
            set_open_api_key(open_api_key_input)

        if not st.session_state.get("open_api_key_configured"):
            st.error("Please configure your Open API key!")
        else:
            st.markdown("Open API Key Configured!")

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖 App de prueba de modelos LLM"
        )
        st.markdown("Made by [**Jorge Jaramillo**](https://github.com/jandresjn/neme-bot-1)")
        st.markdown("Desarrollo de Proyectos de IA")
        st.markdown("Credits for Template [amjadraza](https://github.com/amjadraza/langchain-streamlit-docker-template/blob/main/demo_app/main.py")
        
        st.markdown("---")

        # About component
        faqMD()