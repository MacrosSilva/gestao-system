import streamlit as st
from database.connection import get_session
from database.models import Custo, Produto 

def calcular_custo():
    st.header("Calculo de Custo")
    session = get_session()
    produtos = session.query(Produto).all()
    produto_selecionado = st.selectbox("Selecione o produto", [p.nome for p in produtos])
    custo_producao =st.number_input("Custo do Produto")
    custo_fixo = st.number_input("Custo Fixo")
    custo_variavel = st.number_input("Custo Variavel")
    calcular = st.button("Calcular")


    if calcular:
        custo_total = custo_producao + custo_fixo + custo_variavel
        produto_obj = session.query(Produto).filter(Produto.nome == produto_selecionado).first()
        custo = session.query(Custo).filter(Custo.produto_id == produto_obj.id).first()

        custo.custo_producao = custo_producao
        custo.custo_fixo = custo_fixo
        custo.custo_variavel = custo_variavel
        custo.custo_total = custo_total

        session.commit()
        session.close()

        st.success(f"Custo total calculado: R$ {custo_total:.2f}")
