import platform
import tkinter as tk
import tkinter.font as tkFont
from config import (
    ABOUT_TITLE_FONT_SIZE, ABOUT_TITLE_FONT_WEIGHT, APP_AUTHOR, APP_NAME,
    APP_VERSION, DEV_YEARS, ICON_PATH, LICENSE_PATH, REPO_URL
)
from os import startfile
from scheme import Scheme
from subprocess import run
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from utils import SchemeFileManager
from webbrowser import open

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
        """
        Initializes the AppMenuBar class by setting up the Menu Bar items.
        """
        # Initialize Menu Bar
        self.menu_bar: tk.Menu = tk.Menu(parent)

        # Add Menu Bar items: File
        self.file_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label='Exit', command=lambda: parent.quit())
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Add Menu Bar items: Help
        self.help_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.help_menu.add_command(
            label=f'{APP_NAME} on GitHub',
            command=lambda: open(REPO_URL)
        )
        self.help_menu.add_command(
            label='About',
            command=self.show_about_window
        )
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

    def center_window(self, window: tk.Toplevel) -> None:
        """
        Centers the window on the screen.

        Args:
            window (tk.Toplevel): Window object.
        """
        window.update_idletasks()
        width: int = window.winfo_width()
        height: int = window.winfo_height()
        screen_width: int = window.winfo_screenwidth()
        screen_height: int = window.winfo_screenheight()
        center_x: int = (screen_width - width) // 2
        center_y: int = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def open_license(self) -> None:
        """
        Opens LICENSE file using default system application.
        """
        if platform.system() == 'Windows':   # Windows
            startfile(LICENSE_PATH)
        elif platform.system() == 'Darwin':   # macOS
            run(['open', LICENSE_PATH])
        else:   # Linux and others
            run(['xdg-open', LICENSE_PATH])

    def show_about_window(self) -> None:
        """
        Sets and displays About modal window.
        """
        about_window: tk.Toplevel = tk.Toplevel()

        icon_path: str = ICON_PATH
        # This is necessary for compilation with PyInstaller
        # icon_path: str = path.abspath(path.join(path.dirname(__file__), ICON_PATH))

        # Set window properties
        about_window.iconbitmap(icon_path)
        about_window.resizable(False, False)
        about_window.title('About')

        # Set font properties for app name and version
        title_font: tkFont.Font = tkFont.Font(
            size=ABOUT_TITLE_FONT_SIZE, weight=ABOUT_TITLE_FONT_WEIGHT
        )

        about_message: str = (
            f'Copyright (c) {DEV_YEARS} {APP_AUTHOR}. All rights reserved.\n\n'
            f'This is open source software, released under the MIT License.'
        )

        ttk.Label(
            about_window, text=f'{APP_NAME} v{APP_VERSION}', font=title_font,
            justify=tk.LEFT, padding=(10,10)
        ).pack(anchor='w')
        ttk.Label(
            about_window, text=about_message, justify=tk.LEFT, padding=(10,0)
        ).pack(anchor='w')

        button_frame = ttk.Frame(about_window)

        button_frame.pack(pady=10)
        ttk.Button(
            button_frame, text='License', command=self.open_license
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text='Close', command=lambda: about_window.destroy()
        ).pack(side=tk.LEFT, padx=5)

        self.center_window(about_window)

        # Make window modal and set focus
        about_window.grab_set()
        about_window.focus_set()
        about_window.wait_window()

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
        """
        Initializes the AppFrame class by setting up the widgets.
        """
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