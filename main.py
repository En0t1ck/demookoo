# main.py
from gui import ImageRecognitionApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRecognitionApp(root)
    root.mainloop()
