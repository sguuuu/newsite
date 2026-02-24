# Бэкенд — Школа финансовой культуры

Django REST API для платформы олимпиад и конкурсов по финансовой грамотности.

## Быстрый старт

```bash
# 1. Перейти в папку бэкенда
cd backend

# 2. Активировать виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Установить зависимости (если не установлены)
pip install -r requirements.txt

# 4. Применить миграции
python manage.py migrate

# 5. Создать тестовые данные
python manage.py seed

# 6. Запустить сервер
python manage.py runserver
```

API доступен по адресу: http://localhost:8000/api/
Админ-панель: http://localhost:8000/admin/

---

## Учётные данные (после seed)

| Роль          | Email                  | Пароль     |
|---------------|------------------------|------------|
| Администратор | admin@finansy.ru       | admin123   |
| Педагог       | teacher@finansy.ru     | teacher123 |
| Участник      | student@finansy.ru     | student123 |
| Жюри          | jury@finansy.ru        | jury123    |

---

## Архитектура

```
backend/
├── config/              # Настройки Django
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── users/           # Пользователи, аутентификация
│   ├── events/          # Мероприятия, регистрации, жюри
│   ├── submissions/     # Работы участников, оценки, результаты
│   ├── documents/       # Документы (положения, шаблоны)
│   └── notifications/   # Уведомления
├── media/               # Загруженные файлы (создаётся автоматически)
└── db.sqlite3           # База данных (SQLite)
```

---

## API Endpoints

### Аутентификация (`/api/auth/`)

| Метод  | URL                          | Описание                        | Доступ    |
|--------|------------------------------|---------------------------------|-----------|
| POST   | `/api/auth/login/`           | Вход, получение JWT-токенов     | Все       |
| POST   | `/api/auth/register/`        | Регистрация нового пользователя | Все       |
| POST   | `/api/auth/logout/`          | Выход (инвалидация токена)      | Auth      |
| POST   | `/api/auth/token/refresh/`   | Обновление access-токена        | Все       |
| GET    | `/api/auth/profile/`         | Профиль текущего пользователя   | Auth      |
| PUT    | `/api/auth/profile/`         | Редактировать профиль           | Auth      |
| POST   | `/api/auth/change-password/` | Смена пароля                    | Auth      |
| GET    | `/api/auth/users/`           | Список пользователей            | Admin     |
| POST   | `/api/auth/users/`           | Создать пользователя            | Admin     |
| GET    | `/api/auth/users/{id}/`      | Данные пользователя             | Admin     |
| PUT    | `/api/auth/users/{id}/`      | Редактировать пользователя      | Admin     |
| DELETE | `/api/auth/users/{id}/`      | Удалить пользователя            | Admin     |
| POST   | `/api/auth/users/{id}/block/`| Заблокировать пользователя      | Admin     |
| POST   | `/api/auth/users/{id}/activate/` | Активировать пользователя  | Admin     |
| GET    | `/api/auth/users/stats/`     | Статистика по ролям             | Admin     |

### Мероприятия (`/api/events/`)

| Метод  | URL                                 | Описание                        | Доступ         |
|--------|-------------------------------------|---------------------------------|----------------|
| GET    | `/api/events/`                      | Список мероприятий              | Все            |
| POST   | `/api/events/`                      | Создать мероприятие             | Admin          |
| GET    | `/api/events/{id}/`                 | Детали мероприятия              | Все            |
| PUT    | `/api/events/{id}/`                 | Редактировать                   | Admin          |
| DELETE | `/api/events/{id}/`                 | Удалить                         | Admin          |
| POST   | `/api/events/{id}/register/`        | Зарегистрироваться              | Participant    |
| POST   | `/api/events/{id}/unregister/`      | Отменить регистрацию            | Participant    |
| GET    | `/api/events/{id}/participants/`    | Список участников               | Admin/Teacher  |
| GET    | `/api/events/{id}/stats/`           | Статистика мероприятия          | Admin          |
| POST   | `/api/events/{id}/assign_jury/`     | Назначить жюри                  | Admin          |
| GET    | `/api/events/my-registrations/`     | Мои регистрации                 | Auth           |
| GET    | `/api/events/dashboard-stats/`      | Статистика для дашборда         | Auth           |
| GET    | `/api/events/jury-assignments/`     | Назначения жюри                 | Auth           |

### Работы и оценки (`/api/submissions/`)

| Метод  | URL                                        | Описание                   | Доступ      |
|--------|--------------------------------------------|----------------------------|-------------|
| GET    | `/api/submissions/`                        | Список работ               | Auth        |
| POST   | `/api/submissions/`                        | Загрузить работу           | Participant |
| GET    | `/api/submissions/{id}/`                   | Детали работы              | Auth        |
| DELETE | `/api/submissions/{id}/`                   | Удалить черновик           | Auth        |
| POST   | `/api/submissions/{id}/submit/`            | Подать работу официально   | Participant |
| POST   | `/api/submissions/{id}/assign_jury/`       | Назначить жюри к работе    | Admin       |
| GET    | `/api/submissions/evaluations/`            | Оценки                     | Auth        |
| POST   | `/api/submissions/evaluations/`            | Создать оценку             | Jury        |
| PUT    | `/api/submissions/evaluations/{id}/`       | Обновить черновик оценки   | Jury        |
| POST   | `/api/submissions/evaluations/{id}/finalize/` | Опубликовать оценку     | Jury        |
| GET    | `/api/submissions/results/`                | Итоговые результаты        | Auth        |
| POST   | `/api/submissions/results/`                | Записать результат         | Admin       |

### Документы (`/api/documents/`)

| Метод | URL                            | Описание                 | Доступ |
|-------|--------------------------------|--------------------------|--------|
| GET   | `/api/documents/`              | Список документов        | Все    |
| POST  | `/api/documents/`              | Загрузить документ       | Admin  |
| GET   | `/api/documents/{id}/`         | Детали документа         | Все    |
| DELETE| `/api/documents/{id}/`         | Удалить документ         | Admin  |
| GET   | `/api/documents/{id}/download/`| Скачать файл             | Auth   |

### Уведомления (`/api/notifications/`)

| Метод | URL                                   | Описание                     | Доступ |
|-------|---------------------------------------|------------------------------|--------|
| GET   | `/api/notifications/`                 | Список уведомлений           | Auth   |
| GET   | `/api/notifications/{id}/`            | Одно уведомление             | Auth   |
| POST  | `/api/notifications/{id}/read/`       | Отметить как прочитанное     | Auth   |
| POST  | `/api/notifications/read-all/`        | Прочитать все                | Auth   |
| GET   | `/api/notifications/unread-count/`    | Количество непрочитанных     | Auth   |

---

## Аутентификация в запросах

Используется JWT (Bearer Token). После входа добавляйте заголовок:

```
Authorization: Bearer <access_token>
```

Пример входа:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@finansy.ru", "password": "admin123"}'
```

---

## Фильтрация и поиск

Большинство списков поддерживают:
- `?search=текст` — полнотекстовый поиск
- `?ordering=поле` / `?ordering=-поле` — сортировка
- `?event_type=olympiad` — фильтр по полю
- `?page=2` — пагинация (20 записей на страницу)

Пример:
```
GET /api/events/?event_type=olympiad&status=active&ordering=-start_date
```
