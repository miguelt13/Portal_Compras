import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# ============================
# Lista simulada de registos
# ============================
registos_fornecedores = [
    {
        "nif": "111111111",
        "nome": "Fornecedor Alfa, Lda.",
        "tipologia": "01 - Serviços",
        "pais": "Portugal",
        "distrito": "Lisboa",
        "estado": "Em Início",
        "ultima_atualizacao": "2025-01-10 10:30"
    },
    {
        "nif": "222222222",
        "nome": "Fornecedor Beta, SA",
        "tipologia": "02 - Produtos",
        "pais": "Espanha",
        "distrito": "Madrid",
        "estado": "Pendente de Análise",
        "ultima_atualizacao": "2025-01-12 15:45"
    },
    {
        "nif": "333333333",
        "nome": "Fornecedor Gama, Lda.",
        "tipologia": "01 - Serviços",
        "pais": "Portugal",
        "distrito": "Porto",
        "estado": "Pendente (aguarda atribuição GCC)",
        "ultima_atualizacao": "2025-02-01 08:10"
    },
    {
        "nif": "444444444",
        "nome": "Fornecedor Delta, SL",
        "tipologia": "05 - TI e Software",
        "pais": "Espanha",
        "distrito": "Barcelona",
        "estado": "Potenciais",
        "ultima_atualizacao": "2025-02-03 11:00"
    },
    {
        "nif": "555555555",
        "nome": "Fornecedor Épsilon, Lda.",
        "tipologia": "03 - Consultoria",
        "pais": "Portugal",
        "distrito": "Coimbra",
        "estado": "Aprovado",
        "ultima_atualizacao": "2025-02-05 09:25"
    },
    {
        "nif": "666666666",
        "nome": "Fornecedor Kappa, Inc.",
        "tipologia": "04 - Transporte/Logística",
        "pais": "EUA",
        "distrito": "NY",
        "estado": "Rejeitado",
        "ultima_atualizacao": "2025-02-06 18:40"
    },
    {
        "nif": "777777777",
        "nome": "Fornecedor Ómega, SA",
        "tipologia": "02 - Produtos",
        "pais": "Brasil",
        "distrito": "São Paulo",
        "estado": "Em Homologação",
        "ultima_atualizacao": "2025-02-07 14:00"
    }
]

# ------------------------------
# Listas de opções para filtros
# ------------------------------
tipologias_unicas = sorted(list({r["tipologia"] for r in registos_fornecedores}))
tipologias_opcoes = ["Todas"] + tipologias_unicas

paises_unicos = sorted(list({r["pais"] for r in registos_fornecedores}))
paises_opcoes = ["Todos"] + paises_unicos

distritos_unicos = sorted(list({r["distrito"] for r in registos_fornecedores}))
distritos_opcoes = ["Todos"] + distritos_unicos

# Todos os estados possíveis
ALL_STATES = [
    "Em Início",
    "Pendente de Análise",
    "Pendente (aguarda atribuição GCC)",
    "Potenciais",
    "Aprovado",
    "Rejeitado",
    "Em Homologação"
]

# ============================
# Configurar página
# ============================
st.set_page_config(page_title="DP - Dashboard de Fornecedores", layout="wide")

# ============================
# CSS + Header
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
# Sidebar
# ============================
st.sidebar.markdown("## Menu")
menu_opcoes = [
    "Registos de Fornecedores",
    "Homologação (Indisponível)",
    "Atribuição GCC (Indisponível)",
    "Contratos (Indisponível)"
]
menu_escolhido = st.sidebar.radio("Selecione a opção", menu_opcoes)
if menu_escolhido != "Registos de Fornecedores":
    st.sidebar.warning("Por favor, selecione 'Registos de Fornecedores'.")
    menu_escolhido = "Registos de Fornecedores"

# ============================
# Título da Página
# ============================
st.markdown("## Dashboard de Registos de Fornecedores")

# ============================
# Área de Filtros e Ordenação
# ============================
with st.expander("Filtros e Ordenação"):
    # Filtro por texto (NIF ou Nome)
    texto_filtro = st.text_input("Filtrar por NIF ou Nome:", "")

    # --------------------------
    # Checkboxes de Estados
    # --------------------------
    st.markdown("**Estados a Exibir:**")
    # Vamos distribuir as 7 checkbox em 3 colunas, para não ficar tudo em 1 só
    colA, colB, colC = st.columns(3)

    # Por padrão, 3 estados marcados
    default_checked = {
        "Pendente de Análise": True,
        "Pendente (aguarda atribuição GCC)": True,
        "Em Homologação": True
    }
    
    selected_states = []  # para acumular o que estiver "checkado"
    
    # 1ª coluna
    with colA:
        for estado in ALL_STATES[:3]:  # Em Início, Pendente de Análise, Pendente (aguarda GCC)
            valor_inicial = default_checked.get(estado, False)
            checked = st.checkbox(estado, value=valor_inicial)
            if checked:
                selected_states.append(estado)
    # 2ª coluna
    with colB:
        for estado in ALL_STATES[3:5]:  # Potenciais, Aprovado
            valor_inicial = default_checked.get(estado, False)
            checked = st.checkbox(estado, value=valor_inicial)
            if checked:
                selected_states.append(estado)
    # 3ª coluna
    with colC:
        for estado in ALL_STATES[5:]:  # Rejeitado, Em Homologação
            valor_inicial = default_checked.get(estado, False)
            checked = st.checkbox(estado, value=valor_inicial)
            if checked:
                selected_states.append(estado)

    # --------------------------
    # Tipologia e País lado a lado
    # --------------------------
    col1, col2 = st.columns(2)
    with col1:
        tipologia_filtro = st.selectbox("Filtrar por Tipologia:", tipologias_opcoes, index=0)
    with col2:
        pais_filtro = st.selectbox("Filtrar por País:", paises_opcoes, index=0)

    # --------------------------
    # Distrito e Checkboxes de Responsabilidade lado a lado
    # --------------------------
    col3, col4 = st.columns([1,2])
    with col3:
        distrito_filtro = st.selectbox("Filtrar por Distrito/Estado:", distritos_opcoes, index=0)
    with col4:
        st.markdown("**Responsabilidade:**")
        resp_utilizador = st.checkbox("Registos do Utilizador", value=True)
        resp_perfil = st.checkbox("Registos do Perfil", value=False)
        # Removido o "Outro Check" conforme solicitado
    
    st.write("*(Nesta demo, a ordenação e as checkboxes de Responsabilidade não estão ligadas a nenhuma lógica real de filtragem, apenas ilustrativas.)*")

