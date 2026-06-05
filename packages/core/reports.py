def get_general_statistics(cursor):
    """
    Возвращает общую статистику предприятия.
    """
    total_employees = cursor.execute(
        "SELECT COUNT(*) FROM Employees WHERE status='Работает'"
    ).fetchone()[0]

    total_departments = cursor.execute(
        "SELECT COUNT(*) FROM Departments"
    ).fetchone()[0]

    total_salary = cursor.execute(
        "SELECT SUM(salary) FROM Employees WHERE status='Работает'"
    ).fetchone()[0] or 0

    average_salary = cursor.execute(
        "SELECT AVG(salary) FROM Employees WHERE status='Работает'"
    ).fetchone()[0] or 0

    employees_on_vacation = cursor.execute(
        """
        SELECT COUNT(DISTINCT employee_id) FROM Vacations
        WHERE date('now') BETWEEN start_date AND end_date
        """
    ).fetchone()[0]

    department_distribution = cursor.execute(
        """
        SELECT d.department_name, COUNT(e.employee_id) as cnt
        FROM Departments d
        LEFT JOIN Employees e ON d.department_id = e.department_id AND e.status='Работает'
        GROUP BY d.department_id
        ORDER BY cnt DESC
        """
    ).fetchall()

    return {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_salary": total_salary,
        "average_salary": average_salary,
        "employees_on_vacation": employees_on_vacation,
        "department_distribution": department_distribution,
    }


def list_employees_by_department(cursor):
    """
    Возвращает сотрудников по подразделениям.
    """
    cursor.execute(
        """
        SELECT d.department_name,
               e.last_name || ' ' || e.first_name || ' ' || e.middle_name,
               p.position_name,
               e.salary
        FROM Employees e
        JOIN Departments d ON e.department_id = d.department_id
        JOIN Positions p ON e.position_id = p.position_id
        WHERE e.status='Работает'
        ORDER BY d.department_name, e.last_name
        """
    )
    return cursor.fetchall()


def get_salary_fund_by_department(cursor):
    """
    Возвращает зарплатный фонд по подразделениям.
    """
    cursor.execute(
        """
        SELECT d.department_name,
               COUNT(e.employee_id),
               MIN(e.salary),
               MAX(e.salary),
               AVG(e.salary),
               SUM(e.salary)
        FROM Departments d
        LEFT JOIN Employees e ON d.department_id = e.department_id AND e.status='Работает'
        GROUP BY d.department_id
        """
    )
    return cursor.fetchall()


def list_vacation_schedule(cursor):
    """
    Возвращает график отпусков.
    """
    cursor.execute(
        """
        SELECT e.last_name || ' ' || e.first_name,
               d.department_name,
               v.start_date,
               v.end_date,
               CAST((julianday(v.end_date) - julianday(v.start_date)) AS INTEGER),
               v.vacation_type
        FROM Vacations v
        JOIN Employees e ON v.employee_id = e.employee_id
        JOIN Departments d ON e.department_id = d.department_id
        ORDER BY v.start_date DESC
        """
    )
    return cursor.fetchall()


def list_employee_experience(cursor):
    """
    Возвращает сотрудников по стажу работы.
    """
    cursor.execute(
        """
        SELECT e.last_name || ' ' || e.first_name || ' ' || e.middle_name,
               d.department_name,
               p.position_name,
               e.hire_date,
               CAST((julianday('now') - julianday(e.hire_date)) / 365.25 AS INTEGER)
        FROM Employees e
        JOIN Departments d ON e.department_id = d.department_id
        JOIN Positions p ON e.position_id = p.position_id
        WHERE e.status='Работает'
        ORDER BY e.hire_date
        """
    )
    return cursor.fetchall()


def list_positions_salary(cursor):
    """
    Возвращает статистику по должностям и зарплатам.
    """
    cursor.execute(
        """
        SELECT p.position_name,
               COUNT(e.employee_id),
               MIN(e.salary),
               MAX(e.salary),
               AVG(e.salary)
        FROM Positions p
        LEFT JOIN Employees e ON p.position_id = e.position_id AND e.status='Работает'
        GROUP BY p.position_id
        ORDER BY COUNT(e.employee_id) DESC
        """
    )
    return cursor.fetchall()