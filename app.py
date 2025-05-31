import streamlit as st
import pandas as pd
import plotly.express as px

# Título do aplicativo
st.set_page_config(layout="wide")
st.title("Promotoria de Justiça do Guarujá no e-SAJ")
st.markdown("---")

df = pd.read_csv('cargos_ano.csv')

# Certificar-se de que a coluna 'Ano' é numérica e pode ser usada como índice
df['Ano'] = pd.to_numeric(df['Ano'])
df.set_index('Ano', inplace=True)

# Obter a lista de anos e cargos disponíveis
anos_disponiveis = df.index.unique().tolist()
cargos_disponiveis = [col for col in df.columns if 'PROMOTOR' in col]

# --- Sidebar para seleção de filtros ---
st.sidebar.header("Filtros")

# Seleção de período
ano_inicial = st.sidebar.selectbox(
    "Selecione o ano inicial:",
    options=sorted(anos_disponiveis),
    index=0 # Padrão para o primeiro ano disponível
)

ano_final = st.sidebar.selectbox(
    "Selecione o ano final:",
    options=sorted(anos_disponiveis),
    index=len(anos_disponiveis) - 1 # Padrão para o último ano disponível
)

# Validação do período
if ano_inicial > ano_final:
    st.sidebar.error("O ano inicial não pode ser maior que o ano final. Por favor, ajuste.")
    st.stop() # Interrompe a execução para evitar erros

# Seleção de cargos
cargos_selecionados = st.sidebar.multiselect(
    "Selecione os cargos:",
    options=cargos_disponiveis,
    default=cargos_disponiveis # Seleciona todos os cargos por padrão
)

# Validação de cargos selecionados
if not cargos_selecionados:
    st.sidebar.warning("Nenhum cargo selecionado. Por favor, selecione ao menos um.")
    st.stop() # Interrompe a execução para evitar erros

# --- Filtragem dos dados ---
df_filtrado_periodo = df.loc[ano_inicial:ano_final, cargos_selecionados]

# Preparar dados para o gráfico de linhas (long format)
df_line = df_filtrado_periodo.reset_index().melt(id_vars='Ano', var_name='Cargo', value_name='Valor')

# --- Exibição dos Gráficos ---

st.header("Gráfico de Linhas")
fig_line = px.line(
    df_line,
    x='Ano',
    y='Valor',
    color='Cargo',
    title=f'Interação dos Cargos Selecionados ({ano_inicial}-{ano_final})',
    labels={'Valor': 'Número de Registros'}
)
fig_line.update_xaxes(tickmode='linear') # Garante que todos os anos sejam exibidos se houver dados
st.plotly_chart(fig_line, use_container_width=True)

st.header("Gráfico de Barras")
# Calcular o total (ou média) para o gráfico de barras
df_bar = df_filtrado_periodo.sum().reset_index()
df_bar.columns = ['Cargo', 'Total']

fig_bar = px.bar(
    df_bar,
    x='Cargo',
    y='Total',
    title=f'Interação por Cargo no Período ({ano_inicial}-{ano_final})',
    labels={'Total': 'Total de Registros'}
)
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Dados Filtrados")
st.dataframe(df_filtrado_periodo)

st.markdown("---") 
st.markdown("Desenvolvido por: Pimentel (© 2025) | [GitHub](https://github.com/jespimentel) | [LinkedIn](https://www.linkedin.com/in/jespimentel/)", unsafe_allow_html=True)
# Fim do código
