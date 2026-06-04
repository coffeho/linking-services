import os
import tempfile

from packages.core.auth import authenticate_user, hash_password, AuthenticatedUser
from packages.core.storage import Database


def create_temp_database():
    """
    Создаёт временную базу через существующий Database.

    Пока Database жёстко создаёт файл hr_system.db в текущей папке,
    поэтому тест временно меняет рабочую директорию.
    """
    temp_dir = tempfile.TemporaryDirectory()
    old_cwd = os.getcwd()
    os.chdir(temp_dir.name)

    database = Database()

    return temp_dir, old_cwd, database


def close_temp_database(temp_dir, old_cwd, database):
    database.conn.close()
    os.chdir(old_cwd)
    temp_dir.cleanup()


def test_hash_password_is_stable_for_same_input():
    """
    Один и тот же пароль должен давать один и тот же хеш.

    Это важно, потому что начальные пользователи создаются с этим же
    алгоритмом хеширования.
    """
    assert hash_password("admin") == hash_password("admin")


def test_hash_password_differs_for_different_inputs():
    """
    Разные пароли не должны иметь одинаковый хеш.
    """
    assert hash_password("admin") != hash_password("wrong-password")


def test_authenticate_user_accepts_valid_admin_credentials():
    """
    admin/admin должен проходить авторизацию на демонстрационной базе.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        user = authenticate_user(database.cursor, "admin", "admin")

        assert isinstance(user, AuthenticatedUser)
        assert user.user_id == 1
        assert user.role == "Администратор"
        assert user.full_name == "Главный Администратор"
        assert user.active is True
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_authenticate_user_rejects_wrong_password():
    """
    Неверный пароль должен отклоняться.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        user = authenticate_user(database.cursor, "admin", "wrong-password")

        assert user is None
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_authenticate_user_rejects_unknown_login():
    """
    Несуществующий пользователь не должен проходить авторизацию.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        user = authenticate_user(database.cursor, "unknown", "admin")

        assert user is None
    finally:
        close_temp_database(temp_dir, old_cwd, database)


def test_authenticate_user_returns_inactive_user_state():
    """
    Если пользователь найден, но деактивирован, core возвращает active=False.

    GUI уже решает, какое сообщение показать пользователю.
    """
    temp_dir, old_cwd, database = create_temp_database()

    try:
        database.cursor.execute("UPDATE Users SET active = 0 WHERE login = ?", ("admin",))
        database.conn.commit()

        user = authenticate_user(database.cursor, "admin", "admin")

        assert isinstance(user, AuthenticatedUser)
        assert user.active is False
    finally:
        close_temp_database(temp_dir, old_cwd, database)