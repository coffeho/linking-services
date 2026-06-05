import os
import tempfile

from packages.core.departments import (
    delete_department,
    department_has_employees,
    list_departments,
    save_department,
)
from packages.core.positions import (
    delete_position,
    list_positions,
    position_has_employees,
    save_position,
)
from packages.core.storage import Database


def create_temp_database():
    """
    Создает временную SQLite-базу для теста.

    Database сейчас создает файл hr_system.db в текущей рабочей папке,
    поэтому тест временно переходит во временную директорию.
    """
    temp_dir = tempfile.TemporaryDirectory()
    old_cwd = os.getcwd()
    os.chdir(temp_dir.name)

    database = Database()

    return temp_dir, old_cwd, database


def close_temp_database(temp_dir, old_cwd, database):
    database.conn.close()
    os.chdir(old_cwd)
    temp_dir.cleanup()


def test_list_departments_returns_demo_departments():
    """
    В демонстрационной базе должно быть 5 подразделений.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_departments(database.cursor)

        assert len(rows) == 5
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_department_with_employees_cannot_be_deleted():
    """
    Подразделение, в котором есть сотрудники, нельзя удалить.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        assert department_has_employees(database.cursor, 1) is True

        ok, msg = delete_department(database.cursor, database.conn, 1)

        assert ok is False
        assert "сотрудники" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_save_department_creates_new_department():
    """
    Новое подразделение должно сохраняться в базе.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = save_department(database.cursor, database.conn, "Юридический отдел")

        assert ok is True
        assert "сохранены" in msg.lower()

        rows = list_departments(database.cursor)
        assert any(row[1] == "Юридический отдел" for row in rows)
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_positions_returns_demo_positions():
    """
    В демонстрационной базе должно быть 7 должностей.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_positions(database.cursor)

        assert len(rows) == 7
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_position_with_employees_cannot_be_deleted():
    """
    Должность, на которой есть сотрудники, нельзя удалить.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        assert position_has_employees(database.cursor, 1) is True

        ok, msg = delete_position(database.cursor, database.conn, 1)

        assert ok is False
        assert "сотрудники" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_save_position_rejects_invalid_salary():
    """
    Должность с некорректной зарплатой не должна сохраняться.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = save_position(database.cursor, database.conn, "Юрист", "не число")

        assert ok is False
        assert "зарплата" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_save_position_creates_new_position():
    """
    Новая должность с корректной зарплатой должна сохраняться.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = save_position(database.cursor, database.conn, "Юрист", "80000")

        assert ok is True
        assert "сохранены" in msg.lower()

        rows = list_positions(database.cursor)
        assert any(row[1] == "Юрист" for row in rows)
    finally:
        close_temp_database(temp_dir, old_cwd, database)