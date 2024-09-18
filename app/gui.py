import os
import platform
import subprocess
from webbrowser import open
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter.messagebox import showerror, showinfo
from app.config import (
    ABOUT_TITLE_FONT_SIZE, ABOUT_TITLE_FONT_WEIGHT, APP_AUTHOR, APP_NAME,
    APP_VERSION, DEV_YEARS, ICON_PATH, LICENSE_PATH, REPO_URL
)
from app.scheme import Scheme
from app.utils import AppUtils, DCFileManager, SchemeFileManager

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
    def __init__(self, parent: tk.Tk, user_config: dict) -> None:
        """
        Initializes the AppMenuBar class by setting up the Menu Bar items.
        """
        self.user_config: dict = user_config

        # Initialize Menu Bar
        self.menu_bar: tk.Menu = tk.Menu(parent)

        # Add Menu Bar items: File
        self.file_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.file_menu.add_command(label='Exit', command=lambda: parent.quit())
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        # Add Menu Bar items: Tools
        self.tools_menu: tk.Menu = tk.Menu(self.menu_bar, tearoff=False)
        self.tools_menu.add_command(
            label='Create scheme',
            command=self.show_create_scheme_window
        )
        self.menu_bar.add_cascade(label='Tools', menu=self.tools_menu)

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

    def calculate_entry_width(self, entries: list[tk.StringVar]) -> int:
        """
        Calculates the Entry Widget width based on max entries length from the
        list.

        Args:
            entries (list[tk.StringVar]): The entries list.

        Returns:
            int: The Entry Widget width.
        """
        font: tkFont.Font = tkFont.Font(family='TkDefaultFont')

        # Choose the longest entry
        longest_entry: str = max((entry.get() for entry in entries), key=len)

        text_width: int = font.measure(longest_entry)
        text_length: int = len(longest_entry)

        avg_char_width: float = text_width / text_length

        entry_width: int = int(text_width / avg_char_width) + 5

        return entry_width

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

    def create_scheme(self) -> None:
        """
        Creates the new scheme from current DC configuration.
        """
        pass

    def open_license(self) -> None:
        """
        Opens LICENSE file using default system application.
        """
        if platform.system() == 'Windows':   # Windows
            os.startfile(LICENSE_PATH)
        elif platform.system() == 'Darwin':   # macOS
            subprocess.run(['open', LICENSE_PATH])
        else:   # Linux and others
            subprocess.run(['xdg-open', LICENSE_PATH])

    def show_create_scheme_window(self) -> None:
        """
        Sets and displays Create scheme modal window.
        """
        create_scheme_window: tk.Toplevel = tk.Toplevel()
        icon_path: str = AppUtils.get_asset_path(ICON_PATH)

        # Define and set config paths variables
        cfg_file: tk.StringVar = tk.StringVar()
        xml_file: tk.StringVar = tk.StringVar()
        json_file: tk.StringVar = tk.StringVar()

        cfg_file.set(DCFileManager.get_config(
            self.user_config['doubleCommander']['configPaths']['cfg'])
        )
        xml_file.set(DCFileManager.get_config(
            self.user_config['doubleCommander']['configPaths']['xml'])
        )
        json_file.set(DCFileManager.get_config(
            self.user_config['doubleCommander']['configPaths']['json'])
        )

        # Calculate Entry Widget width
        entry_width: int = self.calculate_entry_width(
            [cfg_file, xml_file, json_file]
        )

        # Set window properties
        create_scheme_window.iconbitmap(icon_path)
        create_scheme_window.resizable(False, False)
        create_scheme_window.title('Create scheme')

        create_scheme_window.columnconfigure(0, weight=1)
        create_scheme_window.columnconfigure(1, weight=3)

        # Path to doublecmd.cfg
        ttk.Label(
            create_scheme_window, text='\'doublecmd.cfg\' path:'
        ).grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

        cfg_path: ttk.Entry = ttk.Entry(
            create_scheme_window, state='readonly', textvariable=cfg_file,
            width=entry_width
        )
        cfg_path.grid(column=1, row=0, sticky=tk.E, padx=10, pady=10)

        # Path to doublecmd.xml
        ttk.Label(
            create_scheme_window, text='\'doublecmd.xml\' path:'
        ).grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)

        xml_path: ttk.Entry = ttk.Entry(
            create_scheme_window, state='readonly', textvariable=xml_file,
            width=entry_width
        )
        xml_path.grid(column=1, row=1, sticky=tk.E, padx=10, pady=5)

        # Path to colors.json
        ttk.Label(
            create_scheme_window, text='\'colors.json\' path:'
        ).grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)

        json_path: ttk.Entry = ttk.Entry(
            create_scheme_window, state='readonly', textvariable=json_file,
            width=entry_width
        )
        json_path.grid(column=1, row=2, sticky=tk.E, padx=10, pady=10)

        # Scheme name entry
        ttk.Label(
            create_scheme_window, text='Scheme name:'
        ).grid(column=0, row=3, sticky=tk.W, padx=10, pady=5)

        scheme_name: ttk.Entry = ttk.Entry(
            create_scheme_window, width=entry_width
        )
        scheme_name.grid(column=1, row=3, sticky=tk.E, padx=10, pady=5)

        ttk.Button(
            create_scheme_window, text='Export', command=self.create_scheme
        ).grid(column=0, row=4, sticky=tk.W, padx=10, pady=10)
        ttk.Button(
            create_scheme_window, text='Cancel',
            command=lambda: create_scheme_window.destroy()
        ).grid(column=1, row=4, sticky=tk.E, padx=10, pady=10)

        self.center_window(create_scheme_window)

        # Make window modal and set focus
        create_scheme_window.grab_set()
        create_scheme_window.focus_set()
        create_scheme_window.wait_window()

    def show_about_window(self) -> None:
        """
        Sets and displays About modal window.
        """
        about_window: tk.Toplevel = tk.Toplevel()

        icon_path: str = AppUtils.get_asset_path(ICON_PATH)

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
        apply_button (ttk.Button): Button to verify and apply the selected
                                   scheme.

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
        self.initialize_scheme()

    def initialize_scheme(self) -> None:
        """
        Initialize object of Scheme class.
        """
        self.scheme = Scheme(
            self.scheme_var.get(), self.user_config['schemes']['path'],
            self.user_config['doubleCommander']['configPaths'],
            self.user_config['doubleCommander']['backupConfigs'],
            self.dark_mode_var.get(),
            self.user_config['schemes']['xmlTags']
        )

    def modify_scheme(self) -> None:
        """
        Applies the selected scheme and updates the configuration accordingly.
        """
        try:
            self.scheme.apply_scheme()
            showinfo(
                title='Info',
                message=(
                    f'Scheme \'{self.scheme_var.get()}\' applied successfully.'
                )
            )
        except Exception as e:
            showerror(
                title='Error',
                message=str(e)
            )

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

        # Initialize, verify and apply scheme
        self.apply_button: ttk.Button = ttk.Button(
            self, text='Apply', command=lambda: (
                self.initialize_scheme(), self.verify_scheme(),
                self.modify_scheme()
            )
        )
        self.apply_button.grid(
            column=0, row=2, columnspan=2, sticky=tk.W, **options
        )

    def verify_scheme(self) -> None:
        """
        Verifies the selected scheme version against target scheme version.
        """
        try:
            self.scheme.verify_scheme()
        except Exception as e:
            showerror(
                title='Error',
                message=str(e)
            )