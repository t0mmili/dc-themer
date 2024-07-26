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
1. Edit **main.py** and uncomment `icon_path` variable.
2. Run command:
   ```sh
   pyinstaller --onefile --windowed --name=dc-themer --icon=./assets/dct-icon-v3.ico --add-data=./assets/dct-icon-v3.ico:assets ./app/main.py
   ```
