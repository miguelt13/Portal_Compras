import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd

# ------------------------------------------------------------------
# Simulação: Registro do fornecedor (se não existir em session_state)
# ------------------------------------------------------------------
if "registro_completo" not in st.session_state:
    st.session_state["registro_completo"] = {
        "designacao": "Fornecedor Exemplo, Lda.",
        "pais_empresa": "Portugal",
        "email": "exemplo@fornecedor.com",
        "nif": "123456789",
        "codigo_conduct": "Aceito",
        "nivel1_label": ["01 - Serviços"],
        "nivel2_labels": ["0101 - Consultoria"],
        "nivel3_labels": ["010101 - Estratégia"],
        "rua": "Rua Exemplo",
        "localidade": "Lisboa",
        "codigo_postal": "1000-001",
        "distrito_estado": "Lisboa",
        "iban": "PT50000201231234567890154",
        "swift": "BPPIPTPL",
        "pais_conta": "Portugal",
        "validade_at": datetime(2025, 2, 8),
        "arquivo_at": type("File", (), {"name": "decl_at.pdf"}),
        "validade_ss": datetime(2025, 2, 8),
        "arquivo_ss": type("File", (), {"name": "decl_ss.pdf"}),
        "validade_certidao": datetime(2025, 2, 8),
        "arquivo_certidao": type("File", (), {"name": "cert_permanente.pdf"}),
        "arquivo_rcbe": type("File", (), {"name": "rcbe.pdf"}),
        "anexos_opcionais": None,
        "sustentabilidade": True,
        "data_aceite_conduta": datetime(2025, 2, 8, 10, 30),
        "data_aceite_principios": datetime(2025, 2, 8, 10, 30)
    }

