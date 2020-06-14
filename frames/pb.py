try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
    import tkinter.ttk as ttk
except ImportError:
    import Tkinter as tk
    import ttk


class RestartableProgress(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.max_input = tk.Entry(self)
        self.restart_button = tk.Button(
            self, text="Restart", command=self.restart
        )
        self.progressbar = ttk.Progressbar(self)
        self.max_input.pack()
        self.restart_button.pack()
        self.progressbar.pack()


    def restart(self):
        self.progressbar['value'] = 0
        self.progress()


    def progress(self):
        max_val = self.max_input.get()
        if max_val:
            self.progressbar['maximum'] = int(max_val)
            if self.progressbar['value'] < self.progressbar['maximum']:
                self.progressbar['value'] += 1
                self.after(10, self.progress)


def main():
    root = tk.Tk()
    rp = RestartableProgress(root)
    rp.pack()
    tk.mainloop()


if __name__ == '__main__':
    main()