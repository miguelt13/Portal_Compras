import streamlit as st
from datetime import datetime

# Configurações iniciais da página
st.set_page_config(page_title="Dashboard Fornecedor", layout="wide")

# =====================================================
# Injeção de CSS para customização do layout e cores
# =====================================================
st.markdown("""
    <style>
    /* ---------- Header (Barra Superior) ---------- */
    .header-bar {
        width: 100%;
        background-color: #3c8dbc;
        padding: 20px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-bar .logo img {
        height: 40px;
    }
    .header-bar .user-info {
        font-size: 16px;
        font-weight: bold;
        color: white;
    }
    
    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: #222d32;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    
    /* ---------- Botões ---------- */
    div.stButton > button {
        background-color: #3c8dbc;
        color: white;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #367fa9;
        color: white;
    }
    
    /* ---------- Espaçamento Vertical (Main Content) ---------- */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* ---------- Estilo para os Cards ---------- */
    .card, .dash-card {
        border: none;
        border-radius: 8px;
        padding: 20px;
        margin: 10px;
        color: white;
        font-family: 'Helvetica Neue', sans-serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
        cursor: pointer;
        text-align: center;
    }
    .card:hover, .dash-card:hover {
        transform: translateY(-5px);
    }
    /* Usando gradiente baseado nas cores definidas: #3c8dbc e #367fa9 */
    .card {
        background: linear-gradient(45deg, #3c8dbc, #367fa9);
    }
    .card h3, .dash-card h4 {
        margin: 0;
        font-size: 18px;
        font-weight: bold;
    }
    .card p, .dash-card p {
        margin: 5px 0 0 0;
        font-size: 14px;
    }
    
    /* ---------- Estilo para Seções Detalhadas ---------- */
    .section-detail {
        background-color: #fff;
        color: #333;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.06);
    }
    .section-detail h4 {
        margin-top: 0;
        color: #3c8dbc;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# Header: Barra Superior
# =====================================================
st.markdown("""
    <div class="header-bar">
        <div class="logo">
            <img src="https://via.placeholder.com/120x40?text=Logo" alt="Logotipo">
        </div>
        <div class="user-info">
            Fornecedor: Exemplo S.A.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# Menu Lateral (Sidebar)
# =====================================================
st.sidebar.title("Menu")
opcoes_menu = [
    "Dashboard Principal",
    "Pendências",
    "Sair"
]
escolha = st.sidebar.radio("Selecione a página:", opcoes_menu)

# =====================================================
# Dados de Exemplo (Simulados) para o Dashboard
# =====================================================
pendencias_principais = [
    {"titulo": "Homologação Pendente", "descricao": "Documentação incompleta", "prazo": "2025-03-01"},
    {"titulo": "Contrato a Assinar", "descricao": "Contrato #12345", "prazo": "2025-02-28"},
    {"titulo": "Atualizar Declarações", "descricao": "Declarações de Não Dívida (SS, AT)", "prazo": "2025-03-05"},
]

indicadores_conformidade = {
    "Declarações AT": {"Validade": "2025-05-10", "Status": "Válido"},
    "Declarações SS": {"Validade": "2025-04-22", "Status": "Válido"},
    "Código de Conduta": {"Aceite": True, "Data Aceitação": "2025-01-10"}
}

atalhos_fluxos = [
    "Questionário de Compliance",
    "Questionário de Sustentabilidade",
    "Homologação",
    "Ver Contratos",
    "Consultar Mercado"
]

agenda_eventos = [
    {"evento": "Prazo Assinatura Contrato #12345", "data": "2025-02-28"},
    {"evento": "Renovação Homologação", "data": "2025-03-30"},
    {"evento": "Prazo para Envio de Proposta (Consulta #987)", "data": "2025-03-05"}
]

historico_interacoes = [
    {"data": "2025-02-17 10:15", "acao": "Submissão de Documentos de Homologação"},
    {"data": "2025-02-18 14:00", "acao": "Receção de Notificação de Assinatura de Contrato"},
    {"data": "2025-02-19 09:30", "acao": "Envio de Declaração de Não Dívida atualizada"}
]

consultas_mercado = [
    {"titulo": "Consulta #987", "status": "Aberta", "prazo": "2025-03-05"},
    {"titulo": "Consulta #654", "status": "Encerrada", "prazo": "2025-02-15"}
]


# =====================================================
# Funções Auxiliares
# =====================================================
def exibir_dashboard_principal():
    """Exibe a visão geral do Dashboard com cards (1 a 6, sem 7-10)."""
    st.subheader("Bem-vindo ao Dashboard do Fornecedor!")
    st.write("Selecione um bloco para ver detalhes.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1. Pendências Principais"):
            st.session_state["secao_detalhe"] = "pendencias"
    with col2:
        if st.button("2. Indicadores de Conformidade"):
            st.session_state["secao_detalhe"] = "conformidade"
    with col3:
        if st.button("3. Atalhos para Fluxos"):
            st.session_state["secao_detalhe"] = "atalhos"
            
    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("4. Agenda / Linha do Tempo"):
            st.session_state["secao_detalhe"] = "agenda"
    with col5:
        if st.button("5. Histórico de Interações"):
            st.session_state["secao_detalhe"] = "historico"
    with col6:
        if st.button("6. Estado das Propostas"):
            st.session_state["secao_detalhe"] = "consultas"

    # Exibição da secção detalhada
    if "secao_detalhe" in st.session_state:
        st.markdown("---")
        if st.session_state["secao_detalhe"] == "pendencias":
            exibir_pendencias()
        elif st.session_state["secao_detalhe"] == "conformidade":
            exibir_conformidade()
        elif st.session_state["secao_detalhe"] == "atalhos":
            exibir_atalhos()
        elif st.session_state["secao_detalhe"] == "agenda":
            exibir_agenda()
        elif st.session_state["secao_detalhe"] == "historico":
            exibir_historico()
        elif st.session_state["secao_detalhe"] == "consultas":
            exibir_consultas()


def exibir_pendencias():
    """Secção 1. Pendências Principais"""
    st.markdown("<div class='section-detail'>", unsafe_allow_html=True)
    st.write("### Pendências Principais")
    for p in pendencias_principais:
        st.write(f"- **{p['titulo']}** — {p['descricao']} (Prazo: {p['prazo']})")
    st.markdown("</div>", unsafe_allow_html=True)


def exibir_conformidade():
    """Secção 2. Indicadores de Conformidade"""
    st.markdown("<div class='section-detail'>", unsafe_allow_html=True)
    st.write("### Indicadores de Conformidade")
    for nome, dados in indicadores_conformidade.items():
        if nome in ["Declarações AT", "Declarações SS"]:
            st.write(f"- **{nome}**: {dados['Status']} (Válido até {dados['Validade']})")
        else:
            st.write(f"- **{nome}**: {'Aceite' if dados['Aceite'] else 'Não Aceite'}")
    st.markdown("</div>", unsafe_allow_html=True)


def exibir_atalhos():
    """Secção 3. Atalhos para Fluxos"""
    st.markdown("<div class='section-detail'>", unsafe_allow_html=True)
    st.write("### Atalhos para Fluxos e Documentos")
    for link in atalhos_fluxos:
        st.write(f"- {link}")
    st.markdown("</div>", unsafe_allow_html=True)


def exibir_agenda():
    """Secção 4. Agenda / Linha do Tempo"""
    st.markdown("<div class='section-detail'>", unsafe_allow_html=True)
    st.write("### Eventos / Agenda")
    for evt in agenda_eventos:
        st.write(f"- **{evt['evento']}** em {evt['data']}")
    st.markdown("</div>", unsafe_allow_html=True)


def exibir_historico():
    """Secção 5. Histórico de Interações"""
    st.markdown("<div class='section-detail'>", unsafe_allow_html=True)
    st.write("### Histórico de Interações Recentes")
    for h in historico_interacoes:
        st.write(f"- {h['data']}: {h['acao']}")
    st.markdown("</div>", unsafe_allow_html=True)


def exibir_consultas():
    """Secção 6. Estado das Propostas (Consultas ao Mercado)"""
    st.markdown("<div class='section-detail'>", unsafe_allow_html=True)
    st.write("### Consultas ao Mercado (Propostas)")
    for c in consultas_mercado:
        st.write(f"- **{c['titulo']}** — Status: {c['status']} | Prazo: {c['prazo']}")
    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# Lógica Principal (Routing)
# =====================================================
if "secao_detalhe" not in st.session_state:
    st.session_state["secao_detalhe"] = None

if escolha == "Dashboard Principal":
    exibir_dashboard_principal()
elif escolha == "Pendências":
    st.title("Pendências")
    # Apenas um atalho para ver Pendências Principais diretamente
    exibir_pendencias()
else:
    st.warning("Selecione uma opção válida ou volte ao Dashboard Principal.")
