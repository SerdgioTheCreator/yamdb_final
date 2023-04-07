# API для проекта YaMDB в контейнере Docker

## Используемые технологии

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## Описание
>Представляет собой расширение возможностей проекта YaMDB для совершения удаленных операций.
>Благодаря этому проекту зарегистрированные и аутентифицированные пользователи получают возможность 
>оставлять рецензии на произведения различных категорий, комментировать рецензии других пользователей,
> просматривать сформированные на основе оценок рейтинги произведений. Сайт не предоставляет прямой доступ
> или ссылки для ознакомления непосредственно с произведениями.


## Расширение функциональности

Функционал проекта адаптирован для использования PostgreSQL и 
развертывания в контейнерах Docker. 


## Установка

### Шаблон для наполнения .env файла:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<pass>
DB_HOST=db 
DB_PORT=5432 
```

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SerdgioTheCreator/
```
- Создать .env файл по предлагаемому выше шаблону. Обязательно изменить 
значения POSTGRES_USER и POSTGRES_PASSWORD
- Собрать и запустить контейнеры

```
docker-compose up -d --build
```

- После успешной сборки выполнить следующие действия:

выполнить миграции

```
docker-compose exec web python manage.py migrate
```

собрать статику

```
docker-compose exec web python manage.py collectstatic --no-input
```

Создать суперюзера Django,
после запроса от терминала ввести логин и пароль для суперюзера

```
docker-compose exec web python manage.py createsuperuser
```

### Команды для заполнения базы данными
- Заполнить базу данными
- Создать резервную копию данных:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

- Приложение доступно по адресу:

```
http://localhost
```

### Примеры API-запросов
Подробные примеры запросов и коды ответов приведены в прилагаемой
документации в формате ReDoc по адресу:

```
http://localhost/redoc
```

## Авторы: Коновалов Сергей, команда ЯндексПрактикум 
