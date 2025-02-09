import streamlit as st
from datetime import datetime

# Configurar o layout da página
st.set_page_config(page_title="Dashboard de Pendentes", layout="wide")

# =====================================================
# Injeção de CSS: Header, Sidebar, Cards e Botões
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
    
    /* ---------- Estilo para os Cards dos Registos ---------- */
    .card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif;
    }
    .card h3 {
        margin: 0;
        color: #3c8dbc;
    }
    .card p {
        margin: 5px 0;
        font-size: 14px;
    }
    .card p strong {
        font-weight: bold;
    }
    
    /* ---------- Estilo para o Botão de Ação nos Cards ---------- */
    .button {
        display: inline-block;
        padding: 6px 12px;
        background-color: #3c8dbc;
        color: white;
        text-decoration: none;
        border-radius: 3px;
        font-size: 14px;
        margin-top: 10px;
    }
    
    /* ---------- Estilo para os Cards do Dashboard ---------- */
    .dash-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin: 10px;
        text-align: center;
        background-color: #f9f9f9;
        font-family: Arial, sans-serif;
        cursor: pointer;
    }
    .dash-card:hover {
        background-color: #e9e9e9;
    }
    .dash-card h4 {
        margin: 0;
        color: #3c8dbc;
    }
    .dash-card p {
        margin: 5px 0 0 0;
        font-size: 12px;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# Header: Barra Superior com Logotipo e Dados do Utilizador
# =====================================================
st.markdown("""
    <div class="header-bar">
        <div class="logo">
            <img src="https://via.placeholder.com/100x40?text=Logo" alt="Logotipo do Cliente">
        </div>
        <div class="user-info">
            Utilizador: João Silva
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# Menu Lateral (Sidebar)
# =====================================================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Registo", 
    "Homologação (Indisponível)", 
    "Dashboard de Pendentes", 
    "Contratos", 
    "Renovação de Contratos"
]
menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)
# Neste exemplo, estamos trabalhando com a opção "Dashboard de Pendentes"
if menu_selecionado != "Dashboard de Pendentes":
    st.sidebar.info("Esta página é o Dashboard de Pendentes.")

# =====================================================
# Dados de Exemplo para os Temas (Pendentes)
# =====================================================
# Cada chave representa um tema, e o valor é uma lista de dicionários com os dados pendentes.
pending_data = {
    "Registo Fornecedores": [
        {"Designação": "Fornecedor Alpha, Lda.", "Data Registo": "2025-02-08 10:30", "NIF": "123456789", "Localização": "Portugal"},
        {"Designação": "Fornecedor Beta, S.A.", "Data Registo": "2025-02-09 14:15", "NIF": "987654321", "Localização": "Espanha"},
        {"Designação": "Fornecedor Gamma, Lda.", "Data Registo": "2025-02-10 09:45", "NIF": "192837465", "Localização": "França"},
        {"Designação": "Fornecedor Delta, Lda.", "Data Registo": "2025-02-10 11:20", "NIF": "564738291", "Localização": "Itália"},
        {"Designação": "Fornecedor Epsilon, S.A.", "Data Registo": "2025-02-11 08:00", "NIF": "102938475", "Localização": "Alemanha"}
    ],
    "Homologação Fornecedores": [
        {"Designação": "Fornecedor Zeta, Lda.", "Data Registo": "2025-02-12 10:00", "NIF": "112233445", "Localização": "Portugal"},
        {"Designação": "Fornecedor Eta, S.A.", "Data Registo": "2025-02-13 12:30", "NIF": "556677889", "Localização": "Espanha"}
    ],
    "Consultas ao Mercado": [
        {"Designação": "Fornecedor Theta, Lda.", "Data Registo": "2025-02-14 09:00", "NIF": "998877665", "Localização": "França"},
        {"Designação": "Fornecedor Iota, S.A.", "Data Registo": "2025-02-14 11:15", "NIF": "443322110", "Localização": "Itália"},
        {"Designação": "Fornecedor Kappa, Lda.", "Data Registo": "2025-02-15 15:45", "NIF": "667788990", "Localização": "Portugal"}
    ],
    "Contratos": [
        {"Designação": "Fornecedor Lambda, Lda.", "Data Registo": "2025-02-16 08:30", "NIF": "101010101", "Localização": "Alemanha"},
        {"Designação": "Fornecedor Mu, S.A.", "Data Registo": "2025-02-17 14:00", "NIF": "202020202", "Localização": "Portugal"},
        {"Designação": "Fornecedor Nu, Lda.", "Data Registo": "2025-02-18 16:20", "NIF": "303030303", "Localização": "Espanha"},
        {"Designação": "Fornecedor Xi, S.A.", "Data Registo": "2025-02-19 09:45", "NIF": "404040404", "Localização": "França"}
    ],
    "Renovação de Contratos": [
        {"Designação": "Fornecedor Omicron, Lda.", "Data Registo": "2025-02-20 10:15", "NIF": "505050505", "Localização": "Itália"}
    ]
}

# =====================================================
# Dashboard: Exibição dos Temas (Cards) no Topo
# =====================================================
st.markdown("## Dashboard de Temas")
# Cria 5 colunas para os 5 temas
dash_cols = st.columns(5)
# Se ainda não existir um tema selecionado, define um padrão
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "Registo Fornecedores"

# Exibe cada "card" do dashboard com o nome do tema e o número de pendentes  
for idx, (theme, data_list) in enumerate(pending_data.items()):
    with dash_cols[idx]:
        # Usando st.button para tornar o card "clicável"
        # O texto do botão inclui o nome do tema e a contagem
        if st.button(f"{theme}\n#: {len(data_list)}"):
            st.session_state.selected_theme = theme

# =====================================================
# Detalhes dos Pendentes para o Tema Selecionado
# =====================================================
st.markdown(f"### Detalhes dos Pendentes para: **{st.session_state.selected_theme}**")

# Se houver registos pendentes para o tema selecionado, exibe-os em "cards"
if pending_data[st.session_state.selected_theme]:
    for supplier in pending_data[st.session_state.selected_theme]:
        card_html = f"""
        <div class="card">
            <h3>{supplier['Designação']}</h3>
            <p><strong>Data Registo:</strong> {supplier['Data Registo']}</p>
            <p><strong>NIF:</strong> {supplier['NIF']}</p>
            <p><strong>Localização:</strong> {supplier['Localização']}</p>
            <a class="button" href="./atribuicao_gcc">Atribuir GCC</a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("Não há registos pendentes para este tema.")

