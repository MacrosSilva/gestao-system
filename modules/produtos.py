import streamlit as st
from database.connection import get_session
from database.models import Produto, Estoque, Precificacao, Custo

def cadastrar_produto():
    st.header("Cadastro de Produto")

    with st.form("form_produto"):
        nome = st.text_input("Nome")
        descricao = st.text_area("Descrição")
        categoria = st.selectbox("Categoria", ["Alimento", "Bebida", "Limpeza", "Outros"])
        unidade = st.selectbox("Unidade", ["un", "kg", "litro", "caixa", "pacote"])
        salvar = st.form_submit_button("Salvar Produto")

        if not nome:
            st.error("o campo nome é obrigatorio")
        else:
            session = get_session()
            produto = Produto(
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                unidade=unidade 
            )
            session.add(produto)
            session.flush()

            session.add(Estoque(produto_id=produto.id, quantidade=0))
            session.add(Custo(produto_id=produto.id))
            session.add(Precificacao(produto_id=produto.id))
            session.commit()
            session.close()
            st.success("Produto cadastrado com sucesso")


def listar_produtos():
    st.header("Produtos Cadastrados")
    session = get_session()
    produtos = session.query(Produto).all()
    
    if not produtos:
        st.info("Nenhum produto cadastrado ainda.")
    else:
        for p in produtos:
            st.write(f"**{p.nome}** - {p.categoria} - {p.unidade}")
    session.close()