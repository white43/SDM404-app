# Student Task Scheduler

## Installation

1. Clone the repository `git clone https://github.com/white43/SDM404-app`
2. `cd SDM404-app`
3. `pip install -r requirements.txt`

## Run the project

```commandline
python main.py
```

## Run tests

```commandline
export PYTHONPATH="${PYTHONPATH}:${pwd}/src/" && pytest tests/*
```

## Build binary files

```commandline
pyinstaller -F --paths=venv/lib/python3.11/site-packages/ --hidden-import "babel.numbers" --add-data "./assets/*:./assets/" main.py
```
```commandline
pyinstaller.exe -F --paths .\venv\Lib\site-packages\ --hidden-import "babel.numbers" --noconsole –add-data ".\assets\*;.\assets\" --clean main.py
```

## Quality

```commandline
radon mi -s main.py src
```
```commandline
radon cc -s main.py src
```
