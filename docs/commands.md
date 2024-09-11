# Commands

## Install dependencies
```sh
pip install -r app/requirements.txt
pip install -r tests/requirements.txt
```

## Run app
```sh
python -m app.main
```

## Run tests
```sh
python tests/run_tests.py
```

## Generate requirements
```sh
pipreqs --force ./app
```

## Build binary
```sh
pyinstaller --onefile --windowed --clean --name=dc-themer --icon=./assets/dct-icon-v3.ico --add-data=./assets:assets --upx-dir='C:\\Program Files\\upx' ./app/main.py
```
