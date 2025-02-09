import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# Configurar o layout da página
st.set_page_config(layout="wide", page_title="Atribuição de GCC")

# ============================
# Injeção de CSS Personalizado
# ============================
st.markdown("""
    <style>
    /* ---------- Top Bar (Header) ---------- */
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
    </style>
    """, unsafe_allow_html=True)

# ============================
# Header: Barra Superior com Logotipo e Dados do Utilizador
# ============================
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

# ============================
# Menu Lateral (Sidebar)
# ============================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Registo", 
    "Homologação (Indisponível)", 
    "Atribuição GCC", 
    "Alteração Dados (Indisponível)", 
    "Consultas ao Mercado (Indisponível)", 
    "Contratos (Indisponível)"
]
menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)
if menu_selecionado != "Atribuição GCC":
    st.sidebar.warning("Por favor, selecione 'Atribuição GCC' para designar um GCC.")
    menu_selecionado = "Atribuição GCC"

# ============================
# Título e Descrição da Página
# ============================
st.title("Atribuição de GCC")
st.write("DP–Coordenador: Atribuir um Gestor de Contratos (GCC) ao fornecedor.")

# ============================
# Exibição dos Dados do Fornecedor (Exemplo)
# ============================
st.subheader("Dados do Fornecedor")

supplier_data = {
    "Designação": "Exemplo Fornecedor, Lda.",
    "Email": "exemplo@fornecedor.com",
    "NIF": "987654321",
    "Tipologia": "Tecnologia",
    "País": "Portugal",
    "IBAN": "PT50000201231234567890154",
    "SWIFT": "BPIXXXXX",
    "Código de Conduta": "Aceite",
    "Data de Registo": "2025-02-08 14:30"
}

# Criar uma tabela HTML estilizada para os dados (sem índice)
html_table = """
<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
    <tr style="background-color: #3c8dbc; color: white;">
      <th style="text-align: center; padding: 9px;">Campo</th>
      <th style="text-align: center; padding: 9px;">Valor</th>
    </tr>
"""
for key, value in supplier_data.items():
    html_table += f"""
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">{key}</td>
      <td style="border: 1px solid #ddd; padding: 8px;">{value}</td>
    </tr>
    """
html_table += "</table></div>"

# Exibe a tabela usando components.html (o HTML já foi definido)
components.html(html_table, height=300)

# ============================
# Exibição dos Anexos do Fornecedor
# ============================
st.subheader("Anexos do Fornecedor")
# Exemplo de anexos (nomes inventados)
anexos = [
    "Contrato_Comercial.pdf",
    "Certificado_de_Qualidade.jpg",
    "Licenca_de_Funcionamento.docx"
]
for anexo in anexos:
    st.markdown(f"- {anexo}")

# ============================
# Formulário para Atribuição de GCC
# ============================
st.subheader("Atribuir GCC ao Fornecedor")
with st.form(key="form_atribuicao"):
    gcc_list = [
        "Ana Silva", 
        "Bruno Costa", 
        "Carla Sousa", 
        "Diogo Ferreira", 
        "Eva Martins", 
        "Fábio Gomes"
    ]
    gcc_selecionado = st.selectbox("Selecione o GCC:", gcc_list)
    submit_atribuicao = st.form_submit_button("Atribuir GCC")
    
    if submit_atribuicao:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dp_coordenador = "João Silva"  # Valor fixo para este exemplo (normalmente obtido via login)
        
        # Em ambiente real, aqui gravaríamos os dados para auditoria
        st.success("GCC atribuído com sucesso!")
        st.write("**Detalhes da Atribuição:**")
        st.write(f"**Data/Hora:** {data_hora}")
        st.write(f"**DP–Coordenador:** {dp_coordenador}")
        st.write(f"**GCC Atribuído:** {gcc_selecionado}")
