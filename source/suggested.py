import sys
import os
import streamlit

from source import mybooks, initialize

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source.initialize import *


def display_books_suggested_details(book):
    """"
    Exibe os detalhes do livro sugerido em um expander.

    Parâmetros:
        book: Lista com informações do livro, onde o índice 4 contém a URL da imagem.
    """
    # Obtém a URL da imagem
    book_img_url = book[4]

    # Personaliza a aparência do expander
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

    # Cria o expander para mostrar os detalhes do livro
    with streamlit.expander("Detalhes do Livro", expanded=True):
        streamlit.markdown('<div class="expander-content">', unsafe_allow_html=True)
        c1, c2 = streamlit.columns([1, 2]) # Cria duas colunas

        with c1:
            streamlit.image(book_img_url, width=200) # Exibe a imagem do livro na primeira coluna
        with c2:
            streamlit.write(f"**Nome:** {book[0]}")    # Nome do livro
            streamlit.write(f"**Autor:** {book[1]}")   # Autor
            streamlit.write(f"**Sinopse:** {book[2]}") # Sinopse, todas na segunda coluna

            left, _,  right = streamlit.columns([1, 1, 1])
            with left:
                if streamlit.button("deletar", type="primary", use_container_width=True):
                    book_user.delete_book(book[0], initialize.streamlit.session_state.id, )
                    streamlit.session_state.clicked_book_suggest = ''  # Limpa o estado do livro
                    streamlit.rerun()  # Atualiza a interface
            with right:
                if streamlit.button("Fechar", type="primary", use_container_width=True):
                    streamlit.session_state.clicked_book_suggest = ''  # Limpa o estado do livro
                    streamlit.rerun()  # Atualiza a interface

        streamlit.markdown('</div>', unsafe_allow_html=True)


def show_books_suggested():
    """
    Exibe uma lista de livros sugeridos em colunas.

    Utiliza as informações dos livros obtidas do banco de dados e cria botões para cada livro,
    permitindo ao usuário visualizar os detalhes do livro selecionado.
    """
    # Título da seção e criação de 5 colunas
    streamlit.markdown("## Livros Sugeridos")
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])

    # Recupera os dados dos livros
    books_data = book_user.return_info(streamlit.session_state.id, 0)
    columns = [c1, c2, c3, c4, c5]

    if(streamlit.session_state.clicked_book_suggest != ''):
        display_books_suggested_details(streamlit.session_state.clicked_book_suggest)

    else:
        for i, book in enumerate(books_data):
            book_name = book[0]
            book_img_url = book[4]

            column = columns[i % 5]

            with column:
                streamlit.image(book_img_url, use_container_width=True)
                # Botão para abrir o modal do livro clicado
                if streamlit.button(f"{book_name}", use_container_width=True):

                    streamlit.session_state.clicked_book_suggest = book
                    streamlit.rerun()  # Atualiza a interface

def add_db_book_suggested(book):
    """
    Adiciona um livro sugerido ao banco de dados com base nas informações fornecidas e
    utiliza a IA para determinar o gênero literário.

    Parâmetros:
        book: Lista com informações do livro.
    """
    # Lista de gêneros literários possíveis
    generos_literarios = [
        "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
        "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
        "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
        "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
    ]

    # Obtém - utilizando o modelo generativo - o gênero do livro com base na lista de gêneros fornecida
    book_genero_prompt = model.generate_content(
        f"Informe o gênero ou os gêneros do livro '{book[0]}' com base na lista {generos_literarios}. "
        "Retorne apenas o nome do gênero ou os gêneros, separados por vírgulas."
    )
    
    # Verifica se a resposta contém os dados esperados e extrai o gênero
    if hasattr(book_genero_prompt, 'candidates') and len(book_genero_prompt.candidates) > 0:
        book_genero_name = book_genero_prompt.candidates[0].content.parts[0].text
    else:
        print("Erro: 'generated_text' não encontrado na resposta.")
        book_genero_name = "Gênero desconhecido" # Valor padrão em caso de erro

    # Insere a URL da imagem do livro na posição correta da lista 'book'
    book.insert(3, mybooks.get_book_image(book[0]))

    # Insere o livro sugerido no banco de dados
    book_user.insert_book(
        user_id=initialize.streamlit.session_state.id,
        book_title=book[0].title(),
        book_author=book[1],
        book_genre=book_genero_name,
        book_assessment=None,
        book_url=book[3], # URL da imagem do livro
        book_read=0 # Marca como não lido
    )
    
    # Atualiza o estado do botão (indicando que a adição foi concluída)
    initialize.streamlit.session_state.clicked_add = ''
