from brain import embedding, ask
from repository import RepoConnection
import time
from interface import InterfaceChat
import threading


def ask_professor(interface: InterfaceChat):
    interface.start_chat()
    
    question = interface.write_user_message()

    def process_in_background():
        try:
            time.sleep(.7)
            interface.set_bot_as_thinking()

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
            interface.write_bot_message('Não consegui processar a sua resposta.')

        interface.finish_chat_bot_message()
        interface.finish_chat()
    
    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    interface = InterfaceChat(action_button=ask_professor)
    interface.run()
