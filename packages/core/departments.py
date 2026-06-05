def list_departments(cursor):
    """
    Возвращает список подразделений с количеством сотрудников.

    Формат строк сохранен таким же, как использовался в main.py.
    """
    cursor.execute(
        """
        SELECT d.department_id, d.department_name, d.manager_id,
               COUNT(e.employee_id) as emp_count
        FROM Departments d
        LEFT JOIN Employees e ON d.department_id = e.department_id
        GROUP BY d.department_id
        """
    )
    return cursor.fetchall()


def department_has_employees(cursor, department_id: int) -> bool:
    """
    Проверяет, есть ли сотрудники в подразделении.
    """
    cursor.execute(
        "SELECT COUNT(*) FROM Employees WHERE department_id = ?",
        (department_id,),
    )
    return cursor.fetchone()[0] > 0


def delete_department(cursor, conn, department_id: int):
    """
    Удаляет подразделение, если в нем нет сотрудников.

    Возвращает:
    - (True, сообщение) при успешном удалении;
    - (False, сообщение) если удалить нельзя.
    """
    if department_has_employees(cursor, department_id):
        return False, "В подразделении есть сотрудники!"

    cursor.execute(
        "DELETE FROM Departments WHERE department_id = ?",
        (department_id,),
    )
    conn.commit()
    return True, "Подразделение удалено!"


def save_department(cursor, conn, name: str, department_id: int | None = None):
    """
    Создает или обновляет подразделение.
    """
    if not name:
        return False, "Введите название!"

    if department_id is None:
        cursor.execute(
            "INSERT INTO Departments (department_name) VALUES (?)",
            (name,),
        )
    else:
        cursor.execute(
            "UPDATE Departments SET department_name=? WHERE department_id=?",
            (name, department_id),
        )

    conn.commit()
    return True, "Данные сохранены!"