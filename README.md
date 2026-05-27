# CRM MVP

Модульный Django-монолит CRM по ТЗ из Excel.

## Стек

- Django 5
- Django REST Framework
- PostgreSQL
- Redis
- Celery + Celery Beat
- Django Channels
- Django Templates + HTMX + Alpine.js + Bootstrap 5

React, Next.js, Vue и микросервисы не используются.

## Реализовано в MVP

- вход в систему через стандартную Django-авторизацию;
- пользователи и роли: администратор, руководитель, менеджер, склад / производство;
- карточки клиентов с контактами, адресами, ответственным, тегами и файлами;
- воронка сделок с этапами из ТЗ и drag-and-drop сменой этапа;
- сделки с товарами и автоматическим подсчетом суммы;
- создание заказа из сделки;
- заказы со статусами оплаты, доставки и работы;
- каталог товаров и категорий;
- задачи с дедлайном, приоритетом, статусом и уведомлениями;
- внутренний центр уведомлений;
- история действий пользователей;
- базовая структура интеграций: Новая Почта, Telegram, Instagram, телефония;
- dashboard и базовая аналитика;
- admin-настройки для этапов, статусов, пользовательских полей и модулей;
- REST API под `/api/`.

## Запуск через Docker Compose

1. Скопируйте `.env.example` в `.env` при необходимости и поменяйте `SECRET_KEY`.
2. Запустите контейнеры:

```bash
docker compose up --build
```

3. Создайте администратора:

```bash
docker compose exec web python manage.py createsuperuser
```

4. Откройте:

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

Если `DATABASE_URL` не задан, проект использует SQLite для локальной разработки.

## Модули проекта

- `users` - пользователи и роли;
- `dashboard` - главный экран и KPI;
- `clients` - база клиентов;
- `deals` - воронка и сделки;
- `orders` - заказы;
- `products` - товары и категории;
- `tasks` - задачи;
- `notifications` - внутренние уведомления;
- `integrations` - подготовка интеграций;
- `analytics` - отчеты;
- `activity_log` - история действий;
- `crm_settings` - настройки CRM.

## API

Все основные сущности доступны через DRF router:

- `/api/users/`
- `/api/clients/`
- `/api/products/`
- `/api/deal-stages/`
- `/api/deals/`
- `/api/orders/`
- `/api/tasks/`
- `/api/notifications/`
- `/api/integrations/providers/`
- `/api/integrations/events/`
- `/api/integrations/shipments/`

API использует session/basic authentication и требует авторизации.
