import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# ==============================================
# Configurações Iniciais
# ==============================================
st.set_page_config(
    page_title="Aprovar Fornecedor (Retorno)",
    layout="wide"
)

# ==============================================
# CSS Personalizado
# ==============================================
st.markdown(r"""
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

/* ---------- Tabela de Dados do Fornecedor (mais espaçada) ---------- */
.nice-table {
    width: 100%;
    border-collapse: separate; /* permite espaçar as células */
    border-spacing: 0 5px;     /* espaçamento vertical entre as “linhas” */
    font-family: Arial, sans-serif;
    margin-top: 1rem;
}

.nice-table tr {
    background-color: #ffffff;
}

.nice-table td {
    padding: 12px;
    border: 1px solid #ddd;
    vertical-align: middle;
}

.field-label {
    background-color: #f7f7f7; /* col. da célula que contém o nome do campo */
    font-weight: bold;
    width: 200px;
    color: #333;
    font-size: 16px;
}

.field-value {
    font-size: 16px;
    color: #444;
}

/* ---------- Tabelas dos Anexos (zebra striping) ---------- */
.striped-table {
    width: 100%;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
    margin-top: 1rem;
}

.striped-table th {
    background-color: #3c8dbc;
    color: white;
    padding: 8px;
    text-align: left;
    font-size: 15px;
}

.striped-table td {
    border: 1px solid #ddd;
    padding: 8px;
    font-size: 14px;
    text-align: left;
}

.striped-table tr:nth-child(even) {
    background-color: #f2f2f2;
}

.striped-table tr:hover {
    background-color: #d9e5f1;
}
</style>
""", unsafe_allow_html=True)

# ==============================================
# Top Bar
# ==============================================
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

# ==============================================
# Menu Lateral
# ==============================================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Pendentes Devolvidos",
    "Aprovar Fornecedor (Retorno)"
]
menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)
if menu_selecionado != "Aprovar Fornecedor (Retorno)":
    st.sidebar.info("Página para aprovar fornecedor após retorno do pedido de mais informações.")

# ==============================================
# Título e Observações
# ==============================================
st.title("Aprovar Fornecedor (Depois de Devolvido)")
st.write("Avalie novamente o fornecedor que já retornou as informações solicitadas:")

observacao = st.text_area("Observações (opcional)", height=100)

col1, col2 = st.columns(2)
aprovar = col1.button("Aprovar")
rejeitar = col2.button("Rejeitar")

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

st.markdown("---")

# ==============================================
# Dados do Fornecedor
# ==============================================
st.subheader("Dados do Fornecedor")

supplier_data = {
    "Designação": "Exemplo Fornecedor, Lda.",
    "Email": "exemplo@fornecedor.com",
    "NIF": "987654321",
    "Tipologia": "Tecnologia",
    "Morada": "Rua do Exemplo, 123, 4000-000 Porto",
    "País": "Portugal",
    "IBAN": "PT50000201231234567890154",
    "SWIFT": "BPIXXXXX",
    "Código de Conduta": "Aceite",
    "Data de Registo": "2025-02-08 14:30"
}

html_table = """
<table class="nice-table">
"""
for key, value in supplier_data.items():
    html_table += f"""
    <tr>
      <td class="field-label">{key}</td>
      <td class="field-value">{value}</td>
    </tr>
    """
html_table += "</table>"

# Exibir a tabela usando components.html
components.html(html_table, height=420, scrolling=False)

st.markdown("---")

# ==============================================
# Anexos do Fornecedor
# ==============================================
st.subheader("Anexos do Fornecedor")

# Exemplos: Declarações AT/SS
anexos_at_ss = [
    {
        "nome": "Declaração AT",
        "ficheiro": "Declaracao_AT_2025.pdf",
        "validade": "2025-12-31"
    },
    {
        "nome": "Declaração SS",
        "ficheiro": "Declaracao_SS_2024.pdf",
        "validade": "2024-09-30"
    }
]

# Exemplos: Outros Anexos (Certidão, RCBE, etc.)
outros_anexos = [
    {
        "nome": "Certidão Permanente",
        "ficheiro": "CertidaoPermanente.pdf"
    },
    {
        "nome": "RCBE",
        "ficheiro": "RCBE.pdf"
    },
    {
        "nome": "Contrato_Comercial",
        "ficheiro": "Contrato_Comercial.pdf"
    },
    {
        "nome": "Certificado_de_Qualidade",
        "ficheiro": "Certificado_de_Qualidade.jpg"
    }
]

# Ícone de Download (exemplo)
download_icon_url = "https://cdn-icons-png.flaticon.com/512/724/724933.png"

# ----------------------------
# Declarações AT/SS
# ----------------------------
st.markdown("**Declarações AT/SS**")
at_ss_html = """
<table class="striped-table">
  <thead>
    <tr>
      <th style="width: 40%;">Documento</th>
      <th style="width: 30%;">Data Validade</th>
      <th style="width: 30%;">Download</th>
    </tr>
  </thead>
  <tbody>
"""
for doc in anexos_at_ss:
    nome = doc["nome"]
    validade = doc["validade"]
    ficheiro = doc["ficheiro"]
    link_download = f"""<a href="#" download="{ficheiro}">
                          <img src="{download_icon_url}" width="20" title="Download {ficheiro}"/>
                       </a>"""
    at_ss_html += f"""
    <tr>
      <td>{nome}</td>
      <td style="text-align:center;">{validade}</td>
      <td style="text-align:center;">{link_download}</td>
    </tr>
    """
at_ss_html += """
  </tbody>
</table>
"""
components.html(at_ss_html, height=200, scrolling=True)

# ----------------------------
# Outros Anexos
# ----------------------------
st.markdown("**Certidão Permanente, RCBE e Outros Documentos**")
outros_html = """
<table class="striped-table">
  <thead>
    <tr>
      <th style="width: 70%;">Documento</th>
      <th style="width: 30%;">Download</th>
    </tr>
  </thead>
  <tbody>
"""
for doc in outros_anexos:
    nome = doc["nome"]
    ficheiro = doc["ficheiro"]
    link_download = f"""<a href="#" download="{ficheiro}">
                          <img src="{download_icon_url}" width="20" title="Download {ficheiro}"/>
                       </a>"""
    outros_html += f"""
    <tr>
      <td>{nome}</td>
      <td style="text-align:center;">{link_download}</td>
    </tr>
    """
outros_html += """
  </tbody>
</table>
"""
components.html(outros_html, height=220, scrolling=True)
