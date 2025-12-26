import tkinter as tk
from src.model import MemoModel
from src.view import View
from src.controller import Controller

if __name__ == "__main__":
    """
    Main entry point for the application.
    Initializes the MVC components and starts the Tkinter main loop.
    """
    # Create the main window
    root = tk.Tk()

    # Create the MVC components
    model = MemoModel()
    view = View(root)
    controller = Controller(model, view)

    # Start the application
    root.mainloop()
