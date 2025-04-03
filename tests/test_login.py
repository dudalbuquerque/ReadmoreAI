import streamlit as st
import pytest
import sqlite3
from source import login
from source.initialize import user

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

def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Readmore_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

@pytest.fixture
def dummy_session(monkeypatch):
    session_state = DummySessionState()

    monkeypatch.setattr(st, "session_state", session_state)
    monkeypatch.setattr(st, "rerun", dummy_rerun)
    monkeypatch.setattr(st, "text_input", dummy_text_input)
    monkeypatch.setattr(st, "button", dummy_button)
    monkeypatch.setattr(st, "columns", lambda sizes: dummy_columns(sizes))

    setup_database()  # Criar a tabela antes do teste rodar

    return session_state

def test_login_success(dummy_session, monkeypatch):
    # Criar a tabela antes de cadastrar usuário
    setup_database()

    # Registrar usuário no mesmo banco
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Readmore_users (nome, data_nascimento, email, senha) VALUES (?, ?, ?, ?)",
                   ("Maria", "1985-05-05", "maria@example.com", "pass1234"))
    conn.commit()
    conn.close()

    login.login()
    
    assert dummy_session.get("username") == "Maria"
    assert dummy_session.get("page") == "Inicio"
