import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configurações Iniciais do Aplicativo ---
st.set_page_config(layout="wide")
st.title("Promotoria de Justiça do Guarujá no e-SAJ")
st.markdown("---")

# --- Carregamento e Preparação dos Dados ---
# Assume-se que 'cargos_ano.csv' está no mesmo diretório ou caminho especificado
try:
    df = pd.read_csv('cargos_ano.csv')
except FileNotFoundError:
    st.error("Erro: O arquivo 'cargos_ano.csv' não foi encontrado. Por favor, verifique o caminho.")
    st.stop() # Interrompe a execução se o arquivo não for encontrado

# Certificar-se de que a coluna 'Ano' é numérica e pode ser usada como índice
df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce') # 'coerce' transforma erros em NaN
df.dropna(subset=['Ano'], inplace=True) # Remove linhas com 'Ano' inválido
df['Ano'] = df['Ano'].astype(int) # Converte para inteiro após a validação
df.set_index('Ano', inplace=True)

# Obter a lista de anos e cargos disponíveis
anos_disponiveis = sorted(df.index.unique().tolist())
cargos_disponiveis = [col for col in df.columns if 'PROMOTOR' in col.upper()] # Usa .upper() para ser case-insensitive

# --- Sidebar para Seleção de Filtros ---
st.sidebar.header("Filtros")

# Seleção de período
if not anos_disponiveis:
    st.sidebar.warning("Nenhum ano disponível nos dados para filtragem.")
    st.stop()

ano_inicial = st.sidebar.selectbox(
    "Selecione o ano inicial:",
    options=anos_disponiveis,
    index=0 # Padrão para o primeiro ano disponível
)

ano_final = st.sidebar.selectbox(
    "Selecione o ano final:",
    options=anos_disponiveis,
    index=len(anos_disponiveis) - 1 # Padrão para o último ano disponível
)

# Validação do período
if ano_inicial > ano_final:
    st.sidebar.error("O ano inicial não pode ser maior que o ano final. Por favor, ajuste.")
    st.stop() # Interrompe a execução para evitar erros

# Seleção de cargos
if not cargos_disponiveis:
    st.sidebar.warning("Nenhum cargo com 'PROMOTOR' encontrado nos dados.")
    st.stop()

cargos_selecionados = st.sidebar.multiselect(
    "Selecione os cargos:",
    options=cargos_disponiveis,
    default=cargos_disponiveis # Seleciona todos os cargos por padrão
)

# Validação de cargos selecionados
if not cargos_selecionados:
    st.sidebar.warning("Nenhum cargo selecionado. Por favor, selecione ao menos um.")
    st.stop() # Interrompe a execução para evitar erros

# --- Filtragem dos Dados ---
# Garante que apenas as colunas selecionadas existam antes de filtrar
cols_to_filter = [col for col in cargos_selecionados if col in df.columns]
if not cols_to_filter:
    st.error("Os cargos selecionados não foram encontrados nas colunas do arquivo CSV.")
    st.stop()

df_filtrado_periodo = df.loc[ano_inicial:ano_final, cols_to_filter]

# --- Exibição dos Gráficos ---

# Gráfico de Linhas: Evolução no período
st.header("Evolução no Período")
# Preparar dados para o gráfico de linhas (long format)
df_line = df_filtrado_periodo.reset_index().melt(id_vars='Ano', var_name='Cargo', value_name='Valor')

fig_line = px.line(
    df_line,
    x='Ano',
    y='Valor',
    color='Cargo',
    title=f'Evolução da Interação dos Cargos Selecionados ({ano_inicial}-{ano_final})',
    labels={'Valor': 'Número de Registros'}
)
fig_line.update_xaxes(tickmode='linear') # Garante que todos os anos sejam exibidos se houver dados
st.plotly_chart(fig_line, use_container_width=True)

---

# Gráfico de Barras: Acumulado por Cargo
st.header("Acumulado por Cargo")
# Calcular o total para o gráfico de barras
df_bar = df_filtrado_periodo.sum().reset_index()
df_bar.columns = ['Cargo', 'Total'] # Renomeia as colunas ANTES de ordenar

# Ordenar o DataFrame pela coluna 'Total' em ordem decrescente
df_bar = df_bar.sort_values(by='Total', ascending=False)

fig_bar = px.bar(
    df_bar,
    x='Cargo',
    y='Total',
    title=f'Total de Interação por Cargo no Período ({ano_inicial}-{ano_final})',
    labels={'Total': 'Total de Registros'},
    color_discrete_sequence=['darkred'], # Define a cor das barras como vermelho escuro
)
st.plotly_chart(fig_bar, use_container_width=True)

---

# Dados Filtrados
st.subheader("Dados Filtrados")
st.dataframe(df_filtrado_periodo)

st.markdown("---")
st.markdown("Desenvolvido por: Pimentel (© 2025) | [GitHub](https://github.com/jespimentel) | [LinkedIn](https://www.linkedin.com/in/jespimentel/)", unsafe_allow_html=True)
