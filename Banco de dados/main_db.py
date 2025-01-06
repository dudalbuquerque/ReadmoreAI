import create
import books
import users

def main():
    my_db = create.DataBase()
    try:
        my_db.create_table_users()
        my_db.create_table_livros()

        user1 = users.USER(my_db)
        
        user1.register_user("Eduarda", 20, "duda@gmail.com", "12345678")

        id_user1 = user1.get_id("duda@gmail.com")
        if user1.check_password(id_user1, "12345678"):
            book1 = books.BOOK(my_db)
            book1.insert_book(id_user1, "E não sobrou nenhum", "Agatha Christie", "Suspense", 1939, "https://m.media-amazon.com/images/I/71u9uqTYBcL.jpg", 5)

    finally:
        my_db.close_conn()

if __name__ == "__main__":
    main()
