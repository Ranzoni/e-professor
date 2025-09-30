import tkinter as tk
from tkinter import scrolledtext, ttk


class InterfaceChat():
    def __init__(self, waiting_message, action_button):
        self.__waiting_message = waiting_message

        self.__answer_started = False

        self.__bot_idx = 0
        self.__user_idx = 0

        self.__bot_type = 'bot'
        self.__user_type = 'user'

        self.__root = tk.Tk()
        self.__root.title('E-Professor - Chatbot Acadêmico')
        self.__root.geometry('600x500')
        self.__root.configure(bg='#f5f5f5')

        frame_chat = tk.Frame(self.__root, bg='#f5f5f5')
        frame_chat.pack(padx=10, pady=10, fill='both', expand=True)

        self.__chatbox = scrolledtext.ScrolledText(
            frame_chat,
            wrap=tk.WORD,
            state='disabled',
            font=('Arial', 11),
            bg='white',
            fg='black',
            relief='flat'
        )
        self.__chatbox.pack(fill='both', expand=True)

        frame_input = tk.Frame(self.__root, bg='#f5f5f5')
        frame_input.pack(fill='x', padx=10, pady=10)

        self._input = ttk.Entry(frame_input, font=('Arial', 11))
        self._input.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self._input.bind('<Return>', lambda event: action_button(self))

        self.__send_button = ttk.Button(frame_input, text='Enviar', command=lambda: action_button(self))
        self.__send_button.pack(side='right')

        footer = tk.Label(self.__root, text='E-Professor © 2025 | Seu guia acadêmico virtual',
                    bg='#f5f5f5', fg='gray', font=('Arial', 9))
        footer.pack(side='bottom', pady=5)

    def __is_user_tag(self, type: str):
        return type == self.__user_type

    def __get_tag_idx(self, type: str):
        if self.__is_user_tag(type):
            return self.__user_type + str(self.__user_idx)
        else:
            return self.__bot_type + str(self.__bot_idx)

    def __get_next_tag_idx(self, type: str):
        if self.__is_user_tag(type):
            self.__user_idx += 1
        else:
            self.__bot_idx += 1
        
        return self.__get_tag_idx(type)

    def __remove_last_tag_idx(self, type: str):
        if self.__is_user_tag(type):
            if self.__user_idx > 0:
                self.__user_idx -= 1
        else:
            if self.__bot_idx > 0:
                self.__bot_idx -= 1

    def __add_message(self, message, type: str):
        self.__chatbox.insert(tk.END, message, self.__get_next_tag_idx(type))
        self.__chatbox.yview(tk.END)

    def __add_same_message(self, message, type: str):
        self.__chatbox.insert(tk.END, message, self.__get_tag_idx(type))
        self.__chatbox.yview(tk.END)

    def __remove_last_message(self, type: str):
        ranges = self.__chatbox.tag_ranges(self.__get_tag_idx(type))
        if ranges:
            start, end = ranges[0], ranges[-1]
            self.__chatbox.delete(start, end)

        self.__remove_last_tag_idx(type)

    def start_chat(self):
        self.__chatbox.config(state='normal')
        self.__send_button.config(state='disabled')

    def finish_chat(self):
        self.__chatbox.config(state='disabled')
        self.__send_button.config(state='enabled')

    def write_user_message(self):
        self.__answer_started = False
        message = self._input.get()
        if message.strip() != '':
            self.__add_message(f'Você: {message}\n\n', self.__user_type)
            self._input.delete(0, tk.END)

        return message
        
    def set_bot_as_thinking(self):
        self.__add_message(f'E-Professor: {self.__waiting_message}', self.__bot_type)

    def write_bot_message(self, bot_answer):
        if not self.__answer_started:
            self.__remove_last_message(self.__bot_type)
            self.__answer_started = True
            self.__add_message('E-Professor: ', self.__bot_type)

        self.__add_same_message(bot_answer, self.__bot_type)

    def finish_chat_bot_message(self):
        self.__add_same_message('\n\n', self.__bot_type)

    def run(self):
        self.__root.mainloop()
        