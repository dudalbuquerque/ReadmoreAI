import os
import sys
import streamlit as st
import requests

# Ajuste de caminho para incluir o diretório pai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from source.initialize import model, book_user
def add_book():
    book_name = st.text_input("Digite o nome do livro:")
    book_assessment = st.feedback(options= "stars", key=int)

    if st.button("Enviar"):
        if book_name:
            # Obter informações do livro usando a API
            book_author = model.generate_content(f"Qual o nome do autor {book_name} (apenas o nome do autor)")

            # Verificar se a resposta tem os atributos esperados
            if hasattr(book_author, 'candidates') and len(book_author.candidates) > 0:
                book_author_name = book_author.candidates[0].content.parts[0].text
            else:
                print("Erro: Não foi possível gerar o autor do livro.")
                book_author_name = None  # Ou algum valor padrão, se necessário
            generos_literarios = [
                "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
                "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
                "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
                "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
            ] 
            
            book_genero_prompt = model.generate_content(f"Informe o gênero ou os gêneros do livro '{book_name}' com base na lista {generos_literarios}. Retorne apenas o nome do gênero ou os gêneros, separados por vírgulas.")
            
            # Verificar se a resposta tem o atributo 'generated_text'
            if hasattr(book_genero_prompt, 'candidates') and len(book_genero_prompt.candidates) > 0:
                book_genero_name = book_genero_prompt.candidates[0].content.parts[0].text
            else:
                print("Erro: 'generated_text' não encontrado na resposta.")
                book_genero_name = None  # Ou algum valor padrão, se necessário


            # Buscar URL da imagem do livro
            book_img_url = get_book_image(book_name)
            user_id = st.session_state.id

            # Inserir no banco de dados
            book_user.insert_book(
                user_id = user_id,  # Exemplo: definir o ID do usuário como 1
                book_title=book_name.title(),
                book_author=book_author_name,
                book_genre=book_genero_name,
                book_assessment=book_assessment+1,
                book_url=book_img_url,
                book_read = 1
            )# user_id, book_title, book_author, book_genre, book_assessment, book_url)
            st.success(f"Livro '{book_name}' adicionado!")
            st.session_state.book_input = False
            st.rerun()
        else:
            st.error("Nome inválido.")

def add_book():
    book_name = st.text_input("Digite o nome do livro:")
    book_assessment = st.feedback(options= "stars", key=int)

    if st.button("Enviar"):
        if book_name:
            # Obter informações do livro usando a API
            book_author = model.generate_content(f"Qual o nome do autor {book_name} (apenas o nome do autor)")

            # Verificar se a resposta tem os atributos esperados
            if hasattr(book_author, 'candidates') and len(book_author.candidates) > 0:
                book_author_name = book_author.candidates[0].content.parts[0].text
            else:
                print("Erro: Não foi possível gerar o autor do livro.")
                book_author_name = None  # Ou algum valor padrão, se necessário
            generos_literarios = [
                "Romance", "Conto", "Fantasia", "Ficção Científica", "Terror/Horror", 
                "Policial/Detetivesco", "Aventura", "Distopia/Utopia", "Romance Histórico", 
                "Biografia", "Autobiografia", "Diário/Cartas", "Poesia", "Tragédia", 
                "Comédia", "Drama", "Fábula", "Lenda", "Crônica", "Suspense/Thriller", "Mistério"
            ] 
            
            book_genero_prompt = model.generate_content(f"Informe o gênero ou os gêneros do livro '{book_name}' com base na lista {generos_literarios}. Retorne apenas o nome do gênero ou os gêneros, separados por vírgulas.")
            
            # Verificar se a resposta tem o atributo 'generated_text'
            if hasattr(book_genero_prompt, 'candidates') and len(book_genero_prompt.candidates) > 0:
                book_genero_name = book_genero_prompt.candidates[0].content.parts[0].text
            else:
                print("Erro: 'generated_text' não encontrado na resposta.")
                book_genero_name = None  # Ou algum valor padrão, se necessário


            # Buscar URL da imagem do livro
            book_img_url = get_book_image(book_name)
            user_id = st.session_state.id

            # Inserir no banco de dados
            book_user.insert_book(
                user_id = user_id,  # Exemplo: definir o ID do usuário como 1
                book_title=book_name.title(),
                book_author=book_author_name,
                book_genre=book_genero_name,
                book_assessment=book_assessment+1,
                book_url=book_img_url,
                book_read = 1
            )# user_id, book_title, book_author, book_genre, book_assessment, book_url)
            st.success(f"Livro '{book_name}' adicionado!")
            st.session_state.book_input = False
            st.rerun()
        else:
            st.error("Nome inválido.")

