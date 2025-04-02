import os
import sys
import streamlit as st
from source.mybooks import get_book_image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from source.initialize import model, book_user
from source import mybooks

def display_books_suggested_details(book):
    """"
    Exibe os detalhes do livro sugerido em um expander.

    Parâmetros:
        book: Lista com informações do livro, onde o índice 4 contém a URL da imagem.
    """
    # Obtém a URL da imagem
    book_img_url = get_book_image(book[0])
    # Personaliza a aparência do expander
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

    # Cria o expander para mostrar os detalhes do livro
    with st.expander("Detalhes do Livro", expanded=True):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown('<div class="expander-content">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 2]) # Cria duas colunas

            with c1:
                st.image(book_img_url, width=200) # Exibe a imagem do livro na primeira coluna
            with c2:
                st.write(f"**Nome:** {book[0]}")    # Nome do livro
                st.write(f"**Autor:** {book[1]}")   # Autor
                st.write(f"**Gênero:** {book[2]}") # Sinopse, todas na segunda coluna

            left, right = st.columns([1, 1])
            with left:
                if st.button("🗑️ Deletar", type="primary", use_container_width=True):
                    book_user.delete_book(book[0],st.session_state.id, )
                    st.session_state.clicked_book_suggest = ''  # Limpa o estado do livro
                    st.rerun()  # Atualiza a interface
            with right:
                if st.button("Adicionar a Meus Livros", use_container_width=True):
                        st.session_state.show_stars = True  # Habilita o slider
                        st.rerun()
            if st.session_state.show_stars:
                left, right = st.columns([3, 1])
                with left:
                    st.write(f"**Quantas estrelas para {book[0]}?**")
                    st.session_state.book_assessment = st.feedback(options= "stars", key=int)
                with right:
                    st.write(" ")
                    st.write(" ")
                    if st.button("✅ Salvar", use_container_width=True):
                        # Atualiza o livro no banco de dados
                        book_user.add_book(
                            st.session_state.id, book[0], book[1], book[2], st.session_state.book_assessment+1
                        )
                        st.session_state.clicked_book_suggest = ''  # Limpa o estado do livro
                        st.session_state.show_stars = False  # Esconde o slider
                        st.rerun()  # Atualiza a interface
        with col2:
            if st.button("❌"):
                st.session_state.clicked_book_suggest = ''  # Limpa o estado do livro
                st.rerun()          
        st.markdown('</div>', unsafe_allow_html=True)


def show_books_suggested():
    """
    Exibe uma lista de livros sugeridos em colunas.

    Utiliza as informações dos livros obtidas do banco de dados e cria botões para cada livro,
    permitindo ao usuário visualizar os detalhes do livro selecionado.
    """
    # Título da seção e criação de 5 colunas
    st.markdown("## Livros Sugeridos")
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])

    # Recupera os dados dos livros
    books_data = book_user.return_info(st.session_state.id, 0)
    columns = [c1, c2, c3, c4, c5]

    if(st.session_state.clicked_book_suggest != ''):
        display_books_suggested_details(st.session_state.clicked_book_suggest)

    else:
        for i, book in enumerate(books_data):
            book_name = book[0]
            book_img_url = book[4]

            column = columns[i % 5]

            with column:
                st.image(book_img_url, use_container_width=True)
                # Botão para abrir o modal do livro clicado
                if st.button(f"{book_name}", use_container_width=True):
                    st.session_state.clicked_book_suggest = book
                    st.rerun()  # Atualiza a interface

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
        f"Informe o gênero ou os gêneros do livro (no máximo 3) '{book[0]}' com base na lista {generos_literarios}. "
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
        user_id=st.session_state.id,
        book_title=book[0].title(),
        book_author=book[1],
        book_genre=book_genero_name,
        book_assessment=None,
        book_url=book[3], # URL da imagem do livro
        book_read=0 # Marca como não lido
    )
    
    # Atualiza o estado do botão (indicando que a adição foi concluída)
    st.session_state.clicked_add = ''
