import tkinter as tk
import webbrowser
from config import APP_AUTHOR, APP_NAME, APP_VERSION, DC_CONFIG_PATHS, DEV_YEARS, REPO_URL, SCHEME_EXTENSIONS, SCHEME_PATH, XML_TAGS
from scheme import Scheme
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from utils import SchemeFileManager

class AppMenuBar:
    def __init__(self, parent):
        about_message = (f'{APP_NAME} v{APP_VERSION}\n\n'
                         f'Copyright (c) {DEV_YEARS} {APP_AUTHOR}. All rights reserved.\n\n'
                         f'This is open source software, released under the MIT License.')

        # Initialize Menu Bar
        self.menu_bar = tk.Menu(parent)

        # Add Menu Bar items
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label='Exit', command=lambda: parent.quit())
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.help_menu.add_command(label=f'{APP_NAME} on GitHub', command=lambda: webbrowser.open(REPO_URL))
        self.help_menu.add_command(label='About', command=lambda: showinfo(title='About', message=about_message))
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

class AppFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.setup_widgets()
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def setup_widgets(self):
        options = {'padx': 5, 'pady': 5}

        # Scheme selector
        self.scheme_var = tk.StringVar(self)
        schemes = SchemeFileManager.list_schemes(SCHEME_PATH, SCHEME_EXTENSIONS)
        self.scheme_selector_label = ttk.Label(self, text='Select scheme:')
        self.scheme_selector_label.grid(column=0, row=0, sticky=tk.W, **options)
        self.scheme_selector = ttk.OptionMenu(self, self.scheme_var, schemes[0], *schemes)
        self.scheme_selector.grid(column=1, row=0, **options)

        # Dark Mode checkbox
        self.dark_mode_var = tk.BooleanVar(self)
        self.dark_mode_tick = ttk.Checkbutton(self, text='Force auto Dark mode', variable=self.dark_mode_var, onvalue=True, offvalue=False, takefocus=False)
        self.dark_mode_tick.grid(column=0, row=1, columnspan=2, sticky=tk.W, **options)

        # Apply Scheme button
        self.apply_button = ttk.Button(self, text='Apply', command=self.modify_scheme)
        self.apply_button.grid(column=0, row=2, columnspan=2, sticky=tk.W, **options)

    def modify_scheme(self):
        try:
            scheme = Scheme(self.scheme_var.get(), SCHEME_PATH, DC_CONFIG_PATHS, self.dark_mode_var.get(), XML_TAGS)
            scheme.apply_scheme()
            showinfo(title='Info', message=f'Scheme \'{self.scheme_var.get()}\' applied successfully.')
        except Exception as e:
            showerror(title='Error', message=f'An unexpected error occurred:\n{str(e)}')