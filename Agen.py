
# импорт всех нужных библиотек


import tkinter as tk
import secrets as se
import pyperclip
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import random
from faker import Faker
import backend
import csv
import sqlite3
import platform

# создаем экземпляр класса Faker под каждую страну

faker_rus = Faker('ru_RU')
faker_us = Faker('en_US')
faker = Faker()



# класс главного окна

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # переменные

        self.r1 = tk.StringVar(master=self)
        self.r2 = tk.StringVar(master=self)

        # заголовок окна

        self.title("Генератор учётной записи")


        # окно с информацией

        button = tk.Button(self, text="?", command=lambda: showinfo("?",
                                                                    "Надёжные пароли начинаются с 12 символов. "
                                                                    "Рекомендованный к использованию:"
                                                                    " \n -Cложный тип пароля от 15 символов."
                                                                    " \n ___Взлом такого пароля займёт более 3000 веков___"),
                           bg='#00ff00', font=('Calibri', 10))
        button.place(x=15, y=25)



        # ОКНА ТЕКСТА И ВЫВОДА
        self.password_lb = tk.Label(self, text='Выберите длину пароля', font=('Helvetica', 14), bg='#8b00ff',
                                    foreground="white")
        self.password_lb.place(x=50, y=60)


        # виджет Scale

        self.scale = ttkb.Scale(self, from_=8, to=100, orient='horizontal',
                                command=self.scale_update, length=200)
        self.scale.place(x=300, y=70)

        # отображение значения Scale

        self.scale_label = ttkb.Label(self, text='', font=(18))
        self.scale_label.place(x=380, y=40)

        # ЧЕКБОКС!!!!!!!!

        self.check_level = tk.Label(self, text='Выберите уровень', font=('Roboto', 14), bg='#8b00ff',
                                    foreground="white")
        self.check_level.place(x=50, y=108)

        self.var = IntVar()
        self.button1 = tk.Radiobutton(self, text='Простой', variable=self.var, value=0, font=('Roboto', 14),
                                      bg='#8b00ff')
        self.button1.place(x=250, y=108)
        self.button2 = tk.Radiobutton(self, text='Средний', variable=self.var, value=1, font=('Roboto', 14),
                                      bg='#8b00ff')
        self.button2.place(x=390, y=108)
        self.button3 = tk.Radiobutton(self, text='Сложный', variable=self.var, value=2, font=('Roboto', 14),
                                      bg='#8b00ff')
        self.button3.place(x=535, y=108)

        self.mail_lb = tk.Label(self, text='Почта', font=('Roboto', 14), bg='#8b00ff', foreground="white")
        self.mail_lb.place(x=50, y=156)

        items = ["Гугл", "Яндекс"]

        self.combobox_mail = ttk.Combobox(self, values=items, font=('Roboto', 14), textvariable=self.r1)
        self.combobox_mail.place(x=130, y=156)

        self.country_lb = tk.Label(self, text='Страна', font=('Roboto', 14), bg='#8b00ff', foreground="white")
        self.country_lb.place(x=50, y=204)
        countries = ['US', 'RUS']
        self.combobox_country = ttk.Combobox(self, values=countries, font=('Roboto', 14), textvariable=self.r2)
        self.combobox_country.place(x=130, y=204)

        self.password = tk.Button(self, text='Сгенерировать', font=('Roboto', 14), command=self.open, state='disabled')
        self.password.place(x=250, y=300)

        self.save = ttkb.Button(self, text='Сохранённые записи', command=self.open1)
        self.save.place(x=25, y=350)


    # позволяет отследить на наличие заполненных данных

        self.r1.trace('w', self.check)
        self.r2.trace('w', self.check)


    # открытие окна и получение значений с виджетов
    def open(self):
        child_window = ChildWindow(self.master, self.scale.get(), self.var.get(),
                                   self.combobox_mail.get(), self.combobox_country.get())


    """
    
    проверка на наличие указанных пользовтелем значений,
    в случае если их нет, кнопка активирована не будет
    
    """
    def check(self, *args):
        if ((self.r1.get() == 'Гугл' or self.r1.get()=='Яндекс') and
                (self.r2.get() == 'US' or self.r2.get() =='RUS') and self.scale.get()):
            self.password.config(state='normal')
        else:
            self.password.config(state='disabled')


    # обновление значения виджета Scale
    def scale_update(self, e):
        self.scale_label.config(text=f'{int(self.scale.get())}')

    # открытие окна 'сохраненные записи'
    def open1(self):
        window = ChildWindow2(self)