def display_book_details(book_name, book_img_url, book_author, book_genre, book_assessment):
    # Estilo personalizado para centralizar o conteúdo do expander
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
    # Caixa expansível para mostrar os detalhes do livro
    with st.expander("Detalhes do Livro", expanded=True):
        col1, col2 = st.columns([10, 1])
        with col1:
            # Aplicando o estilo de centralização dentro do expander
            st.markdown('<div class="expander-content">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(book_img_url, width=200)
                               
            with c2:
                st.write(" ")
                st.write(f"**Nome:** {book_name}")
                st.write(f"**Autor:** {book_author}")
                st.write(f"**Gênero:** {book_genre}")
                st.write("**Avaliação:** ")
                book_assessment = book_user.return_assessment(st.session_state.id, book_name)
                # Exibir estrelas de acordo com a avaliação
                st.markdown("⭐" * book_assessment)
                 
            left, right = st.columns([1, 1])
            with left:
                if st.button("🗑️ Deletar", type="primary", use_container_width=True):
                    book_user.delete_book(book_name, st.session_state.id, )
                    st.session_state.clicked_book = ''  # Limpa o estado do livro
                    st.rerun()  # Atualiza a interface
            with right:
                if st.button("✏️ Editar",  use_container_width=True):
                    st.session_state.show_stars = True  # Habilita o slider
                    st.rerun()
            if st.session_state.show_stars:
                left, right = st.columns([3, 1])
                with left:
                    st.write(f"**Quantas estrelas para {book_name}?**")
                    st.session_state.book_assessment = st.feedback(options= "stars", key=int)
                with right:
                    st.write(" ")
                    st.write(" ")
                    if st.button("✅ Salvar", use_container_width=True):
                        # Atualiza o livro no banco de dados
                        book_user.update_book(
                            st.session_state.id, book_name, book_author, book_genre, st.session_state.book_assessment+1
                        )
                        st.session_state.book_assessment = 0
                        st.session_state.show_stars = False  
                        st.rerun()  # Atualiza a interface          
        with col2:
            if st.button("❌"):
                st.session_state.clicked_book = ''  # Limpa o estado do livro
                st.rerun()  
        st.markdown('</div>', unsafe_allow_html=True)


def show_books():
    st.markdown("## Meus Livros")

    if st.button("Adicionar Livro", type="primary", use_container_width=True):
        st.session_state.book_input = True
        st.rerun()
    
    if st.session_state.book_input == True:
        add_book()

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1])

    books_data = book_user.return_info(st.session_state.id, 1)
    columns = [c1, c2, c3, c4, c5]

    # Exibe os detalhes do livro, caso um livro esteja selecionado
    if st.session_state.clicked_book != '':
        book = st.session_state.clicked_book
        display_book_details(
            book_name=book[0],
            book_img_url=book[4],
            book_author=book[1],
            book_genre=book[2],
            book_assessment=book[3],
        )

    # Exibe a lista de livros, caso nenhum livro esteja selecionado
    else:
        for i, book in enumerate(books_data):
            book_name = book[0]
            book_img_url = book[4]

            column = columns[i % 5]

            with column:
                st.image(book_img_url, use_container_width=True)
                # Botão para abrir o modal do livro clicado
                if st.button(f"{book_name}", key=f"book_{i}", use_container_width=True):
                    st.session_state.clicked_book = book
                    st.rerun()  # Atualiza a interface

        
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
