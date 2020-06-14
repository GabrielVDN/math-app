import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as font
from frames import Practice, Settings
from random import randint
import os
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

# Get parent of current directory.
BASE_DIR = os.path.dirname(__file__)
# Change to the parent
os.chdir(BASE_DIR)

# Set variables of HEX-colors.
# Light grey
LIGHT_BACKGROUND_COLOR = "#e3e3e3"
# Dark grey
DARK_BACKGROUND_COLOR = "#b0b0b0"
# Active buttons
ACTIVE_BUTTON = "#7a7a7a"
# Black
DARK_TEXT_COLOR = "#000000"

# Create a Tkinter widget.
class MathPracticeTool(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the style to 'clam'.
        style = ttk.Style()
        style.theme_use("clam")
        # Create some custom styles.
        style.configure("Background.TFrame", background=LIGHT_BACKGROUND_COLOR)
        style.configure(
            "Buttons.TButton",
            font="Courier 10",
            background=DARK_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
            bordercolor="black",
            relief="solid"
        )

        style.map(
            "Buttons.TButton",
            background=[("active", ACTIVE_BUTTON), ("pressed", DARK_TEXT_COLOR)]
        )

        style.configure(
            "Submit.TButton",
            background=DARK_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
            bordercolor="black",
            relief="solid"
        )

        style.map(
            "Submit.TButton",
            background=[("active", ACTIVE_BUTTON), ("pressed", DARK_TEXT_COLOR)],
            font=[("pressed", ("TkDefaultFont", 18))]
        )

        style.configure(
            "Timer.TLabel",
            font="TkDefaultFont 18",
            background=LIGHT_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
        )

        style.configure(
            "PracticeNrSym.TLabel",
            font="TkDefaultFont 22",
            background=LIGHT_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
        )
        
        style.configure(
            "SettingsText.TLabel",
            font="TkDefaultFont 12",
            background=LIGHT_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
        )

        style.configure(
            "CorrectText.TLabel",
            font="TkDefaultFont 12",
            background=DARK_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
        )

        style.configure(
            "Symbols.TRadiobutton",
            font="TkDefaultFont 8",
            background=LIGHT_BACKGROUND_COLOR,
            foreground=DARK_TEXT_COLOR,
        )

        style.configure(
            "TProgressbar",
            background='green',
            troughcolor=DARK_BACKGROUND_COLOR
        )

        # Set the overall fontsize to 15 instead of 10.
        font.nametofont("TkDefaultFont").configure(size=15)
  
        container = ttk.Frame(self)
        container.grid()
        # Set the widget's background.
        self["background"] = LIGHT_BACKGROUND_COLOR
        # Center your Frame in the middele-top
        self.title("Math Practice Tool")
        self.columnconfigure(0, weight=1)
        # Give the widget a default size.
        self.geometry("560x313")
        
        # Create the countdown.
        self.current_time = tk.StringVar(value="02:00")
        self.timer_running = False

        # Set the default input values for the time.
        self.minutes_input_value = tk.StringVar(value=2)
        self.seconds_input_value = tk.StringVar(value=0)
        # In 'chosen_symbol_index' you'll store the value of the selected Radiobutton.
        self.chosen_symbol_index = tk.IntVar()
        # Stringsvar to store the chosen symbol with '+' as default.
        self.chosen_symbol = tk.StringVar(value="+")
        # Create the 2 Stringsvars, so that a string can be inputed 
        # and a messagebox can popuped, for the range of numbers with a default.
        self.input_from_value = tk.StringVar(value="1")
        self.input_to_value = tk.StringVar(value="101")
        # Create the the IntVars for the number of questions with a default.
        self.number_questions_input = tk.IntVar(value=10)
        # Create the the IntVars that tracks the number of questions answerd.
        self.number_questions_input_value = tk.IntVar()
        self.number_questions_input_value.set(self.number_questions_input.get())
        # Create all needed IntVar's and StringVar's.
        self.first_nr_value = tk.IntVar()
        self.second_nr_value = tk.IntVar()
        # Create the StringVar that will hold the users answer input.
        self.input_value = tk.StringVar()
        # Create a var that tracks the progress bar.
        self.pro_bar = tk.IntVar(value=0)
        self.max_progressbar = tk.IntVar()
        # Create a variable let's know if there are no errors.
        self.no_errors = True

        self.frames = {}

        settings_frame = Settings(
            container, self, lambda: self.show_frame(Practice)
        )
        practice_frame = Practice(
            container, self, lambda: self.show_frame(Settings)
        )
        settings_frame.grid(row=0, column=0, sticky="NESW")
        practice_frame.grid(row=0, column=0, sticky="NESW")

        self.frames[Settings] = settings_frame
        self.frames[Practice] = practice_frame
        
        self.show_frame(Practice)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.number_questions_input_value.set(self.number_questions_input.get())
        try:
            self.no_errors = True
            self.stop_timer()
            minutes_time = int(self.minutes_input_value.get())
            seconds_time = int(self.seconds_input_value.get())
            if seconds_time > 59:
                minutes_time += seconds_time//60
                seconds_time = seconds_time%60
            self.current_time.set(f"{minutes_time:02d}:{seconds_time:02d}")
        except ValueError:
            self.no_errors = False
            messagebox.showerror(
                title='Invalid Input', message='Invalid time input!'
            )
    
    def decrement_time(self):
        current_time = self.current_time.get()

        if self.timer_running and current_time != "00:00":            
            minutes, seconds = current_time.split(":")

            if int(seconds) > 0:
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else:
                seconds = 59
                minutes = int(minutes) - 1

            self.current_time.set(f"{minutes:02d}:{seconds:02d}")
            self._timer_decrement_job = self.after(1000, self.decrement_time)
        elif self.timer_running and current_time == "00:00":
            print("You ran out of time!")
            self.reset_timer()

    
    def get_selected_symbol(self):
        symbols = ["+", "-", "x", "÷"]
        self.chosen_symbol.set(symbols[self.chosen_symbol_index.get()])

    def get_number_questions(self):
        try:
            # Only generate numbers if the input is a number.
            int(self.input_value.get())
            if self.number_questions_input_value.get() != 1:
                self.number_questions_input_value.set(
                    self.number_questions_input_value.get() - 1
                )
                self.generate_numbers()
            else:
                print("Exerrcise done, you crushed it!")
                self.number_questions_input_value.set(
                    self.number_questions_input.get()
                )
                self.reset_timer()
        except ValueError:
            pass
        
    def generate_numbers(self):
        if self.chosen_symbol_index.get() == 3:
            try:
                self.no_errors = True
                # Generate 2 random values.
                self.second_nr_value.set(
                    randint(int(self.input_from_value.get()),
                        int(self.input_to_value.get()))
                    )
                self.first_nr_value.set(
                    randint(1, 15) * self.second_nr_value.get()
                    )
            except ValueError:
                self.no_errors = False
                messagebox.showerror(
                    title='Invalid Input', message='Invalid number range input!'
                )
        else:
            try:
                self.no_errors = True
                # Generate 2 random values.
                self.first_nr_value.set(
                    randint(int(self.input_from_value.get()),
                        int(self.input_to_value.get()))
                    )
                self.second_nr_value.set(
                    randint(int(self.input_from_value.get()),
                        int(self.input_to_value.get()))
                    )
            except ValueError:
                self.no_errors = False
                messagebox.showerror(
                    title='Invalid Input', message='Invalid number range input!'
                )


app = MathPracticeTool()
app.iconbitmap('math_icon.ico')
app.mainloop()
