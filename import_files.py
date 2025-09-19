import os
from file_reader import read
import datetime
from repository import RepoConnection
from brain import embedding


def __register_log(text):
    print(f'{text}: {datetime.datetime.now()}')

def import_new_files():
    __register_log('Importação de arquivos iniciada')

    folder = 'files'

    if os.path.exists(folder):
        __register_log('Listando os arquivos')
        files = os.listdir(folder)

        for file in files:
            __register_log(f'Checando o arquivo {file}')

            repository = RepoConnection()
            repository.connect()
            
            if repository.file_exists(file):
                __register_log('Arquivo já importado')
                continue

            __register_log('Incorporando o arquivo...')
            try:
                file_id = repository.save_file(file)
                for chunk, percent in read(f'{folder}/{file}'):
                    content_embedded = embedding(chunk)
                    repository.save_embedding(content_embedded, chunk, file_id)
                    __register_log(f'Incorporação em {percent}%')

                repository.commit()
            except Exception as e:
                __register_log(f"Falha na incorporação: {e}")
                repository.rollback()

            del repository

    __register_log('Importação de arquivos finalizada')

if __name__ == "__main__":
    import_new_files()