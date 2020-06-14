import tkinter as tk
from tkinter import ttk, messagebox


# Create a Tkinter themed widget.
class Settings(ttk.Frame):
    def __init__(self, parent, controller, show_settings):
        super().__init__(parent)

        self.controller = controller
        self.columnconfigure(0, weight=1)

        # Set the frame's background.
        self["style"] = "Background.TFrame"

        # Add the Radiobuttons.
        add_label_button = ttk.Radiobutton(
            self, text="➕", variable=controller.chosen_symbol_index,
            value=0,
            style='Symbols.TRadiobutton', cursor="hand2"
            )
        add_label_button.grid(row=0, column=0)

        subtraction_label_button = ttk.Radiobutton(
            self, text="➖", variable=controller.chosen_symbol_index,
            value=1,
            style='Symbols.TRadiobutton', cursor="hand2"
            )
        subtraction_label_button.grid(row=1, column=0)

        multiplication_label_button = ttk.Radiobutton(
            self, text="✖️", variable=controller.chosen_symbol_index,
            value=2,
            style='Symbols.TRadiobutton', cursor="hand2"
            )
        multiplication_label_button.grid(row=2, column=0)
        
        division_label_button = ttk.Radiobutton(
            self, text="➗", variable=controller.chosen_symbol_index,
            value=3,
            style='Symbols.TRadiobutton', cursor="hand2"
            )
        division_label_button.grid(row=3, column=0)

        # Let the user input a from value and a to value.
        numbers_range_from = ttk.Label(
            self, text="From", style="SettingsText.TLabel"
            )
        numbers_range_from.grid(row=0, column=1)

        input_from_label = ttk.Entry(self, width=6,
            textvariable=controller.input_from_value,
            font=("TkDefaultFont", 16)
        )
        input_from_label.grid(row=1, column=1)
        input_from_label.focus()
        # Focus on 'input_to_label' when 'Enter' is pressed.
        def bind_input_to_label(event):
            controller.generate_numbers()
            if controller.no_errors:
                input_to_label.focus()
        # Bind 'Enter' to the Enty field.
        input_from_label.bind("<Return>", bind_input_to_label)

        numbers_range_to = ttk.Label(
            self, text="To", style="SettingsText.TLabel"
            )
        numbers_range_to.grid(row=0, column=3)

        hyphen_symbol = ttk.Label(
            self, text="- ", style="PracticeNrSym.TLabel"
        )
        hyphen_symbol.grid(row=1, column=2)

        input_to_label = ttk.Entry(
            self, width=6, textvariable=controller.input_to_value,
            font=("TkDefaultFont", 16)
        )
        input_to_label.grid(row=1, column=3)
        # Focus on 'input_to_label' when 'Enter' is pressed.
        def bind_minutes_input_label(event):
            controller.generate_numbers()
            if controller.no_errors:
                minutes_input_label.focus()
        # Bind 'Enter' to the Enty field.
        input_to_label.bind("<Return>", bind_minutes_input_label)

        # Let the user input a 'amount_of_minutes' and a 'amount_of_minutes'.
        minutes_label = ttk.Label(
            self, text="Minutes", style="SettingsText.TLabel"
            )
        minutes_label.grid(row=2, column=1)

        minutes_input_label = ttk.Entry(
            self, width=6, textvariable=controller.minutes_input_value,
            font=("TkDefaultFont", 16)
            )
        minutes_input_label.grid(row=3, column=1)
         # Focus on 'minutes_input_label' when 'Enter' is pressed.
        def bind_seconds_input_label(event):
            controller.reset_timer()
            if controller.no_errors:
                seconds_input_label.focus()
        # Bind 'Enter' to the Enty field.
        minutes_input_label.bind("<Return>", bind_seconds_input_label)

        seconds_label = ttk.Label(
            self, text="Seconds", style="SettingsText.TLabel"
            )
        seconds_label.grid(row=2, column=3)

        hyphen_symbol = ttk.Label(
            self, text=": ", style="PracticeNrSym.TLabel"
        )
        hyphen_symbol.grid(row=3, column=2)

        seconds_input_label = ttk.Entry(
            self, width=6, textvariable=controller.seconds_input_value,
            font=("TkDefaultFont", 16)
            )
        seconds_input_label.grid(row=3, column=3)
         # Focus on 'input_to_value' when 'Enter' is pressed.
        def bind_number_questions_input_label(event):
            controller.reset_timer()
            if controller.no_errors:
                number_questions_input_label.focus()
        # Bind 'Enter' to the Enty field.
        seconds_input_label.bind("<Return>", bind_number_questions_input_label)

        # Let the user input the 'number of questions'.
        number_questions_label = ttk.Label(
            self, text="Number of questions:", style="SettingsText.TLabel")
        number_questions_label.grid(row=4, column=1, columnspan=2)

        number_questions_input_label = ttk.Entry(
            self, width=6, textvariable=controller.number_questions_input,
            font=("TkDefaultFont", 16)
            )
        number_questions_input_label.grid(row=4, column=3)
         # Focus on 'number_questions_input_label' when 'Enter' is pressed.
        def bind_input_from_label(event):
            self.check_for_integer()
            if controller.no_errors:
                input_from_label.focus()
        # Bind 'Enter' to the Enty field.
        number_questions_input_label.bind("<Return>", bind_input_from_label)

        # The button to switch back to the'practice' frame.
        go_back_button = ttk.Button(
            self, text="← Back", style="Buttons.TButton", width=8,
            cursor="hand2",
            command=lambda:[
                show_settings(),
                controller.get_selected_symbol(),
                controller.generate_numbers(),
                controller.reset_timer(),
                self.check_for_integer()
                ]
            )
        go_back_button.grid(row=4)



        # Add padding in between every label.
        for child in self.winfo_children():
            child.grid_configure(padx=8, pady=8)

    def check_for_integer(self):
        try:
            int(self.controller.number_questions_input.get())
            self.controller.pro_bar.set(0)
        except:
            messagebox.showerror(
                title='Invalid Input',
                message='Invalid number of questions input!'
            )
