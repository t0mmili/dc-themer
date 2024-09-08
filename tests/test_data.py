CONFIG_CURRENT_VERSION = 2
CONFIG_READ_VERSION = 1
DARK_MODE = False
DC_BACKUP_CONFIGS = False
DC_CONFIG_PATHS = {
    "cfg": "doublecmd.cfg",
    "json": "colors.json",
    "xml": "doublecmd.xml"
}
DC_CONFIG_CFG_MOCK = {
    "cfgSource": {
        "name": "doublecmd-test-1.cfg",
        "content": "SplashForm=-1\n"
            "DarkMode=2\n"
    },
    "cfgTarget": {
        "name": "doublecmd-test-2.cfg",
        "content": "SplashForm=-1\n"
            "DarkMode=3\n"
    }
}
DC_CONFIG_JSON_MOCK = {
    "jsonSource": {
        "name": "colors-test-1.cfg",
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
}"""
    },
    "jsonTarget": {
        "name": "colors-test-2.cfg",
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
        "name": "doublecmd-test-1.xml",
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
</doublecmd>
""",
        "version": "15"
    },
    "xmlTarget": {
        "name": "doublecmd-test-2.xml",
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
""",
        "version": "14"
    }
}
SCHEME_NAME = 'scheme'
SCHEME_PATH = './schemes'
SCHEME_XML_TAGS = [
    "Colors",
    "Fonts"
]
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