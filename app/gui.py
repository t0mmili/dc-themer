import tkinter as tk
import webbrowser
from config import APP_AUTHOR, APP_NAME, APP_VERSION, DC_CONFIG_PATHS, DEV_YEARS, REPO_URL, SCHEME_EXTENSIONS, SCHEME_PATH, XML_TAGS
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from utils import Scheme

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

        # Field options
        options = {'padx': 5, 'pady': 5}

        # Scheme Selector label
        self.scheme_selector_label = ttk.Label(self, text='Select scheme:')
        self.scheme_selector_label.grid(column=0, row=0, sticky=tk.W, **options)

        # Scheme Selector
        scheme_path = SCHEME_PATH
        scheme_exts = SCHEME_EXTENSIONS
        schemes = Scheme.list_schemes(scheme_path, scheme_exts)
        self.scheme_var = tk.StringVar(self)

        self.scheme_selector = ttk.OptionMenu(self, self.scheme_var, schemes[0], *schemes)
        self.scheme_selector.grid(column=1, row=0, **options)

        # Apply Scheme button
        self.apply_button = ttk.Button(self, text='Apply')
        self.apply_button['command'] = self.modify_scheme
        self.apply_button.grid(column=0, row=1, columnspan=2, sticky=tk.W, **options)

        # Add Frame options
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def modify_scheme(self):
        try:
            dc_configs = DC_CONFIG_PATHS
            scheme_name = self.scheme_var.get()
            scheme_path = SCHEME_PATH
            xml_tags = XML_TAGS

            scheme = Scheme(scheme_name, scheme_path, dc_configs, xml_tags)
            scheme.apply_scheme()

            showinfo(title='Info', message=f'Scheme \'{scheme_name}\' applied successfully.')
        except Exception as e:
            showerror(title='Error', message=f'Exception:\n{str(e)}')