# окно которое появляется после нажатия кнопки "сгенерировать"
class ChildWindow(tk.Toplevel):
    def __init__(self, parent, scale_value=8, var_value=1, combobox_male_value='None',
                 combobox_country_value='None'):
        super().__init__(parent)


        # определение занчений с предыдущего окна
        self.combobox_country_value = combobox_country_value
        self.combobox_male_value = combobox_male_value
        self.scale_value = scale_value
        self.var_value = var_value

        # заголовок и иконка
        self.title("Учётная запись")

        if platform.system() == 'Windows':
            self.iconbitmap(r'C:\Users\Tanya\PycharmProjects\generator_app\app\icon.ico')

        # параметры окна
        self.geometry(calculate_window())


        # все виджеты
        self.password_entry_lb = tk.Label(self, text='Ваш пароль')
        self.password_entry_lb.place(x=120, y=50)

        self.entry = tk.Entry(self)
        self.entry.insert(10, f'{self.generate_password()}')
        self.entry.place(x=250, y=50)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda: self.copy_to_clipboard(self.entry), bootstyle='outline')
        self.copies.place(x=450, y=45)

        self.again = ttkb.Button(self, text='Сгенерировать заново', command=self.generate)
        self.again.place(x=250, y=350)

        self.nick_lb = tk.Label(self, text='Ваш ник')
        self.nick_lb.place(x=120, y=90)

        self.nick_entry = tk.Entry(self)
        self.nick_entry.insert(10, f'{self.generate_nick()}')
        self.nick_entry.place(x=250, y=90)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda : self.copy_to_clipboard(self.nick_entry), bootstyle='outline')
        self.copies.place(x=450, y=85)

        self.fio_lb = tk.Label(self, text='Ваше ФИО')
        self.fio_lb.place(x=120, y=130)

        self.fio_entry = tk.Entry(self)
        self.fio_entry.insert(10, f'{self.get_fio()}')
        self.fio_entry.place(x=250, y=130)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda : self.copy_to_clipboard(self.fio_entry), bootstyle='outline')
        self.copies.place(x=450, y=125)

        self.adress_lb = tk.Label(self, text='Адрес')
        self.adress_lb.place(x=120, y=170)

        self.adress_entry = tk.Entry(self)
        self.adress_entry.insert(10, f'{self.generate_adress()}')
        self.adress_entry.place(x=250, y=170)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda : self.copy_to_clipboard(self.adress_entry), bootstyle='outline')
        self.copies.place(x=450, y=165)

        self.birth_lb = tk.Label(self, text='Дата рождения')
        self.birth_lb.place(x=120, y=210)

        self.birth_entry = tk.Entry(self)
        self.birth_entry.insert(10, f'{self.birth_date()}')
        self.birth_entry.place(x=250, y=210)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda : self.copy_to_clipboard(self.birth_entry), bootstyle='outline')
        self.copies.place(x=450, y=205)

        self.gmail_lb = tk.Label(self, text='Ваша Почта')
        self.gmail_lb.place(x=120, y=250)

        self.gmail_entry = tk.Entry(self)
        self.gmail_entry.insert(10, f'{self.choose_mail()}')
        self.gmail_entry.place(x=250, y=250)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda : self.copy_to_clipboard(self.gmail_entry), bootstyle='outline')
        self.copies.place(x=450, y=245)

        self.phone_lb = tk.Label(self, text='Ном. телефона')
        self.phone_lb.place(x=120, y=290)

        self.phone_entry = tk.Entry(self)
        self.phone_entry.insert(10, f'{self.gen_phone()}')
        self.phone_entry.place(x=250, y=290)

        self.copies = ttkb.Button(self, text='Скопировать', command=lambda : self.copy_to_clipboard(self.phone_entry), bootstyle='outline')
        self.copies.place(x=450, y=285)

        # Кнопка для закрытия дочернего окна
        self.btn_close = ttkb.Button(self, text='Вернуться', command=lambda: self.destroy())
        self.btn_close.place(x=540, y=350)

        self.dbsave = ttkb.Button(self, text='Сохранить', command=self.save)
        self.dbsave.place(x=50, y=350)


    # основная функция копирования данных со строк
    def copy_to_clipboard(self, entry):
        copying = entry.get()
        pyperclip.copy(copying)


    # функция генерации адреса
    def generate_password(self):

        len = int(self.scale_value)
        CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        low = 'abcdefghijklmnopqrstuvwxyz'
        signs = '!@#$%^&*()-_|+=;:,./?\\`~[]{}'
        digits = '1234567890'
        allowed_chars = ''
        if self.var_value == 0:
            allowed_chars += low
        elif self.var_value == 1:
            allowed_chars += low + CAPS
        elif self.var_value == 2:
            allowed_chars += low + CAPS + signs + digits

        return ''.join(se.choice(allowed_chars) for _ in range(len))


    # функция генерации ников
    def generate_nick(self):
        first_names = ['black', 'white',
                       ' green', ' blue', ' red', ' white', ' black', ' yellow', ' orange', ' pink', ' purple',
                       ' silver',
                       ' gold', ' wooden', ' metal', ' plastic', ' stone', ' glass', ' ']
        last_names = ['dog', 'moon', 'rose', 'melon', 'bird', 'horse', 'sheep', 'cow', 'duck', 'goose',
                      'fish',
                      'crab', 'snake', 'bee', 'butterfly', 'dragonfly', 'ant', 'spider', 'dolphin', 'whale', 'seal',
                      'penguin', 'rabbit', 'squirrel', 'monkey', 'elephant', 'tiger', 'lion', 'bear', 'zebra',
                      'giraffe',
                      'camel']
        signs = ['_', ':', '.', '-', '|', '@', '$', '^', '*', ' ']
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        sign, sign1, sign2 = random.sample(signs, 3)
        result = sign + first_name + sign1 + last_name + sign2
        return result


    # генерация ФИО
    def get_fio(self):
        lang = self.combobox_country_value
        if lang == 'RUS':
            return faker_rus.name()
        elif lang == 'US':
            return faker_us.name()
        else:
            return 'None'


    # дата
    @staticmethod
    def birth_date():
        return faker.date('%d-%m-%Y')


    # адрес
    def generate_adress(self):
        lang = self.combobox_country_value
        if lang == 'RUS':
            return faker_rus.address()
        elif lang == 'US':
            return faker_us.address()

    # почта
    def choose_mail(self):
        mail = self.combobox_male_value
        if mail == 'Яндекс':
            return self.generate_nick() + '@yandex.ru'
        elif mail == 'Гугл':
            return self.generate_nick() + '@gmail.com'
        else:
            return 'None'

    # телефон
    def gen_phone(self):
        global country_code
        lang = self.combobox_country_value
        first = str(random.randint(900, 999)) + ' '
        second = str(random.randint(100, 999)) + ' '
        lasts = map(str, [random.randint(10, 99) for i in range(2)])
        if lang == 'RUS':
            country_code = '+7 '
        elif lang == 'US':
            country_code = '+1 '
        phone = country_code + first + second + '-'.join(lasts)
        return phone


    # вставка значений(заново)
    def update_entry(self, entry, generate_function):
        entry.delete(0, END)
        final_value = generate_function()
        entry.insert(10, final_value)


    def generate(self):
        self.update_entry(self.entry, self.generate_password)
        self.update_entry(self.adress_entry, self.generate_adress)
        self.update_entry(self.nick_entry, self.generate_nick)
        self.update_entry(self.gmail_entry, self.choose_mail)
        self.update_entry(self.birth_entry, self.birth_date)
        self.update_entry(self.fio_entry, self.get_fio)
        self.update_entry(self.phone_entry, self.gen_phone)

    # сохранение данных (с помощью функции, взятой с "бекенда" приложения,
    # то есть работающего с базой данных)
    def save(self):
        backend.enter(self.fio_entry.get(), self.nick_entry.get(),
                      self.gmail_entry.get(), self.entry.get(), self.phone_entry.get(),
                      self.adress_entry.get(), self.birth_entry.get())
        messagebox.showinfo("i", "Запись сохранена")



