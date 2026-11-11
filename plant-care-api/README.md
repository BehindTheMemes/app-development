# ДЗ №9 — API-first проектирование сервиса

## 0. Тема проекта

**Plant Care API** — REST API для управления домашними растениями и графиком их полива.

### Зачем этот API

API нужен, чтобы приложения для ухода за растениями могли единообразно получать, создавать, изменять и удалять данные о растениях пользователя.

---

## 1. OpenAPI-спецификация

Основная спецификация находится в корне проекта:

```text
api.yaml
```

Использована версия **OpenAPI 3.0.3**.

API содержит пять требуемых операций:

| HTTP-метод | Endpoint | Назначение |
|---|---|---|
| GET | `/plants` | получить список растений |
| GET | `/plants/{plantId}` | получить одно растение |
| POST | `/plants` | создать растение |
| PATCH | `/plants/{plantId}` | изменить данные растения |
| DELETE | `/plants/{plantId}` | удалить растение |

Таким образом, присутствуют все требуемые глаголы: GET для списка, GET для одного объекта, POST, PATCH и DELETE.

### Аутентификация

Для операций используется схема:

```yaml
bearerAuth:
  type: http
  scheme: bearer
  bearerFormat: JWT
```

В API предусмотрен ответ `401 Unauthorized`, когда запрос не содержит корректных данных аутентификации.

Для операций с конкретным растением предусмотрен `404 Not Found`, если растение не существует или недоступно текущему пользователю.

### DTO

Внешние структуры API описаны в:

```text
components:
  schemas:
```

Используются отдельные DTO:

- `PlantCreateRequest` — данные для создания;
- `PlantUpdateRequest` — данные для частичного изменения;
- `PlantResponse` — данные, возвращаемые клиенту;
- `PlantListResponse` — ответ со списком;
- `DeleteResponse` — результат удаления;
- `ErrorResponse` — единый формат ошибки.

Внешний контракт не раскрывает внутреннюю структуру хранения данных.

### Ответы и ошибки

Для каждой операции предусмотрен успешный ответ `200`.

Также присутствуют ошибочные ответы:

- `401` — пользователь не аутентифицирован;
- `404` — объект не найден или недоступен;
- `422` — данные запроса не прошли валидацию.

---

## 2. Кодогенерация

Код был сгенерирован из `api.yaml` с помощью **OpenAPI Generator**.

Использованный генератор:

```text
python-flask
```

Команда генерации:

```powershell
openapi-generator-cli generate -i api.yaml -g python-flask -o generated_service
```

В результате OpenAPI Generator создал каталог:

```text
generated_service/
```

Внутри находится сгенерированный серверный каркас на Python с Flask/Connexion:

```text
generated_service/
├── openapi_server/
│   ├── controllers/
│   ├── models/
│   ├── openapi/
│   └── test/
├── .openapi-generator/
├── Dockerfile
├── README.md
├── requirements.txt
├── setup.py
└── ...
```

### Важно

`generated_service` — результат работы OpenAPI Generator. Поэтому в нём нет отдельного `app.py`.

Точка запуска сгенерированного сервера:

```text
generated_service/openapi_server/__main__.py
```

Сам сгенерированный `openapi_server/openapi/openapi.yaml` является копией/обработанной версией исходного контракта, которую использует Connexion.

Сгенерированные контроллеры содержат заглушки вида:

```python
return 'do some magic!'
```

Это нормально: `python-flask` генерирует **серверный каркас**, а не готовую бизнес-логику. Реализация хранения растений и бизнес-правил в рамках данного задания не требуется.

---

## 3. Установка и запуск

### Требования

Для запуска необходимы:

- Python;
- Java 11+ для OpenAPI Generator;
- OpenAPI Generator CLI.

Генерация уже была выполнена, поэтому Java необходима только если нужно повторно сгенерировать `generated_service`.

### Установка зависимостей

Перейти в каталог сгенерированного сервиса:

```powershell
cd generated_service
```

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать его в Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

