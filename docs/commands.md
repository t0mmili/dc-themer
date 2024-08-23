# Commands

## Run app
```sh
python app/main.py
```

## Generate requirements
```sh
pipreqs --force ./app
```

## Build binary
1. Edit **gui.py** and uncomment `icon_path` variable.
2. Edit **main.py** and uncomment `icon_path` variable.
3. Run command:
   ```sh
   pyinstaller --onefile --windowed --clean --name=dc-themer --icon=./assets/dct-icon-v3.ico --add-data=./assets/dct-icon-v3.ico:assets --upx-dir='C:\\Program Files\\upx' ./app/main.py
   ```
