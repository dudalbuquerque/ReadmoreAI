import streamlit
import requests
import os
from PIL import Image

# Define o caminho absoluto para a pasta `img`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "img")

# Certifica-se de que a pasta `img` existe
os.makedirs(IMG_DIR, exist_ok=True)

def resize(path: str, size=(360, 580)) -> str:
    with Image.open(path) as image:
        resized = image.resize(size)
        resized.save(path)
        return path

def add_book() -> None:
    if streamlit.session_state.book_input:
        book_name = streamlit.text_input("Digite o nome do livro:")
        book_img = get_book(book_name)
        if streamlit.button("Enviar"):
            if book_name and book_img != None:
                streamlit.session_state.book_input = False
                streamlit.success(f"Livro '{book_name}' Adicionado!")
                streamlit.session_state.titles.append(book_name)
                streamlit.session_state.books.append(resize(book_img))
                streamlit.rerun()
            else:
                streamlit.error("Nome Inválido.")
    else:
        if streamlit.button("Adcionar Livro", use_container_width=True):
            streamlit.session_state.book_input = True
            streamlit.rerun()

def show_books() -> None:
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

def suggest_books() -> None:
    streamlit.markdown("## Livros Sugeridos")
    if streamlit.button("Sugerir Livros", use_container_width=True, type="primary"):
        pass

def get_book_image(book_name):
    api_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_name}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            image_url = data["items"][0]["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            return image_url
    return None

def download_image(url, book_name):
    safe_name = "".join(c for c in book_name if c.isalnum() or c in " _-").strip()
    file_path = os.path.join(IMG_DIR, f"{safe_name}.jpg")

    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        return file_path
    else:
        return None

def get_book(book_name):
    url = get_book_image(book_name)
    if url is None:
        return None
    else:
        return download_image(url, book_name)
