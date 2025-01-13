import streamlit

def chat():
    streamlit.title("Chat Simples")
    streamlit.markdown("### Histórico do Chat")
    for message in streamlit.session_state.messages:
        streamlit.write(message)
    
    with streamlit.form("chat_form", clear_on_submit=True):
        user_input = streamlit.text_input("Digite sua mensagem:", key="chat_input")
        submitted = streamlit.form_submit_button("Enviar")
    
    if submitted and user_input:
        streamlit.session_state.messages.append(f"Você: {user_input}")
        streamlit.session_state.messages.append(f"Bot: Eu recebi sua mensagem '{user_input}'")
        streamlit.rerun()
