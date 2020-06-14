import tkinter as tk
from tkinter import ttk, messagebox
import winsound
import os
import time
import xlsxwriter


# Create a Tkinter themed widget.
class Practice(ttk.Frame):
    def __init__(self, parent, controller, show_settings):
        super().__init__(parent)
        
        self.controller = controller

        self.exercises = []

        # Set the frame's background.
        self["style"] = "Background.TFrame"

        # Set initail number values.
        controller.generate_numbers()

        # list of calc funcs
        self.calc_funcs = [
            self.add, self.substract, self.multiplicate, self.divide
        ]
        self.calced_value = tk.IntVar()

        # This button start the countdown.
        start_timer_button = ttk.Button(
            self, text="start ▶️", width=8,
            cursor="hand2",
            command=lambda:[self.start_timer(), self.reset_progressbar()],
            style="Buttons.TButton"
        )
        start_timer_button.grid(row=0, columnspan=2, sticky="W")

        export_button = ttk.Button(
            self, text="📝", width=2, style="Buttons.TButton", cursor="hand2",
            command=lambda:[self.export_excel()]
        )
        export_button.grid(row=0, column=4, sticky="W")
        
        settings_button = ttk.Button(
            self, text="⚙️", width=2, style="Buttons.TButton", cursor="hand2",
            command=lambda:[show_settings(), self.disable_entry()]
        )
        settings_button.grid(row=0, column=5, sticky="E")

        timer_frame = ttk.Frame(self)
        timer_frame.grid(row=0, columnspan=6)
        
        timer_counter = ttk.Label(
            timer_frame,
            textvariable=controller.current_time,
            style="Timer.TLabel"
        )
        timer_counter.grid()

        first_nr_label = ttk.Label(
            self, textvariable=controller.first_nr_value,
            style="PracticeNrSym.TLabel"
        )
        first_nr_label.grid(row=1, column=0)

        math_symbol_label = ttk.Label(
            self, textvariable=controller.chosen_symbol,
            style="PracticeNrSym.TLabel"
        )
        math_symbol_label.grid(row=1, column=1)

        second_nr_label = ttk.Label(
            self, textvariable=controller.second_nr_value,
            style="PracticeNrSym.TLabel"
        )
        second_nr_label.grid(row=1, column=2)

        equal_sign_label = ttk.Label(
            self, text="=", style="PracticeNrSym.TLabel"
        )
        equal_sign_label.grid(row=1, column=3)

        # 'self.' is so that 'input_value_frame' is available in 'start_timer',
        # and you can .focus() on it every time you click on other buttons.
        self.input_value_frame = ttk.Entry(
            self, width=9, textvariable=controller.input_value,
            font=("Segoe UI", 15 ), state="disabled"
        )
        self.input_value_frame.grid(row=1, column=4, columnspan=2)
        # Focus on 'input_value_frame' when 'Enter' is pressed.
        def bind_input_value_frame(event):
            # Check first if the timer is running, else show a warning.
            if controller.timer_running:
                self.submit()
            else:
                messagebox.showwarning(title='Countdown not running',
                message="You can't submit if the countdown isn't running!" +
                    "\n Click 'start ▶️' to be able to submit your answers. ")
        # Bind 'Enter' to the Enty field.
        self.input_value_frame.bind("<Return>", bind_input_value_frame)

        self.progress_bar = ttk.Progressbar(self,
            orient=tk.HORIZONTAL,
            mode='determinate',
            length=500,
            maximum=controller.max_progressbar.get(),
            variable=controller.pro_bar,
            style="TProgressbar"
            )
        self.progress_bar.grid(row=3, columnspan=6)

        self.correct_answers_label = ttk.Label(
            self,
            text=str(controller.pro_bar.get()) + "/" +
                str(controller.number_questions_input.get()),
            style="CorrectText.TLabel"
        )
        self.correct_answers_label.grid(row=3, columnspan=6)

        submit_input_value = ttk.Button(
            self, text="Submit", cursor="hand2", style="Submit.TButton",
            command=lambda:[self.submit()]
            )
        submit_input_value.grid(row=4, columnspan=6, sticky="EW")

        # Add padding in between every label.
        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=14)
            
    def start_timer(self):
        self.input_value_frame.focus()
        self.calculate()
        if not self.controller.timer_running:
            self.controller.timer_running = True
            self.controller.decrement_time()
            self.controller.pro_bar.set(0)
            self.input_value_frame["state"] = "enabled"
            # Empty the list of 'self.exercises' if the timer isn't running.
            self.exercises = []

    def disable_entry(self):
            # Clear the Entry field and focus on it.
            self.input_value_frame.delete(0, 'end')
            self.input_value_frame.focus()
            
            self.input_value_frame["state"] = "disabled"

    # calc funcs
    def add(self):
        """
        add two random numbers
        """
        self.calced_value.set(
            self.controller.first_nr_value.get()+
                self.controller.second_nr_value.get()
        )
    def substract(self):
        """
        substract two random numbers
        """
        self.calced_value.set(
            self.controller.first_nr_value.get()-
                self.controller.second_nr_value.get()
        )
    def multiplicate(self):
        """
        multiplicate two random numbers
        """
        self.calced_value.set(
            self.controller.first_nr_value.get()*
                self.controller.second_nr_value.get()
        )
    def divide(self):
        """
        divide two random numbers
        """
        self.calced_value.set(
            self.controller.first_nr_value.get()/
                self.controller.second_nr_value.get()
        )
    def calculate(self):
        # Calculate values.
        self.calc_funcs[self.controller.chosen_symbol_index.get()]()
        print(self.calced_value.get())    

    def get_correction(self):
        try:
            # Get parent of current directory.
            os.chdir(os.path.dirname(__file__))
            print(self.controller.input_value.get())  
            if self.calced_value.get() == int(self.controller.input_value.get()):
                print("CORRECT!" + "\n")
                winsound.PlaySound("Correct_Answer.wav", winsound.SND_ASYNC)
                self.controller.pro_bar.set(self.controller.pro_bar.get()+1)
            else:
                print("INCORRECT!" + "\n")
                winsound.PlaySound("no.wav", winsound.SND_ASYNC)
            self.calculate()
        except ValueError:
            pass

    def reset_progressbar(self):
        self.progress_bar["maximum"] = self.controller.number_questions_input.get()
        self.correct_answers_label["text"] = str(self.controller.pro_bar.get()) + "/" + str(self.controller.number_questions_input.get())

    def submit(self):
        # Check first if the timer is running, else show a warning.
        if self.controller.timer_running:
            # Make a list of all the given values and append it to 'self.exercises'
            try:
                self.exercises.append([
                    self.controller.first_nr_value.get(),
                    self.controller.second_nr_value.get(),
                    self.controller.chosen_symbol.get(),
                    self.calced_value.get(),
                    int(self.controller.input_value.get()),
                    int(self.controller.input_value.get()) == self.calced_value.get()
                ])
            except:
                pass

            self.controller.get_number_questions()
            self.get_correction()
            self.correct_answers_label["text"] = str(self.controller.pro_bar.get()) + "/" + str(self.controller.number_questions_input.get())


            # Clear the Entry field and focus on it.
            self.input_value_frame.delete(0, 'end')
            self.input_value_frame.focus()

        else:
            messagebox.showwarning(title='Countdown not running',
            message="You can't submit if the countdown isn't running!" +
                "\n Click 'start ▶️' to be able to submit your answers. ")

    def export_excel(self):
        print("Exported to excel!")
        print(self.exercises)

        workbook = xlsxwriter.Workbook('results.xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        headers = [
            'Exercise', 'Solution', 'Your answer', 'Right/Wrong',
        ]
        try:
            row = 0
            for header in headers:
                col = headers.index(header)
                worksheet.write(row, col, header, bold)

            row = 1
            for exercise in self.exercises:
                task = f'{exercise[0]}{exercise[2]}{exercise[1]}='
                worksheet.write(row, 0, task)
                worksheet.write(row, 1, exercise[3])
                worksheet.write(row, 2, exercise[4])
                if exercise[5] == True:
                    correction = 'Right'
                    color = workbook.add_format({'color': 'green'})
                else:
                    correction = 'Wrong'
                    color = workbook.add_format({'color': 'red'})
                worksheet.write(row, 3, correction, color)
                row += 1

            workbook.close()
            os.system('start ' + os.path.abspath('results.xlsx'))
        except:
            messagebox.showwarning(
                title='Close excel file',
                message="It looks like that you are trying to view your results but already "+
                " have the excel file open. Close the file and try again.")