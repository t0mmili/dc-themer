# Building binary

## Windows
```sh
pyinstaller --onefile --windowed --clean --name=dc-themer --icon=./assets/dct-icon-v3.ico --add-data=./assets:assets --upx-dir='<path_to_UPX>' ./app/main.py
```