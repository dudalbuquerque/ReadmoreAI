import sys
import os
import streamlit
import requests
from src import mybooks

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar corretamente o módulo "initialize" de src
from src import initialize

import google.generativeai as genai
from db import create, books

genai.configure(api_key= '-')
model = genai.GenerativeModel('gemini-pro')

# Conexão com o banco de dados
my_db = create.DataBase()
book_user = books.BOOK(my_db)

def display_books_suggested_details(book):
    # Corrigir a atribuição do book_img_url
    book_img_url = book[4]  # A URL da imagem do livro está no índice 4 de cada livro
    streamlit.markdown(
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
    with streamlit.expander("Detalhes do Livro", expanded=True):
        streamlit.markdown('<div class="expander-content">', unsafe_allow_html=True)
        c1, c2 = streamlit.columns([1, 2])
        with c1:
            streamlit.image(book_img_url, width=200)
        with c2:
            streamlit.write(f"**Nome:** {book[0]}")
            streamlit.write(f"**Autor:** {book[1]}")
            streamlit.write(f"**Sinopse:** {book[2]}")
            if streamlit.button("Fechar", type="primary", use_container_width=True):
                streamlit.session_state.clicked_book_suggested = ''  # Limpa o estado do livro
                streamlit.rerun()  # Atualiza a interface
        streamlit.markdown('</div>', unsafe_allow_html=True)


def show_books_suggested():
    streamlit.markdown("## Livros Sugeridos")
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])

    books_data = book_user.return_info(streamlit.session_state.id, 0)
    columns = [c1, c2, c3, c4, c5]

    for i, book in enumerate(books_data):
        book_name = book[0]
        book_img_url = book[4]

        column = columns[i % 5]

        with column:
            streamlit.image(book_img_url, use_container_width=True)
            # Botão para abrir o modal do livro clicado
            if streamlit.button(f"{book_name}", use_container_width=True):
                streamlit.session_state.clicked_book_sugerido = book
                streamlit.rerun()  # Atualiza a interface

def add_db_book_suggested(book):
    generos_literarios = [
        "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
        "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
        "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
        "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
    ]
    # Obtém o gênero do livro com base na lista de gêneros fornecida
    book_genero_prompt = model.generate_content(
        f"Informe o gênero ou os gêneros do livro '{book[0]}' com base na lista {generos_literarios}. "
        "Retorne apenas o nome do gênero ou os gêneros, separados por vírgulas."
    )
    
    # Verifica se a resposta contém os dados esperados
    if hasattr(book_genero_prompt, 'candidates') and len(book_genero_prompt.candidates) > 0:
        book_genero_name = book_genero_prompt.candidates[0].content.parts[0].text
    else:
        print("Erro: 'generated_text' não encontrado na resposta.")
        book_genero_name = "Gênero desconhecido"  # Valor padrão em caso de erro
    book.insert(3, mybooks.get_book_image(book[0]))
    # Insere o livro sugerido no banco de dados
    book_user.insert_book(
        user_id=initialize.streamlit.session_state.id,
        book_title=book[0].title(),
        book_author=book[1],
        book_genre=book_genero_name,
        book_assessment=None,
        book_url=book[3],  # URL da imagem do livro
        book_read=0  # Marca como não lido
    )
    
    # Atualiza o estado do botão
    initialize.streamlit.session_state.clicked_add = ''
