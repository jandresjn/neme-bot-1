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


from dotenv import load_dotenv, find_dotenv

# Carga las variables del archivo .env
load_dotenv(find_dotenv())

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

# Page title
def main():

    sidebar()
    
    # Main content
    st.title("Probando modelos LLM - Demo🦊")
    st.markdown(
    """
    **Aplicación de Modelos de Lenguaje Libres en Chatbots de Data Aumentada**
    """
    )
    # Initialize chat history
     #Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

        # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    
    
    # User-provided prompt
    user_input = st.chat_input()
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_llama2_response(st.session_state.messages[-1]["content"])
                    placeholder = st.empty()
                    full_response = ''
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
