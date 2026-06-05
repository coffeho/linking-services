import os
import tempfile

from packages.core.storage import Database
from packages.core.vacations import (
    delete_vacation,
    list_active_employees_for_vacation,
    list_vacations,
    save_vacation,
    validate_vacation_dates,
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


def test_list_vacations_returns_demo_vacations():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_vacations(database.cursor)

        assert len(rows) == 5
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_active_employees_for_vacation_returns_working_employees():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_active_employees_for_vacation(database.cursor)

        assert len(rows) == 15
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_validate_vacation_dates_accepts_valid_range():
    ok, msg = validate_vacation_dates("2024-07-01", "2024-07-21")

    assert ok is True
    assert msg == "OK"


def test_validate_vacation_dates_rejects_invalid_format():
    ok, msg = validate_vacation_dates("01.07.2024", "2024-07-21")

    assert ok is False
    assert "формате" in msg


def test_validate_vacation_dates_rejects_end_before_start():
    ok, msg = validate_vacation_dates("2024-07-21", "2024-07-01")

    assert ok is False
    assert "раньше" in msg


def test_save_vacation_creates_new_vacation():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = save_vacation(
            database.cursor,
            database.conn,
            1,
            "2024-10-01",
            "2024-10-10",
            "Ежегодный оплачиваемый",
        )

        assert ok is True
        assert "сохранены" in msg.lower()

        rows = list_vacations(database.cursor)
        assert len(rows) == 6
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_save_vacation_rejects_invalid_range():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = save_vacation(
            database.cursor,
            database.conn,
            1,
            "2024-10-10",
            "2024-10-01",
            "Ежегодный оплачиваемый",
        )

        assert ok is False
        assert "раньше" in msg
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_delete_vacation_removes_vacation():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows_before = list_vacations(database.cursor)
        assert len(rows_before) == 5

        ok, msg = delete_vacation(database.cursor, database.conn, 1)

        assert ok is True
        assert "удал" in msg.lower()

        rows_after = list_vacations(database.cursor)
        assert len(rows_after) == 4
    finally:
        close_temp_database(temp_dir, old_cwd, database)