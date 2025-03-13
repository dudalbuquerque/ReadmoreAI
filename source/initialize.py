import streamlit
import google.generativeai as genai
from database import create, books, users

# Configuração da API do Google Generative AI
genai.configure(api_key='-')
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Conexão com o banco de dados
my_db = create.DataBase()
book_user = books.BOOK(my_db)
user = users.USER(my_db)

def session_state():
    if "page" not in streamlit.session_state:
        streamlit.session_state.page = "Login"
    if "clicked_book" not in streamlit.session_state:
        streamlit.session_state.clicked_book = ''
    if "clicked_book_suggest" not in streamlit.session_state:
        streamlit.session_state.clicked_book_suggest = ''
    if "clicked_add" not in streamlit.session_state:
        streamlit.session_state.clicked_add = ''
    if "menu_expanded" not in streamlit.session_state:
        streamlit.session_state.menu_expanded = False
    if "validation" not in streamlit.session_state:
        streamlit.session_state.validation = ''    
    if "username" not in streamlit.session_state:
        streamlit.session_state.username = ''
    if "id" not in streamlit.session_state:
        streamlit.session_state.id = ''
    if "book_assessment" not in streamlit.session_state or not isinstance(streamlit.session_state.book_assessment, (int, float)):
        streamlit.session_state.book_assessment = 0
    if "show_stars" not in streamlit.session_state:
        streamlit.session_state.show_stars = False     
    if "book_input" not in streamlit.session_state:
        streamlit.session_state.book_input = False