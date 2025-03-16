import streamlit as st
from source.initialize import session_state

def main():
    """Página principal com navegação e opção de logout na barra lateral."""
    pages = {
        "ReadmoreAI": [
            st.Page("source/mybooks.py", title="Meus Livros"),
            st.Page("source/suggested.py", title="Lista de livros sugeridos"),
            st.Page("source/searchbook.py", title="Buscar Livro"),
        ],
    }
    pg = st.navigation(pages)
    pg.run()
    with st.sidebar:
        col1, _, col3 = st.columns([1, 1, 1])
        with col1:
            st.write(st.session_state.username)
        with col3:
            if st.button("Logout", type="primary", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()

if __name__ == "__main__":
    main()
