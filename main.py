import customtkinter as ctk
import random
import time


class SpeedTypingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.resizable(False, False)
        self.title("Speed Typing App")

        self.label_sentence = ctk.CTkLabel(master=self, text="Sentence will be displayed here", width=900, height=75,
                                           fg_color="deeppink", justify="center", font=("New York", 20), wraplength=800,
                                           text_color="#4D4D4D")
        self.label_sentence.pack(padx=10, pady=10)

        self.text_input = ctk.CTkTextbox(master=self)
        self.text_input.pack(padx=50, pady=15, expand=True, fill=ctk.BOTH)
        self.text_input.bind("<Key>", self.check_text_input)

        self.button = ctk.CTkButton(master=self, text="START",
                                    command=self.random_sentence)
        self.button.pack(padx=10, pady=10)

        self.label_result = ctk.CTkLabel(master=self, text="")
        self.label_result.pack(padx=50, pady=10, expand=True, fill=ctk.BOTH)

        self.start = time.time()
        self.correct_char = 0
        self.current_index = 0
        self.previous_text = ""

    def random_sentence(self):
        with open("sentences.txt") as file:
            sentences = file.readlines()
            sentence = random.choice(sentences)

        self.label_sentence.configure(text=sentence)

    def backspace_key(self):
        if self.current_index >= 0:
            self.current_index -= 1

    def check_text_input(self, event):
        self.update_previous_text()
        user_text = self.text_input.get("0.0", "end").rstrip()

        # need to add checking if the text wasn't removed (letter or all of it)
        # if yes -> then current_index changes AND correct_char probably too (it depends on whether the correct or incorrect characters were removed)

        if user_text:
            if self.current_index < len(self.label_sentence.cget("text")):
                print(f"User: {user_text[-1]}")
                print(f"Sentence: {self.label_sentence.cget("text")[self.current_index]}")
                print(self.current_index)
                if user_text[-1] == self.label_sentence.cget("text")[self.current_index]:
                    self.correct_char += 1
                self.current_index += 1

    def update_previous_text(self):
        self.previous_text = self.text_input.get("0.0", "end").rstrip()












if __name__ == "__main__":
    app = SpeedTypingApp()
    app.mainloop()
