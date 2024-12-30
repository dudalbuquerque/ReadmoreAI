import streamlit

def session_state():
    if "page" not in streamlit.session_state:
        streamlit.session_state.page = "Login"
    if "username" not in streamlit.session_state:
        streamlit.session_state.username = None
    if "books" not in streamlit.session_state:
        streamlit.session_state.books = []
    if "titles" not in streamlit.session_state:
        streamlit.session_state.titles = []
    if "messages" not in streamlit.session_state:
        streamlit.session_state.messages = []
    if "book_input" not in streamlit.session_state:
        streamlit.session_state.book_input = False
