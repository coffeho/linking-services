import os
import tempfile

from packages.core.employees import (
    delete_employee,
    employee_exists,
    list_employees,
)
from packages.core.storage import Database


def create_temp_database():
    temp_dir = tempfile.TemporaryDirectory()
    old_cwd = os.getcwd()
    os.chdir(temp_dir.name)

    database = Database()

    return temp_dir, old_cwd, database


def close_temp_database(temp_dir, old_cwd, database):
    database.conn.close()
    os.chdir(old_cwd)
    temp_dir.cleanup()


def test_list_employees_returns_initial_demo_employees():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_employees(database.cursor)

        assert len(rows) == 15
        assert rows[0][0] == 1
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_employees_filters_by_last_name():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_employees(database.cursor, "Иванов")

        assert len(rows) >= 1
        assert any("Иванов" in row[1] for row in rows)
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_employees_filters_by_first_name():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_employees(database.cursor, "Анна")

        assert len(rows) >= 1
        assert any("Анна" in row[2] for row in rows)
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_employee_exists_returns_true_for_existing_employee():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        assert employee_exists(database.cursor, 1) is True
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_delete_employee_removes_employee_from_database():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        assert employee_exists(database.cursor, 1) is True

        delete_employee(database.cursor, database.conn, 1)

        assert employee_exists(database.cursor, 1) is False
    finally:
        close_temp_database(temp_dir, old_cwd, database)