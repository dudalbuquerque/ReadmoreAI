import streamlit

from src import initialize, pages

API_KEY = 'AIzaSyDuLwMbjOhECPfvXYtK4aG8bDAYHKpYiLE'

# Inicializador de Variáveis do Usuário
initialize.session_state()
if streamlit.session_state.page == "Login":
    pages.login()
elif streamlit.session_state.page == "Cadastro":
    pages.cadastro()
elif streamlit.session_state.page == "Main":
    pages.main()
