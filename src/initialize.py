import streamlit

def session_state():
    if "page" not in streamlit.session_state:
        streamlit.session_state.page = "Login"
    if "clicked_book" not in streamlit.session_state:
        streamlit.session_state.clicked_book = ''
    if "clicked_book_suggest" not in streamlit.session_state:
        streamlit.session_state.clicked_book_suggest = ''
    if "clicked_add" not in streamlit.session_state:
        streamlit.session_state.clicked_add = ''
    if "username" not in streamlit.session_state:
        streamlit.session_state.username = ''
    if "id" not in streamlit.session_state:
        streamlit.session_state.id = ''
    if "email" not in streamlit.session_state:
        streamlit.session_state.email = ''
    if "idade" not in streamlit.session_state:
        streamlit.session_state.idade = ''    
    if "books" not in streamlit.session_state:
        streamlit.session_state.books = []
    if "titles" not in streamlit.session_state:
        streamlit.session_state.titles = []
    if "messages" not in streamlit.session_state:
        streamlit.session_state.messages = []
    if "book_input" not in streamlit.session_state:
        streamlit.session_state.book_input = False
    if "sugeridos" not in streamlit.session_state:
        streamlit.session_state.sugeridos = []
    if "nomes_sugeridos" not in streamlit.session_state:
        streamlit.session_state.nomes_sugeridos = []