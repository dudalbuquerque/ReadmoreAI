import streamlit
from source import initialize, login

# Inicializador de Variáveis do Usuário
initialize.session_state()
if streamlit.session_state.page == "Login":
    login.login()
elif streamlit.session_state.page == "Cadastro":
    login.cadastro()
elif streamlit.session_state.page == "Forget password":
    login.update_pass()
elif streamlit.session_state.page == "Main":
    login.main()
