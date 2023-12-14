import streamlit as st
import random
import time
import os
from components.sidebar import sidebar

from langchain.chat_models.azureml_endpoint import AzureMLChatOnlineEndpoint
from langchain.chat_models.azureml_endpoint import LlamaContentFormatter
from langchain.schema import HumanMessage,SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
import whisper
from components.faq import faqMD
import torch
from langchain.llms import OpenAI
from langchain import PromptTemplate

from dotenv import load_dotenv, find_dotenv

# Carga las variables del archivo .env
load_dotenv(find_dotenv())


def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True
    print('OPENAI API key is Configured Successfully!')

# Template para detectar palabras repetidas
template = """Texto: {texto}

Instrucciones: Identifica las palabras que se repiten en el texto anterior y lista cada palabra repetida junto con la cantidad de veces que aparece.

Palabras repetidas:"""
prompt = PromptTemplate(template=template, input_variables=["texto"])
#def transcribe(audio_path):
 #   audio = whisper.load_audio(audio_path)
  #  audio = whisper.pad_or_trim(audio)
   # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    #_, probs = model.detect_language(mel)
    #print(f"Detected language: {max(probs, key=probs.get)}")
    #options = whisper.DecodingOptions()
    #result = whisper.decode(model, mel, options)
    #return result.text
def transcribe(audio_path):
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)

    # Convertir el numpy array a un tensor de PyTorch en FP32
    audio = torch.tensor(audio, dtype=torch.float32)

    # Crea el espectrograma log-Mel y asegúrate de que esté en FP32
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    return result.text

parameters = {
    "max_length": 200,
    "temperature": 0.6,
    "do_sample": True,
    "max_new_tokens": 200
}

# Usa las variables de entorno en lugar de las cadenas codificadas
endpoint_url = os.environ['AZURE_ENDPOINT_URL']
endpoint_api_key = os.environ['AZURE_API_KEY']

chat_llama_chain = AzureMLChatOnlineEndpoint(
    endpoint_url=endpoint_url,
    endpoint_api_key=endpoint_api_key,
    content_formatter=LlamaContentFormatter(),
    model_kwargs=parameters
)

def generate_llama2_response(prompt_input):
    output = chat_llama_chain(messages=[
    HumanMessage(content=str(prompt_input))])
    return output.content


model = whisper.load_model("base")
model.device

llm = OpenAI(temperature=0.9)
# Page title
def main():

    with st.sidebar:
        st.title("Instrucciones 🐹")

        st.sidebar.subheader('1. Configuración de Key')
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
            os.environ["OPENAI_API_KEY"] =str(open_api_key_input)

        if not st.session_state.get("open_api_key_configured"):
            st.error("Please configure your Open API key!")
        else:
            st.markdown("Open API Key Configured!")

        st.sidebar.subheader('2. ¡Sube un audio o habla en el chat!')
        uploaded_file = st.sidebar.file_uploader("Subir audio", type=['txt', 'pdf','wav','mp3'])
        
        if uploaded_file:
            st.write("Audio subido con éxito.")
            st.write("¡**Espera las correcciones a continuación** :sunglasses:!")
            st.session_state['uploaded_file'] = uploaded_file

            # Aquí puedes procesar el archivo según el modelo seleccionado, 
            # por ejemplo:
            # if model_option == "Modelo A":
            #     process_with_model_a(uploaded_file)
        st.sidebar.subheader('3. Espera las recomendaciones del experto 🐹')
        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "Desarrollar un prototipo de aplicación de procesamiento de lenguaje natural (PLN) que utilice un modelo para transcribir texto de audio o video y, posteriormente, emplee un modelo de lenguaje para identificar y cuantificar muletillas en el habla. La aplicación apunta a mejorar las habilidades de comunicación verbal de los usuarios proporcionando retroalimentación específica y sugerencias para mejorar."
        )
        st.markdown("Made by [**Jorge Jaramillo**](https://github.com/jandresjn/neme-bot-1) y [Leonardo Grisales](https://github.com/jandresjn/neme-bot-1)")
        st.markdown("Procesamiento de Datos Secuenciales - UAO")
        #st.markdown("Credits for Template [amjadraza](https://github.com/amjadraza/langchain-streamlit-docker-template/blob/main/demo_app/main.py")
        
        st.markdown("---")

        # About component
        faqMD()
    
    # Main content
    st.title(" :balloon: Detector de muletillas- Demo🦊")
    st.markdown(
    """
    **Aplicación de IA para**
    """
    )

    if uploaded_file is not None:
    # Guarda el archivo de audio en un directorio temporal
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.audio(uploaded_file.name)
        st.write("Transcribiendo...")
        transcription = transcribe(uploaded_file.name)

        # Muestra la transcripción
        st.write("Transcripción:")
        st.text_area("Resultado:", transcription, height=250)
        # Formatear el prompt con la transcripción
        formatted_prompt = prompt.format(texto=transcription)

        # Ejecutar el modelo de lenguaje con el prompt formateado
        palabras_repetidas = llm(formatted_prompt)

        # Mostrar las palabras repetidas
        st.write("Análisis de Palabras Repetidas:")
        st.text(palabras_repetidas)


if __name__ == "__main__":
    main()
