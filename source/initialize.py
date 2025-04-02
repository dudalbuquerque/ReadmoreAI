import streamlit as st
import google.generativeai as genai
from database import create, books, users

# Configuração da API do Google Generative AI (único ponto de configuração)
genai.configure(api_key="AIzaSyCW1jKDPvrpHFZY1Jc_uiPfz559i8Pwn-s")
model = genai.GenerativeModel("gemini-2.0-flash")

# Conexão com o banco de dados
my_db = create.DataBase()
book_user = books.BOOK(my_db)
user = users.USER(my_db)

def session_state():
    """Inicializa as variáveis de estado da sessão, se ainda não existirem."""
    defaults = {
        "page": "Login",
        "clicked_book": "",
        "clicked_book_suggest": "",
        "clicked_add": "",
        "validation": "",
        "username": "",
        "id": "",
        "email": "",
        "idade": "",
        "books": [],
        "titles": [],
        "messages": [],
        "book_input": False,
        "show_stars": False,
        "sugeridos": [],
        "nomes_sugeridos": []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
