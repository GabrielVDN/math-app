import tkinter as tk
import tkinter.ttk as ttk
 
 
root = tk.Tk()
root.geometry('400x200')
root.title('Test progress bar')
root.columnconfigure(0, weight=1)
 
int_var = tk.IntVar(value=0)
input_value = tk.StringVar(value="4")
inputed_value = tk.StringVar()
inputed_value.set(input_value.get())

style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", background='blue')

progbar = ttk.Progressbar(
    root,
    orient=tk.HORIZONTAL, 
    mode='determinate',
    length=200,
    maximum=int(inputed_value.get()),
    variable=int_var,
    style="TProgressbar"
)
progbar.grid(row=0, column=0, pady=15)

text = ttk.Label(
    root,
    text=str(int_var.get()) + "/" + inputed_value.get()
)
text.grid(row=0, column=0)

btn = ttk.Button(root, text='Start',
    command=lambda:[add1(), get_inputed_value(input_value), focus_btn()])
def focus_btn():
    # Clear the Entry field and focus on it.
    entry_field.delete(0, 'end')
    entry_field.focus()
btn.grid(row=1, column=0)

entry_field = ttk.Entry(root, textvariable=input_value)
def bind_entry_field(event):
    get_inputed_value(input_value)
    # Clear the Entry field and focus on it.
    entry_field.delete(0, 'end')
    entry_field.focus()
# Bind 'Enter' to the Enty field.
entry_field.bind("<Return>", bind_entry_field)
entry_field.grid(row=2, column=0, pady=15)
entry_field.focus()

def get_inputed_value(inputed_value):
    inputed_value.set(input_value.get())

def add1():
    if int_var.get() == int(inputed_value.get()):
        int_var.set(0)
    else:
        int_var.set(int_var.get()+1)
    text["text"] = str(int_var.get()) + "/" + inputed_value.get()


root.mainloop()