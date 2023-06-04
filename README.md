# Foodgram

 Умеешь ты озадачить и работёнки поткинуть.....)
 Со всеми замечаниями справился, структуру немного переделал, столкнулся с такой проблемай как циклическая ошибка ипортов,
 ты наверно знаешь про такую, оч не здоровая штука.....+)

 http://158.160.17.206/recipes
![ci/cd_foodgram workflow](https://github.com/doroshenkokb/foodgram-project-react/actions/workflows/my_project_workflows.yml/badge.svg)

## Описание

Cервис Foodgram и API для него. Реализован CI/CD проекта. Пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", скачивать список продуктов в формате '.pdf'

### Доступный функционал

- Аутентификация реализована с помощью стандартного модуля DRF - Authtoken.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.На прочий фунционал наложено ограничение в виде административных ролей и авторства.
- Управление пользователями.
- Возможность получения подробной информации о себе и ее редактирование.
- Возможность подписаться на других пользователей и отписаться от них.
- Получение списка всех тегов и ингредиентов.
- Получение списка всех рецептов, их добавление. Получение, обновление и удаление конкретного рецепта.
- Возможность добавить рецепт в избранное.
- Возможность добавить рецепт в список покупок.
- Возможность скачать список покупок в PDF формате.
- Фильтрация по полям.

#### Реализовано при помощи

- Python 3.7
- Django 3.2.15
- Django Rest Framework 3.12.4
- Docker
- Docker-compose
- PostgreSQL
- Gunicorn
- Nginx
- GitHub Actions
- Выделенный сервер Linux Ubuntu 22.04 с публичным IP

#### Локальный запуск проекта

- Склонировать репозиторий:

```bash
   git clone <название репозитория>
```

```bash
   cd <название репозитория> 
```

Cоздать и активировать виртуальное окружение:

Команда для установки виртуального окружения на Mac или Linux:

```bash
   python3 -m venv env
   source env/bin/activate
```

Команда для Windows:

```bash
   python -m venv venv
   source venv/Scripts/activate
```

- Перейти в директорию infra:

```bash
   cd infra
```

- Создать файл .env по образцу:

```bash
   cp .env.example .env
```

- Выполнить команду для доступа к документации:

```bash
   docker-compose up 
```

Установить зависимости из файла requirements.txt:

```bash
   cd ..
   cd backend
   pip install -r requirements.txt
```

```bash
   python manage.py migrate
```

Заполнить базу тестовыми данными об ингредиентах и тегов :

```bash
   python manage.py load_ingredients
   python manage.py load_tags
```

Создать суперпользователя, если необходимо:

```bash
python manage.py createsuperuser
```

- Запустить локальный сервер:

```bash
   python manage.py runserver
```

#### Установка на удалённом сервере

- Выполнить вход на удаленный сервер
- Установить docker:

```bash
   sudo apt install docker.io
   ```

- Установить docker-compose:

``` bash
    sudo apt install docker-compose     
```

или воспользоваться официальной [инструкцией](https://docs.docker.com/compose/install/)

- Находясь локально в директории infra/, скопировать файлы docker-compose.yml и nginx.conf на удаленный сервер:

```bash
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```

- Для правильной работы workflow необходимо добавить в Secrets данного репозитория на GitHub переменные окружения:

```bash

DOCKER_USERNAME=<имя пользователя DockerHub>
DOCKER_PASSWORD=<пароль от DockerHub>

USER=<username для подключения к удаленному серверу>
HOST=<ip сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш приватный SSH-ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<id вашего Телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```

#### Workflow проекта

- **запускается при выполнении команды git push**
- **tests:** проверка кода на соответствие PEP8.
- **build_and_push_to_docker_hub:** сборка и размещение образа проекта на DockerHub.
- **deploy:** автоматический деплой на боевой сервер и запуск проекта.
- **send_massage:** отправка уведомления пользователю в Телеграм.

#### После успешного результата работы workflow зайдите на боевой сервер

- Примените миграции:

```bash
   sudo docker-compose exec backend python manage.py migrate
```

- Подгружаем статику:

```bash
   sudo docker-compose exec backend python manage.py collectstatic --no-input
```

- Заполните базу тестовыми данными об ингредиентах и тегах:

```bash
   sudo docker-compose exec backend python manage.py load_ingredients
   udo docker-compose exec backend python manage.py load_tags
```

- Создайте суперпользователя:

```bash
   sudo docker-compose exec backend python manage.py createsuperuser
```

Проект доступен по адресу: <http://158.160.17.206/recipes>

Доступ в админку:

```bash
   email - admin@mail.ru
   пароль - 12345
```

Пользователь:

```bash
   email - user1@mail.ru
   пароль - P@ssword12345
```


#### Автор

 [https://github.com/doroshenkokb](http://github.com/doroshenkokb)