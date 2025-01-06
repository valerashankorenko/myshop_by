# myshop_by

## О проекте
Веб приложение для интернет магазина, где можно управлять категориями, подкатегориями и товарами, а так же просматривать товары в каталоге.

## Стек технологий
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLite](https://www.sqlite.org/)

## Как запустить проект локально:
1. Клонировать репозиторий и перейти в его директорию в командной строке:
```shell
git clone git@github.com:valerashankorenko/myshop_by.git
```
2. Переход в директорию myshop_by
```shell
cd myshop_by
```
3. Cоздать и активировать виртуальное окружение:
 - для Linux/MacOS
```shell
python3 -m venv venv
source venv/bin/activate
```
- для Windows
```shell
python -m venv venv
source venv/Scripts/activate
```
4. Обновить пакетный менеджер pip
```shell
python3 -m pip install --upgrade pip
```
5. Установить зависимости из файла requirements.txt:
```shell
pip install -r requirements.txt
```
6. Применение миграций
```shell
python manage.py migrate
```
7. В корневой директории создать файл .env и заполнить своими данными:
```
DJANGO_DEBUG=True(для разработки)
ALLOWED_HOSTS=localhost,127.0.0.1
SECRET_KEY=секретный ключ Django
Данные для суперпользователя
DJANGO_SUPERUSER_USERNAME=your_first_username
DJANGO_SUPERUSER_EMAIL=email
DJANGO_SUPERUSER_PASSWORD=password
DJANGO_SUPERUSER_FIRST_NAME=your_first_name
DJANGO_SUPERUSER_LAST_NAME=your_last_name
DJANGO_SUPERUSER_PHONE_NUMBER=your_phone_number(Формат номера: +375XXXXXXXXX)
```
8. Создать суперпользователя
```shell
python manage.py create_superuser
```
9. Наполнение базы данных тестовыми данными
```shell
python manage.py load_database
```
10. Запуск тестов 
```shell
python manage.py test
```
11. Запуск проекта
```shell
python manage.py runserver
```

## Автор проекта:
Валерий Шанкоренко<br/>
Github: 👉 [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram: 📱 [@valeron007](https://t.me/valeron007)<br/>
E-mail: 📧 valerashankorenko@yandex.by<br/>