import streamlit as st
import pytest
import sqlite3
from database import users
from source import login

class DummySessionState(dict):
    def __init__(self):
        super().__init__()
        self.__dict__ = self

def dummy_rerun():
    pass

def dummy_text_input(label, **kwargs):
    if "Nome" in label:
        return "Maria"
    elif "Senha" in label:
        return "pass1234"
    return ""

def dummy_button(label, **kwargs):
    return label == "Entrar"

class DummyContainer:
    def button(self, label, **kwargs):
        return dummy_button(label, **kwargs)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def dummy_columns(sizes):
    return (DummyContainer(), DummyContainer(), DummyContainer())

@pytest.fixture
def dummy_session(monkeypatch):
    session_state = DummySessionState()
    monkeypatch.setattr(st, "session_state", session_state)
    monkeypatch.setattr(st, "rerun", dummy_rerun)
    monkeypatch.setattr(st, "text_input", dummy_text_input)
    monkeypatch.setattr(st, "button", dummy_button)
    monkeypatch.setattr(st, "columns", lambda sizes: dummy_columns(sizes))
    return session_state

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
            password VARCHAR(8) NOT NULL,
            registration_date DATE
        );
    """)
    conn.commit()
    
    class DummyDB:
        def __init__(self, conn):
            self.conn = conn
            self.cursor = conn.cursor()
    
    dummy_db_obj = DummyDB(conn)
    yield dummy_db_obj
    conn.close()

@pytest.fixture
def dummy_user(dummy_db):
    return users.USER(dummy_db)

def test_login_success(dummy_session, monkeypatch, dummy_db, dummy_user):
    cursor = dummy_db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Readmore_users';")
    assert cursor.fetchone() is not None, "Table Readmore_users does not exist"

    monkeypatch.setattr("source.initialize.user", dummy_user)
    
    dummy_user.register_user("Maria", "1985-05-05", "maria@example.com", "pass1234")
    login.login()
    
    assert dummy_session.get("username") == "Maria"
    assert dummy_session.get("page") == "Inicio"
