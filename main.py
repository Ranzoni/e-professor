from brain import embedding, ask, get_question_transformed
from repository import RepoConnection
import time
from interface import InterfaceChat
import threading
from log_file import LogFile


def ask_professor(interface: InterfaceChat):
    interface.start_chat()
    log_file = LogFile()
    
    question = interface.write_user_message()
    log_file.register_log(question, 'QUESTIONAMENTO DO USUÁRIO')

    def process_in_background():
        try:
            time.sleep(.7)
            interface.set_bot_as_thinking()

            question_transformed = get_question_transformed(question)
            log_file.register_log(question_transformed, 'PERGUNTA TRANSFORMADA PELO BOT')

            question_embedded = embedding(question_transformed)
            
            repository = RepoConnection()
            repository.connect()
            chunks = repository.get_relevants_contents(question_embedded)
            repository.disconnect()
            

            if len(chunks) == 0:
                interface.write_bot_message('Desculpe, mas eu não tenho conhecimento sobre este assunto.')
                log_file.register_log('Nenhum chunk encontrado.', 'CHUNKS ENCONTRADOS')
            else:
                content_to_learn = '\n'.join(chunks)
                log_file.register_log(content_to_learn, 'CHUNKS ENCONTRADOS')

                log_file.register_log('', 'RESPOSTA DO BOT')
                for answer_chunk in ask(question, content_to_learn):
                    interface.write_bot_message(answer_chunk)
                    log_file.register_log_same_line(answer_chunk)

        except Exception as e:
            print(f'Erro: {str(e)}')
            interface.write_bot_message('Não consegui processar a sua resposta.')

        interface.finish_chat_bot_message()
        interface.finish_chat()
    
    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    interface = InterfaceChat(
        waiting_message='Deixe-me pensar, só um instante...',
        action_button=ask_professor
    )
    interface.run()
