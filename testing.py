import tkinter as tk
from tkinter import ttk


class SecondaryWindow(tk.Toplevel):

    # Class attribute that indicates whether this child window
    # is being used (alive) or not.
    alive = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=300, height=200)
        self.title("Secondary Window")
        self.button_close = ttk.Button(
            self,
            text="Close window",
            command=self.destroy
        )
        self.button_close.place(x=75, y=75)
        self.focus()
        # Set the window as alive once created.
        self.__class__.alive = True

    def destroy(self):
        # Restore the attribute on close.
        self.__class__.alive = False
        return super().destroy()


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=400, height=300)
        self.title("Main Window")
        self.button_open = ttk.Button(
            self,
            text="Open secondary window",
            command=self.open_secondary_window
        )
        self.button_open.place(x=100, y=100)

    def open_secondary_window(self):
        if not SecondaryWindow.alive:
            self.secondary_window = SecondaryWindow()


main_window = MainWindow()
main_window.mainloop()