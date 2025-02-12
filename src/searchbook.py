import streamlit
import google.generativeai as genai
from src import mybooks, initialize, suggested
from db import create, books

# Configuração da API do Google Generative AI
genai.configure(api_key='-')
model = genai.GenerativeModel('gemini-pro')

# Conexão com o banco de dados
my_db = create.DataBase()
book_user = books.BOOK(my_db)

def display_book_suggested(book):
    """
    Exibe um livro sugerido com imagem, nome, autor e sinopse.
    """
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
    
    # Exibe o livro sugerido em um Expander
    with streamlit.expander("Livro sugerido", expanded=True):
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
            col1, col2 = streamlit.columns(2)
            
            with col1:
                if streamlit.button("Adicionar a livros sugeridos", use_container_width=True, key=f"add_suggested_{book[0]}"):
                    initialize.streamlit.session_state.clicked_add = book
            
            with col2:
                if streamlit.button("Voltar", use_container_width=True):
                    initialize.streamlit.session_state.clicked_add = ''
                    streamlit.rerun()

def gen_book(genre):
    """
    Gera uma sugestão de livro com base no gênero fornecido e na lista de livros do usuário.
    """
    generos_literarios = [
        "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
        "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
        "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
        "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
    ]
    
    suggested = None
    
    if genre:
        # Valida o gênero fornecido
        genre = model.generate_content(
            f"Retorne o gênero da lista de {generos_literarios}, que é mais parecido com {genre}. Retorne apenas o gênero"
        ).text.strip()
        
        book_list = book_user.books_list(streamlit.session_state.id, genre)

        if book_list:
            suggested = model.generate_content(
                f"Gere uma sugestão de livro com base na lista de nomes e notas: {book_list}, não repita o que tem na lista. "
                f"Liste da seguinte forma: Nome do Livro - Nome do Autor - Sinopse do Livro. "
                f"Não inclua caracteres especiais."
            ).text.strip()

    if not genre or (not book_list and not suggested):
        book_list = book_user.books_list(streamlit.session_state.id, "")
        if not book_list:
            suggested = model.generate_content(
                f"Gere uma sugestão de livro com base no gênero {genre} e na lista de nomes e notas: {book_list}, não repita o que tem na lista. "
                f"Liste da seguinte forma: Nome do Livro - Nome do Autor - Sinopse do Livro. "
                f"Não inclua caracteres especiais."
            ).text.strip()
        else:
            suggested = model.generate_content(
                f"Gere uma sugestão de livro com base na lista de nomes e notas: {book_list}, não repita o que tem na lista. "
                f"Liste da seguinte forma: Nome do Livro - Nome do Autor - Sinopse do Livro. "
                f"Não inclua caracteres especiais."
            ).text.strip()
        
    suggested = suggested.split(" - ")
    initialize.streamlit.session_state.clicked_book_suggest = suggested
    streamlit.rerun()

def suggest_books():
    """
    Interface principal para sugerir livros com base no gênero informado pelo usuário.
    """
    streamlit.markdown("## Buscar Livros")

    # Exibe livro sugerido se houver um salvo na sessão
    if initialize.streamlit.session_state.clicked_book_suggest:
        display_book_suggested(initialize.streamlit.session_state.clicked_book_suggest)
    
    # Adiciona livro à lista de sugeridos se houver um marcado para adição
    if initialize.streamlit.session_state.clicked_add:
        suggested.add_db_book_suggested(initialize.streamlit.session_state.clicked_add)
        initialize.streamlit.session_state.clicked_add = ''
        streamlit.rerun()

    # Entrada de texto para o gênero literário
    genre = streamlit.text_input("Algum gênero literário específico? (Se não, clique em sugerir)", placeholder="...")

    # Botão para sugerir um livro
    if streamlit.button("Sugerir livro", use_container_width=True, type="primary"):
        gen_book(genre)
