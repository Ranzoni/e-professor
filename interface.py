import tkinter as tk
from tkinter import scrolledtext, ttk


class InterfaceChat():
    def __init__(self, action_button):
        self.__root = tk.Tk()
        self.__root.title("E-Professor - Chatbot Acadêmico")
        self.__root.geometry("600x500")
        self.__root.configure(bg="#f5f5f5")

        frame_chat = tk.Frame(self.__root, bg="#f5f5f5")
        frame_chat.pack(padx=10, pady=10, fill="both", expand=True)

        self.__chatbox = scrolledtext.ScrolledText(
            frame_chat,
            wrap=tk.WORD,
            state="disabled",
            font=("Arial", 11),
            bg="white",
            fg="black",
            relief="flat"
        )
        self.__chatbox.pack(fill="both", expand=True)

        frame_input = tk.Frame(self.__root, bg="#f5f5f5")
        frame_input.pack(fill="x", padx=10, pady=10)

        self._input = ttk.Entry(frame_input, font=("Arial", 11))
        self._input.pack(side="left", fill="x", expand=True, padx=(0, 5))

        send_button = ttk.Button(frame_input, text="Enviar", command=lambda: action_button(self))
        send_button.pack(side="right")

        footer = tk.Label(self.__root, text="E-Professor © 2025 | Seu guia acadêmico virtual",
                    bg="#f5f5f5", fg="gray", font=("Arial", 9))
        footer.pack(side="bottom", pady=5)

    def write_user_message(self):
        message = self._input.get()
        if message.strip() != "":
            self.__chatbox.config(state="normal")
            self.__chatbox.insert(tk.END, "Você: " + message + "\n", "user")
            self.__chatbox.insert(tk.END, "\n", "bot")
            # self.__chatbox.insert(tk.END, "E-Professor: " + "Um minuto, estou pensando..." + "\n\n", "bot")
            self.__chatbox.insert(tk.END, "E-Professor: ", "bot")
            self.__chatbox.mark_set("bot_response_start", self.__chatbox.index(tk.END+"-1c"))
            # self.__chatbox.insert(tk.END, "\n\n", "bot")
            self.__chatbox.config(state="disabled")
            self.__chatbox.yview(tk.END)
            self._input.delete(0, tk.END)

            self.write_bot_message("Um minuto, estou pensando...")

            return message

    def write_bot_message(self, bot_answer):
        self.__chatbox.config(state="normal")

        start_answer = self.__chatbox.index("bot_response_start")
        end_answer = self.__chatbox.index("end-2c") 
        actual_answer = self.__chatbox.get(start_answer, end_answer)
        self.__chatbox.delete(start_answer, end_answer)
        self.__chatbox.insert(start_answer, actual_answer + bot_answer, "bot")

        self.__chatbox.config(state="disabled")
        self.__chatbox.yview(tk.END)

    def run(self):
        self.__root.mainloop()
        