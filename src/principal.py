import streamlit
from src import mybooks, suggest

def main():
    tabs = streamlit.tabs(["Meus Livros", "Lista de livros sugeridos"])
    
    with tabs[0]:
        mybooks.show_books()
        mybooks.add_book()

    with tabs[1]:
        suggest.show_books_suggested()
    
    suggest.suggest_books()