# ============================
# Função de Filtragem
# ============================
def filtrar_registos(
    registos, texto="", estados_selecionados=None,
    tipologia="Todas", pais="Todos", distrito="Todos"
):
    if estados_selecionados is None or len(estados_selecionados) == 0:
        # Se nenhum estado estiver selecionado, retornamos lista vazia
        return []

    filtrados = registos
    
    # Filtra pelos estados que estão "checkados"
    filtrados = [r for r in filtrados if r["estado"] in estados_selecionados]
    
    # Filtro por texto (NIF ou Nome)
    if texto:
        texto_lower = texto.lower()
        filtrados = [
            r for r in filtrados
            if (texto_lower in r["nif"].lower() or texto_lower in r["nome"].lower())
        ]

    # Filtro por tipologia
    if tipologia != "Todas":
        filtrados = [r for r in filtrados if r["tipologia"] == tipologia]

    # Filtro por país
    if pais != "Todos":
        filtrados = [r for r in filtrados if r["pais"] == pais]

    # Filtro por distrito
    if distrito != "Todos":
        filtrados = [r for r in filtrados if r["distrito"] == distrito]

    # Checkboxes de "Responsabilidade" (demonstrativo - não implementado)
    # if resp_utilizador:
    #     pass
    # if resp_perfil:
    #     pass
    return filtrados

# Aplica os filtros (se o usuário não tiver checkado nada em 'Estados', retorna vazio)
lista_filtrada = filtrar_registos(
    registos_fornecedores,
    texto=texto_filtro,
    estados_selecionados=selected_states,
    tipologia=tipologia_filtro,
    pais=pais_filtro,
    distrito=distrito_filtro
)

# ============================
# Exibição da Tabela (HTML)
# ============================
st.markdown("### Registos Encontrados")

if not lista_filtrada:
    st.info("Nenhum registo encontrado com os filtros aplicados, ou nenhum estado foi selecionado.")
else:
    # Ícones de “Ordenar” e “Editar”
    sort_icon_url = "https://cdn-icons-png.flaticon.com/512/892/892837.png"   # Ícone setas de ordenação
    edit_icon_url = "https://cdn-icons-png.flaticon.com/512/1159/1159633.png" # Ícone de lápis (editar)

    tabela_html = f"""
    <div style="overflow-x:auto;">
      <table style="width:100%; border-collapse: collapse; font-size: 14px; font-family: Arial, sans-serif;">
        <thead>
          <tr style="background-color: #3c8dbc; color: white;">
            <th style="padding: 8px;">NIF
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por NIF"/>
              </a>
            </th>
            <th style="padding: 8px;">Nome Fornecedor
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por Nome"/>
              </a>
            </th>
            <th style="padding: 8px;">Tipologia
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por Tipologia"/>
              </a>
            </th>
            <th style="padding: 8px;">País
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por País"/>
              </a>
            </th>
            <th style="padding: 8px;">Distrito/Estado
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por Distrito"/>
              </a>
            </th>
            <th style="padding: 8px;">Estado (Registo)
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por Estado"/>
              </a>
            </th>
            <th style="padding: 8px;">Data/Hora
              <a href="#" style="margin-left:5px;">
                <img src="{sort_icon_url}" width="16" title="Ordenar por Data/Hora"/>
              </a>
            </th>
            <th style="padding: 8px;">Ações</th>
          </tr>
        </thead>
        <tbody>
    """

    for reg in lista_filtrada:
        nif = reg["nif"]
        nome = reg["nome"]
        tipologia = reg["tipologia"]
        pais = reg["pais"]
        distrito = reg["distrito"]
        estado = reg["estado"]
        data_hora = reg["ultima_atualizacao"]

        # Ícone de “editar” (link fictício)
        link_editar = f"""
          <a href="#" title="Editar {nif}">
            <img src="{edit_icon_url}" width="20"/>
          </a>
        """

        tabela_html += f"""
          <tr style="border: 1px solid #ddd;">
            <td style="padding: 8px;">{nif}</td>
            <td style="padding: 8px;">{nome}</td>
            <td style="padding: 8px;">{tipologia}</td>
            <td style="padding: 8px;">{pais}</td>
            <td style="padding: 8px;">{distrito}</td>
            <td style="padding: 8px;">{estado}</td>
            <td style="padding: 8px;">{data_hora}</td>
            <td style="padding: 8px; text-align: center;">{link_editar}</td>
          </tr>
        """
    tabela_html += "</tbody></table></div>"

    components.html(tabela_html, height=400, scrolling=True)
