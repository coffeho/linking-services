import os
import tempfile

from packages.core.orders import create_or_update_order, execute_order
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


def get_employee_status(cursor, employee_id: int):
    return cursor.execute(
        "SELECT status FROM Employees WHERE employee_id = ?",
        (employee_id,),
    ).fetchone()[0]


def get_order_status(cursor, order_id: int):
    return cursor.execute(
        "SELECT status FROM Orders WHERE order_id = ?",
        (order_id,),
    ).fetchone()[0]


def test_dismissal_order_workflow_changes_employee_and_order_status():
    """
    Integration test: создание и исполнение приказа на увольнение.

    Проверяется связка:
    - временная SQLite-база;
    - создание приказа;
    - исполнение приказа;
    - изменение статуса сотрудника;
    - изменение статуса приказа.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        employee_id = 1

        assert get_employee_status(database.cursor, employee_id) == "Работает"

        ok, msg = create_or_update_order(
            database.cursor,
            database.conn,
            "Увольнение",
            "2024-10-01",
            employee_id,
            "Уволить сотрудника по собственному желанию",
            {},
        )

        assert ok is True

        order_id = 4
        assert get_order_status(database.cursor, order_id) == "Не исполнен"

        ok, msg = execute_order(database.cursor, database.conn, order_id)

        assert ok is True
        assert "успешно" in msg.lower()

        assert get_employee_status(database.cursor, employee_id) == "Уволен"
        assert get_order_status(database.cursor, order_id) == "Исполнен"

    finally:
        close_temp_database(temp_dir, old_cwd, database)