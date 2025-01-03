import streamlit

import initialize
import login
import cadastro
import main

# Inicializador
initialize.session_state()

# Página de Login
if streamlit.session_state.page == "Login":
    login.page_login()
# Página de Cadastro
elif streamlit.session_state.page == "Cadastro":
    cadastro.page_cadastro()
# Página Principal
elif streamlit.session_state.page == "Main":
    main.page()
