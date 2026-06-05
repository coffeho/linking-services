# HR System

Учебный проект: система кадрового учета на Python и Tkinter.

## Текущее состояние

На начальном этапе проект представлял собой один файл `main.py`.

В этом файле находились:

- GUI на Tkinter;
- работа с SQLite;
- авторизация пользователей;
- учет сотрудников;
- подразделения;
- должности;
- отпуска;
- приказы;
- переводы;
- отчеты;
- управление пользователями.

Проект постепенно преобразуется в структурированный инженерный проект согласно требованиям курса.

На текущем этапе уже выделены:

- `app/ui/main_window.py` — основной Tkinter-интерфейс приложения;
- `main.py` — тонкая совместимая обертка для старого запуска `python main.py`;
- `packages/core/storage.py` — работа с SQLite, создание таблиц и начальная загрузка демонстрационных данных;
- `packages/core/auth.py` — авторизация пользователей и хеширование паролей;
- `packages/core/models.py` — доменные модели HR-системы;
- `packages/core/employees.py` — операции чтения, поиска и удаления сотрудников;
- `packages/core/departments.py` — операции подразделений;
- `packages/core/positions.py` — операции должностей;
- `packages/core/vacations.py` — операции отпусков;
- `packages/core/transfers.py` — операции переводов;
- `packages/core/orders.py` — операции кадровых приказов;
- `packages/core/reports.py` — операции формирования отчетов;
- `tests/smoke/` — smoke-тесты базового поведения исходного монолита;
- `tests/unit/` — unit-тесты core-модулей;
- `Makefile` и `scripts/` — единые команды для запуска и проверки проекта;
- `docs/` — проектная документация;
- `mkdocs.yml` — конфигурация сборки документации через MkDocs;
- `Dockerfile` и `infra/compose.yaml` — контейнерная проверка проекта.

## Системные зависимости

Проект проверяется на Python 3.12.

Для Linux/WSL может понадобиться установить Tkinter отдельно:

```bash
sudo apt install -y python3-tk
```

Если виртуальное окружение не создаётся, также установите поддержку `venv`:

```bash
sudo apt install -y python3.12-venv
```

Runtime-зависимости для обычного запуска описаны в:

```text
requirements.txt
```

Dev-зависимости для тестов, покрытия, документации и сборки пакета описаны в:

```text
requirements-dev.txt
```

## Подготовка окружения

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установите зависимости для разработки:

```bash
make setup
```

## Запуск приложения

```bash
make run
```

Команда запускает Tkinter-приложение из:

```text
app/ui/main_window.py
```

Корневой `main.py` оставлен как совместимая обертка, поэтому старый запуск также остается доступен:

```bash
python main.py
```

Для запуска GUI нужен графический интерфейс. В WSL без настроенного `$DISPLAY` команда может завершиться ошибкой:

```text
_tkinter.TclError: no display name and no $DISPLAY environment variable
```

В таком случае для проверки проекта используйте тесты:

```bash
make test
```

## Тестовые аккаунты

- `admin / admin`
- `hr_manager / hr_manager`
- `accountant / accountant`
- `employee / employee`

## Команды проекта

Основные действия выполняются через `Makefile`.

```bash
make help
```

Показывает список доступных команд.

```bash
make setup
```

Устанавливает зависимости для разработки.

```bash
make run
```

Запускает HR-приложение.

```bash
make test
```

Запускает все тесты.

```bash
make smoke-test
```

Запускает smoke-тесты.

```bash
make auth-test
```

Запускает unit-тесты авторизации.

```bash
make coverage
```

Запускает тесты с отчётом покрытия.

```bash
make docs
```

Собирает проектную документацию через MkDocs.

```bash
make build-lib
```

Собирает переиспользуемый core-компонент как Python-пакет.

```bash
make install-lib-local
```

Устанавливает проект локально в editable-режиме.

```bash
make check
```

