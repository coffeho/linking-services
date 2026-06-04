from dataclasses import dataclass
from typing import Optional
import hashlib


@dataclass(frozen=True)
class AuthenticatedUser:
    """
    Данные пользователя, который успешно прошёл авторизацию.

    Этот объект нужен, чтобы GUI не работал с сырым tuple из SQLite:
    вместо user[0], user[1], user[2] можно использовать понятные поля.
    """

    user_id: int
    role: str
    full_name: str
    active: bool


def hash_password(password: str) -> str:
    """
    Возвращает SHA-256 хеш пароля.

    Сейчас используется тот же алгоритм, что и в исходном монолите,
    чтобы не менять существующее поведение и не ломать тестовые аккаунты.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(cursor, login: str, password: str) -> Optional[AuthenticatedUser]:
    """
    Проверяет логин и пароль пользователя.

    Возвращает AuthenticatedUser, если пользователь найден.
    Возвращает None, если логин или пароль неверные.

    cursor передаётся снаружи, потому что на этом этапе мы ещё не
    переписываем слой хранения данных, а только выносим авторизацию
    из Tkinter-кода в core-модуль.
    """
    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT user_id, role, full_name, active FROM Users
        WHERE login = ? AND password = ?
        """,
        (login, hashed_password),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return AuthenticatedUser(
        user_id=row[0],
        role=row[1],
        full_name=row[2],
        active=bool(row[3]),
    )