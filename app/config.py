# General information
APP_AUTHOR = 't0mmili'
APP_NAME = 'DC Themer'
APP_VERSION = '0.3.0'
DEV_YEARS = '2024'
REPO_URL = 'https://github.com/t0mmili/dc-themer'

# Assets
ICON_PATH = './assets/dct-icon-v3.ico'

# GUI
WINDOW_HEIGHT = 140
WINDOW_WIDTH = 285

# User config
DEFAULT_USER_CONFIG = {
    "configVersion": 1,
    "doubleCommander": {
        "backupConfigs": True,
        "configPaths": {
            "cfg": "%APPDATA%\\doublecmd\\doublecmd.cfg",
            "json": "%APPDATA%\\doublecmd\\colors.json",
            "xml": "%APPDATA%\\doublecmd\\doublecmd.xml"
        }
    },
    "schemes": {
        "extensions": [
            "cfg", "json", "xml"
        ],
        "path": "./schemes",
        "xmlTags": [
            "Colors", "Fonts"
        ]
    }
}
USER_CONFIG_PATH = 'dc-themer.json'
USER_CONFIG_VERSION = 1