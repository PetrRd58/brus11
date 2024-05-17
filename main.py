import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv

# Функция для расчета количества бруса
def calculate_lumber_length(length, width, height):
    wall_area = 2 * (length + width) * height  # Площадь стен
    lumber_volume = wall_area * 1.2  # Объем бруса (площадь стен умноженная на 20% для учета толщины стен)
    return lumber_volume

# Функция для сохранения данных о здании в базу данных
def save_building_data_to_db(name, length, width, height, lumber_quantity):
    conn = sqlite3.connect('buildings.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS buildings
                      (id INTEGER PRIMARY KEY,
                      name TEXT,
                      length REAL,
                      width REAL,
                      height REAL,
                      brus_quantity REAL)''')
    cursor.execute("INSERT INTO buildings (name, length, width, height, brus_quantity) VALUES (?, ?, ?, ?, ?)",
                   (name, length, width, height, lumber_quantity))
    conn.commit()
    conn.close()

# Функция для сохранения данных о здании в файл CSV
def save_building_data_to_csv(name, length, width, height, lumber_quantity):
    with open('buildings.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, length, width, height, lumber_quantity])

# Функция для обработки нажатия кнопки "Рассчитать количество бруса"
def calculate_lumber():
    try:
        length = float(length_entry.get())
        width = float(width_entry.get())
        height = float(height_entry.get())

        lumber_quantity = calculate_lumber_length(length, width, height)

        lumber_result_label.config(text="Количество бруса: {:.2f} куб. м".format(lumber_quantity))
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите числовые значения для длины, ширины и высоты.")

# Функция для обработки нажатия кнопки "Сохранить данные"
def save_data():
    name = name_entry.get()
    length = length_entry.get()
    width = width_entry.get()
    height = height_entry.get()
    brus_quantity = lumber_result_label.cget("text").split(": ")[1].split(" ")[0]

    save_building_data_to_db(name, length, width, height, brus_quantity)
    save_building_data_to_csv(name, length, width, height, brus_quantity)
    messagebox.showinfo("Успех", "Данные успешно сохранены.")

# Создание графического интерфейса
root = tk.Tk()
root.title("Расчет количества бруса для строения")

name_label = tk.Label(root, text="Название здания:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

length_label = tk.Label(root, text="Длина здания (м):")
length_label.grid(row=1, column=0, padx=5, pady=5)
length_entry = tk.Entry(root)
length_entry.grid(row=1, column=1, padx=5, pady=5)

width_label = tk.Label(root, text="Ширина здания (м):")
width_label.grid(row=2, column=0, padx=5, pady=5)
width_entry = tk.Entry(root)
width_entry.grid(row=2, column=1, padx=5, pady=5)

height_label = tk.Label(root, text="Высота здания (м):")
height_label.grid(row=3, column=0, padx=5, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=3, column=1, padx=5, pady=5)

calculate_button = tk.Button(root, text="Рассчитать количество бруса", command=calculate_lumber)
calculate_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

lumber_result_label = tk.Label(root, text="Количество бруса: ")
lumber_result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

save_button = tk.Button(root, text="Сохранить данные", command=save_data)
save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
