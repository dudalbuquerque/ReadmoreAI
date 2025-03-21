import streamlit as st
from source import mybooks, suggested
from source.initialize import session_state, model, book_user

def display_book_suggested(book):
    """
    Exibe um livro sugerido com imagem, nome, autor e sinopse.
    """
    # Estilo personalizado para centralizar os elementos
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
    
    with st.expander("Livro sugerido", expanded=True):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown('<div class="expander-content">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 2]) # Cria duas colunas

            with c1:
                book_img_url = mybooks.get_book_image(book[0])
                st.image(book_img_url, width=200) # Exibe a imagem do livro na primeira coluna
            with c2:
                st.write(f"**Nome:** {book[0]}")    # Nome do livro
                st.write(f"**Autor:** {book[1]}")   # Autor
                st.write(f"**Sinopse:** {book[2]}") # Sinopse, todas na segunda coluna

                if st.button("Adicionar a livros sugeridos", use_container_width=True, key=f"add_suggested_{book[0]}"):
                        st.session_state.clicked_add = book
                        st.session_state.clicked_book_suggest = ''

        with col2:
            if st.button("❌", key="close_suggestion"):
                st.session_state.clicked_book_suggest = ''
                st.session_state.clicked_add = ''
                st.rerun()         
        st.markdown('</div>', unsafe_allow_html=True)

def gen_book(none, author, genre, title):
    book_list = book_user.books_list(st.session_state.id, genre)
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
            Retorne o livro com o título {title}. 
            Liste no seguinte formato, sem destaques ou formatação especial: Nome do Livro - Nome do Autor - Sinopse do Livro. 
            A sinopse deve ser clara e envolvente, sem revelar spoilers importantes. 
            Não utilize caracteres especiais.
            """
        ).text.strip()
        
    suggested = suggested.split(" - ")
    st.session_state.clicked_book_suggest = suggested
    st.rerun()

def suggest_books():
    """
    Interface principal para sugerir livros com base no gênero informado pelo usuário.
    """
    st.markdown("## Buscar Livros")


    # Exibe livro sugerido se houver um salvo na sessão
    if st.session_state.clicked_book_suggest:
        display_book_suggested(st.session_state.clicked_book_suggest)
    
    # Adiciona livro à lista de sugeridos se houver um marcado para adição
    if st.session_state.clicked_add:
        suggested.add_db_book_suggested(st.session_state.clicked_add)
        st.session_state.clicked_add = ''
        st.rerun()

    
    
    option = st.selectbox(
        "Deseja pesquisa por algo específico? ",
        ("Nenhum","Autor/Autora", "Gênero", "Título"),
    )

    if option == "Nenhum":
        if st.button("Sugerir livro", use_container_width=True, type="primary"):
            gen_book(True, None, None, None)
    
    elif option == "Autor/Autora":
        name_author = st.text_input("Digite o nome do autor ou autora: ", placeholder="...")
        if st.button("Pesquisar autor/autora", use_container_width=True, type="primary"):
            if name_author:
                gen_book(None, name_author, None, None)
            else:
                st.warning("Digite o nome do autor/autora do livro.")    
    
    elif option == "Gênero":
        option_genre = st.selectbox(
        "Deseja pesquisa por algo específico? ",
            (        
            "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
            "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
            "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
            "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
            )
        )

        if st.button("Sugerir livro", use_container_width=True, type="primary"):
           gen_book(None, None, option_genre, None)

    elif option == "Título":
        title = st.text_input("Digite o título do livro: ", placeholder="...")
        if st.button("Pesquisar livro", use_container_width=True, type="primary"):
            if title:
                gen_book(None, None, None, title)
            else:
                st.warning("Digite o título do livro.")
