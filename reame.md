Платформа питомника включает в себя разделы:

- Породы
- Собаки
- Пользователи
- Отзывы

Виртуальное окружение используемое для проекта: venv

1) После настройки виртуального окружения установите зависимости из файла [requirements.txt](requirements.txt)
 
```bash
pip install -r requirements.txt
```

2) Заполните .env файл согласно файла .env_sample
3) Создайте базу данных при помощи команды

```bash
python manage.py ccdb
```

4) Создайте миграции при помощи команды 

```bash
python manage.py makemigrations
 ```

5) Примените созданные миграции

```bash
python manage.py migrate
 ```

6) Выполните команду для создания основных пользователей

```bash
python manage.py ccsu
 ```

7) Выполните команду для заполнения базы данных

```bash
python manage.py loaddata dogs.json
 ```

8) Выполните команду для запуска redis сервера

```bash
redis-server
 ```

9) Выполните команду для запуска приложения, желательно
в отдельном терминале
 
 ```bash
python manage.py runserver
 ```