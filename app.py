import streamlit as st
from database.connection import criar_tabelas
from modules.produtos import cadastrar_produto, listar_produtos

criar_tabelas()

st.title("🏪 Sistema de Gestão")
pagina = st.sidebar.selectbox("Menu", ["Cadastro de Produtos", "Produtos Cadastrados"])
                                       
if pagina == "Cadastro de Produtos":
    cadastrar_produto()
elif pagina == "Produtos Cadastrados":
    listar_produtos()
    