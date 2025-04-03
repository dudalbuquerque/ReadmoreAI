import os
import sqlite3
import pytest
from database import create

@pytest.fixture
def dummy_db_file(tmp_path):
    db_file = tmp_path / "test_db.db"

    original_expanduser = os.path.expanduser
    os.path.expanduser = lambda path: str(db_file) if path == "~/Teste0Readmore.db" else original_expanduser(path)
    yield db_file

    os.path.expanduser = original_expanduser
    if db_file.exists():
        db_file.unlink()

def test_create_tables(dummy_db_file):
    db = create.DataBase()
    
    db.create_table_users()
    db.create_table_livros()
    
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = db.cursor.fetchall()
    table_names = [table[0] for table in tables]
    
    assert "Readmore_USERS" in table_names
    assert "Readmore_books" in table_names
    
    db.close_conn()
