from datetime import datetime


def list_vacations(cursor):
    """
    Возвращает список отпусков для отображения в GUI.

    Формат строк сохранен таким же, как раньше использовался в main.py.
    """
    cursor.execute(
        """
        SELECT v.vacation_id,
               e.last_name || ' ' || e.first_name as full_name,
               v.start_date, v.end_date, v.vacation_type,
               CAST((julianday(v.end_date) - julianday(v.start_date)) AS INTEGER) as days
        FROM Vacations v
        JOIN Employees e ON v.employee_id = e.employee_id
        ORDER BY v.start_date DESC
        """
    )
    return cursor.fetchall()


def list_active_employees_for_vacation(cursor):
    """
    Возвращает сотрудников со статусом 'Работает' для выбора в форме отпуска.
    """
    cursor.execute(
        """
        SELECT employee_id, last_name || ' ' || first_name || ' ' || middle_name
        FROM Employees WHERE status='Работает'
        """
    )
    return cursor.fetchall()


def validate_vacation_dates(start_date: str, end_date: str):
    """
    Проверяет корректность периода отпуска.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return False, "Дата должна быть в формате ГГГГ-ММ-ДД"

    if end < start:
        return False, "Дата окончания не может быть раньше даты начала"

    return True, "OK"


def save_vacation(
    cursor,
    conn,
    employee_id: int,
    start_date: str,
    end_date: str,
    vacation_type: str,
    vacation_id: int | None = None,
):
    """
    Создает или обновляет отпуск.
    """
    ok, msg = validate_vacation_dates(start_date, end_date)
    if not ok:
        return False, msg

    if vacation_id is None:
        cursor.execute(
            """
            INSERT INTO Vacations (employee_id, start_date, end_date, vacation_type)
            VALUES (?, ?, ?, ?)
            """,
            (employee_id, start_date, end_date, vacation_type),
        )
    else:
        cursor.execute(
            """
            UPDATE Vacations SET employee_id=?, start_date=?, end_date=?, vacation_type=?
            WHERE vacation_id=?
            """,
            (employee_id, start_date, end_date, vacation_type, vacation_id),
        )

    conn.commit()
    return True, "Данные сохранены!"


def delete_vacation(cursor, conn, vacation_id: int):
    """
    Удаляет отпуск.
    """
    cursor.execute("DELETE FROM Vacations WHERE vacation_id = ?", (vacation_id,))
    conn.commit()
    return True, "Отпуск удалён!"