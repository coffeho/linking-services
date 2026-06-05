from typing import Optional


def list_employees(cursor, search_text: str = ""):
    """
    Возвращает список сотрудников для отображения в таблице GUI.

    На текущем этапе функция возвращает строки в том же формате,
    который уже использовал main.py, чтобы не менять поведение интерфейса.
    """
    query = """
        SELECT e.employee_id, e.last_name, e.first_name, e.middle_name,
               e.birth_date, e.hire_date, d.department_name, p.position_name,
               e.salary, e.status
        FROM Employees e
        LEFT JOIN Departments d ON e.department_id = d.department_id
        LEFT JOIN Positions p ON e.position_id = p.position_id
    """

    params = ()

    if search_text:
        query += " WHERE e.last_name LIKE ? OR e.first_name LIKE ?"
        pattern = f"%{search_text}%"
        params = (pattern, pattern)

    cursor.execute(query, params)
    return cursor.fetchall()


def delete_employee(cursor, conn, employee_id: int):
    """
    Удаляет сотрудника по идентификатору.

    Возвращает True, если операция выполнена.
    """
    cursor.execute("DELETE FROM Employees WHERE employee_id = ?", (employee_id,))
    conn.commit()
    return True


def employee_exists(cursor, employee_id: int) -> bool:
    """
    Проверяет, существует ли сотрудник.

    Используется в тестах и дальнейших бизнес-операциях.
    """
    cursor.execute(
        "SELECT COUNT(*) FROM Employees WHERE employee_id = ?",
        (employee_id,),
    )
    return cursor.fetchone()[0] > 0