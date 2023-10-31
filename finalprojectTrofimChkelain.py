import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import re

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('employee_db.db')
cursor = conn.cursor()

# Создаем таблицу для хранения информации о сотрудниках
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        phone_number TEXT,
        email TEXT,
        salary REAL
    )
''')
conn.commit()

# Функция для добавления нового сотрудника
def add_employee():
    full_name = full_name_entry.get()
    phone_number = phone_number_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if full_name and phone_number and email and salary:
        cursor.execute('''
            INSERT INTO employees (full_name, phone_number, email, salary)
            VALUES (?, ?, ?, ?)
        ''', (full_name, phone_number, email, salary))
        conn.commit()
        messagebox.showinfo("Успешно", "Сотрудник добавлен")
        clear_entries()
    else:
        messagebox.showerror("Ошибка", "Заполните все поля")

# Функция для изменения данных сотрудника
def edit_employee_info():
    selected_item = employee_list.curselection()
    if not selected_item:
        return

    index = selected_item[0]
    employee_info = employee_list.get(index)
    employee_id = int(re.search(r'ID: (\d+)', employee_info).group(1))

    # Создаем новое окно для ввода новых данных сотрудника
    edit_window = tk.Toplevel(root)
    edit_window.title("Изменить данные сотрудника")

    # Загружаем текущие данные сотрудника
    cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
    employee_data = cursor.fetchone()

    current_full_name = employee_data[1]
    current_email = employee_data[3]
    current_phone = employee_data[2]

    current_full_name_label = tk.Label(edit_window, text="Текущее ФИО:")
    current_full_name_label.pack()

    current_full_name_entry = tk.Entry(edit_window)
    current_full_name_entry.insert(0, current_full_name)
    current_full_name_entry.pack()

    current_email_label = tk.Label(edit_window, text="Текущая почта:")
    current_email_label.pack()

    current_email_entry = tk.Entry(edit_window)
    current_email_entry.insert(0, current_email)
    current_email_entry.pack()

    current_phone_label = tk.Label(edit_window, text="Текущий номер телефона:")
    current_phone_label.pack()

    current_phone_entry = tk.Entry(edit_window)
    current_phone_entry.insert(0, current_phone)
    current_phone_entry.pack()

    def update_employee_data():
        new_full_name = current_full_name_entry.get()
        new_email = current_email_entry.get()
        new_phone = current_phone_entry.get()

        if new_full_name and new_email and new_phone:
            cursor.execute('''
                UPDATE employees
                SET full_name = ?, email = ?, phone_number = ?
                WHERE id = ?
            ''', (new_full_name, new_email, new_phone, employee_id))
            conn.commit()
            messagebox.showinfo("Успешно", "Данные сотрудника обновлены")
            edit_window.destroy()
            view_employees()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    update_button = tk.Button(edit_window, text="Изменить данные", command=update_employee_data)
    update_button.pack()

# Функция для отображения списка сотрудников
def view_employees():
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    employee_list.delete(0, tk.END)
    for row in rows:
        employee_list.insert(tk.END,
                             f"ID: {row[0]}, ФИО: {row[1]}, Телефон: {row[2]}, Email: {row[3]}, Зарплата: {row[4]}")

# Функция для поиска сотрудника по ФИО
def search_employee():
    name = search_name_entry.get()
    cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', ('%' + name + '%',))
    rows = cursor.fetchall()
    employee_list.delete(0, tk.END)
    if rows:
        for row in rows:
            employee_list.insert(tk.END,
                                 f"ID: {row[0]}, ФИО: {row[1]}, Телефон: {row[2]}, Email: {row[3]}, Зарплата: {row[4]}")
    else:
        messagebox.showinfo("Результат", "Сотрудники не найдены")

# Функция для очистки полей ввода
def clear_entries():
    full_name_entry.delete(0, tk.END)
    phone_number_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

def delete_all_employees():
    confirmed = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить всех сотрудников?")
    if confirmed:
        cursor.execute('DELETE FROM employees')
        conn.commit()
        view_employees()

# Функция для удаления сотрудника
def delete_employee():
    selected_item = employee_list.curselection()
    if not selected_item:
        return

    index = selected_item[0]
    employee_info = employee_list.get(index)

    # Извлекаем идентификатор сотрудника с использованием регулярного выражения
    match = re.search(r'ID: (\d+)', employee_info)
    if match:
        employee_id = int(match.group(1))
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        messagebox.showinfo("Успешно", "Сотрудник удален")
        view_employees()
    else:
        messagebox.showerror("Ошибка", "Невозможно определить идентификатор сотрудника")

# Функция для изменения данных сотрудника
def edit_employee():
    selected_item = employee_list.curselection()
    if not selected_item:
        return

    index = selected_item[0]
    employee_info = employee_list.get(index)
    employee_id = int(re.search(r'ID: (\d+)', employee_info).group(1))

    # Создаем новое окно для ввода новой зарплаты
    edit_window = tk.Toplevel(root)
    edit_window.title("Изменить зарплату")

    salary_label = tk.Label(edit_window, text="Новая зарплата:")
    salary_label.pack()

    new_salary_entry = tk.Entry(edit_window)
    new_salary_entry.pack()

    def update_salary():
        new_salary = new_salary_entry.get()
        try:
            new_salary = float(new_salary)
            cursor.execute('UPDATE employees SET salary = ? WHERE id = ?', (new_salary, employee_id))
            conn.commit()
            messagebox.showinfo("Успешно", "Зарплата сотрудника обновлена")
            edit_window.destroy()
            view_employees()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат зарплаты")

    update_button = tk.Button(edit_window, text="Изменить", command=update_salary)
    update_button.pack()

# Создаем главное окно
root = tk.Tk()
root.title("Список сотрудников компании")

delete_all_button = tk.Button(root, text="Удалить всех сотрудников", command=delete_all_employees)
delete_all_button.grid(row=11, column=0, columnspan=2)

# Создаем и размещаем элементы интерфейса

full_name_label = tk.Label(root, text="ФИО:")
full_name_label.grid(row=0, column=0)
full_name_entry = tk.Entry(root)
full_name_entry.grid(row=0, column=1)

phone_number_label = tk.Label(root, text="Номер телефона:")
phone_number_label.grid(row=1, column=0)
phone_number_entry = tk.Entry(root)
phone_number_entry.grid(row=1, column=1)

email_label = tk.Label(root, text="Email:")
email_label.grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

salary_label = tk.Label(root, text="Зарплата:")
salary_label.grid(row=3, column=0)
salary_entry = tk.Entry(root)
salary_entry.grid(row=3, column=1)

add_button = tk.Button(root, text="Добавить сотрудника", command=add_employee)
add_button.grid(row=4, column=0, columnspan=2)

view_button = tk.Button(root, text="Просмотреть сотрудников", command=view_employees)
view_button.grid(row=5, column=0, columnspan=2)

search_name_label = tk.Label(root, text="Поиск по ФИО:")
search_name_label.grid(row=6, column=0)
search_name_entry = tk.Entry(root)
search_name_entry.grid(row=6, column=1)

search_button = tk.Button(root, text="Найти", command=search_employee)
search_button.grid(row=7, column=0, columnspan=2)

employee_list = tk.Listbox(root, height=10, width=60)
employee_list.grid(row=8, column=0, columnspan=2)

delete_button = tk.Button(root, text="Удалить сотрудника", command=delete_employee)
delete_button.grid(row=9, column=0, columnspan=2)

edit_button = tk.Button(root, text="Изменить зарплату", command=edit_employee)
edit_button.grid(row=10, column=0, columnspan=2)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
scrollbar.grid(row=8, column=2, rowspan=3, sticky=tk.N + tk.S)

employee_list = tk.Listbox(root, height=10, width=60, yscrollcommand=scrollbar.set)
employee_list.grid(row=8, column=0, columnspan=2)
scrollbar.config(command=employee_list.yview)

delete_button = tk.Button(root, text="Удалить сотрудника", command=delete_employee)
delete_button.grid(row=9, column=0, columnspan=2)

edit_button = tk.Button(root, text="Изменить зарплату", command=edit_employee)
edit_button.grid(row=10, column=0, columnspan=2)
edit_info_button = tk.Button(root, text="Изменить данные о сотруднике", command=edit_employee_info)
edit_info_button.grid(row=15, column=0, columnspan=2)  # Изменили row для корректного размещения
# Запускаем главное окно
root.mainloop()

# Закрываем соединение с базой данных при выходе из программы
conn.close()