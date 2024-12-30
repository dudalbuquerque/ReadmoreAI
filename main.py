import streamlit
from resize import resize

# Página inicial
if "page" not in streamlit.session_state:
    streamlit.session_state.page = "Login"
# Usuário inicial
if "username" not in streamlit.session_state:
    streamlit.session_state.username = None
# Livros
if "books" not in streamlit.session_state:
    streamlit.session_state.books = []
# Preciso melhorar esses comentários...
if "messages" not in streamlit.session_state:
    streamlit.session_state.messages = []

def add_book(book: str) -> None:
    streamlit.session_state.books.append(resize(book))

# Página de Login
if streamlit.session_state.page == "Login":
    streamlit.image("img/user.png", width=100)

    streamlit.title("Login")
    username = streamlit.text_input("Nome de Usuário", placeholder="Digite seu nome")
    password = streamlit.text_input("Senha", type="password", placeholder="Digite sua senha")

    # Colunas para alinhamento bos botões
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])
    with c1:
        if streamlit.button("Entrar", type="primary", use_container_width=True):
            if username and password:
                streamlit.session_state.username = username
                streamlit.session_state.page = "Main"
                streamlit.rerun()
            else:
                streamlit.error("Por favor, preencha todos os campos.")
    with c5:
        if streamlit.button("Cadastrar-se", use_container_width=True):
            streamlit.error("Erro")

# Página Principal
elif streamlit.session_state.page == "Main":
    streamlit.title("Chat Simples")
    # Exibe o histórico de mensagens
    streamlit.markdown("### Histórico do Chat")
    for message in streamlit.session_state.messages:
        streamlit.write(message)

    # Adiciona um botão para enviar a mensagem
    with streamlit.form("chat_form", clear_on_submit=True):
        user_input = streamlit.text_input("Digite sua mensagem:", key="chat_input")
        submitted = streamlit.form_submit_button("Enviar")
        
    # Adiciona a mensagem ao histórico se o botão for clicado
    if submitted and user_input:
        streamlit.session_state.messages.append(f"Você: {user_input}")
        streamlit.session_state.messages.append(f"Bot: Eu recebi sua mensagem '{user_input}'")
        streamlit.rerun()

    streamlit.markdown("## Meus Livros")
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])
    for i, book in enumerate(streamlit.session_state.books):
        if i % 5 == 0:
            with c1:
                streamlit.image(book)
        elif i % 5 == 1:
            with c2:
                streamlit.image(book)
        elif i % 5 == 2:
            with c3:
                streamlit.image(book)
        elif i % 5 == 3:
            with c4:
                streamlit.image(book)
        elif i % 5 == 4:
            with c5:
                streamlit.image(book)
        
    if streamlit.button("Adcionar Livros", use_container_width=True):
        add_book("img/livro.jpg")
        streamlit.rerun()

    streamlit.markdown("## Livros Sugeridos")
    if streamlit.button("Sugerir Livros", use_container_width=True, type="primary"):
        pass
