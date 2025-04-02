class BOOK:
    def __init__(self, db):
            self.db = db
        
    def get_all_books(self, user_id):
        query = "SELECT title, url FROM Readmore_books WHERE user_id = ?"
        self.db.cursor.execute(query, (user_id,))
        books = self.db.cursor.fetchall()
        return [{"title": book[0], "url": book[1]} for book in books]

    def search_book(self, book_title, user_id, book_id):
        query = "SELECT * FROM Readmore_books WHERE title = ? AND user_id = ? AND id = ?;"
        self.db.cursor.execute(query, (book_title, user_id, book_id))
        book = self.db.cursor.fetchone()
        if book:
            #print(f"O livro '{book_title}' está na base de dados.")
            return True
        else:
            #print("Não encontrei este livro!!")
            return False
        

    def insert_book(self, user_id, book_title, book_author, book_genre, book_assessment, book_url, book_read):
        book_id = self.get_idbook(book_title, user_id)
        check = self.search_book(book_title, user_id, book_id)
        if not check:
            self.db.cursor.execute(
                """
                INSERT INTO Readmore_books (title, author, genre, assessment, url, read, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (book_title, book_author, book_genre, book_assessment, book_url, book_read, user_id)
            )
            self.db.conn.commit()
            #print("livro inserido!")
        else:
            return 0
        
    def return_assessment(self, user_id, book_title):
        book_id = self.get_idbook(book_title, user_id)
        query = "SELECT assessment FROM Readmore_books WHERE user_id = ? AND id = ?"
        self.db.cursor.execute(query, (user_id, book_id))
        assessment = self.db.cursor.fetchone()
        return assessment[0]
    
    def return_condition_book(self, user_id, book_title):
        query = "SELECT read FROM Readmore_books WHERE user_id = ? AND title = ?"
        self.db.cursor.execute(query, (user_id, book_title))
        condition_book = self.db.cursor.fetchone()

        if condition_book and condition_book[0] == "True":
            return True
        else:
            return False



    def get_idbook(self, book_title, user_id):
        query = "SELECT id FROM Readmore_books WHERE user_id = ? AND title = ?"
        self.db.cursor.execute(query, (user_id, book_title))
        idbook = self.db.cursor.fetchone()

        if idbook:
            return idbook[0]
        else:
            #print("Livro não encontrado!")
            return None

    def delete_book(self, title_for_delete, user_id):
        book_id = self.get_idbook(title_for_delete, user_id)
        query = "DELETE FROM Readmore_books WHERE title = ? AND id = ? AND user_id = ?;"
        self.db.cursor.execute(query, (title_for_delete, book_id, user_id))
        self.db.conn.commit()
        return


    def return_info(self, user_id, book_read):
        query = "SELECT title, author, genre, assessment, url, read read FROM Readmore_books WHERE user_id = ? AND read = ?;"
        self.db.cursor.execute(query, (user_id, book_read))
        books = self.db.cursor.fetchall()
        return books

    def books_list(self, user_id, book_genre):
        if(book_genre == ''):
            query = "SELECT title, assessment FROM Readmore_books WHERE user_id = ?;"
            self.db.cursor.execute(query, (user_id, ))
        else:
            query = "SELECT title, assessment FROM Readmore_books WHERE user_id = ? AND genre = ?;"
            self.db.cursor.execute(query, (user_id, book_genre))
        books = self.db.cursor.fetchall()
        return books
    
    def book_count(self, user_id):
        query = "SELECT COUNT(*) FROM Readmore_books WHERE user_id = ? AND READ = ?;"
        self.db.cursor.execute(query, (user_id, True))
        amount_read = self.db.cursor.fetchone()[0]
        self.db.cursor.execute(query, (user_id, False))
        amount_not_read = self.db.cursor.fetchone()[0] 
        return amount_read, amount_not_read
    
    def update_book(self, user_id, book_name, book_author, book_genre, book_assessment):
        query = """
            UPDATE Readmore_books 
            SET assessment = ? 
            WHERE user_id = ? AND title = ? AND author = ? AND genre = ?
        """
        self.db.cursor.execute(query, (book_assessment, user_id, book_name, book_author, book_genre))
        self.db.conn.commit()
    
    def add_book(self, user_id, book_name, book_author, book_genre, book_assessment):
        query = """
            UPDATE Readmore_books 
            SET read = ?, assessment = ?
            WHERE user_id = ? AND title = ? AND author = ? AND genre = ?
        """
        self.db.cursor.execute(query, (True, book_assessment, user_id, book_name, book_author, book_genre))
        self.db.conn.commit()

    
    

