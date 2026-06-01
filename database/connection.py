from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria o banco de dados SQLite na raiz do projeto
engine = create_engine("sqlite:///gestao.db", echo=False)

# Base para os models
Base = declarative_base()

# Sessão para interagir com o banco
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def criar_tabelas():
    Base.metadata.create_all(engine)

    