import streamlit as st
import re
import random
from datetime import datetime

st.set_page_config(page_title="Definir Login e Password", layout="wide")

# -------------------------------------------------
# Injeção de CSS: header, sidebar, botões e inputs
# -------------------------------------------------
st.markdown("""
    <style>
    /* ---------- Header (Barra Superior) ---------- */
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
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header e Sidebar
# -------------------------------------------------
st.markdown("""
    <div class="header-bar">
        <div class="logo">
            <img src="https://via.placeholder.com/100x40?text=Logo" alt="Logo">
        </div>
        <div class="user-info">
            Definir Login e Password
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## Menu")
menu_opcoes = ["Definir Login e Password", "Outras Opções"]
menu_selecionado = st.sidebar.radio("Selecione a opção", menu_opcoes)

# -------------------------------------------------
# Instruções para o Utilizador
# -------------------------------------------------
st.write("### Bem-vindo! Por favor, defina seu login e password para acessar o sistema.")
st.write("""
Sua password deve conter:
- Pelo menos **8 caracteres**;
- Pelo menos **uma letra maiúscula**;
- Pelo menos **uma letra minúscula**;
- Pelo menos **um número**;
- Pelo menos **um caractere especial** (por exemplo: `@`, `#`, `$`, `%`, etc).

Exemplo: **Abc@1234**
""")

# -------------------------------------------------
# Container para os Inputs (limitação da largura)
# -------------------------------------------------
st.markdown('<div style="max-width: 400px; margin: auto;">', unsafe_allow_html=True)

username = st.text_input("Nome de Utilizador")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirmar Password", type="password")

st.markdown("</div>", unsafe_allow_html=True)

submit = st.button("Definir Login e Password")

# -------------------------------------------------
# Função para validar a password
# -------------------------------------------------
def validar_password(pw):
    padrao = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$'
    return re.match(padrao, pw)

# Usamos st.session_state para manter o estado do fluxo
if "dados_salvos" not in st.session_state:
    st.session_state.dados_salvos = False
if "email_enviado" not in st.session_state:
    st.session_state.email_enviado = False

# -------------------------------------------------
# Processamento da criação do login e password
# -------------------------------------------------
if submit:
    if not username or not email or not password or not confirm_password:
        st.error("Por favor, preencha todos os campos.")
    elif password != confirm_password:
        st.error("As passwords não coincidem. Por favor, tente novamente.")
    elif not validar_password(password):
        st.error("A password não atende aos requisitos.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("Login e Password definidos com sucesso!")
        st.write(f"**Nome de Utilizador:** {username}")
        st.write(f"**Email:** {email}")
        st.write(f"**Data/Hora:** {timestamp}")
        # Aqui, na prática, os dados seriam gravados no backend.
        st.session_state.dados_salvos = True

# -------------------------------------------------
# Botão para Enviar Código de Verificação
# -------------------------------------------------
if st.session_state.dados_salvos and not st.session_state.email_enviado:
    if st.button("Enviar Código de Verificação por Email"):
        codigo_verificacao = random.randint(100000, 999999)
        st.session_state.email_enviado = True
        st.session_state.codigo_verificacao = codigo_verificacao
        st.success(f"Código de verificação {codigo_verificacao} enviado para {email}!")
        
# -------------------------------------------------
# Campo para Inserir o Código de Verificação (aparece após o envio)
# -------------------------------------------------
if st.session_state.email_enviado:
    codigo_inserido = st.text_input("Insira o Código de Verificação recebido por Email", key="codigo_inserido")
    if st.button("Verificar Código"):
        if codigo_inserido == str(st.session_state.codigo_verificacao):
            st.success("Código verificado! Fornecedor aprovado.")
        else:
            st.error("Código incorreto. Tente novamente.")
