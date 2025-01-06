class BOOK:
    def __init__(self, db):
            self.db = db
        

    def search_book(self, book_title, user_id, book_id):
        query = "SELECT * FROM Readmore_books WHERE title = ? AND user_id = ? AND id = ?;"
        self.db.cursor.execute(query, (book_title, user_id, book_id))
        book = self.db.cursor.fetchone()
        if book:
            print(f"O livro '{book_title}' está na base de dados.")
            return True
        else:
            print("Não encontrei este livro!!")
            return False

    def insert_book(self, user_id, book_title, book_author, book_genre, book_yearpublication, book_url, book_assessment):
        book_id = self.get_idbook(book_title, user_id)
        check = self.search_book(book_title, user_id, book_id)
        if not check:
            self.db.cursor.execute(
                """
                INSERT INTO Readmore_books (title, author, genre, year_publication, url, assessment, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (book_title, book_author, book_genre, book_yearpublication, book_url, book_assessment, user_id)
            )
            self.db.conn.commit()
            print("livro inserido!")

    def get_url(self, book_title, id_user):
        query = "SELECT url FROM Readmore_books WHERE title = ? AND user_id = ?"
        self.db.cursor.execute(query, (book_title, id_user))
        book_url = self.db.cursor.fetchone()

        if book_url:
            return book_url[0]
        else:
            return


    def get_idbook(self, book_title, user_id):
        query = "SELECT id FROM Readmore_books WHERE user_id = ? AND title = ?"
        self.db.cursor.execute(query, (user_id, book_title))
        idbook = self.db.cursor.fetchone()

        if idbook:
            return idbook[0]
        else:
            #print("Livro não encontrado!")
            return None

    def update_url(self, book_id, id_user, new_url):
        query = """
                UPDATE Readmore_books SET url = ? WHERE id = ? AND user_id = ?;
                """
        self.db.cursor.execute(query, (new_url, book_id, id_user))
        self.db.cursor.fetchone()
        self.db.conn.commit()


    def delete_book(self, titulo_para_deletar, book_id, user_id):
        query = "DELETE FROM Readmore_books WHERE title = ? AND id = ? AND user_id = ?;"
        self.db.cursor.execute(query, (titulo_para_deletar, book_id, user_id))
        self.db.conn.commit()
        result = self.db.procurando_livro(titulo_para_deletar)
        if result:
            print("Livro deletado com sucesso!!")
        else:
            print("Erro ao deletar")
