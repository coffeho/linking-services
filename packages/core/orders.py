import json
from datetime import datetime


def list_orders(cursor):
    """
    Возвращает список приказов для отображения в GUI.
    """
    cursor.execute(
        """
        SELECT o.order_id, o.order_type, o.order_date,
               e.last_name || ' ' || e.first_name as full_name,
               o.description, o.status
        FROM Orders o
        LEFT JOIN Employees e ON o.employee_id = e.employee_id
        ORDER BY o.order_date DESC, o.order_id DESC
        """
    )
    return cursor.fetchall()


def get_order_details(cursor, order_id: int):
    """
    Возвращает полные данные приказа для исполнения.
    """
    cursor.execute(
        """
        SELECT order_type, employee_id, description, order_date, order_data
        FROM Orders WHERE order_id = ?
        """,
        (order_id,),
    )
    return cursor.fetchone()


def get_order_data(cursor, order_id: int):
    """
    Возвращает JSON-данные приказа.
    """
    cursor.execute(
        "SELECT order_data FROM Orders WHERE order_id = ?",
        (order_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return row[0]


def list_employees_for_order(cursor):
    """
    Возвращает сотрудников для выбора в форме приказа.
    """
    cursor.execute(
        """
        SELECT employee_id, last_name || ' ' || first_name || ' ' || middle_name
        FROM Employees
        ORDER BY last_name
        """
    )
    return cursor.fetchall()


def list_departments_for_order(cursor):
    """
    Возвращает подразделения для динамических полей приказа.
    """
    cursor.execute("SELECT department_id, department_name FROM Departments")
    return cursor.fetchall()


def list_positions_for_order(cursor):
    """
    Возвращает должности для динамических полей приказа.
    """
    cursor.execute("SELECT position_id, position_name FROM Positions")
    return cursor.fetchall()


def create_or_update_order(
    cursor,
    conn,
    order_type: str,
    order_date: str,
    employee_id,
    description: str,
    order_data: dict,
    order_id: int | None = None,
):
    """
    Создает или обновляет приказ.
    """
    order_data_json = json.dumps(order_data, ensure_ascii=False)

    if order_id is None:
        cursor.execute(
            """
            INSERT INTO Orders (order_type, order_date, employee_id, description, order_data, status)
            VALUES (?, ?, ?, ?, ?, 'Не исполнен')
            """,
            (order_type, order_date, employee_id, description, order_data_json),
        )
    else:
        cursor.execute(
            """
            UPDATE Orders SET order_type=?, order_date=?, employee_id=?,
            description=?, order_data=?
            WHERE order_id=?
            """,
            (order_type, order_date, employee_id, description, order_data_json, order_id),
        )

    conn.commit()
    return True, "Приказ сохранён!"


def delete_order(cursor, conn, order_id: int, status: str):
    """
    Удаляет приказ, если он не исполнен.
    """
    if status == "Исполнен":
        return False, "Нельзя удалить исполненный приказ!"

    cursor.execute("DELETE FROM Orders WHERE order_id = ?", (order_id,))
    conn.commit()
    return True, "Приказ удалён!"


def execute_order(cursor, conn, order_id: int):
    """
    Исполняет приказ и применяет изменения к данным системы.
    """
    order = get_order_details(cursor, order_id)

    if order is None:
        return False, "Приказ не найден"

    order_type, employee_id, description, order_date, order_data = order

    cursor.execute("SELECT status FROM Orders WHERE order_id = ?", (order_id,))
    status_row = cursor.fetchone()
    if status_row and status_row[0] == "Исполнен":
        return False, "Приказ уже исполнен!"

    if order_type == "Прием на работу":
        _execute_hire_order(cursor, employee_id, order_date)

    elif order_type == "Увольнение":
        _execute_dismissal_order(cursor, employee_id)

    elif order_type == "Перевод":
        _execute_transfer_order(cursor, employee_id, order_data, order_date)

    elif order_type == "Отпуск":
        _execute_vacation_order(cursor, employee_id, order_data)

    elif order_type == "Изменение оклада":
        _execute_salary_change_order(cursor, employee_id, order_data)

    elif order_type == "Премия":
        _execute_bonus_order(order_data)

    elif order_type == "Взыскание":
        pass

    cursor.execute(
        "UPDATE Orders SET status = 'Исполнен' WHERE order_id = ?",
        (order_id,),
    )

    conn.commit()
    return True, f"Приказ '{order_type}' успешно исполнен!"


def _parse_order_data(order_data):
    if not order_data:
        return {}
    return json.loads(order_data)


def _execute_hire_order(cursor, employee_id, order_date):
    """
    Прием на работу — активация сотрудника.
    """
    if employee_id:
        cursor.execute(
            """
            UPDATE Employees SET status = 'Работает', hire_date = ?
            WHERE employee_id = ?
            """,
            (order_date, employee_id),
        )


def _execute_dismissal_order(cursor, employee_id):
    """
    Увольнение сотрудника.
    """
    cursor.execute(
        """
        UPDATE Employees SET status = 'Уволен'
        WHERE employee_id = ?
        """,
        (employee_id,),
    )

    cursor.execute(
        """
        DELETE FROM Vacations
        WHERE employee_id = ? AND start_date > date('now')
        """,
        (employee_id,),
    )


def _execute_transfer_order(cursor, employee_id, order_data, order_date):
    """
    Перевод в другое подразделение.
    """
    data = _parse_order_data(order_data)

    new_department_id = data.get("new_department_id")
    new_position_id = data.get("new_position_id")

    cursor.execute(
        """
        SELECT department_id FROM Employees WHERE employee_id = ?
        """,
        (employee_id,),
    )
    old_department_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO Transfers (employee_id, old_department_id, new_department_id, transfer_date)
        VALUES (?, ?, ?, ?)
        """,
        (employee_id, old_department_id, new_department_id, order_date),
    )

    if new_position_id:
        cursor.execute(
            """
            UPDATE Employees
            SET department_id = ?, position_id = ?
            WHERE employee_id = ?
            """,
            (new_department_id, new_position_id, employee_id),
        )
    else:
        cursor.execute(
            """
            UPDATE Employees
            SET department_id = ?
            WHERE employee_id = ?
            """,
            (new_department_id, employee_id),
        )


def _execute_vacation_order(cursor, employee_id, order_data):
    """
    Отправка в отпуск.
    """
    data = _parse_order_data(order_data)

    start_date = data.get("start_date")
    end_date = data.get("end_date")
    vacation_type = data.get("vacation_type", "Ежегодный оплачиваемый")

    cursor.execute(
        """
        INSERT INTO Vacations (employee_id, start_date, end_date, vacation_type)
        VALUES (?, ?, ?, ?)
        """,
        (employee_id, start_date, end_date, vacation_type),
    )

    today = datetime.now().strftime("%Y-%m-%d")
    if start_date <= today <= end_date:
        cursor.execute(
            """
            UPDATE Employees SET status = 'В отпуске'
            WHERE employee_id = ?
            """,
            (employee_id,),
        )


def _execute_salary_change_order(cursor, employee_id, order_data):
    """
    Изменение оклада.
    """
    data = _parse_order_data(order_data)
    new_salary = data.get("new_salary")

    if new_salary:
        cursor.execute(
            """
            UPDATE Employees SET salary = ?
            WHERE employee_id = ?
            """,
            (new_salary, employee_id),
        )


def _execute_bonus_order(order_data):
    """
    Премия пока не изменяет данные.

    На следующем этапе можно добавить отдельную таблицу премий.
    """
    _parse_order_data(order_data)