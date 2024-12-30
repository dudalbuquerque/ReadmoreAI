import streamlit

import initialize
import login
import main

# Inicializador
initialize.session_state()

# Página de Login
if streamlit.session_state.page == "Login":
    login.page()
# Página Principal
elif streamlit.session_state.page == "Main":
    main.page()
