import streamlit as st  

# Adicione a função configure_page aqui
def configure_page():
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":bar_chart:")

# Chame a função configure_page imediatamente após defini-la
configure_page()

st.sidebar.markdown('Desenvolvido por Lennon')

st.markdown('# Bem-Vindo ao Analisador de vendas')

st.divider()

st.markdown(
    '''
        by: ***Lennon***.

    '''
)

