import streamlit
from db import users, create
from src import initialize

my_db = create.DataBase()
user = users.USER(my_db)

def update_password():
    streamlit.title("Forget PassWord")

    if initialize.streamlit.session_state.validation == '':
        username = streamlit.text_input("Nome de usuário", "Digite nome usuário")
        email = streamlit.text_input("Qual o email cadastrado?", "Digite seu email")
        check_email = streamlit.text_input("Confirme seu email", "Digite novamente seu email")
        date_of_birth = streamlit.date_input("Qual sua data de nascimento?", value=None)

        streamlit.write("")  # Outro espaço

        c1, _, c3 = streamlit.columns([1, 1, 1])
        with c1:
            if streamlit.button("Trocar a senha", use_container_width=True):
                if(email == check_email):
                    validation = user.check_id(username, email, date_of_birth)

                    if validation:
                        initialize.streamlit.session_state.validation = validation
                    else:
                        streamlit.error("Erro")
        with c3:
            if streamlit.button("Voltar", type="primary", use_container_width=True):                 
                    initialize.streamlit.session_state.page = "Login"                 
                    streamlit.rerun()

    if initialize.streamlit.session_state.validation:
        password = streamlit.text_input("Senha", type="password", placeholder="Digite sua senha")
        check_password = streamlit.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        streamlit.write("")  # Outro espaço

        c1, _, c3 = streamlit.columns([1, 1, 1])
        with c1:
            if streamlit.button("Alterar", use_container_width=True):
                if password == check_password:
                    user.update_password(initialize.streamlit.session_state.validation)
                    streamlit.session_state.page = "Forget password"
                    streamlit.rerun()
                else:
                    streamlit.error("As senhas não coincidem!")
        with c3:
            if streamlit.button("Voltar", type="primary", use_container_width=True):                 
                    initialize.streamlit.session_state.page = "Login"                 
                    streamlit.rerun()


