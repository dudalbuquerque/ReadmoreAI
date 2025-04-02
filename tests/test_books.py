import sqlite3
import pytest
from database import books

@pytest.fixture
def dummy_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE Readmore_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100),
            genre VARCHAR(100),
            assessment INTEGER,
            url TEXT,
            read TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
    """)
    conn.commit()

    class DummyDB:
        def __init__(self, conn):
            self.conn = conn
            self.cursor = conn.cursor()

        def procurando_livro(self, titulo):
            self.cursor.execute("SELECT * FROM Readmore_books WHERE title = ?", (titulo,))
            return self.cursor.fetchone()

    db = DummyDB(conn)
    yield db
    conn.close()

@pytest.fixture
def book_module(dummy_db):
    return books.BOOK(dummy_db)

def test_insert_and_get_book(book_module):
    user_id = 1

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Teste",
        book_author="Autor Teste",
        book_genre="Ficção",
        book_assessment=4,
        book_url="http://exemplo.com/imagem.jpg",
        book_read="True"
    )

    books_list = book_module.get_all_books(user_id)
    assert any(b['title'] == "Livro Teste" for b in books_list)

def test_search_book(book_module):
    user_id = 1

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Pesquisa",
        book_author="Autor Pesquisa",
        book_genre="Drama",
        book_assessment=5,
        book_url="http://exemplo.com/imagem2.jpg",
        book_read="True"
    )

    book_id = book_module.get_idbook("Livro Pesquisa", user_id)
    found = book_module.search_book("Livro Pesquisa", user_id, book_id)
    assert found is True

    not_found = book_module.search_book("Livro Inexistente", user_id, 999)
    assert not_found is False

def test_get_idbook(book_module):
    user_id = 1
    assert book_module.get_idbook("Livro Desconhecido", user_id) is None

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Identificacao",
        book_author="Autor ID",
        book_genre="Comédia",
        book_assessment=3,
        book_url="http://exemplo.com/imagem3.jpg",
        book_read="False"
    )

    book_id = book_module.get_idbook("Livro Identificacao", user_id)
    assert book_id is not None

def test_return_condition_book(book_module):
    user_id = 1

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Lido",
        book_author="Autor Lido",
        book_genre="Romance",
        book_assessment=4,
        book_url="http://exemplo.com/imagem4.jpg",
        book_read="True"
    )

    condition = book_module.return_condition_book(user_id, "Livro Lido")
    assert condition is True

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Nao Lido",
        book_author="Autor Nao Lido",
        book_genre="Ficção Científica",
        book_assessment=3,
        book_url="http://exemplo.com/imagem5.jpg",
        book_read="False"
    )

    condition = book_module.return_condition_book(user_id, "Livro Nao Lido")
    assert condition is False

def test_books_list(book_module):
    user_id = 1

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Generico",
        book_author="Autor Generico",
        book_genre="Aventura",
        book_assessment=4,
        book_url="http://exemplo.com/imagem6.jpg",
        book_read="True"
    )

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro Especifico",
        book_author="Autor Especifico",
        book_genre="Drama",
        book_assessment=5,
        book_url="http://exemplo.com/imagem7.jpg",
        book_read="True"
    )

    list_all = book_module.books_list(user_id, "")
    assert len(list_all) >= 2

    list_drama = book_module.books_list(user_id, "Drama")
    assert any("Livro Especifico" in book for book in list_drama)

def test_delete_book(book_module, dummy_db):
    user_id = 1

    book_module.insert_book(
        user_id=user_id,
        book_title="Livro para Deletar",
        book_author="Autor Delete",
        book_genre="Mistério",
        book_assessment=3,
        book_url="http://exemplo.com/imagem8.jpg",
        book_read="True"
    )

    book_id = book_module.get_idbook("Livro para Deletar", user_id)
    book_module.delete_book("Livro para Deletar", book_id, user_id)
    result = dummy_db.procurando_livro("Livro para Deletar")
    assert result is None
