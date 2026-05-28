# CRM MVP

Новый MVP CRM на Django с одним базовым Django app `crm`.

## Архитектура

Базовая CRM реализована внутри одного приложения:

```text
config/
crm/
  models/
  views/
  forms/
  services/
  api/
  templates/crm/
  static/crm/
```

Отдельные Django apps для клиентов, сделок, заказов, товаров, задач и уведомлений не используются.

## Стек

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Django Templates
- HTMX
- Alpine.js
- Bootstrap 5 + кастомный CSS

React, Next.js и Vue не используются.

## Что входит в MVP

- Авторизация пользователей.
- Профили и роли: администратор, руководитель, менеджер, склад / производство.
- Красивый layout: sidebar, topbar, карточки, таблицы, фильтры, badge.
- Dashboard с KPI, новыми сделками, просроченными задачами, заказами и историей.
- CRUD для клиентов.
- CRUD для сделок и pipeline с drag-and-drop сменой этапа.
- CRUD для заказов и позиций заказов.
- CRUD для товаров.
- CRUD для задач.
- Центр внутренних уведомлений.
- История действий пользователей.
- Настройки: этапы, пользовательские поля, заготовки интеграций.
- REST API под `/api/`.
- Docker Compose для Django, PostgreSQL, Redis и Celery.

## Запуск через Docker Compose

```bash
docker compose up --build
```

В другом терминале создайте администратора:

```bash
docker compose exec web python manage.py createsuperuser
```

Откройте:

- CRM: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/

## Локальный запуск без Docker

```bash
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Если `DATABASE_URL` не задан, используется SQLite. В Docker используется PostgreSQL из `docker-compose.yml`.

## Проверка после запуска

1. Войти через `/login/`.
2. Открыть dashboard `/`.
3. Создать клиента `/clients/new/`.
4. Создать товар `/products/new/`.
5. Создать сделку `/deals/new/`.
6. Перетащить сделку между этапами на `/deals/`.
7. Создать заказ из карточки сделки.
8. Добавить позицию в заказ.
9. Создать задачу `/tasks/new/`.
10. Проверить уведомления `/notifications/`.
11. Проверить историю в `/settings/`.
12. Проверить API `/api/clients/`.

## Celery

Worker:

```bash
celery -A config worker -l info
```

Beat:

```bash
celery -A config beat -l info
```

Celery использует `REDIS_URL`.
