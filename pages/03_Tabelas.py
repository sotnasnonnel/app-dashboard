from pathlib import Path

import streamlit as st
import pandas as pd


from utilidades import leitura_de_dados

leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

st.sidebar.markdown('## Seleção de Tabelas')
tabela_selecionada = st.sidebar.selectbox('Selecione a tabela que voce deseja ver:',
                    ['Vendas', 'Produtos' , 'Filiais'])


def mostra_tabela_produtos():
    st.dataframe(df_produtos)

def mostra_tabela_filiais():
    st.dataframe(df_filiais)

def mostra_tabela_vendas():
    st.sidebar.divider()
    st.sidebar.markdown('### Filtrar Tabela')
    colunas_selecioandas = st.sidebar.multiselect('Selecione as colunas da tabela:',
                                                  list(df_vendas.columns),
                                                  list(df_vendas.columns))
    
    col1, col2 = st.sidebar.columns(2)
    filtro_selecionado = col1.selectbox('Filtrar Coluna',
                                        list(df_vendas.columns))
    valores_unicos_coluna = (df_vendas[filtro_selecionado].unique())

    valor_filtro= col2.selectbox('Valor do Filtro',
                                 valores_unicos_coluna)
    
    filtrar = col1.button('Filtrar')
    limpar = col1.button('Limpar')

    if filtrar:
        st.dataframe(df_vendas.loc[df_vendas[filtro_selecionado] == valor_filtro, colunas_selecioandas])
    elif limpar:
        st.dataframe(df_vendas[colunas_selecioandas], height=800)
    else:
        st.dataframe(df_vendas[colunas_selecioandas], height=800)


if tabela_selecionada == 'Produtos':
    mostra_tabela_produtos()
elif tabela_selecionada == 'Filiais':
    mostra_tabela_filiais()
elif tabela_selecionada == 'Vendas':
    mostra_tabela_vendas()


