import sqlite3
import os

class DataBase:
    def __init__(self):
        # Define o caminho do banco de dados no diretório do usuário
        db_path = os.path.expanduser("~/Teste0Readmore.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table_users(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Readmore_USERS(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                name VARCHAR(100) NOT NULL,
                date_of_birth DATE NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password VARCHAR(8) NOT NULL,
                registration_date DATE
            )
            """
        ) 
        self.conn.commit()
    
    def create_table_livros(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Readmore_books(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(100),
                genre VARCHAR(100),
                assessment INTEGER CHECK(assessment BETWEEN 0 AND 5),
                url TEXT,
                read BOOLEAN NOT NULL,  
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Readmore_users (id),
                UNIQUE(title, author, user_id)
            )
            """
        ) #(id_livro, titulo, autor_a, genero, avaliacao, url, user_id)   
        self.conn.commit()

    def close_conn(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Erro ao fechar o banco de dados: {e}")

def main():
    my_db = DataBase()  # Instancia o banco de dados
    try:
        # Criando as tabelas
        my_db.create_table_users()
        my_db.create_table_livros()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
