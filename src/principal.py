import streamlit
from src import suggested
from src import mybooks, sidebar, searchbook


def main():
    # Inicializa o estado do menu como sempre expandido
    streamlit.session_state.menu_expanded = True

    # Exibe diretamente o menu
    sidebar.menu_expanded()

    tabs = streamlit.tabs(["Meus Livros", "Lista de livros sugeridos", "Buscar Livros"])
    
    with tabs[0]:
        mybooks.show_books()
        mybooks.add_book()

    with tabs[1]:
        suggested.show_books_suggested()

    with tabs[2]:
        searchbook.suggest_books()
