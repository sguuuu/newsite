# Запуск проекта

## Каждый раз при запуске (ежедневно)

Открыть **3 терминала** и выполнить по одному в каждом:

### Терминал 1 — MariaDB
```powershell
# Запустить сервер базы данных
Start-Process -FilePath "C:\Program Files\MariaDB 12.2\bin\mysqld.exe" -ArgumentList "--defaults-file=C:\Program Files\MariaDB 12.2\data\my.ini" -WindowStyle Hidden
```
> Оставить терминал открытым. MariaDB работает в фоне.

### Терминал 2 — Бэкенд (Django)
```bash
cd C:\Users\user\PycharmProjects\PythonProject28\backend
venv\Scripts\activate
python manage.py runserver
```
> Сервер доступен на http://localhost:8000

### Терминал 3 — Фронтенд (Vue.js)
```bash
cd C:\Users\user\PycharmProjects\PythonProject28\frontend
npm run dev
```
> Приложение доступно на http://localhost:5173

---

## Тестовые пользователи

| Email | Пароль | Роль |
|-------|--------|------|
| admin@finansy.ru | admin123 | Администратор |
| teacher@finansy.ru | teacher123 | Педагог |
| student@finansy.ru | student123 | Участник |
| jury@finansy.ru | jury123 | Жюри |

---

## Первоначальная настройка (только один раз)

### 1. MariaDB — установка и создание БД

```powershell
# Установить MariaDB
winget install MariaDB.Server --accept-source-agreements --accept-package-agreements

# Запустить (первый раз)
Start-Process -FilePath "C:\Program Files\MariaDB 12.2\bin\mysqld.exe" -ArgumentList "--defaults-file=C:\Program Files\MariaDB 12.2\data\my.ini" -WindowStyle Hidden

# Создать базу данных (подождать 5 секунд после запуска)
& "C:\Program Files\MariaDB 12.2\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS finansovaya_kultura CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 2. Бэкенд — установка зависимостей и миграции

```bash
cd C:\Users\user\PycharmProjects\PythonProject28\backend

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Загрузить тестовые данные
python manage.py seed
```

### 3. Фронтенд — установка пакетов

```bash
cd C:\Users\user\PycharmProjects\PythonProject28\frontend
npm install
```

---

## Остановка MariaDB

```powershell
& "C:\Program Files\MariaDB 12.2\bin\mysqladmin.exe" -u root shutdown
```

---

## Настройки .env (backend/.env)

```
DB_ENGINE=mariadb
DB_NAME=finansovaya_kultura
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:5500,http://localhost:5173,http://127.0.0.1:5173
```
