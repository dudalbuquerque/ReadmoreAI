import streamlit

class USER:
    def __init__(self, db):
            self.db = db

    def register_user(self, user_name, user_date_of_birth, user_email, user_password):
            # checando user, pelo email
            self.db.cursor.execute("SELECT id FROM Readmore_users WHERE email = ?", (user_email,)) 
            if self.db.cursor.fetchone():
                streamlit.error("O email já está cadastrado!")
                return False
            
            # insere o novo usuário
            self.db.cursor.execute(
                """
                INSERT INTO Readmore_users(name, date_of_birth, email, password, registration_date)
                VALUES (?, ?, ?, ?, CURRENT_DATE);
                """, (user_name, user_date_of_birth, user_email, user_password)
            )
            self.db.conn.commit()
            print("Cadastrado com sucesso!")
            return True

    def check_password(self, user_id, user_password):
        query = "SELECT password FROM Readmore_users WHERE id = ?"
        self.db.cursor.execute(query, (user_id,))
        resultado_senha = self.db.cursor.fetchone()

        if resultado_senha and resultado_senha[0] == user_password:
            return True
        return False

    def get_id(self, username):
        query = "SELECT id FROM Readmore_users WHERE name = ?"
        self.db.cursor.execute(query, (username,))
        copia_id = self.db.cursor.fetchone()

        if copia_id:
            return copia_id[0]
        else:
            print("Usuário não encontrado!")
            return None
    """
    def esqueceu_senha(self, user_id, new_password):
        query = "UPDATE Readmore_users SET senha = ? WHERE id = ? ;"
        self.db.cursor.execute(query, (new_password, user_id))
        self.db.conexao.commit()   
    """