### Запуск

Из каталога `generated_service` выполнить:

```powershell
python -m openapi_server
```

После запуска сервер работает на:

```text
http://localhost:8080
```

Swagger UI:

```text
http://localhost:8080/ui/
```

OpenAPI JSON:

```text
http://localhost:8080/openapi.json
```

---

## 4. Проверка API

После запуска сервера можно проверить endpoint списка:

```powershell
curl.exe http://localhost:8080/plants `
  -H "Authorization: Bearer test-token"
```

Проверка получения одного растения:

```powershell
curl.exe http://localhost:8080/plants/3fa85f64-5717-4562-b3fc-2c963f66afa6 `
  -H "Authorization: Bearer test-token"
```

Создание растения:

```powershell
curl.exe -X POST http://localhost:8080/plants `
  -H "Authorization: Bearer test-token" `
  -H "Content-Type: application/json" `
  -d '{"name":"Ficus","species":"Ficus elastica","wateringIntervalDays":10}'
```

Изменение:

```powershell
curl.exe -X PATCH http://localhost:8080/plants/3fa85f64-5717-4562-b3fc-2c963f66afa6 `
  -H "Authorization: Bearer test-token" `
  -H "Content-Type: application/json" `
  -d '{"wateringIntervalDays":14}'
```

Удаление:

```powershell
curl.exe -X DELETE http://localhost:8080/plants/3fa85f64-5717-4562-b3fc-2c963f66afa6 `
  -H "Authorization: Bearer test-token"
```

Поскольку сгенерированные контроллеры являются заглушками, эти запросы проверяют прежде всего маршрутизацию и соответствие серверного каркаса OpenAPI-контракту. Полноценная бизнес-логика в контроллерах для задания не требуется.

---

## 5. Как делали

### Использование AI

Для проектирования использовался AI-ассистент.

Итоговый промт:

> Придумай небольшой самостоятельный REST API для сервиса ухода за домашними растениями. Нужна OpenAPI 3.0 спецификация с GET списка, GET одного объекта, POST, PATCH и DELETE. Для каждого endpoint добавь summary, параметры, 200 и минимум один ошибочный статус. Используй Bearer authentication и DTO в components.schemas. Внутренние структуры хранения не должны попадать во внешний контракт. Подготовь Python Flask service skeleton, соответствующий этой спецификации.

### Что было сделано вручную

После генерации были проверены и при необходимости исправлены:

- структура OpenAPI 3.0.3;
- набор HTTP-методов;
- `summary` у операций;
- path/query-параметры;
- request body;
- успешные и ошибочные ответы;
- DTO в `components.schemas`;
- схема Bearer-аутентификации;
- соответствие generated service исходной спецификации;
- README и инструкции запуска.

Кодогенерация выполнялась командой:

```powershell
openapi-generator-cli generate -i api.yaml -g python-flask -o generated_service
```

---

## 7. Проверка спецификации

`api.yaml` можно открыть в Swagger Editor:

1. Открыть `editor.swagger.io`.
2. Вставить содержимое `api.yaml`.
3. Проверить отсутствие ошибок в OpenAPI-документе.

Дополнительно спецификацию можно импортировать в Postman:

**Import → OpenAPI**

После импорта Postman создаст коллекцию запросов на основе API-контракта.

---

## 8. Структура проекта

```text
plant-care-api/
├── api.yaml
├── README.md
├── generate.ps1
├── generate.sh
├── .gitignore
└── generated_service/
    ├── openapi_server/
    │   ├── controllers/
    │   ├── models/
    │   ├── openapi/
    │   └── test/
    ├── .openapi-generator/
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    └── ...
```

Файлы `.openapi-generator/`, `openapi_server/models/`, `openapi_server/controllers/` и остальные файлы внутри `generated_service` оставлены, поскольку они являются результатом работы OpenAPI Generator.

Файл `api.yaml` является исходной спецификацией проекта и должен оставаться в корне репозитория.
