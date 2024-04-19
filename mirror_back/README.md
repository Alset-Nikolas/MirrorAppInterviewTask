# Mirror Backend

## Деплой на проде

1. ` cp .env-template .env` и заполняем нужными конфигами файл .env

## PyCharm Remote Debugging используя локальный интерпретатор

В корне проекта:

1. Ставим pyenv для активации python 3.9.13 https://linux-notes.org/ustanovka-pyenv-v-unix-linux/

   3.1. Обновляем pyenv `cd /home/znbiz/.pyenv/plugins/python-build/../.. && git pull && cd -`

   3.2. Ставим нужную версию python `pyenv install 3.9.13` (инструкция для mac в случае проблемы
   установки https://github.com/pyenv/pyenv/issues/1740#issuecomment-814001188 )

   3.3. Устанавливаем плагин
   pyenv-virtualenv https://www.liquidweb.com/kb/how-to-install-pyenv-virtualenv-on-ubuntu-18-04/

   3.4. Локально в папке с проектом прописываем версию python `pyenv local 3.9.13`

   3.5. Перезагружаем терминал

   3.6. Создаём песочницу `pyenv virtualenv 3.9.13 mirror_back_3.9.13`

   3.7. Активируем песочницу `pyenv activate mirror_back_3_3.9.13`
   Если у вас mac, то на этой команде может возникнуть ошибка тут поможет следущие команды `eval "$(pyenv init -)"` и 
   `eval "$(pyenv virtualenv-init -)"`. После снова пробуем выполнить активацию окружения
   3.8. Устанавливаем poetry `pip install poetry==1.2.2`

2. poetry install
3. Дальше задаём интерпретатор в PyCharm
   `File -> Settings -> Project: main -> Project Interpreter ->
   (нажимаем на шестерёнку) -> Add ->  System Interpreter ->
   (заполняем в поле "Interpreter" ставим путь до интерпретатора, который
   установили через pipenv, в моём случае это
   "/home/znbiz/.pyenv/versions/3.7.6/envs/mirror_back_3_3.9.13/bin/python3.9") -> Ok -> Ok`
4. Запускаем rest в PyCharm `Run -> Run "run_rest"`

## Добавление новых зависимостей

Добавляем новую зависимость

```shell
poetry add <библиотека>=<версия>
```

Образ собирается через **poetry**, обновлять **requirements** не нужно

## Создание и накатывание миграций

```shell
alembic revision --autogenerate -m "Added account table"
alembic upgrade heads
```
