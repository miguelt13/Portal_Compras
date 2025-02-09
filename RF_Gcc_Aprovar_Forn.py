import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# Configurar o layout da página
st.set_page_config(page_title="Avaliação do Fornecedor", layout="wide")

# ============================
# Injeção de CSS Personalizado
# ============================
st.markdown("""
    <style>
    /* ---------- Top Bar (Header) ---------- */
    .header-bar {
        width: 100%;
        background-color: #3c8dbc;
        padding: 20px;
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
    div.stButton > button, .action-button {
        background-color: #3c8dbc;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 14px;
        cursor: pointer;
    }
    .action-button:hover {
        background-color: #367fa9;
    }
    
    /* ---------- Tabela de Dados do Fornecedor ---------- */
    .supplier-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        font-family: Arial, sans-serif;
    }
    .supplier-table th, .supplier-table td {
        border: 1px solid #ddd;
        padding: 9px;
        text-align: center;
    }
    .supplier-table th {
        background-color: #3c8dbc;
        color: white;
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
            Utilizador: GCC - João Silva
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================
# Menu Lateral (Sidebar)
# ============================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Dashboard de Pendentes",
    "Avaliação do Fornecedor"
]
menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)
if menu_selecionado != "Avaliação do Fornecedor":
    st.sidebar.info("Esta página é para a avaliação do fornecedor.")

# ============================
# Título e Observações
# ============================
st.title("Avaliação do Fornecedor")
st.write("Por favor, insira suas observações e escolha uma ação abaixo:")

# Campo de observações
observacao = st.text_area("Observações", height=100)

# ============================
# Botões de Ação: Aprovar, Rejeitar, Devolver
# ============================
col1, col2, col3 = st.columns(3)
aprovar = col1.button("Aprovar")
rejeitar = col2.button("Rejeitar")
devolver = col3.button("Devolver")

if aprovar:
    acao = "Aprovado"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.success(f"Fornecedor {acao} com sucesso!")
    st.write(f"**Data/Hora:** {timestamp}")
    st.write(f"**Observações:** {observacao}")
elif rejeitar:
    acao = "Rejeitado"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.error(f"Fornecedor {acao}!")
    st.write(f"**Data/Hora:** {timestamp}")
    st.write(f"**Observações:** {observacao}")
elif devolver:
    acao = "Devolvido (Solicitar mais informações)"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.warning(f"Fornecedor {acao}!")
    st.write(f"**Data/Hora:** {timestamp}")
    st.write(f"**Observações:** {observacao}")

st.markdown("---")

# ============================
# Exibição dos Dados do Fornecedor (Tabela HTML)
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
      <td style="font-weight: bold;">{key}</td>
      <td>{value}</td>
    </tr>
    """
html_table += "</table></div>"

# Exibe a tabela usando components.html para renderizar o HTML
components.html(html_table, height=300)

# ============================
# Exibição dos Anexos do Fornecedor
# ============================
st.subheader("Anexos do Fornecedor")
anexos = [
    "Contrato_Comercial.pdf",
    "Certificado_de_Qualidade.jpg",
    "Licenca_de_Funcionamento.docx"
]
for anexo in anexos:
    st.markdown(f"- {anexo}")
