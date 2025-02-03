import streamlit
from src import initialize, main_pages

# Inicializador de Variáveis do Usuário
initialize.session_state()
if streamlit.session_state.page == "Login":
    main_pages.login()
elif streamlit.session_state.page == "Cadastro":
    main_pages.cadastro()
elif streamlit.session_state.page == "Main":
    main_pages.main()
