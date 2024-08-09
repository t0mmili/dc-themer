import tkinter as tk
import webbrowser
from config import APP_AUTHOR, APP_NAME, APP_VERSION, DEV_YEARS, REPO_URL
from scheme import Scheme
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from utils import SchemeFileManager

class AppMenuBar:
    """
    A class to create and manage the application's menu bar.

    Attributes:
        menu_bar (tk.Menu): The main menu bar container.
        file_menu (tk.Menu): The file submenu of the menu bar.
        help_menu (tk.Menu): The help submenu of the menu bar.

    Args:
        parent (tk.Tk): The parent widget, typically an instance of Tk or
                        a top-level window.
    """
    def __init__(self, parent: tk.Tk) -> None:
        about_message: str = (
            f'{APP_NAME} v{APP_VERSION}\n\n'
            f'Copyright (c) {DEV_YEARS} {APP_AUTHOR}. All rights reserved.\n\n'
            f'This is open source software, released under the MIT License.'
        )

        # Initialize Menu Bar
        self.menu_bar: tk.Menu = tk.Menu(parent)

        # Add Menu Bar items
        self.file_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label='Exit', command=lambda: parent.quit())
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.help_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.help_menu.add_command(
            label=f'{APP_NAME} on GitHub',
            command=lambda: webbrowser.open(REPO_URL)
        )
        self.help_menu.add_command(
            label='About',
            command=lambda: showinfo(title='About', message=about_message)
        )
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

class AppFrame(ttk.Frame):
    """
    A class for the main application frame, containing UI elements.

    Attributes:
        scheme_var (StringVar): Variable to hold the selected scheme name.
        dark_mode_var (BooleanVar): Variable to store the state of
                                    the dark mode checkbox.
        scheme_selector_label (ttk.Label): Label for the scheme selector
                                           dropdown.
        scheme_selector (ttk.OptionMenu): Dropdown menu to select a scheme.
        dark_mode_tick (ttk.Checkbutton): Checkbox to enable or disable auto
                                          dark mode.
        apply_button (ttk.Button): Button to apply the selected scheme.

    Args:
        container (tk.Tk): The parent widget, typically an instance of Tk or
                           a top-level window.
        user_config (dict): The configuration dictionary loaded from user
                            settings.
    """
    def __init__(self, container: tk.Tk, user_config: dict) -> None:
        super().__init__(container)
        self.user_config: dict = user_config

        self.setup_widgets()
        self.grid(padx=10, pady=10, sticky=tk.NSEW)

    def setup_widgets(self) -> None:
        """
        Sets up the widgets in the frame.
        """
        options: dict = {'padx': 5, 'pady': 5}

        # Scheme selector
        self.scheme_var: tk.StringVar = tk.StringVar(self)
        schemes = SchemeFileManager.list_schemes(
            self.user_config['schemes']['path'],
            self.user_config['schemes']['extensions']
        )
        self.scheme_selector_label: ttk.Label = ttk.Label(
            self, text='Select scheme:'
        )
        self.scheme_selector_label.grid(
            column=0, row=0, sticky=tk.W, **options
        )
        self.scheme_selector: ttk.OptionMenu = ttk.OptionMenu(
            self, self.scheme_var, schemes[0], *schemes
        )
        self.scheme_selector.grid(column=1, row=0, **options)

        # Dark Mode checkbox
        self.dark_mode_var = tk.BooleanVar(self)
        self.dark_mode_tick: ttk.Checkbutton = ttk.Checkbutton(
            self, text='Force auto Dark mode', variable=self.dark_mode_var,
            onvalue=True, offvalue=False, takefocus=False
        )
        self.dark_mode_tick.grid(
            column=0, row=1, columnspan=2, sticky=tk.W, **options
        )

        # Apply Scheme button
        self.apply_button: ttk.Button = ttk.Button(
            self, text='Apply', command=self.modify_scheme
        )
        self.apply_button.grid(
            column=0, row=2, columnspan=2, sticky=tk.W, **options
        )

    def modify_scheme(self) -> None:
        """
        Applies the selected scheme and updates the configuration accordingly.
        """
        try:
            scheme = Scheme(
                self.scheme_var.get(), self.user_config['schemes']['path'],
                self.user_config['doubleCommander']['configPaths'],
                self.user_config['doubleCommander']['backupConfigs'],
                self.dark_mode_var.get(),
                self.user_config['schemes']['xmlTags']
            )
            scheme.apply_scheme()
            showinfo(
                title='Info',
                message=(
                    f'Scheme \'{self.scheme_var.get()}\' '
                    f'applied successfully.'
                )
            )
        except Exception as e:
            showerror(
                title='Error',
                message=str(e)
            )