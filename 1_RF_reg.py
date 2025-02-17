import streamlit as st
import re
from datetime import datetime
import pandas as pd

# Lê o Excel com as 6 colunas:
# ID NÍVEL 1 | NOME NÍVEL 1 | ID NÍVEL 2 | NOME NÍVEL 2 | ID NÍVEL 3 | NOME NÍVEL 3
df_tipologia = pd.read_excel(r"C:\Clientes_2025\BPI\Tipologia_Fornecimento.xlsx")

# Caso necessário, ajuste nomes das colunas (se não baterem exatamente):
# df_tipologia.columns = [
#     "ID NÍVEL 1", "NOME NÍVEL 1",
#     "ID NÍVEL 2", "NOME NÍVEL 2",
#     "ID NÍVEL 3", "NOME NÍVEL 3"
# ]

# 1) Garante que as colunas de ID sejam string e sem espaços extras
for col in ["ID NÍVEL 1", "ID NÍVEL 2", "ID NÍVEL 3"]:
    df_tipologia[col] = df_tipologia[col].astype(str).str.strip()

# 2) Se desejar manter sempre 2 dígitos no Nível 1, 4 dígitos no Nível 2 e 6 no Nível 3:
df_tipologia["ID NÍVEL 1"] = df_tipologia["ID NÍVEL 1"].str.zfill(2)
df_tipologia["ID NÍVEL 2"] = df_tipologia["ID NÍVEL 2"].str.zfill(4)
df_tipologia["ID NÍVEL 3"] = df_tipologia["ID NÍVEL 3"].str.zfill(6)

st.set_page_config(page_title="Portal de Fornecedores - Registo", layout="wide")

