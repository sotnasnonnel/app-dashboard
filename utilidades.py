from pathlib import Path
import streamlit as st
import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import git
import os

COMISSAO = 0.08

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, repo_dir, file_path):
        self.repo_dir = repo_dir
        self.file_path = file_path
        self.repo = git.Repo(repo_dir)

    def on_modified(self, event):
        if event.src_path.endswith(self.file_path):
            print(f"{self.file_path} has been modified")
            self.repo.git.add(self.file_path)
            self.repo.index.commit(f"Update {self.file_path}")
            self.repo.git.push()

def monitor_file(repo_dir, file_path):
    event_handler = ChangeHandler(repo_dir, file_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def leitura_de_dados():
    if not 'dados' in st.session_state:
        pasta_tabelas = Path(__file__).parents[0] / 'dados'
        # st.write(str(pasta_tabelas))

        df_vendas = pd.read_excel(pasta_tabelas / 'vendas.xlsx', index_col=0, parse_dates=True)
        df_filiais = pd.read_excel(pasta_tabelas / 'filiais.xlsx', index_col=0, parse_dates=True)
        df_produtos = pd.read_excel(pasta_tabelas / 'produtos.xlsx', index_col=0, parse_dates=True)
        dados = {'df_vendas': df_vendas,
                 'df_filiais': df_filiais,
                 'df_produtos': df_produtos}
        st.session_state['caminho_datasets'] = pasta_tabelas
        st.session_state['dados'] = dados

if __name__ == "__main__":
    repo_dir = '/path/to/your/repo'
    file_path = 'path/to/your/excel/file.xlsx'
    monitor_file(repo_dir, file_path)
    leitura_de_dados()
    st.write("Monitoring file and reading data")