Выполняет основную проверку проекта: тесты и сборку документации.

```bash
make docker-build
```

Собирает Docker-образ для проверки проекта.

```bash
make docker-check
```

Запускает проверку внутри Docker-контейнера.

```bash
make compose-check
```

Запускает проверку через Docker Compose.

```bash
make clean
```

Удаляет временные файлы.

## Проверка проекта

Базовая проверка после клонирования:

```bash
python3 -m venv .venv
source .venv/bin/activate
make setup
make check
```

Команда `make check` выполняет:

```bash
make test
make docs
```

Ожидаемый результат:

```text
тесты проходят
документация собирается
```

Также можно запускать отдельные группы тестов:

```bash
make smoke-test
make auth-test
python -m pytest tests/unit/test_models.py -v
python -m pytest tests/unit/test_employees.py -v
python -m pytest tests/unit/test_departments_positions.py -v
python -m pytest tests/unit/test_vacations.py -v
python -m pytest tests/unit/test_transfers.py -v
python -m pytest tests/unit/test_orders.py -v
python -m pytest tests/unit/test_reports.py -v
```

## Контейнерная проверка

Tkinter GUI требует графический интерфейс, поэтому контейнер используется для воспроизводимой проверки тестов и документации, а не для открытия окна приложения.

Сборка Docker-образа:

```bash
make docker-build
```

Запуск проверки внутри контейнера:

```bash
make docker-check
```

Проверка через Docker Compose:

```bash
make compose-check
```

## Smoke-тесты

Smoke-тесты фиксируют базовое поведение исходного монолита до рефакторинга.

Они проверяют:

- загрузку `main.py` как модуля без запуска Tkinter-окна;
- наличие совместимых экспортов `Database` и `HRSystemApp`;
- создание основных таблиц SQLite;
- загрузку начальных демонстрационных данных.

Запуск smoke-тестов:

```bash
make smoke-test
```

## Unit-тесты

Unit-тесты проверяют переиспользуемые core-модули отдельно от Tkinter-интерфейса.

На текущем этапе проверяются:

- `packages/core/auth.py` — авторизация и хеширование паролей;
- `packages/core/models.py` — доменные модели;
- `packages/core/employees.py` — операции сотрудников;
- `packages/core/departments.py` и `packages/core/positions.py` — справочники подразделений и должностей;
- `packages/core/vacations.py` — операции отпусков;
- `packages/core/transfers.py` — операции переводов;
- `packages/core/orders.py` — операции приказов;
- `packages/core/reports.py` — операции отчетов.

Пример запуска отдельного тестового файла:

```bash
python -m pytest tests/unit/test_auth.py -v
```

## Документация

Проектная документация находится в папке:

```text
docs/
```

На текущем этапе добавлены:

- `docs/index.md` — главная страница документации;
- `docs/specification.md` — спецификация HR-системы;
- `docs/domain.md` — описание предметной области;
- `docs/architecture.md` — архитектурное описание;
- `docs/team.md` — разделение обязанностей в команде;
- `docs/diagrams.md` — страница с описанием диаграмм;
- `docs/diagrams/` — редактируемые Mermaid-диаграммы.

Документация собирается автоматически через MkDocs:

```bash
make docs
```

Результат сборки помещается в папку:

```text
site/
```

Папка `site/` является сгенерированным артефактом и не хранится в Git.

## Сборка core-компонента

Переиспользуемая логика находится в:

```text
packages/core/
```

Проект содержит `pyproject.toml`, поэтому core-компонент можно установить локально и собрать как Python-пакет.

Локальная установка в editable-режиме:

```bash
make install-lib-local
```

Сборка пакета:

```bash
make build-lib
```

Сгенерированные артефакты сборки помещаются в:

```text
dist/
build/
*.egg-info/
```

Эти файлы не хранятся в Git.

## Текущая структура проекта

