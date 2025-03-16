import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from source.initialize import model, book_user
from source import mybooks

def display_books_suggested_details(book):
    """
    Exibe os detalhes do livro sugerido em um expander.
    
    Parâmetros:
        book: Lista com informações do livro, onde:
              índice 0: Nome, índice 1: Autor, índice 2: Sinopse, índice 3: URL da imagem.
    """
    book_img_url = book[3]
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
            st.write(f"**Nome:** {book[0]}")
            st.write(f"**Autor:** {book[1]}")
            st.write(f"**Sinopse:** {book[2]}")
            left, _, right = st.columns([1, 1, 1])
            with left:
                if st.button("Deletar", type="primary", use_container_width=True):
                    book_user.delete_book(book[0], st.session_state.id)
                    st.session_state.clicked_book_suggest = ""
                    st.rerun()
            with right:
                if st.button("Fechar", type="primary", use_container_width=True):
                    st.session_state.clicked_book_suggest = ""
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def show_books_suggested():
    """Exibe a lista de livros sugeridos em colunas."""
    st.markdown("## Livros Sugeridos")
    cols = st.columns(5)
    books_data = book_user.return_info(st.session_state.id, 0)
    if st.session_state.clicked_book_suggest:
        display_books_suggested_details(st.session_state.clicked_book_suggest)
    else:
        for i, book in enumerate(books_data):
            book_name = book[0]
            column = cols[i % 5]
            with column:
                st.image(book[4], use_container_width=True)
                if st.button(f"{book_name}", use_container_width=True):
                    st.session_state.clicked_book_suggest = book
                    st.rerun()

def add_db_book_suggested(book):
    """
    Adiciona um livro sugerido ao banco de dados.
    
    Parâmetros:
        book: Lista com informações do livro [título, autor, sinopse].
              Será inserida a URL da imagem na posição 3 para manter a ordem: [título, autor, sinopse, imagem].
    """
    generos_literarios = [
        "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
        "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
        "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
        "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
    ]
    book_genero_response = model.generate_content(
        f"Informe o gênero ou os gêneros do livro {book[0]} com base na lista {generos_literarios}. Retorne apenas o nome do gênero ou os gêneros, separados por vírgulas."
    )
    if hasattr(book_genero_response, "candidates") and book_genero_response.candidates:
        book_genero_name = book_genero_response.candidates[0].content.parts[0].text
    else:
        book_genero_name = "Gênero desconhecido"
    book.insert(3, mybooks.get_book_image(book[0]))
    book_user.insert_book(
        user_id=st.session_state.id,
        book_title=book[0].title(),
        book_author=book[1],
        book_genre=book_genero_name,
        book_assessment=None,
        book_url=book[3],
        book_read=0
    )
    st.session_state.clicked_add = ""

show_books_suggested()
