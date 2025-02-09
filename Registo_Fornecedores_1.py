import streamlit as st
import re

# Configurar o layout para ocupar a largura total da tela
st.set_page_config(layout="wide")

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
# Top Bar (Header) com logotipo e info do utilizador
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
# Funções de Validação
# ============================
def validar_email(email: str) -> bool:
    """
    Valida a sintaxe do email utilizando uma expressão regular.
    """
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None

def validar_nif(nif: str) -> bool:
    """
    Valida o NIF português:
      - Deve ter 9 dígitos.
      - Calcula o dígito de controlo de acordo com a regra:
        soma = dígito1*9 + dígito2*8 + ... + dígito8*2
        resto = soma % 11
        se resto < 2 => dígito de controlo = 0, senão = 11 - resto.
    """
    if len(nif) != 9 or not nif.isdigit():
        return False
    soma = sum(int(nif[i]) * (9 - i) for i in range(8))
    resto = soma % 11
    digito_esperado = 0 if resto < 2 else 11 - resto
    return int(nif[-1]) == digito_esperado

# ============================
# Lista simulada de NIFs já registados (exemplo)
# ============================
nifs_registados = ["123456789"]

# ============================
# Menu Lateral
# ============================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Registo", 
    "Homologação (Indisponível)", 
    "Alteração Dados (Indisponível)", 
    "Consultas ao Mercado (Indisponível)", 
    "Contratos (Indisponível)"
]

menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)

if menu_selecionado != "Registo":
    st.sidebar.warning("Esta opção não está disponível nesta fase. Por favor, selecione 'Registo'.")
    menu_selecionado = "Registo"  # Forçamos a seleção para "Registo"

# ============================
# Página Principal: Registo de Fornecedores
# ============================
st.title("Portal de Fornecedores - Registo")
st.write("Preencha os dados abaixo para efetuar o registo no Portal de Compras do BPI.")

with st.form(key="form_registo"):
    
    st.header("Dados do Fornecedor")
    
    # Campo Designação (Nome/Razão Social) - ocupa toda a largura
    designacao = st.text_input("Designação (Nome/Razão Social):")
    
    # Linha com duas colunas para Email e NIF
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email:")
    with col2:
        nif = st.text_input("NIF:")
    
    # Tipologia de Fornecimento
    tipologia_opcoes = [
        "Consultoria", 
        "Tecnologia", 
        "Manutenção", 
        "Fornecimento de Materiais", 
        "Outros"
    ]
    tipologia = st.multiselect("Tipologia de Fornecimento:", options=tipologia_opcoes)
    
    # Localização
    pais = st.selectbox("Localização (País):", options=["Portugal", "Espanha", "França", "Alemanha", "Itália", "Outros"])
    
    # Dados Bancários
    st.subheader("Dados Bancários")
    col3, col4 = st.columns(2)
    with col3:
        iban = st.text_input("IBAN:")
    with col4:
        swift = st.text_input("SWIFT:")
    
    # Código de Conduta
    st.subheader("Código de Conduta")
    st.write("Por favor, leia o Código de Conduta do BPI abaixo:")
    
    codigo_conduta_texto = """
    <h4>Código de Conduta do BPI</h4>
    <p>
    Este código estabelece os princípios e as normas de conduta que todos os parceiros comerciais devem cumprir no âmbito das suas relações com o BPI.
    </p>
    <p>
    1. Respeito pelos colaboradores e clientes.
    </p>
    <p>
    2. Integridade nas relações comerciais.
    </p>
    <p>
    3. Compromisso com a transparência e a ética.
    </p>
    <p>
    4. Cumprimento das legislações em vigor e das normas internas do BPI.
    </p>
    <p>
    5. Responsabilidade social e ambiental.
    </p>
    <p>
    [Este texto é um exemplo. Em ambiente de produção, o Código de Conduta deverá conter o conteúdo completo e detalhado.]
    </p>
    """
    
    st.markdown(
        f"""
        <div style="height: 250px; overflow-y: auto; border: 1px solid #ccc; padding: 10px;">
            {codigo_conduta_texto}
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    opcao_codigo = st.radio(
        "Selecione como pretende proceder em relação ao Código de Conduta:",
        options=[
            "Aceitar o Código de Conduta do BPI", 
            "Fazer upload do meu próprio Código de Conduta"
        ]
    )
    
    arquivo_codigo = None
    if opcao_codigo == "Fazer upload do meu próprio Código de Conduta":
        arquivo_codigo = st.file_uploader("Envie o seu Código de Conduta (PDF, DOC, DOCX):", type=["pdf", "doc", "docx"])
    
    # Anexos Opcionais
    st.subheader("Anexos (opcional)")
    anexos = st.file_uploader(
        "Anexe documentos adicionais (PDF, imagens, DOC):", 
        type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
        accept_multiple_files=True
    )
    
    # Botão de submissão
    submit = st.form_submit_button("Submeter Registo")
    
    # Processamento do formulário
    if submit:
        erros = False
        
        # Validação do Email
        if not email:
            st.error("O campo Email é obrigatório.")
            erros = True
        elif not validar_email(email):
            st.error("O Email introduzido não tem um formato válido.")
            erros = True
        
        # Validação do NIF
        if not nif:
            st.error("O campo NIF é obrigatório.")
            erros = True
        elif not nif.isdigit():
            st.error("O NIF deve conter apenas dígitos.")
            erros = True
        elif len(nif) != 9:
            st.error("O NIF deve ter 9 dígitos.")
            erros = True
        elif not validar_nif(nif):
            st.error("O NIF introduzido não é válido.")
            erros = True
        elif nif in nifs_registados:
            st.error("Este NIF já se encontra registado no Portal.")
            erros = True
        
        # Validação do Código de Conduta
        if opcao_codigo == "Aceitar o Código de Conduta do BPI":
            codigo_aceite = True
        else:
            if arquivo_codigo is None:
                st.error("É necessário fazer o upload do seu Código de Conduta para avaliação.")
                erros = True
            else:
                codigo_aceite = False  # Neste caso, o código será avaliado pela DP
        
        if not erros:
            st.success(
                "Registo submetido com sucesso!\n\n"
                "Estado do registo: **Pendente**.\n\n"
                "O registo foi encaminhado para a Direção de Procurement para análise."
            )
            # Aqui deverá ser implementada a lógica para guardar os dados (ex.: base de dados, envio de email, etc.)
