# Async-chat

## Описание
Утилита позволяющая читать чать по сокету и записывать все сообщения в файл асинхронно.
 А также авторизовываться, регистрироваться и отправлять сообщения.

## Требования

*Python 3.7*


1. Скачать репозиторий:

```sh
git clone https://github.com/Safintim/async-chat.git
cd async-chat 
pip install -r requirements.txt
```

2. Читать чат
```sh
python3 read_chat.py
```

3. Написать сообщение в чат
```sh
python3 write_chat.py -m Hi
```

## Параметры командной строки

- --host (-ht) хост.
- --port (-p) порт.
- --filepath (-f) путь к файлу, куда будут записываться сообщения из чата. (только для read_chat)
- --token (-t) токен авторизации. (только для write_chat)
- --message (-m) сообщение. (только для write_chat)

## Конфигурационный файл

Для сохранения настроек создайте рядом со скриптом файл .env, следующего содержимого:

```sh
HOST=host
READ_PORT=read_port
WRITE_PORT=write_port
TOKEN=token
FILEPATH=~/chat.txt
```