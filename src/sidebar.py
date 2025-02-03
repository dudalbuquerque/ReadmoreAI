import streamlit
from src import initialize

# Tela Principal com Sidebar
def menu_expanded():
    with streamlit.sidebar:
        streamlit.title("Menu")

        c1, _, c3= streamlit.columns([1, 1, 1])
        with c1:
            streamlit.write(f"{initialize.streamlit.session_state.username}")
        
        with c3:
            if streamlit.button("Logout", type="primary", use_container_width=True):                 
                initialize.streamlit.session_state.page = "Login"                 
                streamlit.rerun()
