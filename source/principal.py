import streamlit
from source.initialize import *

def main():
    pages = {
    "ReadmoreAI": [
        streamlit.Page("source/mybooks.py", title="Meus Livros"),
        streamlit.Page("source/suggested.py", title="Lista de livros sugeridos"),
        streamlit.Page("source/searchbook.py", title="Buscar Livro"),
    ],
    }

    pg = streamlit.navigation(pages)
    pg.run()
    with streamlit.sidebar:
        c1, _, c3= streamlit.columns([1, 1, 1])
        with c1:
            streamlit.write(f"{streamlit.session_state.username}")
        
        with c3:
            if streamlit.button("Logout", type="primary", use_container_width=True):                 
                streamlit.session_state.page = "Login"                 
                streamlit.rerun()
    # Inicializa o estado do menu como sempre expandido
    #streamlit.session_state.menu_expanded = True


    """
    tabs = streamlit.tabs(["Meus Livros", "Lista de livros sugeridos", "Buscar Livros"])
    
    with tabs[0]:
        mybooks.show_books()
        mybooks.add_book()

    with tabs[1]:
        suggested.show_books_suggested()

    with tabs[2]:
        searchbook.suggest_books()    
    """