# ============================
# Injeção de CSS Personalizado
# ============================
st.markdown(
    """
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
    /* ---------- Espaçamento Vertical ---------- */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================
# Top Bar (Header)
# ============================
st.markdown(
    """
    <div class="header-bar">
        <div class="logo">
            <img src="https://via.placeholder.com/100x40?text=Logo" alt="Logotipo do Cliente">
        </div>
        <div class="user-info">
            Utilizador: Sem Utilizador Definido
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================
# Funções de Validação
# ============================
def validar_email(email: str) -> bool:
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None

def validar_nif(nif: str) -> bool:
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
    menu_selecionado = "Registo"  # Força a seleção para "Registo"

st.title("Portal de Fornecedores - Registo")
st.write("Preencha os dados abaixo para efetuar o registo no Portal de Compras do BPI.")

# =====================================================
# ETAPA 1: Dados Básicos e Código de Conduta
# =====================================================
if "registro_minimo" not in st.session_state:
    with st.form(key="form_minimo"):
        st.header("Dados Básicos do Fornecedor")
        # Exibe a Designação e País da Empresa lado a lado (proporção 3:1)
        col_basic, col_pais = st.columns([3, 1])
        with col_basic:
            designacao = st.text_input("Designação (Nome/Razão Social):")
        with col_pais:
            pais_empresa = st.selectbox("País", 
                                        options=["Portugal", "Espanha", "França", "Alemanha", "Itália", 
                                                 "Reino Unido", "Estados Unidos", "Brasil", "Outros"],
                                        index=0)
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            email_field = st.text_input("Email:")
        with col2:
            nif_field = st.text_input("NIF:")
        
        st.subheader("Código de Conduta")
        st.write("Por favor, leia o Código de Conduta do BPI no seguinte link:")
        st.markdown("[Clique aqui para ler o Código de Conduta do BPI](https://www.bancobpi.pt/contentservice/getContent?documentName=PR_UCMS02078313)", unsafe_allow_html=True)
        
        opcao_codigo = st.radio("Aceita o Código de Conduta do BPI?", options=["Aceito", "Não Aceito"])
        
        submit_minimo = st.form_submit_button("Continuar")
        
        if submit_minimo:
            # Validações mínimas
            if opcao_codigo == "Não Aceito":
                st.error("Não é possível continuar o registo sem aceitar o Código de Conduta.")
                st.stop()
            if not email_field:
                st.error("O campo Email é obrigatório.")
                st.stop()
            elif not validar_email(email_field):
                st.error("O Email introduzido não tem um formato válido.")
                st.stop()
            if not nif_field:
                st.error("O campo NIF é obrigatório.")
                st.stop()
            elif not nif_field.isdigit():
                st.error("O NIF deve conter apenas dígitos.")
                st.stop()
            elif len(nif_field) != 9:
                st.error("O NIF deve ter 9 dígitos.")
                st.stop()
            elif not validar_nif(nif_field):
                st.error("O NIF introduzido não é válido.")
                st.stop()
            elif nif_field in nifs_registados:
                st.error("Este NIF já se encontra registado no Portal.")
                st.stop()
            
            st.session_state["registro_minimo"] = {
                "designacao": designacao,
                "pais_empresa": pais_empresa,
                "email": email_field,
                "nif": nif_field,
                "codigo_conduct": opcao_codigo,
            }
            st.success("Dados básicos registados com sucesso! Prossiga para o 'Registo Completo' na aba abaixo.")

# Se ainda não passou pela etapa 1, paramos
if "registro_minimo" not in st.session_state:
    st.stop()

# =====================================================
# CRIA DUAS ABAS: (1) Registo de Fornecedores / (2) Questionário DORA
# =====================================================
tab_registo, tab_dora = st.tabs(["Registo de Fornecedores", "Questionário DORA"])

# =====================================================
# ABA 1 - REGISTO DE FORNECEDORES
# =====================================================
with tab_registo:
    st.header("Complemento do Registo")
    
    # Recuperar dados já preenchidos (se houver)
    dados_atual = st.session_state.get("registro_completo", {})

    # -------------------------------
    # Seção de Tipologia de Fornecimento (seleção dinâmica)
    # -------------------------------
    st.subheader("Tipologia de Fornecimento")
    
    # Nível 1 (multiselect com remoção de duplicados)
    df_nivel1 = df_tipologia[["ID NÍVEL 1", "NOME NÍVEL 1"]].drop_duplicates(subset=["ID NÍVEL 1", "NOME NÍVEL 1"])
    nivel1_opcoes = [f"{row['ID NÍVEL 1']} - {row['NOME NÍVEL 1']}" for _, row in df_nivel1.iterrows()]
    selected_nivel1_labels = st.multiselect("Selecione o(s) Nível(es) 1:", nivel1_opcoes, key="nivel1_dyn")
    selected_ids_1 = [lbl.split(" - ")[0] for lbl in selected_nivel1_labels]
    
    # Nível 2 (filtrado com base nos IDs do Nível 1 e remoção de duplicados)
    df_nivel2 = df_tipologia[df_tipologia["ID NÍVEL 1"].isin(selected_ids_1)].drop_duplicates(subset=["ID NÍVEL 2", "NOME NÍVEL 2"])
    nivel2_opcoes = [f"{row['ID NÍVEL 2']} - {row['NOME NÍVEL 2']}" for _, row in df_nivel2.iterrows()]
    selected_nivel2_labels = st.multiselect("Selecione o(s) Nível(es) 2:", nivel2_opcoes, key="nivel2_dyn")
    selected_ids_2 = [lbl.split(" - ")[0] for lbl in selected_nivel2_labels]
    
    # Nível 3 (filtrado com base nos IDs do Nível 2 e remoção de duplicados)
    df_nivel3 = df_tipologia[df_tipologia["ID NÍVEL 2"].isin(selected_ids_2)].drop_duplicates(subset=["ID NÍVEL 3", "NOME NÍVEL 3"])
    nivel3_opcoes = [f"{row['ID NÍVEL 3']} - {row['NOME NÍVEL 3']}" for _, row in df_nivel3.iterrows()]
    selected_nivel3_labels = st.multiselect("Selecione o(s) Nível(es) 3:", nivel3_opcoes, key="nivel3_dyn")
    
    # Resumo dinâmico em tabela
    if selected_nivel1_labels or selected_nivel2_labels or selected_nivel3_labels:
        resumo = {
            "Nível 1": [", ".join(selected_nivel1_labels)],
            "Nível 2": [", ".join(selected_nivel2_labels)],
            "Nível 3": [", ".join(selected_nivel3_labels)]
        }
        st.markdown("### Resumo da Seleção")
        st.table(pd.DataFrame(resumo))
    else:
        st.info("Nenhuma tipologia selecionada.")

    # -------------------------------
    # Formulário para o restante dos dados
    # -------------------------------
    with st.form("form_registo_completo", clear_on_submit=False):
        # Endereço
        st.subheader("Endereço")
        col_end1, col_end2 = st.columns(2, gap="large")
        with col_end1:
            rua = st.text_input("Rua:", value=dados_atual.get("rua", ""))
        with col_end2:
            localidade = st.text_input("Localidade:", value=dados_atual.get("localidade", ""))
        col_end3, col_end4 = st.columns(2, gap="large")
        with col_end3:
            codigo_postal = st.text_input("Código Postal:", value=dados_atual.get("codigo_postal", ""))
        with col_end4:
            # Campo Distrito / Estado (substituindo o antigo campo País do endereço)
            distrito_estado = st.text_input("Distrito / Estado:", value=dados_atual.get("distrito_estado", ""))
        
        # Dados Bancários com novo campo: País da Conta
        st.subheader("Dados Bancários")
        col_b1, col_b2, col_b3 = st.columns([3, 3, 1], gap="large")
        with col_b1:
            iban = st.text_input("IBAN:", value=dados_atual.get("iban", ""))
        with col_b2:
            swift = st.text_input("SWIFT:", value=dados_atual.get("swift", ""))
        with col_b3:
            pais_conta = st.selectbox("País da Conta:", 
                                       options=["Portugal", "Espanha", "França", "Alemanha", "Itália", 
                                                "Reino Unido", "Estados Unidos", "Brasil", "Outros"],
                                       index=0)
        
        # Anexos Obrigatórios
        st.subheader("Anexos Obrigatórios")
        st.write("Por favor, anexe os seguintes documentos:")
        col_at, col_ss = st.columns(2, gap="large")
        with col_at:
            st.markdown("**Declaração AT**")
            validade_at = st.date_input("Data de Validade (Declaração AT)",
                                        value=dados_atual.get("validade_at", datetime.today()))
            arquivo_at = st.file_uploader("Anexar Declaração AT", 
                                          type=["pdf", "jpg", "jpeg", "png", "doc", "docx"], 
                                          key="arquivo_at")
        with col_ss:
            st.markdown("**Declaração SS**")
            validade_ss = st.date_input("Data de Validade (Declaração SS)",
                                        value=dados_atual.get("validade_ss", datetime.today()))
            arquivo_ss = st.file_uploader("Anexar Declaração SS", 
                                          type=["pdf", "jpg", "jpeg", "png", "doc", "docx"], 
                                          key="arquivo_ss")
        
        col_certidao, col_rcbe = st.columns(2, gap="large")
        with col_certidao:
            st.markdown("**Certidão Permanente**")
            validade_certidao = st.date_input("Data de Validade (Certidão Permanente)",
                                              value=dados_atual.get("validade_certidao", datetime.today()))
            arquivo_certidao = st.file_uploader("Anexar Certidão Permanente", 
                                                type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
                                                key="arquivo_certidao")
        with col_rcbe:
            st.markdown("**RCBE**")
            arquivo_rcbe = st.file_uploader("Anexar RCBE", 
                                            type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
                                            key="arquivo_rcbe")
        
        # Anexos (Opcional)
        st.subheader("Anexos (Opcional)")
        anexos_opcionais = st.file_uploader("Anexe documentos adicionais:", 
                                            type=["pdf", "jpg", "jpeg", "png", "doc", "docx"],
                                            accept_multiple_files=True,
                                            key="anexos_opcionais")
        
        # Princípios de Sustentabilidade
        st.subheader("Princípios de Sustentabilidade")
        st.write("Por favor, leia os princípios de sustentabilidade no seguinte link: [Princípios de Sustentabilidade](https://www.bancobpi.pt/sustentabilidade/governacao/estrategia-governo-sustentabilidade)")
        sust_checkbox = st.checkbox("Confirmo que li e aceito os Princípios de Sustentabilidade")
        
        # Botão Gravar / Atualizar
        btn_gravar = st.form_submit_button("Gravar / Atualizar Registo")
    
        if btn_gravar:
            if not sust_checkbox:
                st.error("É necessário ler e aceitar os Princípios de Sustentabilidade para continuar o registo.")
                st.stop()
            # Atualiza o registro completo usando os valores armazenados na etapa 1 para os campos básicos
            st.session_state["registro_completo"] = {
                "designacao": st.session_state.get("registro_minimo", {}).get("designacao", ""),
                "pais_empresa": st.session_state.get("registro_minimo", {}).get("pais_empresa", ""),
                "email": st.session_state.get("registro_minimo", {}).get("email", ""),
                "nif": st.session_state.get("registro_minimo", {}).get("nif", ""),
                "codigo_conduct": st.session_state.get("registro_minimo", {}).get("codigo_conduct", ""),
                "nivel1_label": selected_nivel1_labels,
                "nivel2_labels": selected_nivel2_labels,
                "nivel3_labels": selected_nivel3_labels,
                "rua": rua,
                "localidade": localidade,
                "codigo_postal": codigo_postal,
                "distrito_estado": distrito_estado,
                "iban": iban,
                "swift": swift,
                "pais_conta": pais_conta,
                "validade_at": validade_at,
                "arquivo_at": arquivo_at,
                "validade_ss": validade_ss,
                "arquivo_ss": arquivo_ss,
                "validade_certidao": validade_certidao,
                "arquivo_certidao": arquivo_certidao,
                "arquivo_rcbe": arquivo_rcbe,
                "anexos_opcionais": anexos_opcionais,
                "sustentabilidade": sust_checkbox
            }
            if not selected_ids_1 or selected_ids_1[0] != "05":
                st.success(
                    "Registo submetido com sucesso!\n\n"
                    "Estado do registo: **Pendente**.\n\n"
                    "O registo foi encaminhado para a Direção de Procurement para análise."
                )
            else:
                if not st.session_state.get("questionario_dora_submetido", False):
                    st.info(
                        "Devido à tipologia '05 - IT', aceda ao separador 'Questionário DORA' para preenchê-lo. "
                        "Depois volte aqui para concluir o registo."
                    )
                else:
                    st.success(
                        "Questionário DORA já submetido. Agora pode concluir o registo final."
                    )
    
    # Botão de conclusão final (se aplicável)
    registro_cplt = st.session_state.get("registro_completo", {})
    if registro_cplt.get("nivel1_label"):
        nivel1_ids = [lbl.split(" - ")[0] for lbl in registro_cplt["nivel1_label"]]
    else:
        nivel1_ids = []
    if "05" in nivel1_ids and st.session_state.get("questionario_dora_submetido", False):
        if st.button("Concluir Registo Final"):
            st.success(
                "Registo submetido com sucesso!\n\n"
                "Estado do registo: **Pendente**.\n\n"
                "O registo foi encaminhado para a Direção de Procurement para análise."
            )
            # Aqui poderia salvar em BD ou outro procedimento final

# =====================================================
# ABA 2 - QUESTIONÁRIO DORA
# =====================================================
with tab_dora:
    st.header("Questionário DORA")
    dados_registo = st.session_state.get("registro_completo", {})
    nivel1_ids = []
    if dados_registo.get("nivel1_label"):
        nivel1_ids = [lbl.split(" - ")[0] for lbl in dados_registo["nivel1_label"]]
    if "05" not in nivel1_ids:
        st.warning("Só precisa preencher o DORA se escolheu o Nível 1 = '05' (IT) na aba anterior.")
    else:
        if st.session_state.get("questionario_dora_submetido", False):
            st.success("O Questionário DORA já foi submetido com sucesso!")
            st.info("Volte ao Separador 'Registo de Fornecedores' para concluir o registo.")
        else:
            with st.form("form_dora"):
                dora_respostas = {}
                st.markdown("### 1. Informações Gerais")
                dora_respostas["seg_atuacao"] = st.text_input("1) Segmento de atuação:")
                dora_respostas["prod_serv"] = st.text_area("2) Principais produtos/serviços ofertados:")
                dora_respostas["num_func"] = st.text_input("3) Número aproximado de funcionários:")
                dora_respostas["local_inst"] = st.text_area("4) Localização das principais instalações (sede, filiais, data centers):")
                st.markdown("### 2. Estrutura de Governança e Compliance")
                frameworks_opcoes = ["ISO 27001", "NIST CSF", "COBIT", "Outras"]
                dora_respostas["frameworks"] = st.multiselect("2.1) Quais frameworks ou normas de segurança da informação a sua organização adota?",
                                                               options=frameworks_opcoes,
                                                               help="Selecione quantas forem aplicáveis.")
                dora_respostas["frameworks_outras"] = ""
                if "Outras" in dora_respostas["frameworks"]:
                    dora_respostas["frameworks_outras"] = st.text_input("Especifique quais outras normas/frameworks:")
                dora_respostas["certificacoes"] = st.text_area("2.2) Possui certificações formais em segurança ou privacidade? Se sim, indique quais:")
                dora_respostas["resp_ciber"] = st.radio("2.3) Existe na sua organização um responsável ou uma equipe dedicada à gestão de risco e cibersegurança?",
                                                      options=["Sim", "Não"])
                dora_respostas["resp_ciber_desc"] = ""
                if dora_respostas["resp_ciber"] == "Sim":
                    dora_respostas["resp_ciber_desc"] = st.text_area("Se sim, descreva a estrutura ou indique como está organizada:")
                st.markdown("### 3. Gestão de Riscos e Avaliação Contínua")
                dora_respostas["risco_metodologia"] = st.text_area("3.1) Como vocês identificam, avaliam e tratam riscos de TIC? Descreva brevemente o processo.")
                freq_opcoes = ["Mensal", "Trimestral", "Semestral", "Anual", "Outro"]
                dora_respostas["freq_riscos"] = st.radio("3.2) Com que frequência é feita a revisão ou atualização da avaliação de riscos (Risk Assessment)?",
                                                        options=freq_opcoes)
                dora_respostas["freq_riscos_outro"] = ""
                if dora_respostas["freq_riscos"] == "Outro":
                    dora_respostas["freq_riscos_outro"] = st.text_input("Indique qual:")
                dora_respostas["testes_vuln"] = st.radio("3.3) Vocês realizam testes de vulnerabilidade e/ou testes de invasão (penetration tests)?",
                                                        options=["Sim, regularmente", "Sim, mas esporadicamente", "Não realizamos"])
                dora_respostas["testes_vuln_desc"] = ""
                if dora_respostas["testes_vuln"] in ["Sim, regularmente", "Sim, mas esporadicamente"]:
                    dora_respostas["testes_vuln_desc"] = st.text_area("Se sim, descreva a frequência e se há empresa externa envolvida:")
                st.markdown("### 4. Segurança da Informação e Cibersegurança")
                ctrl_opcoes = ["Criptografia de dados em repouso", "Criptografia de dados em trânsito (TLS/SSL)", "Outros mecanismos"]
                dora_respostas["controles"] = st.multiselect("4.1) Quais controles de segurança são adotados para proteger dados em trânsito e em repouso?",
                                                           options=ctrl_opcoes)
                dora_respostas["controles_outros"] = ""
                if "Outros mecanismos" in dora_respostas["controles"]:
                    dora_respostas["controles_outros"] = st.text_input("Especifique os outros mecanismos:")
                dora_respostas["politicas_si"] = st.radio("4.2) A sua organização possui políticas formais de segurança da informação documentadas e divulgadas aos colaboradores?",
                                                         options=["Sim", "Não"])
                dora_respostas["iam_proc"] = st.radio("4.3) Existe um processo de gestão de acessos e identidades (IAM), incluindo revisão periódica de permissões e uso de MFA?",
                                                     options=["Sim", "Não", "Em implementação"])
                dora_respostas["monitoramento"] = st.text_area("4.4) Como vocês monitoram eventuais acessos não autorizados, atividades suspeitas ou violações de política?")
                dora_respostas["atualizacoes"] = st.text_area("4.5) Como tratam atualizações de software, patches e correções de vulnerabilidades críticas? Indique a periodicidade.")
                st.markdown("### 5. Continuidade de Negócios e Recuperação de Desastres")
                dora_respostas["bcp_drp"] = st.radio("5.1) A organização possui um BCP e DRP formalmente documentados?",
                                                   options=["Sim", "Não"])
                bcp_test_opcoes = ["Semestral", "Anual", "Não são testados", "Outro"]
                dora_respostas["freq_bcp_drp"] = st.radio("5.2) Com que frequência esses planos são testados ou simulados?",
                                                        options=bcp_test_opcoes)
                dora_respostas["freq_bcp_drp_outro"] = ""
                if dora_respostas["freq_bcp_drp"] == "Outro":
                    dora_respostas["freq_bcp_drp_outro"] = st.text_input("Indique qual:")
                dora_respostas["rto_rpo_def"] = st.radio("5.3) Existe definição clara de RTO e RPO para os serviços críticos?",
                                                       options=["Sim, definidos e conhecidos pelas áreas envolvidas", "Não, ainda não definidos"])
                dora_respostas["rto_rpo_valor"] = ""
                if dora_respostas["rto_rpo_def"].startswith("Sim"):
                    dora_respostas["rto_rpo_valor"] = st.text_input("Se sim, qual é o RTO/RPO para os principais serviços?")
                backup_opcoes = ["Backup periódico automatizado", "Armazenamento em local diferente do site principal (offsite)",
                                 "Criptografia de backups", "Testes regulares de restauração", "Outro"]
                dora_respostas["backup"] = st.multiselect("5.4) Como é feito o backup dos dados?",
                                                         options=backup_opcoes)
                dora_respostas["backup_outro"] = ""
                if "Outro" in dora_respostas["backup"]:
                    dora_respostas["backup_outro"] = st.text_input("Especifique outro método de backup:")
                st.markdown("### 6. Proteção e Privacidade de Dados")
                dora_respostas["gdpr"] = st.radio("6.1) Existem políticas ou processos para a proteção de dados pessoais, em conformidade com leis como GDPR?",
                                                 options=["Sim", "Não"])
                dora_respostas["dpo"] = st.radio("6.2) Há um encarregado de proteção de dados (DPO) ou figura equivalente responsável pela privacidade?",
                                                options=["Sim", "Não"])
                dora_respostas["vazamento_desc"] = st.text_area("6.3) Como são tratados eventuais incidentes de vazamento de dados pessoais?")
                st.markdown("### 7. Gestão de Terceiros e Subcontratados (Cadeia de Suprimentos)")
                dora_respostas["terceirizacao"] = st.radio("7.1) Vocês terceirizam ou subcontratam parte dos serviços que nos prestam?",
                                                         options=["Sim", "Não"])
                dora_respostas["terceirizacao_desc"] = ""
                if dora_respostas["terceirizacao"] == "Sim":
                    dora_respostas["terceirizacao_desc"] = st.text_area("Se sim, descreva qual parcela do serviço e como é feito o gerenciamento de riscos:")
                dora_respostas["terceirizacao_sla"] = st.text_area("7.2) Quais cláusulas contratuais ou SLAs são estabelecidos com subfornecedores para segurança e continuidade?")
                st.markdown("### 8. Notificação e Gestão de Incidentes")
                dora_respostas["gestao_incidentes"] = st.radio("8.1) A sua organização possui um processo formal de gestão de incidentes de TIC e cibersegurança?",
                                                             options=["Sim, documentado e testado", "Não"])
                not_opcoes = ["Imediatamente (em até X horas)", "Em até 24 horas", "Em até 72 horas", "Outro"]
                dora_respostas["prazo_notif"] = st.radio("8.2) Qual o prazo de notificação que vocês adotam para comunicar um incidente relevante aos clientes?",
                                                        options=not_opcoes)
                dora_respostas["prazo_notif_outro"] = ""
                if dora_respostas["prazo_notif"] == "Outro":
                    dora_respostas["prazo_notif_outro"] = st.text_input("Se 'Outro', indique:")
                dora_respostas["contato_incidentes"] = st.text_input("8.3) Quem é o ponto de contato oficial para tratar incidentes de segurança?")
                st.markdown("### 9. Conformidade com a DORA e Regulamentações Financeiras")
                dora_respostas["ciente_dora"] = st.radio("9.1) Vocês estão cientes das obrigações introduzidas pela DORA no que tange à resiliência digital?",
                                                        options=["Sim", "Não"])
                dora_respostas["medidas_dora"] = ""
                if dora_respostas["ciente_dora"] == "Sim":
                    dora_respostas["medidas_dora"] = st.text_area("Se sim, descreva as principais medidas que estão implementando ou já implementaram.")
                dora_respostas["testes_resil"] = st.radio("9.2) Vocês teriam condições de participar de testes de resiliência conjuntos?",
                                                        options=["Sim", "Não"])
                dora_respostas["evidencias_reg"] = st.radio("9.3) Estão preparados para fornecer relatórios ou evidências adicionais quando exigido?",
                                                          options=["Sim", "Não"])
                st.markdown("### 10. Declaração Final")
                dora_respostas["declaracao_final"] = st.radio("10.1) Declaro que todas as informações prestadas neste questionário são verdadeiras e fidedignas.",
                                                            options=["Sim, confirmo", "Não confirmo"])
                dora_submit = st.form_submit_button("Submeter Questionário DORA")
            if dora_submit:
                if not dora_respostas["seg_atuacao"]:
                    st.error("Por favor, preencha ao menos o campo 'Segmento de atuação' (1.1).")
                elif dora_respostas["declaracao_final"] != "Sim, confirmo":
                    st.error("É preciso confirmar a veracidade das informações para submeter o Questionário DORA.")
                else:
                    st.session_state["questionario_dora_respostas"] = dora_respostas
                    st.session_state["questionario_dora_submetido"] = True
                    st.success("Questionário DORA submetido com sucesso!")
                    st.info("Volte ao Separador 'Registo de Fornecedores' para concluir o registo, caso necessário.")
