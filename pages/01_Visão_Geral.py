from pathlib import Path
from datetime import date, timedelta
import streamlit as st
import pandas as pd
import plotly_express as px

from utilidades import leitura_de_dados, COMISSAO

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

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
                'Gênero Cliente': 'cliente_genero'}

df_vendas = df_vendas[df_vendas.index.notnull()]

hoje = date.today()
primeiro_dia_mes_anterior = date(hoje.year, hoje.month - 1, 1) if hoje.month > 1 else date(hoje.year - 1, 12, 1)
data_inicial_def = primeiro_dia_mes_anterior

data_final_def = df_vendas.index.max()
if data_final_def is not None:
    data_final_def = data_final_def.date()

data_inicial = st.sidebar.date_input('Data Inicial', data_inicial_def)
data_final = st.sidebar.date_input('Data Final', data_final_def)

analise_selecionada = st.sidebar.selectbox('Analisar:', list(selecao_keys.keys()))
analise_selecionada = selecao_keys[analise_selecionada]

st.markdown('# Dashboard de Análise')

df_vendas_corte = df_vendas[(df_vendas.index.date >= data_inicial) & (df_vendas.index.date <= data_final)]
df_vendas_corte_anterior = df_vendas[(df_vendas.index.date >= data_inicial - timedelta(days=30)) & (
    df_vendas.index.date <= data_final - timedelta(days=30))]

col1, col2, col3, col4 = st.columns(4)

if not df_vendas_corte.empty:
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

if not df_vendas_corte.empty:
    df_vendas_corte['dia_venda'] = df_vendas_corte.index.date
    venda_dia = df_vendas_corte.groupby('dia_venda')['preco'].sum()
    venda_dia.name = 'Valor Venda'

    fig = px.line(venda_dia)
    col21.plotly_chart(fig)

    fig = px.pie(df_vendas_corte, names=analise_selecionada, values='preco')
    fig.update_traces(textinfo='label+percent')
    col22.plotly_chart(fig)

st.divider()
