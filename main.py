import customtkinter as ctk
import random
import time
import os.path

ctk.set_appearance_mode("dark")


class SpeedTypingApp(ctk.CTk):
    """
    A simple speed typing application.

    This application presents the user with a random sentence sourced from a file
    and assesses their typing accuracy and speed.
    """

    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.resizable(False, False)
        self.title("Speed Typing App")

        # create and configure widgets
        self.label_sentence = ctk.CTkLabel(master=self, text="Sentence will be displayed here", width=900, height=150,
                                           justify="center", font=("Consolas", 35), wraplength=900)
        self.label_sentence.pack(padx=10)

        self.text_input = ctk.CTkTextbox(master=self, font=("Consolas", 30), height=150, wrap="word")
        self.text_input.pack(padx=50, expand=True, fill=ctk.BOTH)

        self.button = ctk.CTkButton(master=self, text="START", command=self.start_test, font=("Consolas", 15, "bold"))
        self.button.pack(padx=10, pady=30)

        self.label_result = ctk.CTkLabel(master=self, text="", font=("Ink Free", 35, "bold"))
        self.label_result.pack(padx=50, pady=10, expand=True, fill=ctk.BOTH)

        # Initialize variables
        self.start = None  # Variable to store start time of the test (used in check_text_input and calculate_wpm)
        self.correct_char = 0  # Variable to store number of correctly typed characters (used in check_text_input and calculate_accuracy)
        self.sentence_text = None  # Variable to store the displayed sentence (used in start_test)
        self.user_input = ""  # Variable to store user's input (used in check_text_input)

        self.text_input.configure(state="disabled")

    def random_sentence(self):
        """Select a random sentence from a file."""

        if os.path.exists("sentences.txt"):
            with open("sentences.txt") as file:
                sentences = [line.strip() for line in file if line.strip()]
                if sentences:
                    self.sentence_text = random.choice(sentences)

    def start_test(self):
        """Start the typing test."""

        self.text_input.configure(state="normal")
        self.text_input.bind("<Key>", self.check_text_input)
        self.button.configure(text="Another sentence")
        self.start = time.time()
        self.random_sentence()
        self.label_sentence.configure(text=self.sentence_text)
        self.text_input.delete("1.0", ctk.END)

    def check_text_input(self, event):
        """Check user's input."""

        self.user_input = self.text_input.get("0.0", "end").strip()
        self.correct_char = 0

        # Iterate over the range of the minimum length of user_input and sentence_text
        for i in range(min(len(self.user_input), len(self.sentence_text))):
            # Check if the character in user_input matches the corresponding character in sentence_text
            if self.user_input[i] == self.label_sentence.cget("text")[i]:
                self.correct_char += 1

        self.label_result.configure(text=f"Accuracy: {self.calculate_accuracy():.2f}%")

        # If user has typed the entire sentence
        if len(self.user_input) == len(self.sentence_text):
            self.text_input.configure(state="disabled")
            self.label_result.configure(text=f"Congrats! Your results are:"
                                             f"\nAccuracy: {self.calculate_accuracy():.2f}%, WPM: {self.calculate_wpm():.2f}")
            self.text_input.unbind("<Key>")  # Unbind the key event handler

    def calculate_accuracy(self):
        """Calculate typing accuracy."""

        # Ensure that a sentence is available for comparison
        if not self.sentence_text:
            return 0
        accuracy = (self.correct_char / len(self.sentence_text)) * 100
        return accuracy

    def calculate_wpm(self):
        """Calculate words per minute (WPM)."""

        # Ensure that both start time and user input are available for calculation
        if not self.start or not self.user_input:
            return 0
        user_typing_time = time.time() - self.start  # Calculate time taken by the user to type the sentence
        wpm = ((len(self.user_input) / 5) / user_typing_time) * 60  # Calculate the words (any five characters) per minute
        return wpm


if __name__ == "__main__":
    app = SpeedTypingApp()
    app.mainloop()
