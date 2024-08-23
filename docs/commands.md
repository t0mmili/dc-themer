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
```sh
pyinstaller --onefile --windowed --clean --name=dc-themer --icon=./assets/dct-icon-v3.ico --add-data=./assets:assets --upx-dir='C:\\Program Files\\upx' ./app/main.py
```
