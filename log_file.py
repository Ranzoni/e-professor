from datetime import datetime


class LogFile():
    def __init__(self, file_name: str = None):
        self.__has_content = False
        self.__file_name = 'logs/'
        self.__file_name += file_name if file_name else f'{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt'

    def register_log(self, content: str, topic: str = None):

        with open(self.__file_name, 'a', encoding='utf-8') as f:
            if self.__has_content:
                f.write('\n\n')
            else:
                self.__has_content = True

            if topic:
                f.write(f'[{topic}] \n\n')

            f.write(f'{datetime.now()} - {content}')

    def register_log_same_line(self, content: str):
        with open(self.__file_name, 'a', encoding='utf-8') as f:
            f.write(content)