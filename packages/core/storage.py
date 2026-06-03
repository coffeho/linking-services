import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('hr_system.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_initial_data()
    
    def create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT,
            active INTEGER DEFAULT 1
        )
        ''')
        
        # Таблица подразделений
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES Employees(employee_id)
        )
        ''')
        
        # Таблица должностей
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Positions (
            position_id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_name TEXT NOT NULL,
            base_salary REAL
        )
        ''')
        
        # Таблица сотрудников
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            birth_date DATE,
            hire_date DATE,
            department_id INTEGER,
            position_id INTEGER,
            salary REAL,
            status TEXT DEFAULT 'Работает',
            FOREIGN KEY (department_id) REFERENCES Departments(department_id),
            FOREIGN KEY (position_id) REFERENCES Positions(position_id)
        )
        ''')
        
        # Таблица отпусков
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vacations (
            vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            start_date DATE,
            end_date DATE,
            vacation_type TEXT,
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
        )
        ''')
        
        # Таблица приказов
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_type TEXT,
            order_date DATE,
            employee_id INTEGER,
            description TEXT,
            order_data TEXT,
            status TEXT DEFAULT 'Не исполнен',
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
        )
        ''')
        
        # Таблица переводов
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transfers (
            transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            old_department_id INTEGER,
            new_department_id INTEGER,
            transfer_date DATE,
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
        )
        ''')
        
        self.conn.commit()
    def upgrade_database(self):
        try:
            # Проверяем наличие столбца status
            self.cursor.execute("PRAGMA table_info(Orders)")
            columns = [column[1] for column in self.cursor.fetchall()]
        
            if 'status' not in columns:
                self.cursor.execute("ALTER TABLE Orders ADD COLUMN status TEXT DEFAULT 'Не исполнен'")
                print("✅ Добавлен столбец 'status' в таблицу Orders")
        
            if 'order_data' not in columns:
                self.cursor.execute("ALTER TABLE Orders ADD COLUMN order_data TEXT")
                print("✅ Добавлен столбец 'order_data' в таблицу Orders")
        
            # Обновляем существующие записи
            self.cursor.execute("UPDATE Orders SET status = 'Не исполнен' WHERE status IS NULL")
        
            self.conn.commit()
            print("✅ База данных успешно обновлена!")
        
        except Exception as e:
            print(f"❌ Ошибка обновления БД: {e}")
    
    def insert_initial_data(self):
        # Проверяем, есть ли данные
        self.cursor.execute("SELECT COUNT(*) FROM Users")
        if self.cursor.fetchone()[0] > 0:
            return
        
        # Добавляем пользователей (пароль = login для демонстрации)
        users = [
            ('admin', 'admin', 'Администратор', 'Главный Администратор'),
            ('hr_manager', 'hr_manager', 'HR-менеджер', 'Иванова Мария Петровна'),
            ('accountant', 'accountant', 'Бухгалтер', 'Петрова Анна Сергеевна'),
            ('employee', 'employee', 'Сотрудник', 'Сидоров Иван Иванович'),
        ]
        
        for login, password, role, full_name in users:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute(
                "INSERT INTO Users (login, password, role, full_name) VALUES (?, ?, ?, ?)",
                (login, hashed, role, full_name)
            )
        
        # Подразделения
        departments = [
            'Бухгалтерия',
            'Отдел кадров',
            'IT-отдел',
            'Отдел продаж',
            'Администрация'
        ]
        for dept in departments:
            self.cursor.execute("INSERT INTO Departments (department_name) VALUES (?)", (dept,))
        
        # Должности
        positions = [
            ('Менеджер', 70000),
            ('Бухгалтер', 65000),
            ('Программист', 90000),
            ('HR-специалист', 60000),
            ('Директор', 150000),
            ('Аналитик', 75000),
            ('Администратор', 55000)
        ]
        for pos, salary in positions:
            self.cursor.execute("INSERT INTO Positions (position_name, base_salary) VALUES (?, ?)", (pos, salary))
        
        # Сотрудники
        employees = [
            ('Иванов', 'Иван', 'Иванович', '1985-03-12', '2015-04-01', 3, 3, 90000, 'Работает'),
            ('Петров', 'Петр', 'Сергеевич', '1990-07-21', '2018-06-15', 4, 1, 70000, 'Работает'),
            ('Сидорова', 'Анна', 'Викторовна', '1987-11-02', '2016-09-10', 1, 2, 65000, 'Работает'),
            ('Козлов', 'Сергей', 'Александрович', '1992-05-15', '2019-01-20', 2, 4, 60000, 'Работает'),
            ('Морозова', 'Елена', 'Дмитриевна', '1988-09-30', '2017-03-11', 5, 5, 150000, 'Работает'),
            ('Новиков', 'Алексей', 'Владимирович', '1991-12-08', '2020-02-14', 3, 3, 85000, 'Работает'),
            ('Соколова', 'Ольга', 'Игоревна', '1989-06-25', '2018-08-19', 4, 1, 72000, 'Работает'),
            ('Лебедев', 'Дмитрий', 'Николаевич', '1986-02-17', '2015-10-05', 1, 2, 68000, 'Работает'),
            ('Волкова', 'Татьяна', 'Андреевна', '1993-04-22', '2021-05-12', 2, 4, 58000, 'Работает'),
            ('Зайцев', 'Максим', 'Павлович', '1990-11-11', '2019-07-08', 3, 6, 75000, 'Работает'),
            ('Смирнова', 'Наталья', 'Владимировна', '1987-08-14', '2016-12-20', 4, 1, 71000, 'Работает'),
            ('Кузнецов', 'Андрей', 'Сергеевич', '1991-01-05', '2020-09-15', 5, 7, 55000, 'Работает'),
            ('Павлова', 'Ирина', 'Алексеевна', '1988-07-28', '2017-11-03', 1, 2, 66000, 'Работает'),
            ('Федоров', 'Владимир', 'Иванович', '1984-03-19', '2014-06-22', 3, 3, 95000, 'Работает'),
            ('Михайлова', 'Светлана', 'Петровна', '1992-10-07', '2021-01-30', 2, 4, 59000, 'Работает'),
        ]
        
        for emp in employees:
            self.cursor.execute('''
                INSERT INTO Employees 
                (last_name, first_name, middle_name, birth_date, hire_date, 
                department_id, position_id, salary, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        
        # Отпуска
        vacations = [
            (1, '2024-07-01', '2024-07-21', 'Ежегодный оплачиваемый'),
            (2, '2024-08-10', '2024-08-24', 'Ежегодный оплачиваемый'),
            (3, '2024-06-15', '2024-06-29', 'Ежегодный оплачиваемый'),
            (4, '2024-09-01', '2024-09-14', 'Ежегодный оплачиваемый'),
            (5, '2024-05-20', '2024-06-10', 'Ежегодный оплачиваемый'),
        ]
        
        for vac in vacations:
            self.cursor.execute('''
                INSERT INTO Vacations (employee_id, start_date, end_date, vacation_type)
                VALUES (?, ?, ?, ?)
            ''', vac)
        
        # Приказы
        orders = [
            ('Прием на работу', '2021-05-12', 9, 'Принять на должность HR-специалиста'),
            ('Перевод', '2022-03-15', 6, 'Перевести в отдел разработки'),
            ('Увольнение', '2023-11-20', 12, 'Уволить по собственному желанию'),
        ]
        
        for order in orders:
            self.cursor.execute('''
                INSERT INTO Orders (order_type, order_date, employee_id, description)
                VALUES (?, ?, ?, ?)
            ''', order)
        
        self.conn.commit()
