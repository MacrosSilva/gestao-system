import streamlit as st
from database.connection import criar_tabelas

# Cria as tabelas no banco ao iniciar
criar_tabelas()

st.title("🏪 Sistema de Gestão")
st.success("Banco de dados configurado com sucesso!")
