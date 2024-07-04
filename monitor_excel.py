import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import git
import os

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, repo_dir, file_paths):
        self.repo_dir = repo_dir
        self.file_paths = file_paths
        self.repo = git.Repo(repo_dir)

    def on_modified(self, event):
        if any(event.src_path.endswith(file_path) for file_path in self.file_paths):
            print(f"One of the monitored files has been modified")
            for file_path in self.file_paths:
                self.repo.git.add(file_path)
            self.repo.index.commit(f"Update monitored files")
            self.repo.git.push()

def monitor_files(repo_dir, file_paths):
    event_handler = ChangeHandler(repo_dir, file_paths)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_paths[0]), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    repo_dir = 'C:/Users/LennonSantos/Desktop/dashboard'  # Caminho para o repositório local
    file_paths = [
        'C:/Users/LennonSantos/Desktop/dashboard/dados/vendas.xlsx',
        'C:/Users/LennonSantos/Desktop/dashboard/dados/filiais.xlsx',
        'C:/Users/LennonSantos/Desktop/dashboard/dados/produtos.xlsx'
    ]
    monitor_files(repo_dir, file_paths)
