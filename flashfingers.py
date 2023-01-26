'''
Justin Farnsworth
Flashfingers
October 24, 2020

This program allows users to improve their typing speed. The user will be given
four difficulties to choose from. Once a difficulty has been chosen, the user
must type out the text on the screen as fast and accurately as possible. As the
difficulty increases, the text to copy increases in length and a wider range of
characters are more likely to appear. Once the string has been typed out, the user
can press Enter on the keyboard, where the results will be computed.The results
will show the user the time taken to type out the text as well as the accuracy.
The user is free to do as many sessions as desired.
'''


# Imported modules
from random import choices
from statistics import mean
from itertools import chain, zip_longest
from time import time
import tkinter as tk


# Constants
WHITE = "#ffffff"
BLACK = "#000000"
GREEN = "#00ff00"
YELLOW = "#ffff00"
ORANGE = "#ff7000"
RED = "#ff0000"


# Flashfingers class
class Flashfingers(object):
    # Constructor
    def __init__(self):
        # Initialize and configure the window
        self.__window = tk.Tk()
        self.__window.config(bg=BLACK)
        self.__window.title("Flashfingers")
        self.__window.geometry("800x600")
        self.__window.resizable(width=False, height=False)

        # Generate the font and sizes
        self.__font_style = "Fixedsys"
        self.__small_font = (self.__font_style, 20)
        self.__large_font = (self.__font_style, 40)
        self.__title_font = (self.__font_style, 80)

        # Time variables
        self.__start_time = None
        self.__end_time = None

        # Title label
        self.__string_label = tk.Label(
            self.__window,
            text="FL@5HF1NG3R$",
            font=self.__title_font,
            bg=BLACK,
            fg=WHITE
        )
        self.__string_label.place(relx=0.5, y=60, anchor=tk.CENTER)

        # String label
        self.__string_label = tk.Label(
            self.__window,
            text="Select any difficulty!",
            font=self.__large_font,
            bg=BLACK,
            fg=WHITE
        )
        self.__string_label.place(relx=0.5, y=200, anchor=tk.CENTER)

        # String input field
        self.__string_input = tk.StringVar()
        self.__string_entered = tk.Entry(
            self.__window,
            textvariable=self.__string_input,
            font=self.__large_font,
            bg=BLACK,
            fg=WHITE,
            justify="center"
        )
        self.__string_entered.place(relx=0.5, y=300, width=700, height=80, anchor=tk.CENTER)
        self.__string_entered.bind("<Return>", self.__compute_results)
        self.__string_entered.focus()

        # Info label
        self.__info_label = tk.Label(
            self.__window,
            text="Press ENTER after typing the text above.",
            font=self.__small_font,
            bg=BLACK,
            fg=WHITE
        )

        # Time label
        self.__time_label = tk.Label(
            self.__window,
            font=self.__large_font,
            bg=BLACK,
            fg=WHITE
        )

        # Accuracy label
        self.__accuracy_label = tk.Label(
            self.__window,
            font=self.__large_font,
            bg=BLACK,
            fg=WHITE
        )

        # Easy Button
        self.__easy_button = tk.Button(
            self.__window,
            text="Easy",
            command=lambda: self.__new_session("easy"),
            font=self.__small_font,
            bg=GREEN,
            activebackground=GREEN
        )
        self.__easy_button.place(x=125, y=475, width=150, anchor=tk.CENTER)

        # Medium Button
        self.__medium_button = tk.Button(
            self.__window,
            text="Medium",
            command=lambda: self.__new_session("medium"),
            font=self.__small_font,
            bg=YELLOW,
            activebackground=YELLOW
        )
        self.__medium_button.place(x=308, y=475, width=150, anchor=tk.CENTER)

        # Hard Button
        self.__hard_button = tk.Button(
            self.__window,
            text="Hard",
            command=lambda: self.__new_session("hard"),
            font=self.__small_font,
            bg=ORANGE,
            activebackground=ORANGE
        )
        self.__hard_button.place(x=492, y=475, width=150, anchor=tk.CENTER)

        # Expert Button
        self.__expert_button = tk.Button(
            self.__window,
            text="Expert",
            command=lambda: self.__new_session("expert"),
            font=self.__small_font,
            bg=RED,
            activebackground=RED
        )
        self.__expert_button.place(x=675, y=475, width=150, anchor=tk.CENTER)

        # Reset Button
        self.__reset_button = tk.Button(
            self.__window,
            text="Reset",
            command=self.__reset,
            font=self.__small_font,
            bg=WHITE,
            activebackground=WHITE
        )
        self.__reset_button.place(relx=0.5, y=550, width=700, anchor=tk.CENTER)

    # Run the window loop
    def run(self):
        # Run the tkinter loop
        self.__window.mainloop()

    # Generate a random string based on the difficulty.
    # The greater the difficulty, the longer the string
    # and the more characters are potentially used.
    @staticmethod
    def __generate_random_string(difficulty="medium"):
        # Filter candidate characters based on the difficulty
        if difficulty == "easy":
            # Digits only
            valid_chars = ''.join(chr(i) for i in range(48, 58))
            string_length = 6
        elif difficulty == "medium":
            # Digits and lowercase letters
            valid_chars = ''.join(chr(i) for i in chain(range(48, 58), range(97, 123)))
            string_length = 10
        elif difficulty == "hard":
            # Digits, lowercase letters, and uppercase letters
            valid_chars = ''.join(
                chr(i) for i in chain(range(48, 58), range(65, 91), range(97, 123))
            )
            string_length = 15
        elif difficulty == "expert":
            # Keyboard characters
            valid_chars = ''.join(chr(i) for i in range(33, 127))
            string_length = 20

        # Build and return the string using random valid characters
        return ''.join(choices(valid_chars, k=string_length))

    # Generate a new string and set up the session
    def __new_session(self, difficulty):
        # Clear the contents in the box
        self.__string_entered.delete(0, "end")

        # Generate a random string based on the difficulty
        self.__string_label.config(text=self.__generate_random_string(difficulty))

        # Reset results variables
        self.__time_label.config(text="", fg=WHITE)
        self.__accuracy_label.config(text="", fg=WHITE)
        self.__end_time = None

        # Display the info label
        self.__info_label.place(relx=0.5, y=375, anchor=tk.CENTER)

        # Hide the time and accuracy labels
        self.__time_label.place_forget()
        self.__accuracy_label.place_forget()

        # Automatically select the box so the user can insert input without clicking it
        self.__string_entered.focus()

        # Start timer
        self.__start_time = time()

    # Display the results underneath the input box
    def __compute_results(self, event):
        # Only show the results if the user is in a session and doesn't have an end time
        if self.__start_time and not self.__end_time:
            # Record the end time
            self.__end_time = time()

            # Get the generated string and the input string
            input_string = self.__string_input.get()
            label_string = self.__string_label["text"]

            # Display the total amount of time elapsed
            time_elapsed = round(
                self.__end_time - self.__start_time,
                ndigits=2
            )
            self.__time_label.config(text=f"{time_elapsed}s")

            # Change the time text color, depending on the time
            if time_elapsed <= (0.5 * len(label_string)) + 2:
                self.__time_label.config(fg=YELLOW)
            elif time_elapsed > 1.5 * len(label_string):
                self.__time_label.config(fg=RED)

            # Compute and display the accuracy
            accuracy = round(
                100 * mean(i == j for i, j in zip_longest(input_string, label_string)),
                ndigits=1
            )
            self.__accuracy_label.config(text=f"{accuracy}%")

            # Change the accuracy text color, depending on the score
            if accuracy == 100:
                self.__accuracy_label.config(fg=YELLOW)
            elif accuracy < 70:
                self.__accuracy_label.config(fg=RED)

            # Hide the info label
            self.__info_label.place_forget()

            # Display the time and accuracy labels
            self.__time_label.place(x=50, y=375, anchor=tk.W)
            self.__accuracy_label.place(x=750, y=375, anchor=tk.E)

    # Reset the program to default settings
    def __reset(self):
        # Clear the contents in the box
        self.__string_entered.delete(0, "end")

        # Reset the labels, results, and time to their default values
        self.__string_label.config(text="Select any difficulty!")
        self.__time_label.config(text="", fg=WHITE)
        self.__accuracy_label.config(text="", fg=WHITE)
        self.__start_time = None
        self.__end_time = None

        # Hide the info, time, and accuracy labels
        self.__info_label.place_forget()
        self.__time_label.place_forget()
        self.__accuracy_label.place_forget()


# Execute the program
if __name__ == "__main__":
    app = Flashfingers()
    app.run()
