# Диаграммы проекта

Диаграммы хранятся в редактируемом формате Mermaid (`.mmd`).

Они описывают текущее состояние HR System и ключевые сценарии работы.

## Контекстная диаграмма

Исходник:

```text
docs/diagrams/context.mmd
```

Контекстная диаграмма показывает пользователей, приложение, core-модули, SQLite, тесты, документацию и Makefile.

## Use-case диаграмма

Исходник:

```text
docs/diagrams/use_cases.mmd
```

Use-case диаграмма показывает роли пользователей и основные сценарии HR-системы.

## Sequence-диаграмма авторизации

Исходник:

```text
docs/diagrams/auth_sequence.mmd
```

Диаграмма показывает процесс входа пользователя в систему через `app/ui/main_window.py`, `packages/core/auth.py` и SQLite.

## Sequence-диаграмма исполнения приказа

Исходник:

```text
docs/diagrams/order_execution_sequence.mmd
```

Диаграмма показывает исполнение кадрового приказа через `packages/core/orders.py` и SQLite.