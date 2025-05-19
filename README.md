# InSDL Create

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Настройка путей

Перед началом работы отредактируйте пути в файле `insdl.bat` к файлу `main.py` и перенесите в директорию с PATH для работы во всей системе _(для ручной установки)_

```bat
@echo off
python YOUR_PATH_TO\main.py %* 
```

### Флаги

- `-h` — выводит список всех доступных команд.
- `-vsc` — добавляет папку `.vscode` с уже настроенным **g++**.
- `-bat` — добавлять файл `compile.bat` к вам в проект

### Команды для создания проекта

```sh
$ insdl create PROJECT_NAME -flag
```

### Удаление проекта

```sh
$ insdl del PROJECT_NAME
```

### Компиляция проекта

```sh
$ insdl compile PROJECT_NAME
```

Или запустите `compiler.bat`