from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class User:
    """
    Пользователь системы.

    Используется для представления учетной записи и роли пользователя.
    """

    user_id: int
    login: str
    role: str
    full_name: str
    active: bool = True


@dataclass(frozen=True)
class Department:
    """
    Подразделение организации.
    """

    department_id: int
    department_name: str
    manager_id: Optional[int] = None


@dataclass(frozen=True)
class Position:
    """
    Должность сотрудника.
    """

    position_id: int
    position_name: str
    base_salary: Optional[float] = None


@dataclass(frozen=True)
class Employee:
    """
    Сотрудник организации.
    """

    employee_id: int
    last_name: str
    first_name: str
    middle_name: Optional[str]
    birth_date: Optional[str]
    hire_date: Optional[str]
    department_id: Optional[int]
    position_id: Optional[int]
    salary: float
    status: str = "Работает"

    @property
    def full_name(self) -> str:
        """
        Возвращает ФИО сотрудника без лишних пробелов.
        """
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(part for part in parts if part)

    @property
    def is_working(self) -> bool:
        """
        Проверяет, что сотрудник находится в статусе 'Работает'.
        """
        return self.status == "Работает"


@dataclass(frozen=True)
class Vacation:
    """
    Отпуск сотрудника.
    """

    vacation_id: int
    employee_id: int
    start_date: str
    end_date: str
    vacation_type: str

    @property
    def days(self) -> int:
        """
        Возвращает количество дней между датой начала и датой окончания.

        Используется та же логика разницы дат, что и в текущих SQL-отчетах:
        end_date - start_date.
        """
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return (end - start).days


@dataclass(frozen=True)
class Order:
    """
    Кадровый приказ.
    """

    order_id: int
    order_type: str
    order_date: str
    employee_id: Optional[int]
    description: str
    order_data: Optional[str] = None
    status: str = "Не исполнен"


@dataclass(frozen=True)
class Transfer:
    """
    Перевод сотрудника между подразделениями.
    """

    transfer_id: int
    employee_id: int
    old_department_id: int
    new_department_id: int
    transfer_date: str