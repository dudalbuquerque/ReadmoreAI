import streamlit
import requests
from src import initialize
import google.generativeai as genai
from bancodedados import create, books

# Configuração da API Gemini
API_KEY = 'SUA-CHAVE-API'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Conexão com o banco de dados
my_db = create.DataBase()
book_user = books.BOOK(my_db)

def add_book():
    if streamlit.session_state.get("book_input", False):
        book_name = streamlit.text_input("Digite o nome do livro:")
        book_assessment = streamlit.text_input("Digite sua avaliação: (0 à 5):")
        if streamlit.button("Enviar"):
            if book_name:
                # Obter informações do livro usando a API
                book_author = model.generate_content(f"Qual o nome do autor {book_name} (apenas o nome do autor)")

                # Verificar se a resposta tem os atributos esperados
                if hasattr(book_author, 'candidates') and len(book_author.candidates) > 0:
                    book_author_name = book_author.candidates[0].content.parts[0].text
                else:
                    print("Erro: Não foi possível gerar o autor do livro.")
                    book_author_name = None  # Ou algum valor padrão, se necessário
                
                book_genero = model.generate_content(f"Qual o nome do genero {book_name} (apenas o nome do genero)")

                # Verificar se a resposta tem o atributo 'generated_text'
                if hasattr(book_genero, 'candidates') and len(book_genero.candidates) > 0:
                    book_genero_name = book_genero.candidates[0].content.parts[0].text
                else:
                    print("Erro: 'generated_text' não encontrado na resposta.")
                    book_genero_name = None  # Ou algum valor padrão, se necessário


                # Buscar URL da imagem do livro
                book_img_url = get_book_image(book_name)
                user_id = initialize.streamlit.session_state.id

                # Inserir no banco de dados
                book_user.insert_book(
                    user_id = user_id,  # Exemplo: definir o ID do usuário como 1
                    book_title=book_name,
                    book_author=book_author_name,
                    book_genre=book_genero_name,
                    book_assessment=book_assessment,
                    book_url=book_img_url
                )# user_id, book_title, book_author, book_genre, book_assessment, book_url)
                streamlit.success(f"Livro '{book_name}' adicionado!")
                streamlit.session_state.book_input = False
                streamlit.rerun()
            else:
                streamlit.error("Nome inválido.")
    else:
        if streamlit.button("Adicionar Livro", use_container_width=True):
            streamlit.session_state.book_input = True
            streamlit.rerun()

def show_books():
    streamlit.markdown("## Meus Livros")
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])

    books_data = book_user.get_all_books(user_id=1)
    for i, book in enumerate(books_data):
        book_name = book["title"]
        book_img_url = book["url"]

        if i % 5 == 0:
            with c1:
                streamlit.image(book_img_url, use_container_width=True)  # Atualizado
        elif i % 5 == 1:
            with c2:
                streamlit.image(book_img_url, use_container_width=True)  # Atualizado
        elif i % 5 == 2:
            with c3:
                streamlit.image(book_img_url, use_container_width=True)  # Atualizado
        elif i % 5 == 3:
            with c4:
                streamlit.image(book_img_url, use_container_width=True)  # Atualizado
        elif i % 5 == 4:
            with c5:
                streamlit.image(book_img_url, use_container_width=True)  # Atualizado

def suggest_books():
    streamlit.markdown("## Livros Sugeridos")
    if streamlit.button("Sugerir Livros", use_container_width=True, type="primary"):
        gen_book()

    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])

    for i, (book_name, book_img_url) in enumerate(
        zip(streamlit.session_state.get("nomes_sugeridos", []), streamlit.session_state.get("sugeridos", []))
    ):
        if i % 5 == 0:
            with c1:
                streamlit.image(book_img_url, use_column_width=True)
                streamlit.write(book_name)
        elif i % 5 == 1:
            with c2:
                streamlit.image(book_img_url, use_column_width=True)
                streamlit.write(book_name)
        elif i % 5 == 2:
            with c3:
                streamlit.image(book_img_url, use_column_width=True)
                streamlit.write(book_name)
        elif i % 5 == 3:
            with c4:
                streamlit.image(book_img_url, use_column_width=True)
                streamlit.write(book_name)
        elif i % 5 == 4:
            with c5:
                streamlit.image(book_img_url, use_column_width=True)
                streamlit.write(book_name)

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

def gen_book():
    ai = model.generate_content(
        f"Gere uma sugestão de livro (apenas o nome do livro e do autor) com base nestes livros já lidos: {str(streamlit.session_state.get('titles', []))}"
    )
    book_name = ai.candidates[0].content.parts[0].text
    book_img_url = get_book_image(book_name)

    if book_name and book_img_url:
        streamlit.session_state.nomes_sugeridos.append(book_name)
        streamlit.session_state.sugeridos.append(book_img_url)
        streamlit.experimental_rerun()
