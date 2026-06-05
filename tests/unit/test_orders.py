import os
import tempfile

from packages.core.orders import (
    create_or_update_order,
    delete_order,
    execute_order,
    list_orders,
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


def test_list_orders_returns_demo_orders():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_orders(database.cursor)

        assert len(rows) == 3
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_create_order_adds_new_order():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = create_or_update_order(
            database.cursor,
            database.conn,
            "Увольнение",
            "2024-10-01",
            1,
            "Уволить сотрудника",
            {},
        )

        assert ok is True
        assert "сохран" in msg.lower()

        rows = list_orders(database.cursor)
        assert len(rows) == 4
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_delete_order_rejects_executed_order():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        database.cursor.execute("UPDATE Orders SET status='Исполнен' WHERE order_id=1")
        database.conn.commit()

        ok, msg = delete_order(database.cursor, database.conn, 1, "Исполнен")

        assert ok is False
        assert "исполн" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_delete_order_removes_not_executed_order():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows_before = list_orders(database.cursor)
        assert len(rows_before) == 3

        ok, msg = delete_order(database.cursor, database.conn, 1, "Не исполнен")

        assert ok is True
        assert "удал" in msg.lower()

        rows_after = list_orders(database.cursor)
        assert len(rows_after) == 2
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_execute_dismissal_order_changes_employee_status():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = create_or_update_order(
            database.cursor,
            database.conn,
            "Увольнение",
            "2024-10-01",
            1,
            "Уволить сотрудника",
            {},
        )
        assert ok is True

        order_id = 4

        ok, msg = execute_order(database.cursor, database.conn, order_id)

        assert ok is True
        assert "успешно" in msg.lower()

        status = database.cursor.execute(
            "SELECT status FROM Employees WHERE employee_id = ?",
            (1,),
        ).fetchone()[0]

        assert status == "Уволен"
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_execute_order_rejects_repeated_execution():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        ok, msg = create_or_update_order(
            database.cursor,
            database.conn,
            "Увольнение",
            "2024-10-01",
            1,
            "Уволить сотрудника",
            {},
        )
        assert ok is True

        order_id = 4

        ok, msg = execute_order(database.cursor, database.conn, order_id)
        assert ok is True

        ok, msg = execute_order(database.cursor, database.conn, order_id)

        assert ok is False
        assert "уже" in msg.lower()
    finally:
        close_temp_database(temp_dir, old_cwd, database)