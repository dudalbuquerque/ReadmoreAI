import sqlite3
import os

class DataBase:
    def __init__(self):
        # Gera o caminho absoluto para o banco de dados no diretório atual
        db_path = os.path.join(os.getcwd(), "TesteReadmore.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table_users(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Readmore_USERS(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            name VARCHAR(100) NOT NULL,
            date_of_birth DATE,
            email TEXT NOT NULL UNIQUE,
            password Varchar(8) NOT NULL,
            registration_date DATE
            )
            """
        ) #(id, nome, idade, email, senha, data_de_cadastro)
        self.conn.commit()
    
    def create_table_livros(self):
        self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Readmore_books(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title VARCHAR(100) NOT NULL,
        author VARCHAR(100) NOT NULL,
        genre VARCHAR(100) NOT NULL,
        year_publication INT,
        url TEXT NOT NULL,
        assessment INTEGER CHECK(assessment BETWEEN 0 AND 5),
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Readmore_users (id),
        UNIQUE(title, author, user_id)
        )
        """
        ) #(id_livro, titulo, autor_a, genero, ano_publicacao, caminho_imagem, avaliacao, user_id)   
        self.conn.commit()
        # Adicionar a parte se leu ou se não leu
        ##no gerero eu quero colocar opções mas acho que pode ser na parte com o ptyhon e o front-end.

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
