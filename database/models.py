from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    categoria = Column(String(50))
    unidade = Column(String(20))  # ex: kg, un, litro
    criado_em = Column(DateTime, default=datetime.now)

    estoque = relationship("Estoque", back_populates="produto", uselist=False)
    custo = relationship("Custo", back_populates="produto", uselist=False)
    precificacao = relationship("Precificacao", back_populates="produto", uselist=False)
    movimentacoes = relationship("Movimentacao", back_populates="produto")


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Float, default=0)
    atualizado_em = Column(DateTime, default=datetime.now)

    produto = relationship("Produto", back_populates="estoque")


class Custo(Base):
    __tablename__ = "custos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    custo_producao = Column(Float, default=0)
    custo_fixo = Column(Float, default=0)
    custo_variavel = Column(Float, default=0)
    custo_total = Column(Float, default=0)

    produto = relationship("Produto", back_populates="custo")


class Precificacao(Base):
    __tablename__ = "precificacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    margem_lucro = Column(Float, default=0)
    preco_final = Column(Float, default=0)

    produto = relationship("Produto", back_populates="precificacao")


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    tipo = Column(Enum("entrada", "saida", name="tipo_movimentacao"), nullable=False)
    quantidade = Column(Float, nullable=False)
    observacao = Column(String(255))
    data = Column(DateTime, default=datetime.now)

    produto = relationship("Produto", back_populates="movimentacoes")
                
