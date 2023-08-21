Проект создания beckend части приложения вэб-сервиса для обучения. В проекте риализовано API с помощью Django REST Framework.
Стэк используемых технологий:
- Python 3.7+
- Django 4.2.2
- DRF 3.14.0
- Requests 2.31.0
- Stripe 5.5.0
- Faker 19.2.0
- PostgreSQL
- Celery 5.3.1
- Redis 5.0.0
- Pillow 2.31.0

  С остальными зависимостями которые используются в проекте можно ознакомиться командой:
```
cat requirements.txt
```
#### Вся документация доступна в Swagger и Redoс:

```
http://localhost:8000 /redoc/ или /swagger/
```


1. #### Клонируем репозиторий себе, либо скачиваем zip файл и распаковываем себе на локальную машину

2. #### Создаем виртуальное окружение.

3. #### Устанавливаем зависимости командой:

```
pip install -r requirements.txt
```

4.  #### Для работы нам понадобится установить и настройть базу данных PostgreSQL и брокера Redis 

5. #### Выполняем миграцию командой:

```
python manage.py migrate
```

6. #### Загрузка данных

- Загружаем тестовые данные командой:

```
python manage.py loaddata testdata.json
```

7. #### Запустить сервер командой:

```
python manage.py runserver 8000
```

8. #### Запускаем телеграм бота командой:

```
python manage.py bot_run
```

9. #### Запуск Celery

```
celery -A config worker -l INFO -P eventlet
```

10. #### Запуск celery-beat

```
celery -A config worker --loglevel=info
```
Для монтирования образа проекта и запуска  в docker используем команду:
```
docker-compose up --build
```
