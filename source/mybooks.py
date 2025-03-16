import os
import sys
import streamlit as st
import requests

# Ajuste de caminho para incluir o diretório pai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from source.initialize import model, book_user

def add_book():
    """Exibe a interface para adicionar um novo livro."""
    if st.session_state.get("book_input", False):
        book_name = st.text_input("Digite o nome do livro:")
        _, col_center, _ = st.columns([1, 1, 1])
        with col_center:
            book_assessment = st.slider("Qual a nota do livro:", 0.0, 5.0, 2.5, format="%.1f")
        if st.button("Enviar"):
            if book_name:
                # Obter o nome do autor usando a API generativa
                book_author_response = model.generate_content(
                    f"Qual o nome do autor {book_name} (apenas o nome do autor)"
                )
                if hasattr(book_author_response, "candidates") and book_author_response.candidates:
                    book_author_name = book_author_response.candidates[0].content.parts[0].text
                else:
                    st.error("Erro: Não foi possível gerar o autor do livro.")
                    book_author_name = None
                generos_literarios = [
                    "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
                    "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
                    "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
                    "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
                ]
                book_genero_response = model.generate_content(
                    f"Informe o gênero ou os gêneros do livro {book_name} com base na lista {generos_literarios}. Retorne apenas o nome do gênero ou os gêneros, separados por vírgulas."
                )
                if hasattr(book_genero_response, "candidates") and book_genero_response.candidates:
                    book_genero_name = book_genero_response.candidates[0].content.parts[0].text
                else:
                    st.error("Erro: Não foi possível determinar o gênero do livro.")
                    book_genero_name = None

                book_img_url = get_book_image(book_name)
                user_id = st.session_state.id

                book_user.insert_book(
                    user_id=user_id,
                    book_title=book_name.title(),
                    book_author=book_author_name,
                    book_genre=book_genero_name,
                    book_assessment=book_assessment,
                    book_url=book_img_url,
                    book_read=1
                )
                st.success(f"Livro {book_name} adicionado!")
                st.session_state.book_input = False
                st.rerun()
            else:
                st.error("Nome inválido.")
    else:
        if st.button("Adicionar Livro", use_container_width=True):
            st.session_state.book_input = True
            st.rerun()

def display_book_details(book_name, book_img_url, book_author, book_genre, book_assessment):
    """Exibe os detalhes de um livro em uma seção expansível."""
    st.markdown(
        """
        <style>
        .expander-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Detalhes do Livro", expanded=True):
        st.markdown("<div class=\"expander-content\">", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(book_img_url, width=200)
        with col2:
            st.write(f"**Nome:** {book_name}")
            st.write(f"**Autor:** {book_author}")
            st.write(f"**Gênero:** {book_genre}")
            st.write(f"**Avaliação:** {book_assessment:.1f} / 5")
            left, _, right = st.columns([1, 1, 1])
            with left:
                if st.button("Fechar", type="primary", use_container_width=True):
                    st.session_state.clicked_book = ""
                    st.rerun()
            with right:
                if st.button("Deletar", type="primary", use_container_width=True):
                    book_user.delete_book(book_name, st.session_state.id)
                    st.session_state.clicked_book = ""
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def show_books():
    """Exibe os livros do usuário organizados em colunas."""
    st.markdown("## Meus Livros")
    cols = st.columns(5)
    books_data = book_user.return_info(st.session_state.id, 1)
    if st.session_state.clicked_book:
        book = st.session_state.clicked_book
        display_book_details(
            book_name=book[0],
            book_img_url=book[4],
            book_author=book[1],
            book_genre=book[2],
            book_assessment=book[3],
        )
    else:
        for i, book in enumerate(books_data):
            book_name = book[0]
            book_img_url = book[4]
            column = cols[i % 5]
            with column:
                st.image(book_img_url, use_container_width=True)
                if st.button(f"{book_name}", key=f"book_{i}", use_container_width=True):
                    st.session_state.clicked_book = book
                    st.rerun()

def display_books_suggested_details(book):
    """Exibe os detalhes de um livro sugerido."""
    st.markdown(
        """
        <style>
        .expander-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Detalhes do Livro", expanded=True):
        st.markdown("<div class=\"expander-content\">", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            book_img_url = get_book_image(book[0])
            st.image(book_img_url, width=200)
        with col2:
            st.write(f"**Nome:** {book[0]}")
            st.write(f"**Autor:** {book[1]}")
            st.write(f"**Sinopse:** {book[2]}")
            if st.button("Fechar", type="primary", use_container_width=True):
                st.session_state.clicked_book = ""
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def get_book_image(book_name):
    """Busca a URL da imagem do livro utilizando a API do Google Books."""
    api_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_name}
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["volumeInfo"].get("imageLinks", {}).get("thumbnail")
    return None

show_books()
add_book()
