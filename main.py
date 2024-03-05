import customtkinter as ctk
import random
import time

ctk.set_appearance_mode("dark")


class SpeedTypingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.resizable(False, False)
        self.title("Speed Typing App")

        self.label_sentence = ctk.CTkLabel(master=self, text="Sentence will be displayed here", width=900, height=150,
                                           justify="center", font=("Consolas", 35), wraplength=900)
        self.label_sentence.pack(padx=10)

        self.text_input = ctk.CTkTextbox(master=self, font=("Consolas", 30), height=150)
        # self.text_input.xview_moveto(1)
        self.text_input.pack(padx=50, expand=True, fill=ctk.BOTH)

        self.button = ctk.CTkButton(master=self, text="START", command=self.start_test, font=("Consolas", 15, "bold"))
        self.button.pack(padx=10, pady=30)

        self.label_result = ctk.CTkLabel(master=self, text="", font=("Ink Free", 35, "bold"))
        self.label_result.pack(padx=50, pady=10, expand=True, fill=ctk.BOTH)

        self.start = None
        self.correct_char = 0
        self.sentence_text = None
        self.user_text = None

        self.text_input.configure(state="disabled")

    def random_sentence(self):
        with open("sentences.txt") as file:
            sentences = file.readlines()
            sentence = random.choice(sentences)

            self.sentence_text = sentence.strip()

    def start_test(self):
        self.text_input.configure(state="normal")
        self.text_input.bind("<Key>", self.check_text_input)
        self.button.configure(text="Another sentence")
        self.start = time.time()
        self.random_sentence()
        self.label_sentence.configure(text=self.sentence_text)
        self.text_input.delete("1.0", ctk.END)

    def check_text_input(self, event):
        self.user_text = self.text_input.get("0.0", "end").strip()
        self.correct_char = 0

        for i in range(min(len(self.user_text), len(self.sentence_text))):
            if self.user_text[i] == self.label_sentence.cget("text")[i]:
                self.correct_char += 1

        self.label_result.configure(text=f"Accuracy: {self.calculate_accuracy():.2f}%")

        if len(self.user_text) == len(self.sentence_text):
            self.text_input.configure(state="disabled")
            self.label_result.configure(
                text=f"Congrats! Your results are:\nAccuracy: {self.calculate_accuracy():.2f}%, WPM: {self.calculate_wpm():.2f}")
            self.text_input.unbind("<Key>")

    def calculate_accuracy(self):
        accuracy = (self.correct_char / len(self.sentence_text)) * 100
        return accuracy

    def calculate_wpm(self):
        user_typing_time = time.time() - self.start
        wpm = ((len(self.user_text) / 5) / user_typing_time) * 60
        return wpm


if __name__ == "__main__":
    app = SpeedTypingApp()
    app.mainloop()
