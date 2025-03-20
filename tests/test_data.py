# Misc
ASSET_PATH = 'assets\\default-user-config.json'
AUTO_DARK_MODE = False
DC_BACKUP_CONFIGS = False
DC_CONFIG_PATHS = {
    "cfg": "doublecmd.cfg",
    "json": "colors.json",
    "xml": "doublecmd.xml",
    "test": "%USERPROFILE%"
}
SCHEME_NAME = 'test-scheme'
SCHEME_PATH = './test-schemes'
SCHEME_XML_TAGS = [
    "Colors",
    "Fonts"
]

# User config
CONFIG_VERSION_CURRENT = 2
CONFIG_VERSION_READ_FAIL = 1
CONFIG_VERSION_READ_SUCCESS = 2
USER_CONFIG_DEFAULT = {
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
            "cfg",
            "json",
            "xml"
        ],
        "path": "./schemes",
        "xmlTags": [
            "Colors",
            "Fonts"
        ]
    }
}
USER_CONFIG_PATH = 'dc-themer-test.json'
USER_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "configVersion": {
            "type": "integer",
            "minimum": 1
        },
        "doubleCommander": {
            "type": "object",
            "properties": {
                "backupConfigs": {
                    "type": "boolean"
                },
                "configPaths": {
                    "type": "object",
                    "properties": {
                        "cfg": { "type": "string" },
                        "json": { "type": "string" },
                        "xml": { "type": "string" }
                    },
                    "required": ["cfg", "json", "xml"]
                }
            },
            "required": ["backupConfigs", "configPaths"]
        },
        "schemes": {
            "type": "object",
            "properties": {
                "extensions": {
                    "type": "array",
                    "items": { "type": "string" }
                },
                "path": { "type": "string" },
                "xmlTags": {
                    "type": "array",
                    "items": { "type": "string" }
                }
            },
            "required": ["extensions", "path", "xmlTags"]
        }
    },
    "required": ["configVersion", "doubleCommander", "schemes"]
}

# DC configs
DC_CONFIG_CFG_MOCK = {
    "cfgSource": {
        "content": "SplashForm=-1\n"
          "DarkMode=2\n",
        "schema": """SplashForm = integer
DarkMode = integer
"""
    },
    "cfgTarget": {
        "content": "SplashForm=-1\n"
            "DarkMode=3\n"
    }
}
DC_CONFIG_JSON_MOCK = {
    "jsonSource": {
        "content": """{
  Styles : [
    {
      Name : "Dark",
      Log : {
        InfoColor : 1234567,
        ErrorColor : 1234567,
        SuccessColor : 1234567
      }
    }
  ],
  FileColors : [
    {
      Name : "json",
      Masks : "*.json",
      Colors : [
        0,
        65280
      ],
      Attributes : ""
    }
  ]
}""",
        "schema": """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "Styles": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Name": {
            "type": "string"
          },
          "Log": {
            "type": "object",
            "properties": {
              "InfoColor": {
                "type": "integer",
                "minimum": 0
              },
              "ErrorColor": {
                "type": "integer",
                "minimum": 0
              },
              "SuccessColor": {
                "type": "integer",
                "minimum": 0
              }
            },
            "required": ["InfoColor", "ErrorColor", "SuccessColor"]
          }
        },
        "required": ["Name", "Log"]
      }
    },
    "FileColors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "Name": {
            "type": "string"
          },
          "Masks": {
            "type": "string"
          },
          "Colors": {
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0
            }
          },
          "Attributes": {
            "type": "string"
          }
        },
        "required": ["Name", "Masks", "Colors", "Attributes"]
      }
    }
  },
  "required": ["Styles", "FileColors"]
}"""
    },
    "jsonTarget": {
        "content": """{
  Styles : [
    {
      Name : "Dark",
      Log : {
        InfoColor : 7654321,
        ErrorColor : 7654321,
        SuccessColor : 7654321
      }
    }
  ],
  FileColors : [
  ]
}"""
    }
}
DC_CONFIG_XML_MOCK = {
    "xmlSource": {
        "content": """<?xml version="1.0" encoding="UTF-8"?>
<doublecmd DCVersion="1.1.16 gamma" ConfigVersion="15">
  <Fonts>
    <Main>
      <Name>default</Name>
      <Size>10</Size>
      <Style>0</Style>
      <Quality>0</Quality>
    </Main>
  </Fonts>
  <Colors>
    <UseCursorBorder>True</UseCursorBorder>
    <UseFrameCursor>False</UseFrameCursor>
  </Colors>
</doublecmd>"""
    },
    "xmlTarget": {
        "content": """<?xml version="1.0" encoding="UTF-8"?>
<doublecmd DCVersion="1.0.11 beta" ConfigVersion="14">
  <Fonts>
    <Main>
      <Name>Consolas</Name>
      <Size>12</Size>
      <Style>0</Style>
      <Quality>0</Quality>
    </Main>
  </Fonts>
  <Colors>
    <UseCursorBorder>False</UseCursorBorder>
    <UseFrameCursor>True</UseFrameCursor>
  </Colors>
</doublecmd>
"""
    }
}