```text
.
├── main.py
├── app/
│   └── ui/
│       └── main_window.py
├── packages/
│   └── core/
│       ├── auth.py
│       ├── departments.py
│       ├── employees.py
│       ├── models.py
│       ├── orders.py
│       ├── positions.py
│       ├── reports.py
│       ├── storage.py
│       ├── transfers.py
│       └── vacations.py
├── tests/
│   ├── smoke/
│   │
└── test_database_baseline.py
│   └── unit/
│       ├── test_auth.py
│       ├── test_departments_positions.py
│       ├── test_employees.py
│       ├── test_models.py
│       ├── test_orders.py
│       ├── test_reports.py
│       ├── test_transfers.py
│       └── test_vacations.py
├── docs/
│   ├── index.md
│   ├── specification.md
│   ├── domain.md
│   ├── architecture.md
│   ├── team.md
│   ├── diagrams.md
│   └── diagrams/
│       ├── auth_sequence.mmd
│       ├── context.mmd
│       ├── order_execution_sequence.mmd
│       └── use_cases.mmd
├── infra/
│   └── compose.yaml
├── scripts/
│   ├── build-docs.sh
│   ├── build-lib.sh
│   ├── coverage.sh
│   ├── docker-build.sh
│   ├── docker-test.sh
│   ├── install-lib-local.sh
│   ├── run.sh
│   ├── setup.sh
│   └── test.sh
├── .dockerignore
├── .gitignore
├── .python-version
├── Dockerfile
├── Makefile
├── mkdocs.yml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## История развития

Проект развивается через отдельные ветки и Pull Request.

Уже выполнены этапы:

1. Зафиксирован исходный HR-монолит в `main.py`.
2. Добавлены smoke-тесты базового поведения.
3. Класс `Database` вынесен в `packages/core/storage.py`.
4. Авторизация вынесена в `packages/core/auth.py`.
5. Добавлены unit-тесты авторизации.
6. Добавлены доменные модели в `packages/core/models.py`.
7. Добавлены unit-тесты доменных моделей.
8. Добавлены единые команды через `Makefile`.
9. README дополнен пояснением про запуск Tkinter GUI в WSL.
10. Добавлена спецификация HR-системы.
11. Добавлено описание предметной области.
12. Добавлено архитектурное описание.
13. Описано разделение обязанностей в команде.
14. Добавлена автоматическая сборка документации через MkDocs.
15. Вынесены операции сотрудников в `packages/core/employees.py`.
16. Вынесены операции подразделений и должностей в core-модули.
17. Вынесены операции отпусков в `packages/core/vacations.py`.
18. Вынесены операции переводов в `packages/core/transfers.py`.
19. Вынесены операции приказов в `packages/core/orders.py`.
20. Вынесены операции отчетов в `packages/core/reports.py`.
21. Tkinter-приложение вынесено в `app/ui/main_window.py`, а `main.py` оставлен как тонкая совместимая обертка.
22. Добавлена пакетизация core-компонента через `pyproject.toml`.
23. Добавлена контейнерная проверка проекта.
24. Добавлены диаграммы проекта в редактируемом формате Mermaid.

## Ограничения текущей версии

Проект находится в процессе рефакторинга.

На текущем этапе:

- Tkinter-интерфейс уже вынесен в `app/ui/main_window.py`, но отдельные формы пока не разделены по файлам;
- `main.py` оставлен как совместимая обертка для старого запуска и smoke-тестов;
- `packages/core` содержит основную переиспользуемую логику, но слой хранения `storage.py` пока находится внутри core;
- контейнер используется для проверки тестов и документации, а не для запуска GUI;
- integration-тесты пока не добавлены.

Дальнейшие шаги:

- разделить Tkinter-формы по файлам внутри `app/ui`;
- добавить integration-тесты;
- при необходимости вынести SQLite-слой из `packages/core/storage.py` в отдельный адаптер;
- расширить контейнерное окружение при появлении внешней инфраструктуры.