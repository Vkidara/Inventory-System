# Inventory System

Backend-система для управления складскими запасами.

## Возможности

- создание и управление складами;
- создание товаров;
- учёт количества товаров;
- приход товаров;
- расход товаров;
- перемещение товаров между складами;
- проверка достаточности остатка;
- история движений товаров;
- REST API;
- автоматические тесты;
- миграции базы данных.

## Стек

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest
- Docker / Docker Compose

## Структура проекта

```text
inventory_system/
├── alembic/
│   └── versions/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── README.md

Запуск проекта

1. Клонирование
git clone https://github.com/Vkidara/Inventory-System.git
cd Inventory-System

2. Создание виртуального окружения
python -m venv venv
.\venv\Scripts\Activate.ps1

3. Установка зависимостей
pip install -r requirements.txt

4. Настройка переменных окружения
Создать файл .env на основе .env.example.

5. Запуск PostgreSQL
docker compose up -d

6. Применение миграций
alembic upgrade head

7. Запуск приложения
uvicorn app.main:app --reload

После запуска API будет доступно по адресу: http://127.0.0.1:8000
Документация Swagger: http://127.0.0.1:8000/docs

Тестирование
pytest

Все тесты должны завершиться успешно.

Миграции

Создание новой миграции:
alembic revision --autogenerate -m "description"

Применение миграций:
alembic upgrade head

Проверка текущей версии:
alembic current

Пример .env:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=inventory_db
POSTGRES_PORT=5432