# ------------------------------------------------------------------
# Configurar layout da página e título
# ------------------------------------------------------------------
st.set_page_config(page_title="Dashboard DP - Coordenador", layout="wide")

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

    /* ---------- Estilo para os Cards ---------- */
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
    .button {
        display: inline-block;
        padding: 6px 12px;
        background-color: #3c8dbc;
        color: white !important;
        text-decoration: none;
        border-radius: 3px;
        font-size: 14px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================
# Header: Barra Superior
# ============================
st.markdown("""
    <div class="header-bar">
        <div class="logo">
            <img src="https://via.placeholder.com/100x40?text=Logo" alt="Logotipo do Cliente">
        </div>
        <div class="user-info">
            DP – Coordenador: Ana Martins
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
# Título da Seção Principal
# ============================
st.markdown("## Atribuição de GCC / Encaminhamento")

# ----------------------------
# Formulário de Atribuição de GCC
# ----------------------------
gcc_lista = ["Maria Santos", "João Almeida", "Pedro Costa"]
col_gcc, col_instr, col_botoes = st.columns([2, 4, 2], gap="large")
with col_gcc:
    gcc_selecionado = st.selectbox("Escolha um GCC:", gcc_lista)
with col_instr:
    instrucao = st.text_area("Instruções para o GCC:")
with col_botoes:
    if st.button("Atribuir GCC"):
        st.session_state["gcc_atribuido"] = {
            "gcc": gcc_selecionado,
            "instrucao": instrucao,
            "data_atribuicao": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.success(f"GCC {gcc_selecionado} atribuído com sucesso!")
    if st.button("Encaminhar para Potenciais Fornecedores"):
        st.session_state["fornecedor_encaminhado"] = True
        st.success("Fornecedor encaminhado para Potenciais Fornecedores com sucesso!")

# --------------------------------------------------
# Linha separadora (temática) após atribuição de GCC
# --------------------------------------------------
st.markdown("---")

# ============================
# Exibição (editável) dos Dados do Fornecedor
# ============================
reg = st.session_state["registro_completo"]
st.markdown("## Dados do Fornecedor")

# Dados Básicos
col_basic1, col_basic2 = st.columns(2)
with col_basic1:
    reg["designacao"] = st.text_input("Designação (Nome/Razão Social):", value=reg.get("designacao", ""))
with col_basic2:
    reg["pais_empresa"] = st.text_input("País da Empresa:", value=reg.get("pais_empresa", ""))

col_contact1, col_contact2 = st.columns(2)
with col_contact1:
    reg["email"] = st.text_input("Email:", value=reg.get("email", ""))
with col_contact2:
    reg["nif"] = st.text_input("NIF:", value=reg.get("nif", ""))

# Código de Conduta + Data
st.text_input(
    "Código de Conduta:", 
    value=f"{reg.get('codigo_conduct', '')} (Aceite em: {reg.get('data_aceite_conduta', datetime.now()).strftime('%Y-%m-%d %H:%M')})"
)

# --------------------------------------------------
# Linha separadora para outro “tema”
# --------------------------------------------------
st.markdown("---")

# Tipologia de Fornecimento
st.markdown("### Tipologia de Fornecimento")
nivel1_str = ", ".join(reg.get("nivel1_label", []))
nivel2_str = ", ".join(reg.get("nivel2_labels", []))
nivel3_str = ", ".join(reg.get("nivel3_labels", []))

tipologia_demo = f"Nível 1: {nivel1_str}\nNível 2: {nivel2_str}\nNível 3: {nivel3_str}"
tipologia_input = st.text_area("Tipologia", value=tipologia_demo, height=80)

# --------------------------------------------------
st.markdown("---")

# Endereço (campos lado a lado)
st.markdown("### Endereço")
col_end1, col_end2 = st.columns(2)
with col_end1:
    reg["rua"] = st.text_input("Rua:", value=reg.get("rua", ""))
with col_end2:
    reg["localidade"] = st.text_input("Localidade:", value=reg.get("localidade", ""))

col_end3, col_end4 = st.columns(2)
with col_end3:
    reg["codigo_postal"] = st.text_input("Código Postal:", value=reg.get("codigo_postal", ""))
with col_end4:
    reg["distrito_estado"] = st.text_input("Distrito / Estado:", value=reg.get("distrito_estado", ""))

# --------------------------------------------------
st.markdown("---")

# Dados Bancários (campos lado a lado)
st.markdown("### Dados Bancários")
col_bank1, col_bank2, col_bank3 = st.columns([3, 3, 1])
with col_bank1:
    reg["iban"] = st.text_input("IBAN:", value=reg.get("iban", ""))
with col_bank2:
    reg["swift"] = st.text_input("SWIFT:", value=reg.get("swift", ""))
with col_bank3:
    reg["pais_conta"] = st.text_input("País da Conta:", value=reg.get("pais_conta", ""))

# --------------------------------------------------
st.markdown("---")

# ============================
# Anexos (Tabela HTML + Ícone)
# ============================
st.markdown("### Anexos")

# 1) Montar lista de "Declarações AT/SS"
anexos_at_ss = []
if reg.get("arquivo_at"):
    anexos_at_ss.append({
        "nome": "Declaração AT",
        "ficheiro": reg["arquivo_at"].name,
        "validade": reg["validade_at"].strftime("%Y-%m-%d")
    })
if reg.get("arquivo_ss"):
    anexos_at_ss.append({
        "nome": "Declaração SS",
        "ficheiro": reg["arquivo_ss"].name,
        "validade": reg["validade_ss"].strftime("%Y-%m-%d")
    })

# 2) Montar lista de outros anexos (Certidão, RCBE, etc.)
outros_anexos = []
if reg.get("arquivo_certidao"):
    outros_anexos.append({
        "nome": "Certidão Permanente",
        "ficheiro": reg["arquivo_certidao"].name
    })
if reg.get("arquivo_rcbe"):
    outros_anexos.append({
        "nome": "RCBE",
        "ficheiro": reg["arquivo_rcbe"].name
    })
# Caso haja anexos opcionais, você pode iterar aqui:
# if reg.get("anexos_opcionais"):
#     for item in reg["anexos_opcionais"]:
#         outros_anexos.append({...})

# Ícone de download (ilustrativo, sem funcionalidade real)
download_icon_url = "https://cdn-icons-png.flaticon.com/512/724/724933.png"

# ---- Renderizar Declarações AT/SS ----
if anexos_at_ss:
    st.markdown("**Declarações AT/SS**")
    at_ss_table = """
    <div style="overflow-x:auto;">
      <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
        <tr style="background-color: #3c8dbc; color: white;">
          <th style="text-align: center; padding: 8px;">Documento</th>
          <th style="text-align: center; padding: 8px;">Validade</th>
          <th style="text-align: center; padding: 8px;">Download</th>
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

# ---- Renderizar Outros Anexos ----
if outros_anexos:
    st.markdown("**Outros Documentos**")
    outros_table = """
    <div style="overflow-x:auto;">
      <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
        <tr style="background-color: #3c8dbc; color: white;">
          <th style="text-align: center; padding: 8px;">Documento</th>
          <th style="text-align: center; padding: 8px;">Download</th>
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
    components.html(outros_table, height=200)

# --------------------------------------------------
st.markdown("---")

# ============================
# Princípios
# ============================
st.markdown("### Princípios")
st.text_input(
    "Código de Conduta (Aceite):", 
    value=f"Aceite em: {reg.get('data_aceite_conduta', datetime.now()).strftime('%Y-%m-%d %H:%M')}"
)

st.text_input(
    "Princípios de Sustentabilidade (Aceite):", 
    value=f"Aceite em: {reg.get('data_aceite_principios', datetime.now()).strftime('%Y-%m-%d %H:%M')}"
)

# --------------------------------------------------
st.markdown("---")

# ============================
# Questionário DORA (resumido)
# ============================
if "questionario_dora_respostas" in st.session_state:
    st.markdown("### Questionário DORA")
    dora = st.session_state["questionario_dora_respostas"]
    st.text_input("Segmento de atuação:", value=dora.get("seg_atuacao", ""))
else:
    st.info("Questionário DORA: Não submetido.")

# --------------------------------------------------
st.markdown("---")

# ============================
# Botão de Conclusão Final
# ============================
nivel1_ids = []
if reg.get("nivel1_label"):
    nivel1_ids = [lbl.split(" - ")[0] for lbl in reg["nivel1_label"]]

# Exemplo de regra: se "05" está em nivel1_ids e questionário DORA submetido
if "05" in nivel1_ids and st.session_state.get("questionario_dora_submetido", False):
    if st.button("Concluir Registo Final"):
        st.success(
            "Registo submetido com sucesso!\n\n"
            "Estado do registo: Pendente.\n\n"
            "Encaminhado para a Direção de Procurement para análise."
        )
        # Aqui, poderia salvar em BD, chamar API, etc.
