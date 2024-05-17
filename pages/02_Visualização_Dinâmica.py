from pathlib import Path

import streamlit as st
import pandas as pd

from utilidades import leitura_de_dados, COMISSAO

colunas_analise = ['filial', 'vendedor', 'produto', 'cliente_genero', 'forma_pagamento']
colunas_valor = ['preco', 'comissao']
funcoes_agg = {'soma': 'sum', 'contagem': 'count'}


leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']


df_produtos = df_produtos.rename(columns= {'nome': 'produto'})
df_vendas = df_vendas.reset_index()

df_vendas = pd.merge(left=df_vendas,
                     right=df_produtos[['produto', 'preco']],
                     on='produto',
                     how='left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * COMISSAO


indices_selecionados = st.sidebar.multiselect('Selecione os Índices',
                                              colunas_analise)
col_analises_exc = [c for c in colunas_analise if not  c in indices_selecionados]

colunas_selecionadas = st.sidebar.multiselect('Selecione as Colunas',
                                              col_analises_exc)

analise_selecionada = st.sidebar.selectbox('Selecione o valor da análise:',
                                           colunas_valor)

metrica_selecionada = st.sidebar.selectbox('Selecione a métrica:',
                                           funcoes_agg.keys())

if len(indices_selecionados) > 0 and len(colunas_selecionadas) > 0:
    metrica_selecionada = funcoes_agg[metrica_selecionada]
    vendas_pivotadas = pd.pivot_table(df_vendas, index = indices_selecionados, 
                                      columns= colunas_selecionadas,
                                      values= analise_selecionada,
                                      aggfunc=metrica_selecionada)
    vendas_pivotadas['TOTAL GERAL'] = vendas_pivotadas.sum(axis=1)
    vendas_pivotadas.loc['TOTAL GERAL'] = vendas_pivotadas.sum(axis = 0 ).to_list()
    st.dataframe(vendas_pivotadas)

