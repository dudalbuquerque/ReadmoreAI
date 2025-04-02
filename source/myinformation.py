import os
import sys
import streamlit as st
from source.initialize import session_state, book_user

def myinformation():
    amount = book_user.book_count(st.session_state.id)
    st.markdown(f"#### Olá {st.session_state.username}")
    st.write(" ")
    st.markdown(f"_Sua estante de livros atualmente possui **{amount[0]+amount[1]}** livros._")
    st.markdown(f"_Quantidade de livros lidos: **{amount[0]}**_")
    st.markdown(f"_Quantidade de livros sugeridos/não lidos: **{amount[1]}**_")
    st.write(" ")
    st.write(" ")


    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.page = "Login"
        st.rerun()
