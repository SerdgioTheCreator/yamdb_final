# API для проекта YaMDB в контейнере Docker

## Используемые технологии

[![yamdb_workflow](https://github.com/SerdgioTheCreator/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/SerdgioTheCreator/yamdb_final/actions/workflows/yamdb_workflow.yml)
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
ALLOWED_HOSTS=localhost
DEBUG=False
DB=False #True для sqlite3
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<pass>
DB_HOST=db 
DB_PORT=5432 
```

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SerdgioTheCreator/yamdb_final
```
- Выполнить вход на удаленный сервер
- Установить docker на сервер:

```
apt install docker.io 
```
- Установить docker-compose на сервер:

```
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
- Локально отредактировать файл infra/nginx/default.conf, обязательно в строке server_name вписать IP-адрес сервера
- Скопировать файлы docker-compose.yaml и default.conf из директории infra на сервер:

```
scp docker-compose.yaml <username>@<host>:/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>:/home/<username>/nginx/default.conf
```

- Создать .env файл по предлагаемому выше шаблону. Обязательно изменить 
значения POSTGRES_USER и POSTGRES_PASSWORD
- Для работы с Workflow добавить в Secrets GitHub переменные окружения для работы:
```
DB_ENGINE=django.db.backends.postgresql
ALLOWED_HOSTS=<IP адрес сервера>
DEBUG=False
DB=False #True для sqlite3
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<pass>
DB_HOST=db 
DB_PORT=5432 

DOCKER_USERNAME=<имя пользователя>    
DOCKER_PASSWORD=<пароль от DockerHub>
    
SECRET_KEY=<секретный ключ проекта django>
USER=<username для подключения к серверу>
HOST=<IP адрес сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>
TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```
Workflow состоит из четырёх шагов:
1. Проверка кода на соответствие PEP8 
2. Сборка и публикация образа бекенда на DockerHub. 
3. Автоматический деплой на удаленный сервер. 
4. Отправка уведомления в телеграм-чат.

- собрать и запустить контейнеры на сервере:
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

- Ссылка на развернутый в облаке проект  

```
http://158.160.9.241/
```

### Примеры API-запросов
Подробные примеры запросов и коды ответов приведены в прилагаемой
документации в формате ReDoc по адресу:

```
http://localhost/redoc
```

## Авторы: Коновалов Сергей, команда ЯндексПрактикум 
