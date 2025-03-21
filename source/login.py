import streamlit as st
from source import principal
from datetime import datetime
from source.initialize import user

# Define intervalo de idade para cadastro
current_year = datetime.today().year
min_year = current_year - 105  # Usuários com até 105 anos
max_year = current_year - 18   # Usuários com no mínimo 18 anos

def login():
    """Renderiza a página de login."""
    st.title("Login")
    username = st.text_input("Nome de Usuário", placeholder="Digite seu nome")
    id_user = user.get_id(username)
    password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

    left, middle, right = st.columns([1, 1, 1])
    with left:
        if st.button("Esqueci a senha", type="tertiary"):
            st.session_state.page = "Esqueceu Senha"
            st.rerun()

    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0

    if st.session_state.get("incorrect_password", False):
        st.error(f"Senha incorreta. Você tem {3 - st.session_state.login_attempts} tentativa(s) restante(s).")

    col1, _, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Entrar", type="primary", use_container_width=True):
            if not username or not password:
                st.error("Por favor, preencha todos os campos.")
            elif not id_user:
                st.warning("Este usuário não existe.")
            elif st.session_state.login_attempts >= 3:
                st.error("Você excedeu o limite de tentativas. Tente novamente mais tarde.")
            elif user.check_password(id_user, password):
                st.session_state.username = username
                st.session_state.id = id_user
                st.session_state.page = "Inicio"
                st.session_state.login_attempts = 0
                st.session_state.incorrect_password = False
                st.rerun()
            else:
                st.session_state.login_attempts += 1
                st.session_state.incorrect_password = True

    with col3:
        if st.button("Cadastrar-se", use_container_width=True):
            st.session_state.page = "Cadastro"
            st.rerun()

def cadastro():
    """Renderiza a página de cadastro."""
    st.title("Cadastro")
    if "username" not in st.session_state:
        st.session_state.username = ""
    
    username = st.text_input("Nome de Usuário", placeholder="Digite seu nome", value=st.session_state.username)
    id_user = user.get_id(username) if username else None

    if id_user:
        st.warning("Ops, este não pode, escolha outro!")

    email = st.text_input("Email", placeholder="Digite seu email")
    date_of_birth = st.date_input(
        "Qual sua data de nascimento?",
        value=None,
        format="DD/MM/YYYY",
        min_value=datetime(min_year, 1, 1),
        max_value=datetime(max_year, 12, 31)
    )
    password = st.text_input("Senha", type="password", placeholder="Digite uma senha")
    confirmar_password = st.text_input("Confirmar senha", type="password", placeholder="Digite novamente a senha")

    col1, col2, col3 = st.columns([1, 1, 1])
    with st.container():
        with col1:
            if st.button("Cadastrar", use_container_width=True):
                if not (username and email and date_of_birth and password and confirmar_password):
                    st.error("Por favor, preencha todos os campos.")
                elif password != confirmar_password:
                    st.error("As senhas não coincidem. Tente novamente.")
                else:
                    user.register_user(username, date_of_birth, email, password)
                    st.success("Cadastro realizado com sucesso!")
                    st.session_state.username = username
                    st.session_state.page = "Login"
                    st.rerun()

    with st.container():
        with col3:
            if st.button("Voltar para Login", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()

def update_password():
    """Gerencia o processo de recuperação e alteração da senha do usuário."""
    st.title("Redefinir senha")
    
    if st.session_state.validation == "":
        username = st.text_input("Nome de usuário", placeholder="Digite nome usuário")
        email = st.text_input("Qual o email cadastrado?", placeholder="Digite seu email")
        check_email = st.text_input("Confirme seu email", placeholder="Digite novamente seu email")
        date_of_birth = st.date_input(
            "Qual sua data de nascimento?",
            value=None,
            format="DD/MM/YYYY",
            min_value=datetime(min_year, 1, 1),
            max_value=datetime(max_year, 12, 31)
        )
        st.write("")
        c1, _, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("Trocar a senha", use_container_width=True):
                if email == check_email:
                    validation = user.check_id(username, email, date_of_birth)
                    if validation:
                        st.session_state.validation = validation
                    else:
                        st.error("Erro: Dados de usuário inválidos!")
        with c3:
            if st.button("Voltar", type="primary", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()
                
    if st.session_state.validation:
        password = st.text_input("Senha", type="password", placeholder="Digite sua nova senha")
        check_password = st.text_input("Confirme a senha", type="password", placeholder="Digite novamente a nova senha")
        st.write("")
        c1, _, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("Alterar", use_container_width=True):
                if password == check_password:
                    user.update_password(st.session_state.validation)
                    st.session_state.page = "Esqueceu Senha"
                    st.rerun()
                else:
                    st.error("As senhas não coincidem!")
        with c3:
            if st.button("Voltar", type="primary", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()

def main():
    """Função principal para navegação após o login."""
    principal.main()

def update_pass():
    update_password()
