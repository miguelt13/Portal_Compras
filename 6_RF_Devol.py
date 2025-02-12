import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# Configurar o layout da página
st.set_page_config(
    page_title="Avaliação do Fornecedor - Devolução",
    layout="wide"
)

# =====================================================
# Injeção de CSS Personalizado
# =====================================================
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

/* ---------- Tabela de Dados do Fornecedor (caso queira usar em outra parte) ---------- */
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

# =====================================================
# Header: Barra Superior com Logotipo e Dados do Utilizador
# =====================================================
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

# =====================================================
# Menu Lateral (Sidebar)
# =====================================================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Dashboard de Pendentes",
    "Avaliação do Fornecedor - Devolução"
]
menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)
if menu_selecionado != "Avaliação do Fornecedor - Devolução":
    st.sidebar.info("Esta página é para a devolução do fornecedor para alteração de dados/anexos.")

# =====================================================
# Título e Descrição da Página
# =====================================================
st.title("Avaliação do Fornecedor - Devolução")
st.write("Esta página permite ao GCC devolver o fornecedor para que ele altere os dados ou os anexos. Confira o histórico de interações, insira suas observações e escolha uma ação:")

# =====================================================
# Histórico de Interações
# =====================================================
st.subheader("Histórico de Interações")

historico = [
    {"Data/Hora": "2025-02-07 12:00", "Ação": "Devolvido", "Observações": "Falta anexar o certificado de qualidade.", "Utilizador": "GCC - João Silva"},
    {"Data/Hora": "2025-02-07 15:30", "Ação": "Respondido", "Observações": "Fornecedor enviou o certificado.", "Utilizador": "Fornecedor - Maria Costa"},
    {"Data/Hora": "2025-02-08 09:00", "Ação": "Devolvido", "Observações": "Dados incompletos na ficha.", "Utilizador": "GCC - João Silva"}
]

html_hist = """
<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
    <tr style="background-color: #3c8dbc; color: white;">
      <th style="padding: 8px; text-align: center;">Data/Hora</th>
      <th style="padding: 8px; text-align: center;">Ação</th>
      <th style="padding: 8px; text-align: center;">Observações</th>
      <th style="padding: 8px; text-align: center;">Utilizador</th>
    </tr>
"""
for entry in historico:
    html_hist += f"""
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">{entry['Data/Hora']}</td>
      <td style="border: 1px solid #ddd; padding: 8px;">{entry['Ação']}</td>
      <td style="border: 1px solid #ddd; padding: 8px;">{entry['Observações']}</td>
      <td style="border: 1px solid #ddd; padding: 8px;">{entry['Utilizador']}</td>
    </tr>
    """
html_hist += "</table></div>"

components.html(html_hist, height=200)

st.markdown("---")

# =====================================================
# Observações e Ações
# =====================================================
st.write("Insira suas observações e escolha uma ação:")
observacao = st.text_area("Observações", height=100)

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
    acao = "Devolvido (Solicitar alterações)"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.warning(f"Fornecedor {acao}!")
    st.write(f"**Data/Hora:** {timestamp}")
    st.write(f"**Observações:** {observacao}")

st.markdown("---")

# =====================================================
# Dados do Fornecedor (Campos em Colunas)
# =====================================================
st.subheader("Dados do Fornecedor")

# Exemplo de dados
supplier_data = {
    "Designação (Nome/Razão Social)": "Exemplo Fornecedor, Lda.",
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

# Se deseja que sejam somente leitura, defina disabled=True
# Ex.: st.text_input("Designação:", "Exemplo Fornecedor...", disabled=True)

campos = list(supplier_data.items())

for i in range(0, len(campos), 2):
    c1, c2 = st.columns(2)
    campo1, valor1 = campos[i]
    with c1:
        st.text_input(campo1 + ":", value=valor1, disabled=True)
    
    if i + 1 < len(campos):
        campo2, valor2 = campos[i+1]
        with c2:
            st.text_input(campo2 + ":", value=valor2, disabled=True)

st.markdown("---")

# =====================================================
# Exibição dos Anexos do Fornecedor
# =====================================================
st.subheader("Anexos do Fornecedor")

# Exemplo de anexos AT/SS
anexos_at_ss = [
    {"nome": "Declaração AT", "ficheiro": "Declaracao_AT_2025.pdf", "validade": "2025-12-31"},
    {"nome": "Declaração SS", "ficheiro": "Declaracao_SS_2024.pdf", "validade": "2024-09-30"}
]

# Exemplo de outros anexos
outros_anexos = [
    {"nome": "Certidão Permanente", "ficheiro": "CertidaoPermanente.pdf"},
    {"nome": "RCBE", "ficheiro": "RCBE.pdf"},
    {"nome": "Contrato_Comercial", "ficheiro": "Contrato_Comercial.pdf"},
    {"nome": "Certificado_de_Qualidade", "ficheiro": "Certificado_de_Qualidade.jpg"},
    {"nome": "Licenca_de_Funcionamento", "ficheiro": "Licenca_de_Funcionamento.docx"}
]

# Ícone de Download
download_icon_url = "https://cdn-icons-png.flaticon.com/512/724/724933.png"

# 1) Declarações AT/SS
st.markdown("**Declarações AT/SS**")
at_ss_table = """
<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
    <tr style="background-color: #3c8dbc; color: white;">
      <th style="text-align: center; padding: 9px;">Documento</th>
      <th style="text-align: center; padding: 9px;">Data Validade</th>
      <th style="text-align: center; padding: 9px;">Download</th>
    </tr>
"""
for doc in anexos_at_ss:
    nome = doc["nome"]
    validade = doc["validade"]
    ficheiro = doc["ficheiro"]
    link_download = f"""
    <a href="#" download="{ficheiro}">
        <img src="{download_icon_url}" width="20" title="Download {ficheiro}"/>
    </a>
    """
    at_ss_table += f"""
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">{nome}</td>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{validade}</td>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{link_download}</td>
    </tr>
    """
at_ss_table += "</table></div>"
components.html(at_ss_table, height=200)

# 2) Outros Anexos
st.markdown("**Certidão Permanente, RCBE e Outros Documentos**")
outros_table = """
<div style="overflow-x:auto;">
  <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
    <tr style="background-color: #3c8dbc; color: white;">
      <th style="text-align: center; padding: 9px;">Documento</th>
      <th style="text-align: center; padding: 9px;">Download</th>
    </tr>
"""
for doc in outros_anexos:
    nome = doc["nome"]
    ficheiro = doc["ficheiro"]
    link_download = f"""
    <a href="#" download="{ficheiro}">
        <img src="{download_icon_url}" width="20" title="Download {ficheiro}"/>
    </a>
    """
    outros_table += f"""
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">{nome}</td>
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">{link_download}</td>
    </tr>
    """
outros_table += "</table></div>"
components.html(outros_table, height=220)
