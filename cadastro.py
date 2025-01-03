import streamlit 
import initialize

initialize.session_state()

def page_cadastro():
    # Exibir imagem (descomente a linha abaixo e ajuste o caminho caso necessário)
    # st.image("img/user.png", width=100)

    streamlit.title("Cadastro")
    # Inicializando o campo de texto com session_state
    if "username" not in streamlit.session_state:
        streamlit.session_state.username = ''
    
    # Utilizando text_input para pegar as entradas do usuário
    username = streamlit.text_input("Nome de Usuário", placeholder="Digite seu nome", value=streamlit.session_state.username)
    email = streamlit.text_input("Email", placeholder="Digite seu email")
    idade = streamlit.text_input("Idade", placeholder="Digite sua idade")
    password = streamlit.text_input("Senha", type="password", placeholder="Digite uma senha")
    confimar_password = streamlit.text_input("Confirmar senha", type="password", placeholder="Digite novamente a senha")
    

    # Colunas para alinhamento dos botões
    c1, c2, c3, c4, c5 = streamlit.columns([1, 1, 1, 1, 1])
    
    with c1:
        if streamlit.button("Cadastrar", use_container_width=True):
            # Verificar se todos os campos estão preenchidos
            if username and email and idade and password and confimar_password:
                # Verificar se as senhas coincidem
                if password == confimar_password:
                    # Salvar informações no estado da sessão
                    streamlit.session_state.username = username
                    streamlit.session_state.email = email
                    streamlit.session_state.idade = idade
                    streamlit.session_state.page = "Main"

                    # Atualizar a página
                    streamlit.rerun()
                else:
                    streamlit.error("As senhas não coincidem. Tente novamente.")
            else:
                streamlit.error("Por favor, preencha todos os campos.")

    with c5:
        if streamlit.button("Voltar para Login"):
            # Volta para a página de Login
            streamlit.session_state.page = "Login"
            streamlit.rerun()

if streamlit.session_state.page == "Cadastro":
    page_cadastro()