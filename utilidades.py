from pathlib import Path

import streamlit as st
import pandas as pd

COMISSAO = 0.08

def leitura_de_dados():
    if not 'dados' in st.session_state:
        pasta_tabelas = Path(__file__).parents[0]/ 'dados'
        #st.write(str(pasta_tabelas))

        df_vendas = pd.read_excel(pasta_tabelas / 'vendas.xlsx', index_col=0, parse_dates=True)
        df_filiais = pd.read_excel(pasta_tabelas / 'filiais.xlsx', index_col=0, parse_dates=True)
        df_produtos = pd.read_excel(pasta_tabelas / 'produtos.xlsx', index_col=0, parse_dates=True)
        dados = {'df_vendas': df_vendas,
                'df_filiais': df_filiais,
                'df_produtos': df_produtos}
        st.session_state['caminho_datasets'] = pasta_tabelas
        st.session_state['dados']= dados

