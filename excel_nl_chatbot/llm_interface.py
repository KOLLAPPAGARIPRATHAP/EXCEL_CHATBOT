# llm_interface.py
import streamlit as st
from groq import Groq

def ask_llm(messages):
    """
    Sends full chat history to Groq and returns the latest response.
    Uses Streamlit secrets for API key management.
    """
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error communicating with Groq API: {e}")
        return "Sorry, there was an error processing your request."
