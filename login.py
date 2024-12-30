import streamlit

def page():
    # streamlit.image("img/user.png", width=100)

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
