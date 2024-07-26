import tkinter as tk
from config import APP_NAME, ICON_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from gui import AppFrame, AppMenuBar
from os import path

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main Window size
        window_width = WINDOW_WIDTH
        window_height = WINDOW_HEIGHT

        icon_path = ICON_PATH
        # This is needed for compilation with PyInstaller
        # icon_path = path.abspath(path.join(path.dirname(__file__), ICON_PATH))

        self.iconbitmap(icon_path)
        self.resizable(False, False)
        self.title(APP_NAME)

        # Create an instance of Menu Bar
        self.menu = AppMenuBar(self)
        self.config(menu=self.menu.menu_bar)

        # Find screen center point
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        # Set Main Window geometry
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

if __name__ == '__main__':
    app = App()
    AppFrame(app)
    app.mainloop()