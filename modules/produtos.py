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

    if salvar:
        if not nome:
            st.error("O campo nome é obrigatório")
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
            st.success("Produto cadastrado com sucesso!")


def listar_produtos():
    st.header("Produtos Cadastrados")

    session = get_session()
    produtos = session.query(Produto).all()
    session.close()

    if not produtos:
        st.info("Nenhum produto cadastrado ainda.")
        return

    # Inicializa estados de sessão
    if "editar_id" not in st.session_state:
        st.session_state.editar_id = None
    if "confirmar_exclusao_id" not in st.session_state:
        st.session_state.confirmar_exclusao_id = None

    for p in produtos:
        with st.container(border=True):
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"**{p.nome}**")
                st.caption(f"{p.categoria} • {p.unidade}" + (f" • {p.descricao}" if p.descricao else ""))

            with col2:
                if st.button("✏️ Editar", key=f"editar_{p.id}", use_container_width=True):
                    st.session_state.editar_id = p.id
                    st.session_state.confirmar_exclusao_id = None

            with col3:
                if st.button("🗑️ Excluir", key=f"excluir_{p.id}", use_container_width=True):
                    st.session_state.confirmar_exclusao_id = p.id
                    st.session_state.editar_id = None

            # --- FORMULÁRIO DE EDIÇÃO ---
            if st.session_state.editar_id == p.id:
                st.divider()
                with st.form(f"form_editar_{p.id}"):
                    st.markdown("**Editar Produto**")
                    novo_nome = st.text_input("Nome", value=p.nome)
                    nova_descricao = st.text_area("Descrição", value=p.descricao or "")
                    nova_categoria = st.selectbox(
                        "Categoria",
                        ["Alimento", "Bebida", "Limpeza", "Outros"],
                        index=["Alimento", "Bebida", "Limpeza", "Outros"].index(p.categoria) if p.categoria in ["Alimento", "Bebida", "Limpeza", "Outros"] else 0
                    )
                    nova_unidade = st.selectbox(
                        "Unidade",
                        ["un", "kg", "litro", "caixa", "pacote"],
                        index=["un", "kg", "litro", "caixa", "pacote"].index(p.unidade) if p.unidade in ["un", "kg", "litro", "caixa", "pacote"] else 0
                    )
                    col_salvar, col_cancelar = st.columns(2)
                    salvar = col_salvar.form_submit_button("💾 Salvar", use_container_width=True)
                    cancelar = col_cancelar.form_submit_button("✖ Cancelar", use_container_width=True)

                if salvar:
                    if not novo_nome:
                        st.error("O campo nome é obrigatório")
                    else:
                        session = get_session()
                        produto_db = session.query(Produto).filter(Produto.id == p.id).first()
                        produto_db.nome = novo_nome
                        produto_db.descricao = nova_descricao
                        produto_db.categoria = nova_categoria
                        produto_db.unidade = nova_unidade
                        session.commit()
                        session.close()
                        st.session_state.editar_id = None
                        st.success("Produto atualizado com sucesso!")
                        st.rerun()

                if cancelar:
                    st.session_state.editar_id = None
                    st.rerun()

            # --- CONFIRMAÇÃO DE EXCLUSÃO ---
            if st.session_state.confirmar_exclusao_id == p.id:
                st.divider()
                st.warning(f"Tem certeza que deseja excluir **{p.nome}**? Esta ação não pode ser desfeita.")
                col_confirmar, col_cancelar = st.columns(2)

                if col_confirmar.button("✅ Confirmar exclusão", key=f"confirmar_{p.id}", use_container_width=True):
                    session = get_session()
                    produto_db = session.query(Produto).filter(Produto.id == p.id).first()
                    # Remove registros relacionados antes de excluir o produto
                    if produto_db.estoque:
                        session.delete(produto_db.estoque)
                    if produto_db.custo:
                        session.delete(produto_db.custo)
                    if produto_db.precificacao:
                        session.delete(produto_db.precificacao)
                    for mov in produto_db.movimentacoes:
                        session.delete(mov)
                    session.delete(produto_db)
                    session.commit()
                    session.close()
                    st.session_state.confirmar_exclusao_id = None
                    st.success("Produto excluído com sucesso!")
                    st.rerun()

                if col_cancelar.button("✖ Cancelar", key=f"cancelar_excl_{p.id}", use_container_width=True):
                    st.session_state.confirmar_exclusao_id = None
                    st.rerun()

