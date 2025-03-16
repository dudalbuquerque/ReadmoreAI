import streamlit as st
from source.initialize import session_state
from source import sidebar

def main():
    """Página principal após o login, com navegação entre páginas de livros."""
    pages = {
        "Páginas": [
            st.Page("source/mybooks.py", title="Meus Livros"),
            st.Page("source/suggested.py", title="Lista de Livros Sugeridos"),
            st.Page("source/searchbook.py", title="Buscar Livro"),
        ],
    }
    navigator = st.navigation(pages)
    navigator.run()
    sidebar.menu_expanded()

if __name__ == "__main__":
    main()
