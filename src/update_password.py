import streamlit
from src.initialize import *
from datetime import datetime

# -------------------------------------------------------------------
# Definir intervalo de anos para a data de nascimento
# -------------------------------------------------------------------
ano_atual = datetime.today().year
ano_minimo = ano_atual - 105  # Considera usuários com até 105 anos de idade
ano_maximo = ano_atual - 18   # Considera usuários com no mínimo 18 anos

# -------------------------------------------------------------------
# Função para atualização de senha do usuário
# -------------------------------------------------------------------
def update_password():
    """
    Gerencia o processo de recuperação e alteração da senha do usuário.
    Inicialmente, realiza a validação dos dados informados pelo usuário.
    Se os dados estiverem corretos, solicita a nova senha para alteração.
    """
    streamlit.title("Redefinir senha")
    
    # -------------------------------------------------------------------
    # Se o usuário ainda não foi validado
    # -------------------------------------------------------------------
    if streamlit.session_state.validation == '':
        # Entradas para dados de identificação
        username = streamlit.text_input("Nome de usuário", placeholder="Digite nome usuário")
        email = streamlit.text_input("Qual o email cadastrado?", placeholder="Digite seu email")
        check_email = streamlit.text_input("Confirme seu email", placeholder="Digite novamente seu email")
        
        # Entrada para data de nascimento com limites definidos
        date_of_birth = streamlit.date_input(
            "Qual sua data de nascimento?",
            value=None,
            format="DD/MM/YYYY",
            min_value=datetime(ano_minimo, 1, 1),
            max_value=datetime(ano_maximo, 12, 31)
        )
        
        streamlit.write("")  # Espaço adicional para organização visual
        
        # Criação de colunas para posicionar os botões
        c1, _, c3 = streamlit.columns([1, 1, 1])
        
        # Botão para validar os dados e prosseguir com a troca de senha
        with c1:
            if streamlit.button("Trocar a senha", use_container_width=True):
                # Verifica se os e-mails informados coincidem
                if email == check_email:
                    # Realiza a verificação dos dados do usuário
                    validation = user.check_id(username, email, date_of_birth)
                    if validation:
                        streamlit.session_state.validation = validation
                    else:
                        streamlit.error("Erro: Dados de usuário inválidos!")
        # Botão para voltar à tela de login
        with c3:
            if streamlit.button("Voltar", type="primary", use_container_width=True):
                streamlit.session_state.page = "Login"
                streamlit.rerun()
                
    # -------------------------------------------------------------------
    # Se o usuário já foi validado, solicita a nova senha
    # -------------------------------------------------------------------
    if streamlit.session_state.validation:
        # Entradas para a nova senha e sua confirmação
        password = streamlit.text_input("Senha", type="password", placeholder="Digite sua nova senha")
        check_password = streamlit.text_input("Confirme a senha", type="password", placeholder="Digite novamente sua nova senha")
        
        streamlit.write("")  # Espaço adicional para organização visual
        
        # Criação de colunas para posicionar os botões
        c1, _, c3 = streamlit.columns([1, 1, 1])
        
        # Botão para confirmar a alteração da senha
        with c1:
            if streamlit.button("Alterar", use_container_width=True):
                # Verifica se as senhas informadas coincidem
                if password == check_password:
                    # Atualiza a senha no banco de dados
                    user.update_password(streamlit.session_state.validation)
                    streamlit.session_state.page = "Forget password"  # Redireciona ou atualiza a página conforme necessário
                    streamlit.rerun()
                else:
                    streamlit.error("As senhas não coincidem!")
        
        # Botão para voltar à tela de login
        with c3:
            if streamlit.button("Voltar", type="primary", use_container_width=True):
                streamlit.session_state.page = "Login"
                streamlit.rerun()
