import streamlit as st 
from database.connection import get_session 
from database.models import Estoque, Produto, Movimentacao

def controle_estoque(): 
    st.header("Controle de Estoque") 
    session = get_session()
    produtos = session.query(Produto).all()
    produto_selecionado = st.selectbox("Selecione o produto", [p.nome for p in produtos])
    tipo = st.selectbox("Tipo de Movimentação", ["entrada", "saida"])
    quantidade = st.number_input("Quantidade")
    confirmar = st.button("Confirmar")


    if confirmar:
        produto_obj = session.query(Produto).filter(Produto.nome == produto_selecionado).first() 
        estoque = session.query(Estoque).filter(Estoque.produto_id == produto_obj.id).first()
        if tipo == "entrada":
            estoque.quantidade = estoque.quantidade + quantidade
        else:
            estoque.quantidade = estoque.quantidade - quantidade

        nova_movimentacao = Movimentacao( produto_id=produto_obj.id, tipo=tipo, quantidade=quantidade
        ) 
        session.add(nova_movimentacao)       
        session.commit()
        session.close()
        st.success(f"Movimentação de {quantidade} unidades ({tipo}) registrada com sucesso!")