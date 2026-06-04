from packages.core.models import Employee, User, Vacation


def test_user_is_active_by_default():
    """
    Новый пользователь по умолчанию считается активным.
    """
    user = User(
        user_id=1,
        login="admin",
        role="Администратор",
        full_name="Главный Администратор",
    )

    assert user.active is True


def test_employee_full_name_with_middle_name():
    """
    ФИО сотрудника собирается из фамилии, имени и отчества.
    """
    employee = Employee(
        employee_id=1,
        last_name="Иванов",
        first_name="Иван",
        middle_name="Иванович",
        birth_date="1990-01-01",
        hire_date="2020-01-01",
        department_id=1,
        position_id=1,
        salary=70000,
    )

    assert employee.full_name == "Иванов Иван Иванович"


def test_employee_full_name_without_middle_name():
    """
    Если отчества нет, в ФИО не должно быть лишнего пробела.
    """
    employee = Employee(
        employee_id=1,
        last_name="Иванов",
        first_name="Иван",
        middle_name=None,
        birth_date="1990-01-01",
        hire_date="2020-01-01",
        department_id=1,
        position_id=1,
        salary=70000,
    )

    assert employee.full_name == "Иванов Иван"


def test_employee_is_working_for_working_status():
    """
    Сотрудник со статусом 'Работает' считается работающим.
    """
    employee = Employee(
        employee_id=1,
        last_name="Иванов",
        first_name="Иван",
        middle_name=None,
        birth_date="1990-01-01",
        hire_date="2020-01-01",
        department_id=1,
        position_id=1,
        salary=70000,
        status="Работает",
    )

    assert employee.is_working is True


def test_vacation_days_returns_date_difference():
    """
    Количество дней отпуска считается как разница между датами.
    """
    vacation = Vacation(
        vacation_id=1,
        employee_id=1,
        start_date="2024-07-01",
        end_date="2024-07-21",
        vacation_type="Ежегодный оплачиваемый",
    )

    assert vacation.days == 20