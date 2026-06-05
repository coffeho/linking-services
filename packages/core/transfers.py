def list_transfers(cursor):
    """
    Возвращает историю переводов для отображения в GUI.
    """
    cursor.execute(
        """
        SELECT t.transfer_id,
               e.last_name || ' ' || e.first_name as full_name,
               d1.department_name as old_dept,
               d2.department_name as new_dept,
               t.transfer_date
        FROM Transfers t
        JOIN Employees e ON t.employee_id = e.employee_id
        JOIN Departments d1 ON t.old_department_id = d1.department_id
        JOIN Departments d2 ON t.new_department_id = d2.department_id
        ORDER BY t.transfer_date DESC
        """
    )
    return cursor.fetchall()


def list_working_employees_with_department(cursor):
    """
    Возвращает работающих сотрудников с текущим подразделением
    для выбора в форме перевода.
    """
    cursor.execute(
        """
        SELECT e.employee_id,
               e.last_name || ' ' || e.first_name || ' (' || d.department_name || ')'
        FROM Employees e
        JOIN Departments d ON e.department_id = d.department_id
        WHERE e.status='Работает'
        """
    )
    return cursor.fetchall()


def list_departments_for_transfer(cursor):
    """
    Возвращает подразделения для выбора нового подразделения.
    """
    cursor.execute("SELECT department_id, department_name FROM Departments")
    return cursor.fetchall()


def get_employee_department_id(cursor, employee_id: int):
    """
    Возвращает текущее подразделение сотрудника.
    """
    cursor.execute(
        "SELECT department_id FROM Employees WHERE employee_id = ?",
        (employee_id,),
    )
    row = cursor.fetchone()

    if row is None:
        return None

    return row[0]


def create_transfer(cursor, conn, employee_id: int, new_department_id: int, transfer_date: str):
    """
    Создает перевод сотрудника и обновляет его подразделение.
    """
    old_department_id = get_employee_department_id(cursor, employee_id)

    if old_department_id is None:
        return False, "Сотрудник не найден"

    if old_department_id == new_department_id:
        return False, "Сотрудник уже в этом подразделении!"

    cursor.execute(
        """
        INSERT INTO Transfers (employee_id, old_department_id, new_department_id, transfer_date)
        VALUES (?, ?, ?, ?)
        """,
        (employee_id, old_department_id, new_department_id, transfer_date),
    )

    cursor.execute(
        """
        UPDATE Employees SET department_id = ? WHERE employee_id = ?
        """,
        (new_department_id, employee_id),
    )

    conn.commit()
    return True, "Перевод выполнен!"


def delete_transfer(cursor, conn, transfer_id: int):
    """
    Удаляет запись о переводе.
    """
    cursor.execute("DELETE FROM Transfers WHERE transfer_id = ?", (transfer_id,))
    conn.commit()
    return True, "Перевод удалён!"