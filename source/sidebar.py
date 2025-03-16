import streamlit as st

def menu_expanded():
    """Exibe o menu lateral com informações do usuário e opção de logout."""
    with st.sidebar:
        st.title("Menu")
        st.write(st.session_state.username)
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()
