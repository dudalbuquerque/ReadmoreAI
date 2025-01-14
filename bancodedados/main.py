import create
import books
import users

def main():
    my_db = create.DataBase()
    try:
        # Criando as tabelas
        my_db.create_table_users()
        my_db.create_table_livros()

        # Criando um usuário
        user1 = users.USER(my_db)
        user1.register_user("Eduarda", "2004-08-04", "duda@gmail.com", "12345678")


        # Obtendo o ID do usuário
        id_user1 = user1.get_id("duda@gmail.com")
        
        # Verificando a senha
        if user1.check_password(id_user1, "12345678"):
            # Inserindo um livro
            book1 = books.BOOK(my_db)
            book1.insert_book(
                id_user1, 
                "E não sobrou nenhum", 
                "Agatha Christie", 
                "Suspense", 
                1939, 
                "https://m.media-amazon.com/images/I/71u9uqTYBcL.jpg", 
                5
            )
            print("Livro inserido com sucesso!")
        else:
            print("Senha incorreta.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    
    finally:
        # Fechando a conexão com o banco de dados
        my_db.close_conn()

if __name__ == "__main__":
    main()
