import os
import pytest
from database import create, users, books

@pytest.fixture
def dummy_db_file(tmp_path):
    db_file = tmp_path / "test_integration.db"
    original_expanduser = os.path.expanduser
    os.path.expanduser = lambda path: str(db_file) if path == "~/Teste0Readmore.db" else original_expanduser(path)

    yield db_file
    os.path.expanduser = original_expanduser
    
    if db_file.exists():
        db_file.unlink()

@pytest.fixture
def integration_db(dummy_db_file):
    db = create.DataBase()
    db.create_table_users()
    db.create_table_livros()
    yield db
    db.close_conn()

def test_integration_flow(integration_db):
    user_module = users.USER(integration_db)
    result = user_module.register_user("IntegrationUser", "1990-01-01", "integration@example.com", "pass1234")
    assert result is True

    user_id = user_module.get_id("IntegrationUser")
    assert user_id is not None

    book_module = books.BOOK(integration_db)
    book_module.insert_book(
        user_id=user_id,
        book_title="Integration Book",
        book_author="Author Integration",
        book_genre="Test Genre",
        book_assessment=5,
        book_url="http://example.com/integration.jpg",
        book_read="True"
    )

    books_list = book_module.get_all_books(user_id)
    assert any(b['title'] == "Integration Book" for b in books_list)
