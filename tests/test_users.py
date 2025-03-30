import sqlite3
import pytest
from database import users

@pytest.fixture
def dummy_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE Readmore_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name VARCHAR(100) NOT NULL,
            date_of_birth DATE NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha VARCHAR(8) NOT NULL,
            registration_date DATE
        );
    """)
    conn.commit()

    class DummyDB:
        def __init__(self, conn):
            self.conn = conn
            self.conexao = conn
            self.cursor = conn.cursor()

    db = DummyDB(conn)
    yield db
    conn.close()

@pytest.fixture
def user_module(dummy_db):
    return users.USER(dummy_db)

def test_register_user(user_module, dummy_db):
    result = user_module.register_user("Joao", "1990-01-01", "joao@example.com", "12345678")
    assert result is True

    result_duplicate = user_module.register_user("Joao", "1990-01-01", "joao@example.com", "12345678")
    assert result_duplicate is False

def test_check_password(user_module, dummy_db):
    user_module.register_user("Maria", "1985-05-05", "maria@example.com", "pass1234")
    user_id = user_module.get_id("Maria")
    assert user_module.check_password(user_id, "pass1234") is True
    assert user_module.check_password(user_id, "wrongpass") is False

def test_get_id(user_module, dummy_db):
    assert user_module.get_id("UsuarioNaoExiste") is None

    user_module.register_user("Carlos", "1970-07-07", "carlos@example.com", "abcdef12")
    user_id = user_module.get_id("Carlos")
    assert user_id is not None

def test_check_id(user_module, dummy_db):
    user_module.register_user("Ana", "1995-03-03", "ana@example.com", "passana1")

    email = user_module.check_id("Ana", "ana@example.com", "1995-03-03")
    assert email == "ana@example.com"

    email_incorrect = user_module.check_id("Ana", "wrong@example.com", "1995-03-03")
    assert email_incorrect is None

def test_update_password(user_module, dummy_db):
    user_module.register_user("Pedro", "1980-12-12", "pedro@example.com", "oldpass")
    user_module.update_password("Pedro", "newpass")
    
    user_id = user_module.get_id("Pedro")
    dummy_db.cursor.execute("SELECT senha FROM Readmore_users WHERE id = ?", (user_id,))
    new_password = dummy_db.cursor.fetchone()[0]
    assert new_password == "newpass"
