"""
Compatibility entry point for HR System.

Основной Tkinter-интерфейс перенесен в app/ui/main_window.py.
Этот файл оставлен как тонкая обертка, чтобы старый запуск
`python main.py` продолжал работать.
"""

from app.ui.main_window import HRSystemApp, main
from packages.core.storage import Database

__all__ = ["Database", "HRSystemApp", "main"]


if __name__ == "__main__":
    main()