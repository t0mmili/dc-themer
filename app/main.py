import tkinter as tk
from config import APP_NAME, ICON_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from gui import AppFrame, AppMenuBar
from os import path

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        icon_path = ICON_PATH
        # This is necessary for compilation with PyInstaller
        # icon_path = path.abspath(path.join(path.dirname(__file__), ICON_PATH))

        # Set application window properties
        self.iconbitmap(icon_path)
        self.resizable(False, False)
        self.title(APP_NAME)

        # Create an instance of Menu Bar
        self.menu = AppMenuBar(self)
        self.config(menu=self.menu.menu_bar)

        # Center the window on the screen
        self.center_window(WINDOW_WIDTH, WINDOW_HEIGHT)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = (screen_width - width) // 2
        center_y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')

if __name__ == '__main__':
    app = App()
    AppFrame(app)
    app.mainloop()