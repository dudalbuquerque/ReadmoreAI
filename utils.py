import streamlit
from PIL import Image

# Padrão: 360 / 580
def resize(path: str, size=(270, 405)) -> str:
    with Image.open(path) as image:
        resized = image.resize(size)
        resized.save(path)
        return path

def add_book() -> None:
    if streamlit.session_state.book_input:
        book_name = streamlit.text_input("Digite o nome do livro:")
        if streamlit.button("Enviar"):
            if book_name:
                streamlit.session_state.book_input = False
                streamlit.success(f"Livro '{book_name}' Adicionado!")
                streamlit.session_state.books.append(resize("img/livro.jpg"))
                streamlit.rerun()
            else:
                streamlit.error("Nome Inválido.")
    else:
        if streamlit.button("Adcionar Livro", use_container_width=True):
            streamlit.session_state.book_input = True
            streamlit.rerun()

def show_books():
    streamlit.markdown("## Meus Livros")
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])
    for i, book in enumerate(streamlit.session_state.books):
        if i % 5 == 0:
            with c1:
                streamlit.image(book)
        elif i % 5 == 1:
            with c2:
                streamlit.image(book)
        elif i % 5 == 2:
            with c3:
                streamlit.image(book)
        elif i % 5 == 3:
            with c4:
                streamlit.image(book)
        elif i % 5 == 4:
            with c5:
                streamlit.image(book)

def suggest_books():
    streamlit.markdown("## Livros Sugeridos")
    if streamlit.button("Sugerir Livros", use_container_width=True, type="primary"):
        pass