# окно 'Сохраненные записи'
class ChildWindow2(tk.Toplevel):
    def __init__(self, parent):
        global your_copy
        super().__init__(parent)

        self.title('Сохранённые записи')

        self.geometry(calculate_window())

        # виджеты

        self.button = ttkb.Button(self, text='Экспортировать', command=self.export)
        self.button.place(x=280,y=350)

        if platform.system() == 'Windows':
            self.iconbitmap(r'C:\Users\Tanya\PycharmProjects\generator_app\app\icon.ico')



        self.label = tk.Label(self, text='Учетные записи')
        self.label.pack()

        # виджет 'Дерево', где хранятся все данные

        self.tree = ttk.Treeview(self, height=5)
        self.tree['columns'] = ('ФИО', 'Ник', 'Почта', 'Пароль', 'Номер телефона', 'Адрес', 'Дата рождения')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('ФИО', width=60, anchor=W)
        self.tree.column('Ник', width=60, anchor=W)
        self.tree.column('Почта', width=60, anchor=W)
        self.tree.column('Пароль', width=60, anchor=W)
        self.tree.column('Номер телефона', width=80, anchor=W)
        self.tree.column('Адрес', width=80, anchor=W)
        self.tree.column('Дата рождения', width=80, anchor=W)
        self.tree.heading('#0', text='')
        self.tree.heading('ФИО', text='ФИО')
        self.tree.heading('Ник', text='Ник')
        self.tree.heading('Почта', text='Почта')
        self.tree.heading('Пароль', text='Пароль')
        self.tree.heading('Номер телефона', text='Ном.телефона')
        self.tree.heading('Адрес', text='Адрес')
        self.tree.heading('Дата рождения', text='Дата рождения')
        self.tree.pack()


        # вставка значений с базы данных (функция "show" берем с бекенда)
        for row in backend.show():
            self.tree.insert(parent='', text='', index='end',
                             values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


        # всплывающее меню
        self.popup1 = tk.Menu(self.tree, tearoff=0)
        self.popup1.add_command(
            command=self.copy,
            label="Копировать")
        self.popup1.add_command(
            command=self.delete,
            label="Удалить")
        self.popup1.add_command(
            command=self.quit,
            label="Выйти")

        self.tree.bind('<Button-3>', self.popup_menu)


    # функция меню которая позволяет скопировать всю строку
    def copy(self):
        for selection in self.tree.selection():
            item = self.tree.item(selection)
            fio, nick, mail, password, phone, adress, date = item["values"][0:8]
            text = ("ФИО:{}, Ник:{}, Почта:{}, Пароль:{}, "
                    "Телефон: {}, Адрес:{}, Дата рождения:{}").format(fio, nick, mail, password, phone, adress, date)
            pyperclip.copy(text)  # копировать данные в буфер обмена


    # позволяет удалить всю строку
    def delete(self):
        try:
            selected_item = self.tree.selection()[0]
            values = tuple(self.tree.item(selected_item)['values'])
            self.tree.delete(selected_item)
            conn = sqlite3.connect('table.db')
            cursor = conn.cursor()

            query = "DELETE FROM data WHERE fio=? AND nick=? AND mail=? AND password=? AND phone=? AND adress=? AND date=?"
            cursor.execute(query, (*values,))
            conn.commit()
            conn.close()
            tk.messagebox.showinfo(title='i', message='Запись удалена!')
        except IndexError:
            tk.messagebox.showerror(title='!!!', message='Операция невозможна. \nТаблица пуста')



    def popup_menu(self, event):
        self.tree.identify_row(event.y)
        self.popup1.post(event.x_root, event.y_root)


    # экспортирование данных в csv формат
    def export(self):
        pop = Toplevel(self)
        if platform.system() == 'Windows':
            pop.iconbitmap(r'C:\Users\Tanya\PycharmProjects\generator_app\app\icon.ico')
        pop.geometry('250x150')
        self.v = StringVar()
        Label(pop, text='Сохранить файл как').place(x=50,y=15)
        ttkb.Entry(pop, textvariable=self.v).place(x=46,y=50)
        ttkb.Button(pop, text='Сохранить', width=18,
                   command=lambda: exp(self.v.get())).place(x=50,y=90)

        def exp(x):
            with open(x + '.csv', 'w', newline='') as f:
                chompa = csv.writer(f, dialect='excel')
                for r in backend.show():
                    chompa.writerow(r)
            messagebox.showinfo("Файл сохранён", "Сохранён как " + x + ".csv")

    def view(self):
        if backend.check() is False:
            messagebox.showerror('Тут ничего нет :(')
        else:
            for row in backend.show():
                self.tree.insert(parent='', text='', index='end',
                                 values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))



if __name__ == '__main__':
    app = MainWindow()

    # если система на которой запускается приложение Windows, то изменяется иконка
    if platform.system() == 'Windows':
        app.iconbitmap(r'C:\Users\Tanya\PycharmProjects\generator_app\app\icon.ico')

    style = ttkb.Style("vapor")

    def calculate_window():
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        # Вычисляем координаты окна приложения
        window_width = 700
        window_height = 400
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        return f"{window_width}x{window_height}+{x}+{y}"


    app.geometry(calculate_window())
    app.mainloop()
