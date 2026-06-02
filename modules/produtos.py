import streamlit as st
from database.connection import get_session
from database.models import Produto, Estoque, Precificacao, Custo

def cadastra_produto():
    st.header("Cadastro de Produto")

    with st.form("form_produto"):
        nome = st.text_input("Nome")
        descricao = st.text_area("Descrição")
        categoria = st.selectbox("Categoria", ["Alimento", "Bebida", "Limpeza", "Outros"])
        unidade = st.selectbox("Unidade", ["un", "kg", "litro", "caixa", "pacote"])
