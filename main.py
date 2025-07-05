import tkinter as tk
from gui import ConverterGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterGUI(root)
    app.run()