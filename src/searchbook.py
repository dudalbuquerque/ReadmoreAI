import streamlit
import google.generativeai as genai
from src import mybooks, initialize, suggested
from db import create, books

# Configuração da API do Google Generative AI
genai.configure(api_key='-')
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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

def gen_book(none, author, genre, title):
    book_list = book_user.books_list(streamlit.session_state.id, genre)
    if none:
        if not book_list:
            suggested = model.generate_content(
                """
                Sugira apenas um livro interessante para leitura. 
                Liste da seguinte forma, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
                A sinopse deve ser envolvente e descrever a história sem revelar spoilers importantes. 
                Não inclua caracteres especiais.
                """
            ).text.strip()
        else:
            suggested = model.generate_content(
                f"""
                Sugira apenas um livro que não esteja na lista de nomes e notas: {book_list}. 
                Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
                A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
                Não utilize caracteres especiais.
                """
            ).text.strip()
    elif author:
        if not book_list:
            suggested = model.generate_content(
                f"""
                Sugira apenas um livro escrito por {author}. 
                Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
                A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
                Não utilize caracteres especiais.
                """
            ).text.strip()
        else:
            suggested = model.generate_content(
                f"""
                Sugira apenas um livro escrito por {author} que não esteja na lista de nomes e notas: {book_list}. 
                Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
                A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
                Não utilize caracteres especiais.
                """
            ).text.strip()
    elif genre:
        if not book_list:
            suggested = model.generate_content(
                f"""
                Sugira apenas m livro do gênero {genre}. 
                Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
                A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
                Não utilize caracteres especiais.
                """
            ).text.strip()
        else:
            suggested = model.generate_content(
                f"""
                Sugira apenas um livro do gênero {genre} que não esteja na lista de nomes e notas: {book_list}. 
                Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
                A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
                Não utilize caracteres especiais.
                """
            ).text.strip()        
    elif title:
        suggested = model.generate_content(
            f"""
            Sugira apenas um livro que não esteja na lista de nomes e notas: {book_list} e que tenha um título semelhante ou igual a {title}. 
            Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
            A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
            Não utilize caracteres especiais.
            """
        ).text.strip()
        
    suggested = suggested.split(" - ")
    print(suggested)
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

    
    
    option = streamlit.selectbox(
        "Deseja pesquisa por algo específico? ",
        ("Nenhum","Autor/Autora", "Gênero", "Tílulo"),
    )

    if option == "Nenhum":
        if streamlit.button("Sugerir livro", use_container_width=True, type="primary"):
            gen_book(True, None, None, None)
    
    elif option == "Autor/Autora":
        name_author = streamlit.text_input("Digite o nome do autor ou autora: ", placeholder="...")
        if streamlit.button("Pesquisar autor/autora", use_container_width=True, type="primary"):
            if name_author:
                gen_book(None, name_author, None, None)
            else:
                streamlit.warning("Digite o nome do autor/autora do livro.")    
    
    elif option == "Gênero":
        option_genre = streamlit.selectbox(
        "Deseja pesquisa por algo específico? ",
            (        
            "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
            "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
            "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
            "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
            )
        )

        if streamlit.button("Sugerir livro", use_container_width=True, type="primary"):
           gen_book(None, None, option_genre, None)

    elif option == "Tílulo":
        title = streamlit.text_input("Digite o título do livro: ", placeholder="...")
        if streamlit.button("Pesquisar livro", use_container_width=True, type="primary"):
            if title:
                gen_book(None, None, None, title)
            else:
                streamlit.warning("Digite o título do livro.")
