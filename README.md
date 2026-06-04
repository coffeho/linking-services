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

Уже выделены:

- `packages/core/storage.py` — работа с SQLite, создание таблиц и начальная загрузка демонстрационных данных;
- `packages/core/auth.py` — авторизация пользователей и хеширование паролей;
- `tests/smoke/` — smoke-тесты базового поведения исходного монолита;
- `tests/unit/test_auth.py` — unit-тесты авторизации;
- `Makefile` и `scripts/` — единые команды для запуска и проверки проекта.

## Системные зависимости

Для Linux/WSL может понадобиться установить Tkinter отдельно:

```bash
sudo apt install -y python3-tk
```

Если виртуальное окружение не создаётся, также установите поддержку `venv`:

```bash
sudo apt install -y python3.12-venv
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

Команда запускает Tkinter-приложение из `main.py`.

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
make clean
```

Удаляет временные файлы.

## Проверка проекта

Базовая проверка после клонирования:

```bash
python3 -m venv .venv
source .venv/bin/activate
make setup
make test
```

Ожидаемый результат:

```text
9 passed
```

Также можно запускать отдельные группы тестов:

```bash
make smoke-test
make auth-test
```

Ожидаемый результат:

```text
make smoke-test — 3 passed
make auth-test — 6 passed
```

## Smoke-тесты

Smoke-тесты фиксируют базовое поведение текущего монолита до рефакторинга.

Они проверяют:

- загрузку `main.py` как модуля без запуска Tkinter-окна;
- наличие классов `Database` и `HRSystemApp`;
- создание основных таблиц SQLite;
- загрузку начальных демонстрационных данных.

Запуск smoke-тестов:

```bash
make smoke-test
```

## Unit-тесты авторизации

Unit-тесты авторизации проверяют модуль:

```text
packages/core/auth.py
```

Они проверяют:

- стабильность хеширования пароля;
- успешный вход `admin/admin`;
- отказ при неверном пароле;
- отказ при неизвестном логине;
- корректное состояние деактивированного пользователя.

Запуск:

```bash
make auth-test
```

## Текущая структура проекта

```text
.
├── main.py
├── packages/
│   └── core/
│       ├── auth.py
│       └── storage.py
├── tests/
│   ├── smoke/
│   │   └── test_database_baseline.py
│   └── unit/
│       └── test_auth.py
├── scripts/
│   ├── setup.sh
│   ├── run.sh
│   ├── test.sh
│   └── coverage.sh
├── Makefile
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
6. Добавлены единые команды через `Makefile`.
7. README дополнен пояснением про запуск Tkinter GUI в WSL.