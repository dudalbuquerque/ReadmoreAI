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

genai.configure(api_key='-')
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
        print(book)
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

def display_book_suggested(book):
    # Estilo personalizado para centralizar os elementos
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
    
    # Exibindo o livro sugerido em um Expander
    with streamlit.expander("Livro sugerido", expanded=True):
        # Layout com duas colunas
        c1, c2 = streamlit.columns([1, 2])
        
        with c1:
            # Mostra a imagem do livro
            book_img_url = mybooks.get_book_image(book[0])  
            streamlit.image(book_img_url, width=200)

        with c2:
            # Exibe informações do livro
            streamlit.write(f"**Nome:** {book[0]}")
            streamlit.write(f"**Autor:** {book[1]}")
            streamlit.write(f"**Sinopse:** {book[2]}")

            # Botões para adicionar ou voltar
            col1, col2 = streamlit.columns([1, 1])
            
            with col1:
                if streamlit.button("Adicionar a livros sugeridos", use_container_width=True, key=f"add_suggested_{book[0]}"): initialize.streamlit.session_state.clicked_add = book
            
            with col2:
                if streamlit.button("Voltar", use_container_width=True): streamlit.session_state.clicked_add = '' and streamlit.rerun()

def gen_book(genre):
    generos_literarios = [
        "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
        "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
        "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
        "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
    ]
    suggested = None

    if genre:
        genre = model.generate_content(
            f"Retorne o gênero da lista de {generos_literarios}, que é mais parecido com {genre}. Retorne apenas o gênero"
        ).text.strip()
        genre = str(genre).strip()
        book_list = book_user.books_list(streamlit.session_state.id, genre)

        if book_list != []:
            suggested = model.generate_content(
                f"Gere uma sugestão de livro (apenas o nome, autor e sinopse) com base na lista de nomes e notas: {book_list}, não repita o que tem na lista. "
                f"Liste da seguinte forma: Nome do Livro - Nome do Autor - Sinopse do Livro. "
                f"Não inclua nenhum caractere especial como asteriscos, números ou listas."
            ).text.strip()

    if not genre or book_list == [] and not suggested:
        book_list = book_user.books_list(streamlit.session_state.id, "")
        if book_list == []:
            suggested = model.generate_content(
                f"Gere uma sugestão de livro (apenas o nome, autor e sinopse) com base no gênero {genre} e na lista de nomes e notas: {book_list}, não repita o que tem na lista."
                f"Liste da seguinte forma: Nome do Livro - Nome do Autor - Sinopse do Livro. "
                f"Não inclua nenhum caractere especial como asteriscos, números ou listas."
            ).text.strip()
        else:
            suggested = model.generate_content(
                f"Gere uma sugestão de livro (apenas o nome, autor e sinopse) com base na lista de nomes e notas: {book_list}, não repita o que tem na lista. "
                f"Liste da seguinte forma: Nome do Livro - Nome do Autor - Sinopse do Livro. "
                f"Não inclua nenhum caractere especial como asteriscos, números ou listas."
            ).text.strip()
        
    suggested = suggested.split(" - ")
    initialize.streamlit.session_state.clicked_book_suggest = suggested
    streamlit.rerun()

def suggest_books():
    streamlit.markdown("## Buscar Livros")

    if initialize.streamlit.session_state.clicked_book_suggest != '' :
        book = initialize.streamlit.session_state.clicked_book_suggest
        display_book_suggested(book)


    
    if initialize.streamlit.session_state.clicked_add != '':
        book = initialize.streamlit.session_state.clicked_add
        add_db_book_suggested(book)
        initialize.streamlit.session_state.clicked_add = ''
        streamlit.rerun()

    genre = streamlit.text_input("Algum gênero literário específico? (Se não, clique em sugerir)", placeholder="...")


    if streamlit.button("Sugerir livro", use_container_width=True, type="primary"):
        gen_book(genre)
        
    if initialize.streamlit.session_state.clicked_add != '':
        book = initialize.streamlit.session_state.clicked_add
        add_db_book_suggested(book)
