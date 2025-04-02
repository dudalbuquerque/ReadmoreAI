import streamlit as st
from source.initialize import session_state
from source.mybooks import show_books
from source.suggested import show_books_suggested
from source.searchbook import suggest_books
from source.myinformation import myinformation

def main():
    """Página principal com navegação e opção de logout na barra lateral."""
    tab1, tab2, tab3, tab4 = st.tabs(["Meus Livros", "Lista de livros sugeridos", "Buscar Livro", "Minhas informações"])

    with tab1:
        show_books()
    with tab2:
        show_books_suggested()
    with tab3:
        suggest_books()
    with tab4:
        myinformation()

