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
import tkinter as tk
from random import choice
from numpy import mean
from itertools import chain, zip_longest
from time import time


# Flashfingers class
class Flashfingers:
    # Constructor
    def __init__(self):
        # Initialize and configure the window
        self.__window = tk.Tk()
        self.__window.config(bg="#000000")
        self.__window.title("Flashfingers")
        self.__window.geometry("800x600")
        
        # Generate the font and sizes
        self.__font_style = "Fixedsys"
        self.__small_font = (self.__font_style, 20)
        self.__large_font = (self.__font_style, 40)
        self.__title_font = (self.__font_style, 80)

        # Time variables
        self.__start_time = None
        self.__end_time = None

        # Title label
        self.__stringLabel = tk.Label(
            self.__window, 
            text="FL@5HF1NG3R$", 
            font=self.__title_font,
            bg="#000000",
            fg="#ffffff"
        )
        self.__stringLabel.place(relx=0.5, y=60, anchor=tk.CENTER)

        # String label
        self.__stringLabel = tk.Label(
            self.__window, 
            text="Select any difficulty!", 
            font=self.__large_font,
            bg="#000000",
            fg="#ffffff"
        )
        self.__stringLabel.place(relx=0.5, y=200, anchor=tk.CENTER)

        # String input field
        self.__stringInput = tk.StringVar()
        self.__stringEntered = tk.Entry(
            self.__window, 
            textvariable=self.__stringInput, 
            font=self.__large_font,
            bg="#000000",
            fg="#ffffff"
        )
        self.__stringEntered.place(relx=0.5, y=300, width=700, height=80, anchor=tk.CENTER)
        self.__stringEntered.bind('<Return>', self.__compute_results)

        # Time elapsed label
        self.__timeElapsedLabel = tk.Label(
            self.__window,  
            font=self.__large_font,
            bg="#000000",
            fg="#ffffff"
        )
        self.__timeElapsedLabel.place(x=50, y=375, anchor=tk.W)

        # Accuracy label
        self.__accuracyLabel = tk.Label(
            self.__window,  
            font=self.__large_font,
            bg="#000000",
            fg="#ffffff"
        )
        self.__accuracyLabel.place(x=750, y=375, anchor=tk.E)

        # Easy Button
        self.__easy_button = tk.Button(
            self.__window, 
            text="Easy", 
            command=lambda: self.__new_session("easy"), 
            font=self.__small_font, 
            bg="#00ffff"
        )
        self.__easy_button.place(x=125, y=475, width=150, anchor=tk.CENTER)

        # Medium Button
        self.__medium_button = tk.Button(
            self.__window, 
            text="Medium", 
            command=lambda: self.__new_session("medium"), 
            font=self.__small_font, 
            bg="#00ff00"
        )
        self.__medium_button.place(x=308, y=475, width=150, anchor=tk.CENTER)

        # Hard Button
        self.__hard_button = tk.Button(
            self.__window, 
            text="Hard", 
            command=lambda: self.__new_session("hard"), 
            font=self.__small_font, 
            bg="#ffff00"
        )
        self.__hard_button.place(x=492, y=475, width=150, anchor=tk.CENTER)

        # Expert Button
        self.__expert_button = tk.Button(
            self.__window, 
            text="Expert", 
            command=lambda: self.__new_session("expert"), 
            font=self.__small_font, 
            bg="#ff0000"
        )
        self.__expert_button.place(x=675, y=475, width=150, anchor=tk.CENTER)

        # Reset Button
        self.__reset_button = tk.Button(
            self.__window, 
            text="Reset", 
            command=self.__reset, 
            font=self.__small_font, 
            bg="#ffffff",
        )
        self.__reset_button.place(relx=0.5, y=550, width=700, anchor=tk.CENTER)

        # Run the tkinter loop
        self.__window.mainloop()
    

    # Generate a random string based on the difficulty.
    # The greater the difficulty, the longer the string 
    # and the more characters are potentially used.
    def __generateRandomString(self, difficulty="medium"):
        # Filter candidate characters based on the difficulty
        if difficulty == "easy":
            # Digits only
            validChars = ''.join([chr(i) for i in range(48, 58)])
            stringLength = 6
        elif difficulty == "medium":
            # Digits and lowercase letters
            validChars = ''.join([chr(i) for i in chain(range(48, 58), range(97, 123))])
            stringLength = 10
        elif difficulty == "hard":
            # Digits, lowercase letters, and uppercase letters
            validChars = ''.join([chr(i) for i in chain(range(48, 58), range(65, 91), range(97, 123))])
            stringLength = 15
        elif difficulty == "expert":
            # Keyboard characters
            validChars = ''.join([chr(i) for i in range(33, 127)])
            stringLength = 20
        
        # Build and return the string using random valid characters
        return ''.join([choice(validChars) for i in range(stringLength)])
    

    # Generate a new string and set up the session
    def __new_session(self, difficulty):
        # Clear the contents in the box
        self.__stringEntered.delete(0, "end")

        # Generate a random string, based on the difficulty
        self.__stringLabel.config(text=self.__generateRandomString(difficulty))
        
        # Reset results variables
        self.__timeElapsedLabel.config(text="")
        self.__accuracyLabel.config(text="")
        self.__end_time = None

        # Start timer
        self.__start_time = time()
    

    # Display the results underneath the input box
    def __compute_results(self, event):
        # Only show the time if the user is in a session and doesn't have an end time
        if self.__stringLabel["text"] != "Select any difficulty!" and not self.__end_time:
            # Display the total amount of time elapsed
            self.__end_time = time()
            self.__timeElapsedLabel.config(
                text=f"{round(self.__end_time - self.__start_time, 2)}s"
            )
            
            # Display the accuracy
            input_string = self.__stringInput.get()
            label_string = self.__stringLabel["text"]
            self.__accuracyLabel.config(
                text=f"""{
                    round(
                        100 * mean([i == j for i, j in zip_longest(input_string, label_string)])
                    )
                }%"""
            )
    

    # Reset the program to default settings
    def __reset(self):
        # Clear the contents in the box
        self.__stringEntered.delete(0, "end")

        # Reset the labels, results, and time to their default values
        self.__stringLabel.config(text="Select any difficulty!")
        self.__timeElapsedLabel.config(text="")
        self.__accuracyLabel.config(text="")
        self.__start_time = None
        self.__end_time = None


# Execute the program
if __name__ == "__main__":
    Flashfingers()
