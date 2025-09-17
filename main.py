# import asyncio
from brain import embedding, ask
from repository import RepoConnection
import os
from file_reader import read
import schedule
import time
import datetime
from interface import InterfaceChat
import threading


def import_new_files():
    def register_log(text):
        print(f'{text}: {datetime.datetime.now()}')

    register_log('Importação de arquivos iniciada')

    folder = 'files'

    if os.path.exists(folder):
        register_log('Listando os arquivos')
        files = os.listdir(folder)

        for file in files:
            register_log(f'Checando o arquivo {file}')

            repository = RepoConnection()
            repository.connect()
            
            if repository.file_exists(file):
                register_log('Arquivo já importado')
                continue

            register_log('Incorporando o arquivo...')
            try:
                file_id = repository.save_file(file)
                for chunk, percent in read(f'{folder}/{file}'):
                    content_embedded = embedding(chunk)
                    repository.save_embedding(content_embedded, chunk, file_id)
                    register_log(f'Incorporação em {percent}%')

                repository.commit()
            except Exception as e:
                register_log(f"Falha na incorporação: {e}")
                repository.rollback()

            del repository

    register_log('Importação de arquivos finalizada')

def ask_professor(interface: InterfaceChat):
    question = interface.write_user_message()

    def process_in_background():
        try:
            question_embedded = embedding(question)
            
            repository = RepoConnection()
            repository.connect()
            chunks = repository.get_relevants_contents(question_embedded)
            repository.disconnect()

            if len(chunks) == 0:
                interface.write_bot_message('Desculpe, mas eu não tenho conhecimento sobre este assunto.')
            else:
                content_to_learn = "\n".join(chunks)
                ask_iterator = ask(
                    question=question,
                    knowledge=content_to_learn
                )

                for answer_chunk in ask_iterator:
                    interface.write_bot_message(answer_chunk)
                    
        except Exception as e:
            print(f'Erro: {str(e)}')
            interface.write_bot_message('Não conseugi processar a sua resposta')
    
    # Iniciar thread em background
    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()

# def main():
    # while True:
    #     print('Faça uma pergunta ao professor:')
    #     question = input()
    #     question_embedded = embedding(question)
        
    #     repository = RepoConnection()
    #     repository.connect()
    #     chunks = repository.get_relevants_contents(question_embedded)
    #     repository.disconnect()

    #     if len(chunks) == 0:
    #         print('Desculpe, mas eu não tenho conhecimento sobre este assunto.')
    #     else:
    #         content_to_learn = "\n".join(chunks)
    #         ask_iterator = ask(
    #             question=question,
    #             knowledge=content_to_learn
    #         )

    #         async for answer_cunk in ask_iterator:
    #             print(answer_cunk, end="", flush=True)

    #     print()
    #     print('Deseja continuar?')
    #     another_question = input() == '0'
    #     if not another_question:
    #         break

    #     os.system('cls')

def teste(interface: InterfaceChat):
    question = interface.write_user_message()
    print(question)

    def process_in_background():
        for chunk in 'teste de mensagem de resposta do e-professor...':
            interface.write_bot_message(chunk)
            time.sleep(.1)

    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    interface = InterfaceChat(action_button=teste)
    interface.run()

    # schedule.every(5).seconds.do(import_new_files)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
