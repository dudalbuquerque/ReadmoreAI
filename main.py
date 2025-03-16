import streamlit as st
from source import initialize, login

def main():
    """Ponto de entrada da aplicação."""
    initialize.session_state()
    if st.session_state.page == "Login":
        login.login()
    elif st.session_state.page == "Cadastro":
        login.cadastro()
    elif st.session_state.page == "Esqueceu Senha":
        login.update_pass()
    elif st.session_state.page == "Inicio":
        login.main()

if __name__ == "__main__":
    main()
