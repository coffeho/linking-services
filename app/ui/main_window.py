from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import os

from packages.core.auth import authenticate_user, hash_password

from packages.core.storage import Database


from packages.core.employees import delete_employee as core_delete_employee
from packages.core.employees import list_employees 


from packages.core.departments import (
    delete_department as core_delete_department,
    list_departments,
    save_department,
)
from packages.core.positions import (
    delete_position as core_delete_position,
    list_positions,
    save_position,
)


from packages.core.vacations import (
    delete_vacation as core_delete_vacation,
    list_active_employees_for_vacation,
    list_vacations,
    save_vacation,
)

from packages.core.transfers import (
    create_transfer,
    delete_transfer as core_delete_transfer,
    list_departments_for_transfer,
    list_transfers,
    list_working_employees_with_department,
)

from packages.core.orders import (
    create_or_update_order,
    delete_order as core_delete_order,
    execute_order as core_execute_order,
    get_order_data,
    list_departments_for_order,
    list_employees_for_order,
    list_orders,
    list_positions_for_order,
)

from packages.core.reports import (
    get_general_statistics,
    get_salary_fund_by_department,
    list_employee_experience,
    list_employees_by_department,
    list_positions_salary,
    list_vacation_schedule,
)
# ======================== GUI ПРИЛОЖЕНИЕ ========================

class HRSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Система кадрового учёта")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        self.db = Database()
        self.current_user = None
        self.current_role = None
        
        self.show_login_screen()
    
    # ==================== ЭКРАН АВТОРИЗАЦИИ ====================
    
    def show_login_screen(self):
        self.clear_screen()
        
        login_frame = Frame(self.root, bg='#34495e', padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        Label(login_frame, text="🔐 АВТОРИЗАЦИЯ", font=("Arial", 24, "bold"), 
              bg='#34495e', fg='white').grid(row=0, column=0, columnspan=2, pady=20)
        
        # Логин
        Label(login_frame, text="Логин:", font=("Arial", 12), 
              bg='#34495e', fg='white').grid(row=1, column=0, sticky=W, pady=10)
        self.login_entry = Entry(login_frame, font=("Arial", 12), width=25)
        self.login_entry.grid(row=1, column=1, pady=10)
        
        # Пароль
        Label(login_frame, text="Пароль:", font=("Arial", 12), 
              bg='#34495e', fg='white').grid(row=2, column=0, sticky=W, pady=10)
        self.password_entry = Entry(login_frame, font=("Arial", 12), width=25, show='*')
        self.password_entry.grid(row=2, column=1, pady=10)
        
        # Показать пароль
        self.show_password_var = BooleanVar()
        Checkbutton(login_frame, text="Показать пароль", variable=self.show_password_var,
                   command=self.toggle_password, bg='#34495e', fg='white',
                   selectcolor='#2c3e50', font=("Arial", 10)).grid(row=3, column=1, sticky=W)
        
        # Кнопка входа
        Button(login_frame, text="ВОЙТИ", font=("Arial", 14, "bold"), 
               bg='#27ae60', fg='white', width=20, command=self.login).grid(row=4, column=0, 
                                                                             columnspan=2, pady=20)
        
        # Информация о пользователях
        info_frame = Frame(login_frame, bg='#34495e')
        info_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        Label(info_frame, text="📋 Тестовые аккаунты:", font=("Arial", 11, "bold"), 
              bg='#34495e', fg='#ecf0f1').pack(anchor=W)
        
        accounts = [
            "👤 admin / admin (Администратор)",
            "👤 hr_manager / hr_manager (HR-менеджер)",
            "👤 accountant / accountant (Бухгалтер)",
            "👤 employee / employee (Сотрудник)"
        ]
        
        for acc in accounts:
            Label(info_frame, text=acc, font=("Arial", 9), 
                  bg='#34495e', fg='#bdc3c7').pack(anchor=W, padx=10)
    
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
    
    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        
        if not login or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        # Проверка логина и пароля вынесена в core-модуль auth.py.
        # GUI только передаёт введённые данные и показывает результат пользователю.
        user = authenticate_user(self.db.cursor, login, password)
        
        if user:
            if not user.active:
                messagebox.showerror("Ошибка", "Аккаунт деактивирован!")
                return

            # auth.py возвращает объект AuthenticatedUser с понятными полями,
            # поэтому main.py больше не работает с сырым tuple вида user[0], user[1].
            self.current_user = user.user_id
            self.current_role = user.role
            self.current_user_name = user.full_name
            
            messagebox.showinfo("Успех", f"Добро пожаловать, {self.current_user_name}!")
            self.show_main_screen()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")
    
    # ==================== ГЛАВНЫЙ ЭКРАН ====================
    
    def show_main_screen(self):
        self.clear_screen()
        
        # Верхняя панель
        top_panel = Frame(self.root, bg='#2c3e50', height=80)
        top_panel.pack(fill=X)
        
        Label(top_panel, text="🏢 СИСТЕМА КАДРОВОГО УЧЁТА", 
              font=("Arial", 20, "bold"), bg='#2c3e50', fg='white').pack(side=LEFT, padx=20, pady=20)
        
        user_info = Frame(top_panel, bg='#2c3e50')
        user_info.pack(side=RIGHT, padx=20)
        
        Label(user_info, text=f"👤 {self.current_user_name}", 
              font=("Arial", 12), bg='#2c3e50', fg='#ecf0f1').pack()
        Label(user_info, text=f"Роль: {self.current_role}", 
              font=("Arial", 10), bg='#2c3e50', fg='#bdc3c7').pack()
        
        Button(user_info, text="Выход", command=self.logout, 
               bg='#e74c3c', fg='white', font=("Arial", 10)).pack(pady=5)
        
        # Боковое меню
        side_menu = Frame(self.root, bg='#34495e', width=250)
        side_menu.pack(side=LEFT, fill=Y)
        
        Label(side_menu, text="📂 МЕНЮ", font=("Arial", 16, "bold"), 
              bg='#34495e', fg='white').pack(pady=20)
        
        menu_items = [
            ("👥 Сотрудники", self.show_employees, ['Администратор', 'HR-менеджер', 'Бухгалтер']),
            ("🏢 Подразделения", self.show_departments, ['Администратор', 'HR-менеджер']),
            ("💼 Должности", self.show_positions, ['Администратор', 'HR-менеджер', 'Бухгалтер']),
            ("🌴 Отпуска", self.show_vacations, ['Администратор', 'HR-менеджер']),
            ("📋 Приказы", self.show_orders, ['Администратор', 'HR-менеджер']),
            ("🔄 Переводы", self.show_transfers, ['Администратор', 'HR-менеджер']),
            ("📊 Отчёты", self.show_reports, ['Администратор', 'HR-менеджер', 'Бухгалтер']),
            ("👤 Пользователи", self.show_users, ['Администратор']),
        ]
        
        for text, command, roles in menu_items:
            if self.current_role in roles:
                btn = Button(side_menu, text=text, command=command, 
                           bg='#3498db', fg='white', font=("Arial", 12), 
                           width=20, height=2, relief=FLAT)
                btn.pack(pady=5, padx=10)
        
        # Рабочая область
        self.work_area = Frame(self.root, bg='#ecf0f1')
        self.work_area.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.show_employees()
    
    # ==================== СОТРУДНИКИ ====================
    
    def show_employees(self):
        self.clear_work_area()
        
        Label(self.work_area, text="👥 СОТРУДНИКИ", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        # Панель управления
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
        
        if self.current_role in ['Администратор', 'HR-менеджер']:
            Button(control_panel, text="➕ Добавить", command=self.add_employee, 
                   bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
            Button(control_panel, text="✏️ Изменить", command=self.edit_employee, 
                   bg='#f39c12', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
            Button(control_panel, text="🗑️ Удалить", command=self.delete_employee, 
                   bg='#e74c3c', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        Button(control_panel, text="🔄 Обновить", command=self.show_employees, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        # Поиск
        search_frame = Frame(self.work_area, bg='#ecf0f1')
        search_frame.pack(pady=10)
        
        Label(search_frame, text="🔍 Поиск:", bg='#ecf0f1', font=("Arial", 11)).pack(side=LEFT)
        self.search_employee_var = StringVar()
        self.search_employee_var.trace('w', lambda *args: self.search_employees())
        Entry(search_frame, textvariable=self.search_employee_var, font=("Arial", 11), 
              width=30).pack(side=LEFT, padx=10)
        
        # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        scrollbar_y = Scrollbar(table_frame)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        
        scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)
        
        columns = ('ID', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 
                   'Дата приёма', 'Подразделение', 'Должность', 'Зарплата', 'Статус')
        
        self.employees_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                          yscrollcommand=scrollbar_y.set,
                                          xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.config(command=self.employees_tree.yview)
        scrollbar_x.config(command=self.employees_tree.xview)
        
        for col in columns:
            self.employees_tree.heading(col, text=col)
            self.employees_tree.column(col, width=100)
        
        self.employees_tree.pack(fill=BOTH, expand=True)
        
        self.load_employees()
    
    def load_employees(self, search_text=''):
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)

        rows = list_employees(self.db.cursor, search_text)

        for row in rows:
            self.employees_tree.insert('', END, values=row)
        
    def search_employees(self):
        self.load_employees(self.search_employee_var.get())
    
    def add_employee(self):
        self.employee_window('add')
    
    def edit_employee(self):
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сотрудника!")
            return
        self.employee_window('edit')
    
    def delete_employee(self):
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите сотрудника!")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранного сотрудника?"):
            item = self.employees_tree.item(selected[0])
            employee_id = item['values'][0]
            
            core_delete_employee(self.db.cursor, self.db.conn, employee_id)
            
            messagebox.showinfo("Успех", "Сотрудник удалён!")
            self.show_employees()
    
    def employee_window(self, mode):
        window = Toplevel(self.root)
        window.title("Сотрудник")
        window.geometry("500x600")
        window.configure(bg='#ecf0f1')
        
        Label(window, text="👤 КАРТОЧКА СОТРУДНИКА", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
        
        fields = [
            ("Фамилия:", 'last_name'),
            ("Имя:", 'first_name'),
            ("Отчество:", 'middle_name'),
            ("Дата рождения (ГГГГ-ММ-ДД):", 'birth_date'),
            ("Дата приёма (ГГГГ-ММ-ДД):", 'hire_date'),
            ("Зарплата:", 'salary'),
        ]
        
        entries = {}
        
        for i, (label, field) in enumerate(fields):
            Label(form_frame, text=label, bg='#ecf0f1', font=("Arial", 11)).grid(row=i, column=0, 
                                                                                  sticky=W, pady=5)
            entries[field] = Entry(form_frame, font=("Arial", 11), width=30)
            entries[field].grid(row=i, column=1, pady=5)
        
        # Подразделение
        Label(form_frame, text="Подразделение:", bg='#ecf0f1', font=("Arial", 11)).grid(row=len(fields), 
                                                                                         column=0, sticky=W, pady=5)
        dept_var = StringVar()
        dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, font=("Arial", 11), width=28)
        
        self.db.cursor.execute("SELECT department_id, department_name FROM Departments")
        departments = self.db.cursor.fetchall()
        dept_combo['values'] = [f"{d[0]} - {d[1]}" for d in departments]
        dept_combo.grid(row=len(fields), column=1, pady=5)
        
        # Должность
        Label(form_frame, text="Должность:", bg='#ecf0f1', font=("Arial", 11)).grid(row=len(fields)+1, 
                                                                                     column=0, sticky=W, pady=5)
        pos_var = StringVar()
        pos_combo = ttk.Combobox(form_frame, textvariable=pos_var, font=("Arial", 11), width=28)
        
        self.db.cursor.execute("SELECT position_id, position_name FROM Positions")
        positions = self.db.cursor.fetchall()
        pos_combo['values'] = [f"{p[0]} - {p[1]}" for p in positions]
        pos_combo.grid(row=len(fields)+1, column=1, pady=5)
        
        # Статус
        Label(form_frame, text="Статус:", bg='#ecf0f1', font=("Arial", 11)).grid(row=len(fields)+2, 
                                                                                  column=0, sticky=W, pady=5)
        status_var = StringVar(value='Работает')
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, font=("Arial", 11), width=28)
        status_combo['values'] = ['Работает', 'Уволен', 'В отпуске', 'На больничном']
        status_combo.grid(row=len(fields)+2, column=1, pady=5)
        
        # Заполнение при редактировании
        if mode == 'edit':
            selected = self.employees_tree.selection()[0]
            item = self.employees_tree.item(selected)
            values = item['values']
            
            entries['last_name'].insert(0, values[1])
            entries['first_name'].insert(0, values[2])
            entries['middle_name'].insert(0, values[3] or '')
            entries['birth_date'].insert(0, values[4])
            entries['hire_date'].insert(0, values[5])
            entries['salary'].insert(0, values[8])
            
            # Находим ID подразделения и должности
            for d in departments:
                if d[1] == values[6]:
                    dept_combo.set(f"{d[0]} - {d[1]}")
            
            for p in positions:
                if p[1] == values[7]:
                    pos_combo.set(f"{p[0]} - {p[1]}")
            
            status_combo.set(values[9])
        
        # Кнопка сохранения
        def save():
            try:
                emp_id = int(emp_var.get().split(' - ')[0])
                new_dept_id = int(dept_var.get().split(' - ')[0])
                transfer_date = date_entry.get()
                
                # 1. Получаем ТЕКУЩИЙ отдел сотрудника (он станет "старым")
                self.db.cursor.execute("SELECT department_id FROM Employees WHERE employee_id = ?", (emp_id,))
                old_dept_id = self.db.cursor.fetchone()[0]
                
                if old_dept_id == new_dept_id:
                    messagebox.showerror("Ошибка", "Сотрудник уже находится в этом подразделении!")
                    return
                
                # 2. Сохраняем перевод со всеми 4-мя внешними ключами
                # self.current_user — это ID пользователя, который вошел в систему
                self.db.cursor.execute('''
                    INSERT INTO Transfers (
                        employee_id, 
                        old_department_id, 
                        new_department_id, 
                        transfer_date, 
                        approved_by
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (emp_id, old_dept_id, new_dept_id, transfer_date, self.current_user))
                
                # 3. Обновляем отдел в карточке сотрудника
                self.db.cursor.execute('''
                    UPDATE Employees SET department_id = ? WHERE employee_id = ?
                ''', (new_dept_id, emp_id))
                
                self.db.conn.commit()
                messagebox.showinfo("Успех", "Перевод успешно оформлен и сохранен в истории!")
                window.destroy()
                self.show_transfers()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось выполнить перевод: {e}")
    
    # ==================== ПОДРАЗДЕЛЕНИЯ ====================
    
    def show_departments(self):
        self.clear_work_area()
        
        Label(self.work_area, text="🏢 ПОДРАЗДЕЛЕНИЯ", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
        
        if self.current_role == 'Администратор':
            Button(control_panel, text="➕ Добавить", command=self.add_department, 
                   bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
            Button(control_panel, text="✏️ Изменить", command=self.edit_department, 
                   bg='#f39c12', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
            Button(control_panel, text="🗑️ Удалить", command=self.delete_department, 
                   bg='#e74c3c', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        Button(control_panel, text="🔄 Обновить", command=self.show_departments, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название подразделения', 'ID руководителя', 'Количество сотрудников')
        
        self.departments_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.departments_tree.heading(col, text=col)
            self.departments_tree.column(col, width=200)
        
        self.departments_tree.pack(fill=BOTH, expand=True)
        
        self.load_departments()
    
    def load_departments(self):
        for item in self.departments_tree.get_children():
            self.departments_tree.delete(item)

        rows = list_departments(self.db.cursor)

        for row in rows:
            self.departments_tree.insert('', END, values=row)
        
    def add_department(self):
        self.department_window('add')
    
    def edit_department(self):
        selected = self.departments_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите подразделение!")
            return
        self.department_window('edit')
    
    def delete_department(self):
        selected = self.departments_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите подразделение!")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранное подразделение?"):
            item = self.departments_tree.item(selected[0])
            dept_id = item['values'][0]

            ok, msg = core_delete_department(self.db.cursor, self.db.conn, dept_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                self.show_departments()
            else:
                messagebox.showerror("Ошибка", msg)
    
    def department_window(self, mode):
        window = Toplevel(self.root)
        window.title("Подразделение")
        window.geometry("400x200")
        window.configure(bg='#ecf0f1')
        
        Label(window, text="🏢 ПОДРАЗДЕЛЕНИЕ", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
        
        Label(form_frame, text="Название:", bg='#ecf0f1', font=("Arial", 11)).grid(row=0, column=0, 
                                                                                    sticky=W, pady=10)
        name_entry = Entry(form_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=0, column=1, pady=10)
        
        if mode == 'edit':
            selected = self.departments_tree.selection()[0]
            item = self.departments_tree.item(selected)
            name_entry.insert(0, item['values'][1])
        
        def save():
            name = name_entry.get()

            dept_id = None
            if mode == 'edit':
                dept_id = item['values'][0]

            ok, msg = save_department(self.db.cursor, self.db.conn, name, dept_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                window.destroy()
                self.show_departments()
            else:
                messagebox.showerror("Ошибка", msg)
        
        Button(window, text="💾 СОХРАНИТЬ", command=save, bg='#27ae60', 
               fg='white', font=("Arial", 12, "bold"), width=15).pack(pady=20)
    
    # ==================== ДОЛЖНОСТИ ====================
    
    def show_positions(self):
        self.clear_work_area()
        
        Label(self.work_area, text="💼 ДОЛЖНОСТИ", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
        
        if self.current_role in ['Администратор', 'HR-менеджер']:
            Button(control_panel, text="➕ Добавить", command=self.add_position, 
                   bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
            Button(control_panel, text="✏️ Изменить", command=self.edit_position, 
                   bg='#f39c12', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
            Button(control_panel, text="🗑️ Удалить", command=self.delete_position, 
                   bg='#e74c3c', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        Button(control_panel, text="🔄 Обновить", command=self.show_positions, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Название должности', 'Базовая зарплата', 'Количество сотрудников')
        
        self.positions_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.positions_tree.heading(col, text=col)
            self.positions_tree.column(col, width=200)
        
        self.positions_tree.pack(fill=BOTH, expand=True)
        
        self.load_positions()
    
    def load_positions(self):
        for item in self.positions_tree.get_children():
            self.positions_tree.delete(item)

        rows = list_positions(self.db.cursor)

        for row in rows:
            self.positions_tree.insert('', END, values=row)
    
    def add_position(self):
        self.position_window('add')
    
    def edit_position(self):
        selected = self.positions_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите должность!")
            return
        self.position_window('edit')
    
    def delete_position(self):
        selected = self.positions_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите должность!")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранную должность?"):
            item = self.positions_tree.item(selected[0])
            pos_id = item['values'][0]

            ok, msg = core_delete_position(self.db.cursor, self.db.conn, pos_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                self.show_positions()
            else:
                messagebox.showerror("Ошибка", msg)
    
    def position_window(self, mode):
        window = Toplevel(self.root)
        window.title("Должность")
        window.geometry("400x250")
        window.configure(bg='#ecf0f1')
        
        Label(window, text="💼 ДОЛЖНОСТЬ", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
        
        Label(form_frame, text="Название:", bg='#ecf0f1', font=("Arial", 11)).grid(row=0, column=0, 
                                                                                    sticky=W, pady=10)
        name_entry = Entry(form_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=0, column=1, pady=10)
        
        Label(form_frame, text="Базовая зарплата:", bg='#ecf0f1', font=("Arial", 11)).grid(row=1, column=0, 
                                                                                            sticky=W, pady=10)
        salary_entry = Entry(form_frame, font=("Arial", 11), width=30)
        salary_entry.grid(row=1, column=1, pady=10)
        
        if mode == 'edit':
            selected = self.positions_tree.selection()[0]
            item = self.positions_tree.item(selected)
            name_entry.insert(0, item['values'][1])
            salary_entry.insert(0, item['values'][2])
        
        def save():
            name = name_entry.get()
            salary = salary_entry.get()

            pos_id = None
            if mode == 'edit':
                pos_id = item['values'][0]

            ok, msg = save_position(self.db.cursor, self.db.conn, name, salary, pos_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                window.destroy()
                self.show_positions()
            else:
                messagebox.showerror("Ошибка", msg)
        
        Button(window, text="💾 СОХРАНИТЬ", command=save, bg='#27ae60', 
               fg='white', font=("Arial", 12, "bold"), width=15).pack(pady=20)
    
    # ==================== ОТПУСКА ====================
    
    def show_vacations(self):
        self.clear_work_area()
        
        Label(self.work_area, text="🌴 ОТПУСКА", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
        
        Button(control_panel, text="➕ Добавить", command=self.add_vacation, 
               bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="✏️ Изменить", command=self.edit_vacation, 
               bg='#f39c12', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🗑️ Удалить", command=self.delete_vacation, 
               bg='#e74c3c', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🔄 Обновить", command=self.show_vacations, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Сотрудник', 'Дата начала', 'Дата окончания', 'Тип отпуска', 'Дней')
        
        self.vacations_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.vacations_tree.heading(col, text=col)
            self.vacations_tree.column(col, width=150)
        
        self.vacations_tree.pack(fill=BOTH, expand=True)
        
        self.load_vacations()
    
    def load_vacations(self):
        for item in self.vacations_tree.get_children():
            self.vacations_tree.delete(item)

        for row in list_vacations(self.db.cursor):
            self.vacations_tree.insert('', END, values=row)
    
    def add_vacation(self):
        self.vacation_window('add')
    
    def edit_vacation(self):
        selected = self.vacations_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите отпуск!")
            return
        self.vacation_window('edit')
    
    def delete_vacation(self):
        selected = self.vacations_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите отпуск!")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранный отпуск?"):
            item = self.vacations_tree.item(selected[0])
            vac_id = item['values'][0]

            ok, msg = core_delete_vacation(self.db.cursor, self.db.conn, vac_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                self.show_vacations()
            else:
                messagebox.showerror("Ошибка", msg)
    
    def vacation_window(self, mode):
        window = Toplevel(self.root)
        window.title("Отпуск")
        window.geometry("450x350")
        window.configure(bg='#ecf0f1')
        
        Label(window, text="🌴 ОТПУСК", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
        
        # Сотрудник
        Label(form_frame, text="Сотрудник:", bg='#ecf0f1', font=("Arial", 11)).grid(row=0, column=0, 
                                                                                     sticky=W, pady=10)
        emp_var = StringVar()
        emp_combo = ttk.Combobox(form_frame, textvariable=emp_var, font=("Arial", 11), width=28)
        
        employees = list_active_employees_for_vacation(self.db.cursor)

        emp_combo['values'] = [f"{e[0]} - {e[1]}" for e in employees]
        emp_combo.grid(row=0, column=1, pady=10)
        
        # Дата начала
        Label(form_frame, text="Дата начала (ГГГГ-ММ-ДД):", bg='#ecf0f1', 
              font=("Arial", 11)).grid(row=1, column=0, sticky=W, pady=10)
        start_entry = Entry(form_frame, font=("Arial", 11), width=30)
        start_entry.grid(row=1, column=1, pady=10)
        
        # Дата окончания
        Label(form_frame, text="Дата окончания (ГГГГ-ММ-ДД):", bg='#ecf0f1', 
              font=("Arial", 11)).grid(row=2, column=0, sticky=W, pady=10)
        end_entry = Entry(form_frame, font=("Arial", 11), width=30)
        end_entry.grid(row=2, column=1, pady=10)
        
        # Тип отпуска
        Label(form_frame, text="Тип отпуска:", bg='#ecf0f1', font=("Arial", 11)).grid(row=3, column=0, 
                                                                                       sticky=W, pady=10)
        type_var = StringVar(value='Ежегодный оплачиваемый')
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, font=("Arial", 11), width=28)
        type_combo['values'] = ['Ежегодный оплачиваемый', 'Без сохранения зарплаты', 
                               'Учебный', 'По уходу за ребенком']
        type_combo.grid(row=3, column=1, pady=10)
        
        if mode == 'edit':
            selected = self.vacations_tree.selection()[0]
            item = self.vacations_tree.item(selected)
            
            # Находим сотрудника
            emp_name = item['values'][1]
            for e in employees:
                if emp_name in e[1]:
                    emp_combo.set(f"{e[0]} - {e[1]}")
                    break
            
            start_entry.insert(0, item['values'][2])
            end_entry.insert(0, item['values'][3])
            type_combo.set(item['values'][4])
        
        def save():
            try:
                emp_id = int(emp_var.get().split(' - ')[0])
                start = start_entry.get()
                end = end_entry.get()
                vac_type = type_var.get()

                vac_id = None
                if mode == 'edit':
                    vac_id = item['values'][0]

                ok, msg = save_vacation(
                    self.db.cursor,
                    self.db.conn,
                    emp_id,
                    start,
                    end,
                    vac_type,
                    vac_id,
                )

                if ok:
                    messagebox.showinfo("Успех", msg)
                    window.destroy()
                    self.show_vacations()
                else:
                    messagebox.showerror("Ошибка", msg)

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        Button(window, text="💾 СОХРАНИТЬ", command=save, bg='#27ae60', 
               fg='white', font=("Arial", 12, "bold"), width=15).pack(pady=20)
    
    # ==================== ПРИКАЗЫ ====================
    
    # ==================== ПРИКАЗЫ (ОБНОВЛЁННАЯ ВЕРСИЯ) ====================

    def show_orders(self):
        self.clear_work_area()
    
        Label(self.work_area, text="📋 ПРИКАЗЫ", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
    
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
    
        Button(control_panel, text="➕ Добавить", command=self.add_order, 
               bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="✏️ Изменить", command=self.edit_order, 
               bg='#f39c12', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🗑️ Удалить", command=self.delete_order, 
               bg='#e74c3c', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="✅ Исполнить", command=self.execute_order, 
               bg='#9b59b6', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🔄 Обновить", command=self.show_orders, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
    
    # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
        scrollbar = Scrollbar(table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
    
        columns = ('ID', 'Тип приказа', 'Дата', 'Сотрудник', 'Описание', 'Статус')
    
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                       yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.orders_tree.yview)
    
        for col in columns:
            self.orders_tree.heading(col, text=col)
            if col == 'Описание':
                self.orders_tree.column(col, width=250)
            else:
                self.orders_tree.column(col, width=120)
    
        self.orders_tree.pack(fill=BOTH, expand=True)
    
        self.load_orders()

    def load_orders(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for row in list_orders(self.db.cursor):
            item_id = self.orders_tree.insert('', END, values=row)
            if row[5] == 'Исполнен':
                self.orders_tree.item(item_id, tags=('executed',))
            elif row[5] == 'Отменён':
                self.orders_tree.item(item_id, tags=('cancelled',))

        self.orders_tree.tag_configure('executed', background='#d5f4e6')
        self.orders_tree.tag_configure('cancelled', background='#fadbd8')

    def add_order(self):
        self.order_window('add')

    def edit_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите приказ!")
            return
    
        item = self.orders_tree.item(selected[0])
        if item['values'][5] == 'Исполнен':
            messagebox.showerror("Ошибка", "Нельзя редактировать исполненный приказ!")
            return
    
        self.order_window('edit')

    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите приказ!")
            return

        item = self.orders_tree.item(selected[0])
        order_id = item['values'][0]
        status = item['values'][5]

        if messagebox.askyesno("Подтверждение", "Удалить выбранный приказ?"):
            ok, msg = core_delete_order(self.db.cursor, self.db.conn, order_id, status)

            if ok:
                messagebox.showinfo("Успех", msg)
                self.show_orders()
            else:
                messagebox.showerror("Ошибка", msg)

    def execute_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите приказ для исполнения!")
            return

        item = self.orders_tree.item(selected[0])
        values = item['values']

        if values[5] == 'Исполнен':
            messagebox.showinfo("Информация", "Приказ уже исполнен!")
            return

        order_id = values[0]
        order_type = values[1]

        if not messagebox.askyesno(
            "Подтверждение",
            f"Исполнить приказ типа '{order_type}'?\n\nЭто действие изменит данные в системе.",
        ):
            return

        try:
            ok, msg = core_execute_order(self.db.cursor, self.db.conn, order_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                self.show_orders()
            else:
                messagebox.showerror("Ошибка", msg)

        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror("Ошибка", f"Не удалось исполнить приказ:\n{str(e)}")


    def order_window(self, mode):
        window = Toplevel(self.root)
        window.title("Приказ")
        window.geometry("600x650")
        window.configure(bg='#ecf0f1')
    
        Label(window, text="📋 ПРИКАЗ", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
    
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
    
        # Тип приказа
        Label(form_frame, text="Тип приказа:", bg='#ecf0f1', font=("Arial", 11)).grid(row=0, column=0, 
                                                                                   sticky=W, pady=10)
        type_var = StringVar(value='Прием на работу')
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, font=("Arial", 11), width=35, state='readonly')
        type_combo['values'] = ['Прием на работу', 'Увольнение', 'Перевод', 
                               'Отпуск', 'Изменение оклада', 'Премия', 'Взыскание']
        type_combo.grid(row=0, column=1, pady=10)
        type_combo.bind('<<ComboboxSelected>>', lambda e: update_fields())
    
        # Дата
        Label(form_frame, text="Дата приказа:", bg='#ecf0f1', 
              font=("Arial", 11)).grid(row=1, column=0, sticky=W, pady=10)
        date_entry = Entry(form_frame, font=("Arial", 11), width=37)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.grid(row=1, column=1, pady=10)
    
        # Сотрудник
        Label(form_frame, text="Сотрудник:", bg='#ecf0f1', font=("Arial", 11)).grid(row=2, column=0, 
                                                                                 sticky=W, pady=10)
        emp_var = StringVar()
        emp_combo = ttk.Combobox(form_frame, textvariable=emp_var, font=("Arial", 11), width=35)
    
        employees = list_employees_for_order(self.db.cursor) #!

        emp_combo['values'] = [f"{e[0]} - {e[1]}" for e in employees]
        emp_combo.grid(row=2, column=1, pady=10)
    
        # Описание
        Label(form_frame, text="Описание:", bg='#ecf0f1', font=("Arial", 11)).grid(row=3, column=0, 
                                                                                sticky=NW, pady=10)
        desc_text = Text(form_frame, font=("Arial", 10), width=37, height=4)
        desc_text.grid(row=3, column=1, pady=10)
    
       # Динамические поля (в зависимости от типа приказа)
        dynamic_frame = Frame(form_frame, bg='#ecf0f1')
        dynamic_frame.grid(row=4, column=0, columnspan=2, pady=10)
    
        dynamic_widgets = {}
    
        def update_fields():
            """Обновление полей в зависимости от типа приказа"""
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_widgets.clear()
        
            order_type = type_var.get()
            row = 0
        
            if order_type == 'Перевод':
                Label(dynamic_frame, text="Новое подразделение:", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                dept_var = StringVar()
                dept_combo = ttk.Combobox(dynamic_frame, textvariable=dept_var, 
                                         font=("Arial", 11), width=35)
                
                depts = list_departments_for_order(self.db.cursor)#!

                dept_combo['values'] = [f"{d[0]} - {d[1]}" for d in depts]
                dept_combo.grid(row=row, column=1, pady=5)
                dynamic_widgets['new_department'] = dept_var
            
                row += 1
                Label(dynamic_frame, text="Новая должность:", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                pos_var = StringVar()
                pos_combo = ttk.Combobox(dynamic_frame, textvariable=pos_var, 
                                        font=("Arial", 11), width=35)
                
                positions = list_positions_for_order(self.db.cursor)#!

                pos_combo['values'] = [f"{p[0]} - {p[1]}" for p in positions]
                pos_combo.grid(row=row, column=1, pady=5)
                dynamic_widgets['new_position'] = pos_var
        
            elif order_type == 'Отпуск':
                Label(dynamic_frame, text="Дата начала отпуска:", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                start_var = Entry(dynamic_frame, font=("Arial", 11), width=37)
                start_var.grid(row=row, column=1, pady=5)
                dynamic_widgets['start_date'] = start_var
            
                row += 1
                Label(dynamic_frame, text="Дата окончания отпуска:", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                end_var = Entry(dynamic_frame, font=("Arial", 11), width=37)
                end_var.grid(row=row, column=1, pady=5)
                dynamic_widgets['end_date'] = end_var
            
                row += 1
                Label(dynamic_frame, text="Тип отпуска:", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                vac_type_var = StringVar(value='Ежегодный оплачиваемый')
                vac_type_combo = ttk.Combobox(dynamic_frame, textvariable=vac_type_var, 
                                             font=("Arial", 11), width=35)
                vac_type_combo['values'] = ['Ежегодный оплачиваемый', 'Без сохранения зарплаты', 
                                        'Учебный', 'По уходу за ребенком']
                vac_type_combo.grid(row=row, column=1, pady=5)
                dynamic_widgets['vacation_type'] = vac_type_var
        
            elif order_type == 'Изменение оклада':
                Label(dynamic_frame, text="Новый оклад (руб):", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                salary_var = Entry(dynamic_frame, font=("Arial", 11), width=37)
                salary_var.grid(row=row, column=1, pady=5)
                dynamic_widgets['new_salary'] = salary_var
        
            elif order_type == 'Премия':
                Label(dynamic_frame, text="Сумма премии (руб):", bg='#ecf0f1', 
                      font=("Arial", 11)).grid(row=row, column=0, sticky=W, pady=5)
                bonus_var = Entry(dynamic_frame, font=("Arial", 11), width=37)
                bonus_var.grid(row=row, column=1, pady=5)
                dynamic_widgets['bonus_amount'] = bonus_var
    
        # Заполнение при редактировании
        if mode == 'edit':
            selected = self.orders_tree.selection()[0]
            item = self.orders_tree.item(selected)
            values = item['values']
        
            type_combo.set(values[1])
            date_entry.delete(0, END)
            date_entry.insert(0, values[2])
        
            emp_name = values[3]
            for e in employees:
                if emp_name in e[1]:
                    emp_combo.set(f"{e[0]} - {e[1]}")
                    break
        
            desc_text.insert('1.0', values[4])
        
            # Загружаем дополнительные данные
            order_id = values[0]

            order_data = get_order_data(self.db.cursor, order_id)
        
            update_fields()
        
            if order_data:
                import json
                try:
                    data = json.loads(order_data)
                    for key, value in data.items():
                        if key in dynamic_widgets:
                            widget = dynamic_widgets[key]
                            if isinstance(widget, StringVar):
                                widget.set(value)
                            elif isinstance(widget, Entry):
                                widget.delete(0, END)
                                widget.insert(0, value)
                except:
                    pass
        else:
            update_fields()
    
        # Кнопка сохранения
        def save():
            try:
                emp_id = int(emp_var.get().split(' - ')[0]) if emp_var.get() else None
                order_type = type_var.get()
                order_date = date_entry.get()
                description = desc_text.get('1.0', END).strip()
            
                # Собираем дополнительные данные
                order_data = {}
            
                if order_type == 'Перевод':
                    if 'new_department' in dynamic_widgets:
                        dept_str = dynamic_widgets['new_department'].get()
                        if dept_str:
                            order_data['new_department_id'] = int(dept_str.split(' - ')[0])
                    if 'new_position' in dynamic_widgets:
                        pos_str = dynamic_widgets['new_position'].get()
                        if pos_str:
                            order_data['new_position_id'] = int(pos_str.split(' - ')[0])
            
                elif order_type == 'Отпуск':
                    if 'start_date' in dynamic_widgets:
                        order_data['start_date'] = dynamic_widgets['start_date'].get()
                    if 'end_date' in dynamic_widgets:
                        order_data['end_date'] = dynamic_widgets['end_date'].get()
                    if 'vacation_type' in dynamic_widgets:
                        order_data['vacation_type'] = dynamic_widgets['vacation_type'].get()
            
                elif order_type == 'Изменение оклада':
                    if 'new_salary' in dynamic_widgets:
                        salary_str = dynamic_widgets['new_salary'].get()
                        if salary_str:
                            order_data['new_salary'] = float(salary_str)
                
                elif order_type == 'Премия':
                    if 'bonus_amount' in dynamic_widgets:
                        bonus_str = dynamic_widgets['bonus_amount'].get()
                        if bonus_str:
                            order_data['bonus_amount'] = float(bonus_str)
            
                order_id = None
                if mode == 'edit':
                    order_id = item['values'][0]

                ok, msg = create_or_update_order(
                    self.db.cursor,
                    self.db.conn,
                    order_type,
                    order_date,
                    emp_id,
                    description,
                    order_data,
                    order_id,
                )

                if ok:
                    messagebox.showinfo("Успех", msg)
                    window.destroy()
                    self.show_orders()
                else:
                    messagebox.showerror("Ошибка", msg)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить приказ:\n{str(e)}")
    
        Button(window, text="💾 СОХРАНИТЬ", command=save, bg='#27ae60', 
               fg='white', font=("Arial", 12, "bold"), width=20).pack(pady=15)
    
    # ==================== ПЕРЕВОДЫ ====================
    
    def show_transfers(self):
        self.clear_work_area()
        
        Label(self.work_area, text="🔄 ПЕРЕВОДЫ", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
        
        Button(control_panel, text="➕ Добавить", command=self.add_transfer, 
               bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🗑️ Удалить", command=self.delete_transfer, 
               bg='#e74c3c', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🔄 Обновить", command=self.show_transfers, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Сотрудник', 'Из подразделения', 'В подразделение', 'Дата перевода')
        
        self.transfers_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.transfers_tree.heading(col, text=col)
            self.transfers_tree.column(col, width=180)
        
        self.transfers_tree.pack(fill=BOTH, expand=True)
        
        self.load_transfers()
  
    def load_transfers(self):
        for item in self.transfers_tree.get_children():
            self.transfers_tree.delete(item)

        for row in list_transfers(self.db.cursor):
            self.transfers_tree.insert('', END, values=row)
    
    def add_transfer(self):
        window = Toplevel(self.root)
        window.title("Перевод")
        window.geometry("500x350")
        window.configure(bg='#ecf0f1')
        
        Label(window, text="🔄 ПЕРЕВОД СОТРУДНИКА", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
        
        # Сотрудник
        Label(form_frame, text="Сотрудник:", bg='#ecf0f1', font=("Arial", 11)).grid(row=0, column=0, 
                                                                                     sticky=W, pady=10)
        emp_var = StringVar()
        emp_combo = ttk.Combobox(form_frame, textvariable=emp_var, font=("Arial", 11), width=28)
        
        employees = list_working_employees_with_department(self.db.cursor)

        emp_combo['values'] = [f"{e[0]} - {e[1]}" for e in employees]
        emp_combo.grid(row=0, column=1, pady=10)
        
        # Новое подразделение
        Label(form_frame, text="Новое подразделение:", bg='#ecf0f1', 
              font=("Arial", 11)).grid(row=1, column=0, sticky=W, pady=10)
        dept_var = StringVar()
        dept_combo = ttk.Combobox(form_frame, textvariable=dept_var, font=("Arial", 11), width=28)
        
        departments = list_departments_for_transfer(self.db.cursor)#!

        dept_combo['values'] = [f"{d[0]} - {d[1]}" for d in departments]
        dept_combo.grid(row=1, column=1, pady=10)
        
        # Дата перевода
        Label(form_frame, text="Дата перевода (ГГГГ-ММ-ДД):", bg='#ecf0f1', 
              font=("Arial", 11)).grid(row=2, column=0, sticky=W, pady=10)
        date_entry = Entry(form_frame, font=("Arial", 11), width=30)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.grid(row=2, column=1, pady=10)
        
        def save():
            try:
                emp_id = int(emp_var.get().split(' - ')[0])
                new_dept_id = int(dept_var.get().split(' - ')[0])
                transfer_date = date_entry.get()
                
                # Получаем текущее подразделение
                ok, msg = create_transfer(
                    self.db.cursor,
                    self.db.conn,
                    emp_id,
                    new_dept_id,
                    transfer_date,
                )

                if ok:
                    messagebox.showinfo("Успех", msg)
                    window.destroy()
                    self.show_transfers()
                else:
                    messagebox.showerror("Ошибка", msg)
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        Button(window, text="💾 ВЫПОЛНИТЬ ПЕРЕВОД", command=save, bg='#27ae60', 
               fg='white', font=("Arial", 12, "bold"), width=20).pack(pady=20)
    
    def delete_transfer(self):
        selected = self.transfers_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите перевод!")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранный перевод?"):
            item = self.transfers_tree.item(selected[0])
            transfer_id = item['values'][0]

            ok, msg = core_delete_transfer(self.db.cursor, self.db.conn, transfer_id)

            if ok:
                messagebox.showinfo("Успех", msg)
                self.show_transfers()
            else:
                messagebox.showerror("Ошибка", msg)
    
    # ==================== ОТЧЁТЫ ====================
    
    def show_reports(self):
        self.clear_work_area()
        
        Label(self.work_area, text="📊 ОТЧЁТЫ И СТАТИСТИКА", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=20)
        
        reports_frame = Frame(self.work_area, bg='#ecf0f1')
        reports_frame.pack(pady=20)
        
        Button(reports_frame, text="📋 Общая статистика", command=self.report_general, 
               bg='#3498db', fg='white', font=("Arial", 12), width=25, height=2).grid(row=0, column=0, padx=10, pady=10)
        
        Button(reports_frame, text="👥 Сотрудники по подразделениям", command=self.report_by_department, 
               bg='#3498db', fg='white', font=("Arial", 12), width=25, height=2).grid(row=0, column=1, padx=10, pady=10)
        
        Button(reports_frame, text="💰 Зарплатный фонд", command=self.report_salary, 
               bg='#3498db', fg='white', font=("Arial", 12), width=25, height=2).grid(row=1, column=0, padx=10, pady=10)
        
        Button(reports_frame, text="🌴 График отпусков", command=self.report_vacations, 
               bg='#3498db', fg='white', font=("Arial", 12), width=25, height=2).grid(row=1, column=1, padx=10, pady=10)
        
        Button(reports_frame, text="📅 Сотрудники по стажу", command=self.report_experience, 
               bg='#3498db', fg='white', font=("Arial", 12), width=25, height=2).grid(row=2, column=0, padx=10, pady=10)
        
        Button(reports_frame, text="💼 Должности и зарплаты", command=self.report_positions_salary, 
               bg='#3498db', fg='white', font=("Arial", 12), width=25, height=2).grid(row=2, column=1, padx=10, pady=10)
    
    def report_general(self):
        window = Toplevel(self.root)
        window.title("Общая статистика")
        window.geometry("600x500")
        window.configure(bg='#ecf0f1')

        Label(window, text="📊 ОБЩАЯ СТАТИСТИКА", font=("Arial", 16, "bold"),
            bg='#ecf0f1').pack(pady=10)

        text_frame = Frame(window, bg='white')
        text_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        text = Text(text_frame, font=("Arial", 11), wrap=WORD)
        text.pack(fill=BOTH, expand=True)

        stats = get_general_statistics(self.db.cursor)

        report = f"""
╔═══════════════════════════════════════════════════════╗
║             ОБЩАЯ СТАТИСТИКА ПРЕДПРИЯТИЯ              ║
╚═══════════════════════════════════════════════════════╝

📊 ОСНОВНЫЕ ПОКАЗАТЕЛИ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 Общее количество сотрудников: {stats["total_employees"]}
🏢 Количество подразделений: {stats["total_departments"]}
🌴 Сотрудников в отпуске: {stats["employees_on_vacation"]}

💰 ФИНАНСОВЫЕ ПОКАЗАТЕЛИ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💵 Общий фонд заработной платы: {stats["total_salary"]:,.2f} руб.
📊 Средняя зарплата: {stats["average_salary"]:,.2f} руб.

📋 РАСПРЕДЕЛЕНИЕ ПО ПОДРАЗДЕЛЕНИЯМ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for dept, cnt in stats["department_distribution"]:
            report += f"\n🏢 {dept}: {cnt} чел."

        text.insert('1.0', report)
        text.config(state=DISABLED)
    
    def report_by_department(self):
        window = Toplevel(self.root)
        window.title("Сотрудники по подразделениям")
        window.geometry("900x600")
        window.configure(bg='#ecf0f1')

        Label(window, text="👥 СОТРУДНИКИ ПО ПОДРАЗДЕЛЕНИЯМ", font=("Arial", 16, "bold"),
            bg='#ecf0f1').pack(pady=10)

        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        columns = ('Подразделение', 'ФИО', 'Должность', 'Зарплата')

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        tree.pack(fill=BOTH, expand=True)

        for row in list_employees_by_department(self.db.cursor):
            tree.insert('', END, values=row)
    
    def report_salary(self):
        window = Toplevel(self.root)
        window.title("Зарплатный фонд")
        window.geometry("700x500")
        window.configure(bg='#ecf0f1')

        Label(window, text="💰 ЗАРПЛАТНЫЙ ФОНД", font=("Arial", 16, "bold"),
            bg='#ecf0f1').pack(pady=10)

        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        columns = ('Подразделение', 'Количество', 'Мин. зарплата', 'Макс. зарплата', 'Средняя', 'Общий фонд')

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill=BOTH, expand=True)

        total = 0

        for row in get_salary_fund_by_department(self.db.cursor):
            tree.insert('', END, values=(
                row[0],
                row[1],
                f"{row[2]:,.0f}" if row[2] else "0",
                f"{row[3]:,.0f}" if row[3] else "0",
                f"{row[4]:,.0f}" if row[4] else "0",
                f"{row[5]:,.0f}" if row[5] else "0",
            ))
            total += row[5] if row[5] else 0

        Label(window, text=f"💵 ИТОГО ФОНД ЗАРАБОТНОЙ ПЛАТЫ: {total:,.2f} руб.",
            font=("Arial", 14, "bold"), bg='#ecf0f1', fg='#27ae60').pack(pady=10)
    def report_vacations(self):
        window = Toplevel(self.root)
        window.title("График отпусков")
        window.geometry("900x600")
        window.configure(bg='#ecf0f1')

        Label(window, text="🌴 ГРАФИК ОТПУСКОВ", font=("Arial", 16, "bold"),
            bg='#ecf0f1').pack(pady=10)

        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        columns = ('ФИО', 'Подразделение', 'Начало', 'Окончание', 'Дней', 'Тип')

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        tree.pack(fill=BOTH, expand=True)

        for row in list_vacation_schedule(self.db.cursor):
            tree.insert('', END, values=row)
    def report_experience(self):
        window = Toplevel(self.root)
        window.title("Сотрудники по стажу")
        window.geometry("900x600")
        window.configure(bg='#ecf0f1')

        Label(window, text="📅 СОТРУДНИКИ ПО СТАЖУ РАБОТЫ", font=("Arial", 16, "bold"),
            bg='#ecf0f1').pack(pady=10)

        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        columns = ('ФИО', 'Подразделение', 'Должность', 'Дата приёма', 'Стаж (лет)')

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)

        tree.pack(fill=BOTH, expand=True)

        for row in list_employee_experience(self.db.cursor):
            tree.insert('', END, values=row)
    
    def report_positions_salary(self):
        window = Toplevel(self.root)
        window.title("Должности и зарплаты")
        window.geometry("700x500")
        window.configure(bg='#ecf0f1')

        Label(window, text="💼 ДОЛЖНОСТИ И ЗАРПЛАТЫ", font=("Arial", 16, "bold"),
            bg='#ecf0f1').pack(pady=10)

        table_frame = Frame(window)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        columns = ('Должность', 'Количество', 'Мин. зарплата', 'Макс. зарплата', 'Средняя зарплата')

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)

        tree.pack(fill=BOTH, expand=True)

        for row in list_positions_salary(self.db.cursor):
            tree.insert('', END, values=(
                row[0],
                row[1],
                f"{row[2]:,.0f}" if row[2] else "0",
                f"{row[3]:,.0f}" if row[3] else "0",
                f"{row[4]:,.0f}" if row[4] else "0",
            ))
        
    # ==================== ПОЛЬЗОВАТЕЛИ ====================
    
    def show_users(self):
        self.clear_work_area()
        
        Label(self.work_area, text="👤 ПОЛЬЗОВАТЕЛИ СИСТЕМЫ", font=("Arial", 18, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        control_panel = Frame(self.work_area, bg='#ecf0f1')
        control_panel.pack(pady=10)
        
        Button(control_panel, text="➕ Добавить", command=self.add_user, 
               bg='#27ae60', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="✏️ Изменить", command=self.edit_user, 
               bg='#f39c12', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        Button(control_panel, text="🔒 Деактивировать", command=self.deactivate_user, 
               bg='#e74c3c', fg='white', font=("Arial", 11), width=15).pack(side=LEFT, padx=5)
        Button(control_panel, text="🔄 Обновить", command=self.show_users, 
               bg='#3498db', fg='white', font=("Arial", 11), width=12).pack(side=LEFT, padx=5)
        
        # Таблица
        table_frame = Frame(self.work_area)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        columns = ('ID', 'Логин', 'Роль', 'Полное имя', 'Активен')
        
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)
        
        self.users_tree.pack(fill=BOTH, expand=True)
        
        self.load_users()
    
    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        self.db.cursor.execute('''
            SELECT user_id, login, role, full_name, 
                   CASE WHEN active=1 THEN 'Да' ELSE 'Нет' END
            FROM Users
        ''')
        
        for row in self.db.cursor.fetchall():
            self.users_tree.insert('', END, values=row)
    
    def add_user(self):
        self.user_window('add')
    
    def edit_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя!")
            return
        self.user_window('edit')
    
    def deactivate_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя!")
            return
        
        item = self.users_tree.item(selected[0])
        user_id = item['values'][0]
        
        if user_id == self.current_user:
            messagebox.showerror("Ошибка", "Нельзя деактивировать свой аккаунт!")
            return
        
        if messagebox.askyesno("Подтверждение", "Деактивировать выбранного пользователя?"):
            self.db.cursor.execute("UPDATE Users SET active=0 WHERE user_id=?", (user_id,))
            self.db.conn.commit()
            messagebox.showinfo("Успех", "Пользователь деактивирован!")
            self.show_users()
    
    def user_window(self, mode):
        window = Toplevel(self.root)
        window.title("Пользователь")
        window.geometry("450x400")
        window.configure(bg='#ecf0f1')
        
        Label(window, text="👤 ПОЛЬЗОВАТЕЛЬ", font=("Arial", 16, "bold"), 
              bg='#ecf0f1').pack(pady=10)
        
        form_frame = Frame(window, bg='#ecf0f1')
        form_frame.pack(padx=20, pady=10)
        
        # Логин
        Label(form_frame, text="Логин:", bg='#ecf0f1', font=("Arial", 11)).grid(row=0, column=0, 
                                                                                 sticky=W, pady=10)
        login_entry = Entry(form_frame, font=("Arial", 11), width=30)
        login_entry.grid(row=0, column=1, pady=10)
        
        # Пароль
        Label(form_frame, text="Пароль:", bg='#ecf0f1', font=("Arial", 11)).grid(row=1, column=0, 
                                                                                  sticky=W, pady=10)
        password_entry = Entry(form_frame, font=("Arial", 11), width=30)
        password_entry.grid(row=1, column=1, pady=10)
        
        # Роль
        Label(form_frame, text="Роль:", bg='#ecf0f1', font=("Arial", 11)).grid(row=2, column=0, 
                                                                                sticky=W, pady=10)
        role_var = StringVar(value='Сотрудник')
        role_combo = ttk.Combobox(form_frame, textvariable=role_var, font=("Arial", 11), width=28)
        role_combo['values'] = ['Администратор', 'HR-менеджер', 'Бухгалтер', 'Сотрудник']
        role_combo.grid(row=2, column=1, pady=10)
        
        # Полное имя
        Label(form_frame, text="Полное имя:", bg='#ecf0f1', font=("Arial", 11)).grid(row=3, column=0, 
                                                                                      sticky=W, pady=10)
        name_entry = Entry(form_frame, font=("Arial", 11), width=30)
        name_entry.grid(row=3, column=1, pady=10)
        
        if mode == 'edit':
            selected = self.users_tree.selection()[0]
            item = self.users_tree.item(selected)
            
            login_entry.insert(0, item['values'][1])
            login_entry.config(state='readonly')
            role_combo.set(item['values'][2])
            name_entry.insert(0, item['values'][3])
            
            Label(form_frame, text="(Оставьте пароль пустым,\nчтобы не менять)", 
                  bg='#ecf0f1', font=("Arial", 9), fg='gray').grid(row=4, column=1, sticky=W)
        
        def save():
            login = login_entry.get()
            password = password_entry.get()
            role = role_var.get()
            full_name = name_entry.get()
            
            if not login or not full_name:
                messagebox.showerror("Ошибка", "Заполните обязательные поля!")
                return
            
            try:
                if mode == 'add':
                    if not password:
                        messagebox.showerror("Ошибка", "Введите пароль!")
                        return

                    # Алгоритм хеширования пароля находится в core/auth.py,
                    # чтобы GUI не зависел от деталей хранения паролей.
                    hashed = hash_password(password)
                    self.db.cursor.execute('''
                        INSERT INTO Users (login, password, role, full_name)
                        VALUES (?, ?, ?, ?)
                    ''', (login, hashed, role, full_name))
                else:
                    user_id = item['values'][0]
                    if password:
                        # Используем общий helper из core/auth.py, чтобы создание и изменение
                        # паролей работали одинаково.
                        hashed = hash_password(password)
                        self.db.cursor.execute('''
                            UPDATE Users SET password=?, role=?, full_name=? WHERE user_id=?
                        ''', (hashed, role, full_name, user_id))
                    else:
                        self.db.cursor.execute('''
                            UPDATE Users SET role=?, full_name=? WHERE user_id=?
                        ''', (role, full_name, user_id))
                
                self.db.conn.commit()
                messagebox.showinfo("Успех", "Данные сохранены!")
                window.destroy()
                self.show_users()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
        
        Button(window, text="💾 СОХРАНИТЬ", command=save, bg='#27ae60', 
               fg='white', font=("Arial", 12, "bold"), width=15).pack(pady=20)
    
    # ==================== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ====================
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_work_area(self):
        for widget in self.work_area.winfo_children():
            widget.destroy()
    
    def logout(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.current_user = None
            self.current_role = None
            self.show_login_screen()

# ======================== ЗАПУСК ПРИЛОЖЕНИЯ ========================

def main():
    root = Tk()
    app = HRSystemApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()