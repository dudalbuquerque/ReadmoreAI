import streamlit
from db import users, create
from src import principal, update_password

# conectando com o banco de dados
my_db = create.DataBase()
user = users.USER(my_db)


def login():
    # streamlit.image("img/user.png", width=100)

    streamlit.title("Login")
    
    # Campo para o nome de usuário
    username = streamlit.text_input("Nome de Usuário", placeholder="Digite seu nome")
    id_user = user.get_id(username)

    # Campo para a senha
    password = streamlit.text_input("Senha", type="password", placeholder="Digite sua senha")

    left, midle, right= streamlit.columns([1, 1, 1])
    with left:
        if streamlit.button("Esqueci a senha", type="tertiary"):
            streamlit.session_state.page = "Forget password"
            streamlit.rerun()
    with midle:
            streamlit.write(" ")
            streamlit.write("")
    with right:
            streamlit.write(" ")
            streamlit.write("")            
    # Inicializar tentativas na sessão
    if "login_attempts" not in streamlit.session_state:
        streamlit.session_state.login_attempts = 0

    # Mensagem para senha incorreta
    if "incorrect_password" in streamlit.session_state and streamlit.session_state.incorrect_password:
        streamlit.error("Senha incorreta. Você tem "
                        f"{3 - streamlit.session_state.login_attempts} tentativa(s) restante(s).")

    # Colunas para alinhamento dos botões
    c1, _, c3 = streamlit.columns([1, 1, 1])

    with c1:
        streamlit.write("")
        if streamlit.button("Entrar", type="primary", use_container_width=True):
            c1 = streamlit.columns([1])
            # Verificar se os campos foram preenchidos
            if not username or not password:
                streamlit.error("Por favor, preencha todos os campos.")
            elif not id_user:
                streamlit.warning("Este usuário não existe.")
            elif streamlit.session_state.login_attempts >= 3:
                streamlit.error("Você excedeu o limite de tentativas. Tente novamente mais tarde.")
            elif user.check_password(id_user, password):
                # Login bem-sucedido
                streamlit.session_state.username = username
                streamlit.session_state.id = id_user
                streamlit.session_state.page = "Main"
                streamlit.session_state.login_attempts = 0  # Resetar tentativas
                streamlit.session_state.incorrect_password = False  # Resetar flag
                streamlit.rerun()
            else:
                # Incrementar o contador de tentativas e marcar senha incorreta
                streamlit.session_state.login_attempts += 1
                streamlit.session_state.incorrect_password = True

    with c3:
        streamlit.write("")
        if streamlit.button("Cadastrar-se", use_container_width=True):
            # Redirecionar para a página de cadastro
            streamlit.session_state.page = "Cadastro"
            streamlit.rerun()

def cadastro():
    # Exibir imagem (descomente a linha abaixo e ajuste o caminho caso necessário)
    # st.image("img/user.png", width=100)

    streamlit.title("Cadastro")

    # Inicializando o campo de texto com session_state
    if "username" not in streamlit.session_state:
        streamlit.session_state.username = ''
    
    # Utilizando text_input para pegar as entradas do usuário
    username = streamlit.text_input("Nome de Usuário", placeholder="Digite seu nome", value=streamlit.session_state.username)

    # Verificar se o nome de usuário já existe no banco de dados
    id_user = user.get_id(username) if username else None

    # Mostrar mensagem se o nome de usuário já existe
    if id_user:
        streamlit.warning("Ops, este não pode, escolha outro!")


    # Entradas adicionais
    email = streamlit.text_input("Email", placeholder="Digite seu email")
    date_of_birth = streamlit.text_input("Data de nascimento", placeholder="Digite sua data de nascimento (DD/MM/AAAA)")
    password = streamlit.text_input("Senha", type="password", placeholder="Digite uma senha")
    confirmar_password = streamlit.text_input("Confirmar senha", type="password", placeholder="Digite novamente a senha")

    col1, col2, col3 = streamlit.columns([1, 1, 1])  # Colunas para os botões
    # Validando os dados e cadastrando o usuário
    with streamlit.container():
        with col1:
            if streamlit.button("Cadastrar", use_container_width=True):
                # Validando preenchimento de campos
                if not (username and email and date_of_birth and password and confirmar_password):
                    streamlit.error("Por favor, preencha todos os campos.")
                elif password != confirmar_password:
                    streamlit.error("As senhas não coincidem. Tente novamente.")
                else:
                    # Cadastro do usuário
                    user.register_user(username, date_of_birth, email, password)
                    streamlit.success("Cadastro realizado com sucesso!")

                    # Salvando informações no estado da sessão
                    streamlit.session_state.username = username
                    streamlit.session_state.page = "Login"
                    streamlit.rerun()

    # Botão para voltar para a página de login
    with streamlit.container():
        with col3:
            if streamlit.button("Voltar para Login", use_container_width=True):
                streamlit.session_state.page = "Login"
                streamlit.rerun()

def main():
    principal.main()
def update_pass():
    update_password.update_password()