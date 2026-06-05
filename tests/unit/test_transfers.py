import os
import tempfile

from packages.core.storage import Database
from packages.core.transfers import (
    create_transfer,
    delete_transfer,
    get_employee_department_id,
    list_departments_for_transfer,
    list_transfers,
    list_working_employees_with_department,
)


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


def test_list_transfers_returns_empty_initially():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_transfers(database.cursor)

        assert rows == []
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_working_employees_with_department_returns_demo_employees():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_working_employees_with_department(database.cursor)

        assert len(rows) == 15
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_departments_for_transfer_returns_demo_departments():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_departments_for_transfer(database.cursor)

        assert len(rows) == 5
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_get_employee_department_id_returns_current_department():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        department_id = get_employee_department_id(database.cursor, 1)

        assert department_id == 3
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_create_transfer_rejects_same_department():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        old_department_id = get_employee_department_id(database.cursor, 1)

        ok, msg = create_transfer(
            database.cursor,
            database.conn,
            1,
            old_department_id,
            "2024-10-01",
        )

        assert ok is False
        assert "уже" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_create_transfer_changes_employee_department_and_saves_history():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        old_department_id = get_employee_department_id(database.cursor, 1)
        assert old_department_id == 3

        ok, msg = create_transfer(
            database.cursor,
            database.conn,
            1,
            2,
            "2024-10-01",
        )

        assert ok is True
        assert "выполнен" in msg.lower()

        new_department_id = get_employee_department_id(database.cursor, 1)
        assert new_department_id == 2

        rows = list_transfers(database.cursor)
        assert len(rows) == 1
        assert rows[0][0] == 1
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_create_transfer_rejects_unknown_employee():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = create_transfer(
            database.cursor,
            database.conn,
            999,
            2,
            "2024-10-01",
        )

        assert ok is False
        assert "не найден" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_delete_transfer_removes_transfer_record():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        create_transfer(
            database.cursor,
            database.conn,
            1,
            2,
            "2024-10-01",
        )

        rows_before = list_transfers(database.cursor)
        assert len(rows_before) == 1

        ok, msg = delete_transfer(database.cursor, database.conn, 1)

        assert ok is True
        assert "удал" in msg.lower()

        rows_after = list_transfers(database.cursor)
        assert rows_after == []
    finally:
        close_temp_database(temp_dir, old_cwd, database)