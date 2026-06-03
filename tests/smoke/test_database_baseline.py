import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAIN_PATH = PROJECT_ROOT / "main.py"


def load_monolith_module():
    """
    Загружает текущий main.py как модуль.

    Блок if __name__ == "__main__" не выполняется,
    поэтому Tkinter-окно не открывается во время тестов.
    """
    spec = importlib.util.spec_from_file_location("hr_monolith_main", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_monolith_module_can_be_loaded_without_starting_gui():
    """
    Smoke test: текущий монолит можно загрузить как модуль.
    """
    module = load_monolith_module()

    assert hasattr(module, "Database")
    assert hasattr(module, "HRSystemApp")


def test_database_initializes_required_tables(monkeypatch, tmp_path):
    """
    Smoke test: Database создает все основные таблицы HR-системы.

    База создается во временной папке, чтобы тест не трогал локальный
    файл hr_system.db разработчика.
    """
    monkeypatch.chdir(tmp_path)

    module = load_monolith_module()
    database = module.Database()

    try:
        rows = database.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

        table_names = {row[0] for row in rows}

        required_tables = {
            "Users",
            "Departments",
            "Positions",
            "Employees",
            "Vacations",
            "Orders",
            "Transfers",
        }

        assert required_tables.issubset(table_names)
    finally:
        database.conn.close()


def test_database_inserts_initial_demo_data(monkeypatch, tmp_path):
    """
    Smoke test: при первом запуске добавляются демонстрационные данные.
    """
    monkeypatch.chdir(tmp_path)

    module = load_monolith_module()
    database = module.Database()

    try:
        users_count = database.cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0]
        departments_count = database.cursor.execute("SELECT COUNT(*) FROM Departments").fetchone()[0]
        positions_count = database.cursor.execute("SELECT COUNT(*) FROM Positions").fetchone()[0]
        employees_count = database.cursor.execute("SELECT COUNT(*) FROM Employees").fetchone()[0]
        vacations_count = database.cursor.execute("SELECT COUNT(*) FROM Vacations").fetchone()[0]
        orders_count = database.cursor.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]

        admin = database.cursor.execute(
            "SELECT login, role, active FROM Users WHERE login = 'admin'"
        ).fetchone()

        assert users_count == 4
        assert departments_count == 5
        assert positions_count == 7
        assert employees_count == 15
        assert vacations_count == 5
        assert orders_count == 3

        assert admin == ("admin", "Администратор", 1)
    finally:
        database.conn.close()