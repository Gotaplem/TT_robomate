Запуск локально

1. Клонируем репозиторий и переходим в папку проекта:
git clone https://github.com/Gotaplem/TT_robomate.git
cd TT_robomate

2. Создаём виртуальное окружение и активируем его:
python -m venv venv
.\venv\Scripts\activate  - Windows
 source venv/bin/activate  - Linux / Mac

3. Устанавливаем зависимости:
pip install -r requirements.txt

4. Запускаем сервис:
uvicorn app.main:app --reload

5. Открываем документацию Swagger:
http://127.0.0.1:8000/docs

Загрузка CSV:
python import_events.py path/to/events.csv

Запуск unit и integration тестов:
pytest tests/

test_idempotency.py — проверка идемпотентности POST /events
test_integration.py — интеграционный тест «ингест → DAU»

Docker если нужно:
docker-compose up --build
Поднимется на http://127.0.0.1:8000