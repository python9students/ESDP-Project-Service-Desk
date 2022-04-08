# ESDP Project - Service Desk

Для запуска проекта установите python версии 3.10.0 и pip

После клонирования перейдите в склонированную папку и выполните следующие команды:

Создайте виртуальное окружение командой
```bash
python -m venv venv
```

Активируйте виртуальное окружение командой
```bash
source venv/bin/activate
или
venv\Scripts\activate
```

Установите зависимости командой

```bash
pip install -r requirements.txt
```

Создайте в директории с проектом файл .env и заполните по примеру:

MYSQL_DATABASE=db_name

MYSQL_USERNAME=username

MYSQL_HOST=host

MYSQL_PORT=port

MYSQL_PASSWORD=password

SECRET_KEY=secret_key


Чтобы запустить сервер выполните:

```bash
./manage.py runserver
```

на данный момент на проекте отсутсвуют приложения...