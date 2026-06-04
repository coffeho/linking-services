"""
Переиспользуемая core-логика HR-системы.
"""

from packages.core.auth import AuthenticatedUser, authenticate_user, hash_password
from packages.core.models import (
    Department,
    Employee,
    Order,
    Position,
    Transfer,
    User,
    Vacation,
)
from packages.core.storage import Database

__all__ = [
    "AuthenticatedUser",
    "Database",
    "Department",
    "Employee",
    "Order",
    "Position",
    "Transfer",
    "User",
    "Vacation",
    "authenticate_user",
    "hash_password",
]