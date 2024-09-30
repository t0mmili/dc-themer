import tkinter as tk
from tkinter.messagebox import showerror
from app.config import (
    APP_NAME, ICON_PATH, DEFAULT_USER_CONFIG, USER_CONFIG_PATH,
    USER_CONFIG_VERSION
)
from app.gui import AppFrame, AppMenuBar
from app.user_config import UserConfigManager
from app.utils import AppUtils

class App(tk.Tk):
    """
    The main application class that initializes and runs the tkinter GUI.

    This class inherits from tkinter's Tk class and sets up the application
    window, including setting the window icon, title, and size, and
    initializing the menu bar and main application frame.
    """
    def __init__(self) -> None:
        """
        Initializes the App class by setting up the main application window,
        its properties, and the components.
        """
        super().__init__()

        icon_path: str = AppUtils.get_asset_path(ICON_PATH)

        # Set application window properties
        self.iconbitmap(icon_path)
        self.resizable(False, False)
        self.title(APP_NAME)

        # Create an instance of Menu Bar
        self.menu = AppMenuBar(self, user_config)
        self.config(menu=self.menu.menu_bar)

        # Center the window on the screen
        self.eval('tk::PlaceWindow . center')

def init_user_config() -> dict:
    """
    Initializes the user configuration.

    Returns:
        user_config (dict): The user configuration dictionary.
    """
    default_config_file: str = AppUtils.get_asset_path(DEFAULT_USER_CONFIG)

    default_user_config: dict = UserConfigManager.get_config(
        default_config_file
    )
    user_config_file = UserConfigManager(default_user_config, USER_CONFIG_PATH)

    if not user_config_file.exists():
        user_config_file.create_default()

    user_config: dict = UserConfigManager.get_config(USER_CONFIG_PATH)
    UserConfigManager.verify(USER_CONFIG_VERSION, user_config['configVersion'])

    return user_config

if __name__ == '__main__':
    """
    Main execution point of the application.

    This section initializes user configuration,
    creates the main application window, and starts the event loop.
    """
    try:
        user_config: dict = init_user_config()
        app = App()
        AppFrame(app, user_config)
        app.mainloop()
    except Exception as e:
        showerror(
            title='Error',
            message=str(e)
        )