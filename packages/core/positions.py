def list_positions(cursor):
    """
    Возвращает список должностей с количеством сотрудников.

    Формат строк сохранен таким же, как использовался в main.py.
    """
    cursor.execute(
        """
        SELECT p.position_id, p.position_name, p.base_salary,
               COUNT(e.employee_id) as emp_count
        FROM Positions p
        LEFT JOIN Employees e ON p.position_id = e.position_id
        GROUP BY p.position_id
        """
    )
    return cursor.fetchall()


def position_has_employees(cursor, position_id: int) -> bool:
    """
    Проверяет, есть ли сотрудники на должности.
    """
    cursor.execute(
        "SELECT COUNT(*) FROM Employees WHERE position_id = ?",
        (position_id,),
    )
    return cursor.fetchone()[0] > 0


def delete_position(cursor, conn, position_id: int):
    """
    Удаляет должность, если на ней нет сотрудников.

    Возвращает:
    - (True, сообщение), если должность удалена;
    - (False, сообщение), если удалить нельзя.
    """
    if position_has_employees(cursor, position_id):
        return False, "На этой должности есть сотрудники!"

    cursor.execute(
        "DELETE FROM Positions WHERE position_id = ?",
        (position_id,),
    )
    conn.commit()
    return True, "Должность удалена!"


def save_position(cursor, conn, name: str, salary: str, position_id: int | None = None):
    """
    Создает или обновляет должность.
    """
    if not name or not salary:
        return False, "Заполните все поля!"

    try:
        salary_value = float(salary)
    except ValueError:
        return False, "Базовая зарплата должна быть числом!"

    if position_id is None:
        cursor.execute(
            "INSERT INTO Positions (position_name, base_salary) VALUES (?, ?)",
            (name, salary_value),
        )
    else:
        cursor.execute(
            "UPDATE Positions SET position_name=?, base_salary=? WHERE position_id=?",
            (name, salary_value, position_id),
        )

    conn.commit()
    return True, "Данные сохранены!"