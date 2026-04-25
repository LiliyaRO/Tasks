# Задача 2 - API (todo)

Простой API на ~FastAPI~~ с использованием ~JSON-хранилища~~~ 

#  Функционал

- Создание записи (задачи)
- Чтение записи
- Просмотр списка записей
- Удаление записи

#  Технологии

- Python 3.12
- FastAPI
- SQLAlchemy
- Json

#  Запуск локально

### 1. Клонировать репозиторий

~~~bash
git clone https://github.com/LiliyaRO/Tasks/tree/079f14e83d6cef2fd2e496aa8d3f040b77c5776c/task2
cd task2
~~~


### 2. Установить зависимости

~~~bash
python -m venv venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate    # Windows

pip install -r requirements.txt
~~~

### 3. Запустить сервер

~~~bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
~~~

После запуска приложение доступно по адресу:
 http://localhost:8000/docs#/


#  Структура проекта

~~~
.
├── main.py              # Точка входа FastAPI
├── database.py          # Подключение к базе данных
├── models.py            # модели задач
├── schemas.py           # схемы задач
├── tasks.json           # хранилище задач
├── requirements.txt     # Зависимости
└── README.md            # Вы здесь
└── .gitignore           # откл отслеживание
~~~






