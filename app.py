import streamlit as st
from database.connection import criar_tabelas
from modules.produtos import cadastrar_produto, listar_produtos
from modules.custos import calcular_custo 
from modules.estoque import controle_estoque

criar_tabelas()

st.title("🏪 Sistema de Gestão")
pagina = st.sidebar.selectbox("Menu", ["Cadastro de Produtos", "Produtos Cadastrados", "Calculo de Custo", "Controle de Estoque"])
                                       
if pagina == "Cadastro de Produtos":
    cadastrar_produto()
elif pagina == "Produtos Cadastrados":
    listar_produtos()   
elif pagina == "Calculo de Custo":
    calcular_custo()
elif pagina == "Controle de Estoque":
    controle_estoque()