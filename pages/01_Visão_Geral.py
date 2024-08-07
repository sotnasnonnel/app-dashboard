from pathlib import Path
from datetime import date, timedelta
import streamlit as st
import pandas as pd
import plotly.express as px

# Adicione a função configure_page aqui
def configure_page():
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":bar_chart:")

# Chame a função configure_page imediatamente após defini-la
configure_page()

from utilidades import leitura_de_dados, COMISSAO

# Chame a função de leitura de dados e atribua o resultado a uma variável
leitura_de_dados()

# Verifique se os dados foram carregados corretamente na sessão
if 'dados' in st.session_state:
    df_vendas = st.session_state['dados'].get('df_vendas', pd.DataFrame())
    df_filiais = st.session_state['dados'].get('df_filiais', pd.DataFrame())
    df_produtos = st.session_state['dados'].get('df_produtos', pd.DataFrame())
else:
    st.error("Erro ao carregar dados. Verifique a função leitura_de_dados.")
    st.stop()

# Verifique se os DataFrames não estão vazios
if df_vendas.empty or df_filiais.empty or df_produtos.empty:
    st.error("Um ou mais DataFrames estão vazios. Verifique os dados de entrada.")
    st.stop()

df_produtos = df_produtos.rename(columns={'nome': 'produto'})
df_vendas = df_vendas.reset_index()

df_vendas = pd.merge(left=df_vendas,
                     right=df_produtos[['produto', 'preco']],
                     on='produto',
                     how='left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * COMISSAO

selecao_keys = {'Filial': 'filial',
                'Vendedor': 'vendedor',
                'Produto': 'produto',
                'Forma de Pagamento': 'forma_pagamento',
                'Gênero Cliente': 'cliente_genero',
                }

df_vendas = df_vendas[df_vendas.index.notnull()]
data_final_def = df_vendas.index.max()
data_inicial_def = date(year=data_final_def.year, month=data_final_def.month, day=1)
data_inicial = st.sidebar.date_input('Data Inicial', data_inicial_def)
data_final = st.sidebar.date_input('Data Final', data_final_def)

analise_selecionada = st.sidebar.selectbox('Analisar:', list(selecao_keys.keys()))
analise_selecionada = selecao_keys[analise_selecionada]

st.markdown('# Dashboard de Análise')

df_vendas_corte = df_vendas[(df_vendas.index.date >= data_inicial) & (df_vendas.index.date <= data_final)]
df_vendas_corte_anterior = df_vendas[(df_vendas.index.date >= data_inicial - timedelta(days=30)) & (
    df_vendas.index.date <= data_final - timedelta(days=30))]

col1, col2, col3, col4 = st.columns(4)

valor_vendas = f"R$ {df_vendas_corte['preco'].sum() / 1000:.0f} Mil"
dif_metrica = df_vendas_corte['preco'].sum() - df_vendas_corte_anterior['preco'].sum()
col1.metric('Valor de vendas no período', valor_vendas, float(dif_metrica))

quantidade_vendas = df_vendas_corte['preco'].count()
dif_metrica = df_vendas_corte['preco'].count() - df_vendas_corte_anterior['preco'].count()
col2.metric('Quantidade de vendas no período', quantidade_vendas, int(dif_metrica))

principal_filial = df_vendas_corte['filial'].value_counts().index[0]
col3.metric('Principal filial', principal_filial)

principal_vendedor = df_vendas_corte['vendedor'].value_counts().index[0]
col4.metric('Principal vendedor', principal_vendedor)

st.divider()

col21, col22 = st.columns(2)

df_vendas_corte['dia_venda'] = df_vendas_corte.index.date
venda_dia = df_vendas_corte.groupby('dia_venda')['preco'].sum()
venda_dia.name = 'Valor Venda'

fig = px.line(venda_dia)
col21.plotly_chart(fig)

fig = px.pie(df_vendas_corte, names=analise_selecionada, values='preco')
fig.update_traces(textinfo='label+percent')
col22.plotly_chart(fig)

st.divider()
