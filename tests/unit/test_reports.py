import os
import tempfile

from packages.core.reports import (
    get_general_statistics,
    get_salary_fund_by_department,
    list_employee_experience,
    list_employees_by_department,
    list_positions_salary,
    list_vacation_schedule,
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


def test_get_general_statistics_returns_expected_demo_counts():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        stats = get_general_statistics(database.cursor)

        assert stats["total_employees"] == 15
        assert stats["total_departments"] == 5
        assert stats["total_salary"] > 0
        assert stats["average_salary"] > 0
        assert len(stats["department_distribution"]) == 5
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_employees_by_department_returns_working_employees():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_employees_by_department(database.cursor)

        assert len(rows) == 15
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_get_salary_fund_by_department_returns_departments():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = get_salary_fund_by_department(database.cursor)

        assert len(rows) == 5
        assert sum(row[5] or 0 for row in rows) > 0
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_vacation_schedule_returns_demo_vacations():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_vacation_schedule(database.cursor)

        assert len(rows) == 5
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_employee_experience_returns_working_employees():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_employee_experience(database.cursor)

        assert len(rows) == 15
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_list_positions_salary_returns_demo_positions():
    temp_dir, old_cwd, database = create_temp_database()

    try:
        rows = list_positions_salary(database.cursor)

        assert len(rows) == 7
    finally:
        close_temp_database(temp_dir, old_cwd, database)