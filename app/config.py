# General application information
APP_AUTHOR = 't0mmili'
APP_NAME = 'DC Themer'
APP_VERSION = '0.3.0'
DEV_YEARS = '2024'
REPO_URL = 'https://github.com/t0mmili/dc-themer'

# Application assets
ICON_PATH = './assets/dct-icon-v3.ico'

# Application config
DEFAULT_USER_CONFIG = {
    "configVersion": 1,
    "schemes": {
        "extensions": [
            "cfg", "json", "xml"
        ],
        "path": "./schemes",
        "xmlTags": [
            "Colors", "Fonts"
        ]
    },
    "doubleCommander": {
        "configPaths": {
            "cfg": "%APPDATA%\\doublecmd\\doublecmd.cfg",
            "json": "%APPDATA%\\doublecmd\\colors.json",
            "xml": "%APPDATA%\\doublecmd\\doublecmd.xml"
        }
    }
}
USER_CONFIG_PATH = 'dc-themer.json'
USER_CONFIG_VERSION = 1
WINDOW_HEIGHT = 140
WINDOW_WIDTH = 285