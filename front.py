import streamlit as st

# Page title
def main():
    # Sidebar
    st.sidebar.title("Selección de Modelo")
    model_option = st.sidebar.selectbox(
        "Elija el modelo:",
        ("Modelo OpenAI", "Modelo LLama 2 7B", "Modelo Hugging Open")
    )

    # Main content
    st.title("Probando modelos LLM Libres y Pagos")
    st.markdown(
    """
    Aplicación de Modelos de Lenguaje Libres en Chatbots de Data Aumentada.
    
    - **Jorge Andres Jaramillo Neme**
    """
)
    st.write("Chat:")
    user_input = st.text_input("Escribe tu mensaje aquí:")
    if user_input:
        st.write(f"Usuario: {user_input}")
        # Aquí podrías añadir la respuesta del modelo al mensaje del usuario,
        # algo así como:
        # response = get_model_response(user_input, model_option)
        # st.write(f"Modelo: {response}")
    uploaded_file = st.file_uploader("Subir archivo", type=['txt', 'pdf'])
    
    
    if uploaded_file:
        st.write("Archivo subido con éxito.")
        # Aquí puedes procesar el archivo según el modelo seleccionado, 
        # por ejemplo:
        # if model_option == "Modelo A":
        #     process_with_model_a(uploaded_file)
    


if __name__ == "__main__":
    main()
