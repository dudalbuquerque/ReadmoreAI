import streamlit
from source.initialize import *

def main():
    if streamlit.session_state.id:
        streamlit.session_state.menu_expanded = True
    
    # Se o usuário não estiver logado (ou fez logout), redireciona para a página de login
    if not streamlit.session_state.id or streamlit.session_state.page == "Login":
        streamlit.session_state.menu_expanded = False
        
        # A página será "Login", mas o fluxo não tentará carregar outras páginas
        return

    if streamlit.session_state.menu_expanded:
        pages = {
            "ReadmoreAI": [
                streamlit.Page("source/mybooks.py", title="Meus Livros"),
                streamlit.Page("source/suggested.py", title="Lista de livros sugeridos"),
                streamlit.Page("source/searchbook.py", title="Buscar Livro"),
            ],
        }

        pg = streamlit.navigation(pages)
        pg.run()

        with streamlit.sidebar:
            c1, _, c3 = streamlit.columns([1, 1, 1])
            with c1:
                streamlit.write(f"{streamlit.session_state.username}")

            with c3:
                if streamlit.button("Logout", type="primary", use_container_width=True): 
                    # Resetar todas as variáveis de estado
                    streamlit.session_state.book_input = False
                    streamlit.session_state.show_stars = False
                    streamlit.session_state.book_assessment = 0
                    streamlit.session_state.id = ''
                    streamlit.session_state.username = ''
                    streamlit.session_state.validation = ''
                    streamlit.session_state.menu_expanded = False
                    streamlit.session_state.clicked_add = ''
                    streamlit.session_state.clicked_book = ''
                    streamlit.session_state.page = "Login"  # Definir a página de login explicitamente

                    # Atualiza a interface e reinicia o fluxo para login
                    streamlit.rerun()

