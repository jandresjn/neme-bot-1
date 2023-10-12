import streamlit as st
import random
import time
from components.sidebar import sidebar

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
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Pregúntame sobre tus documentos :)"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hablame mano",
                "Todo bien?",
                "De qué me hablas viejo",
            ]
        )
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
