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
from ttkbootstrap.dialogs import QueryDialog

import backend
import csv


faker_rus = Faker('ru_RU')
faker_us = Faker('en_US')
faker = Faker()




class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.r1 = tk.StringVar(master=self)
        self.r2 = tk.StringVar(master=self)
        self.title("Генератор учётной записи")




        button = ttkb.Button(self, text="?", command=lambda: showinfo("?",
                                                                    "Надёжные пароли начинаются с 12 символов. "
                                                                    "Рекомендованный к использованию:"
                                                                    " \n -Cложный тип пароля от 15 символов."
                                                                    " \n ___Взлом такого пароля займёт более 3000 веков___"))
        button.grid(column=0,row=0, pady=10, padx=10, sticky='w')

        # Кнопка для открытия дочернего окна

        # ОКНА ТЕКСТА И ВЫВОДА
        self.password_lb = ttkb.Label(self, text='Выберите длину пароля', foreground="white", font=(24))
        self.password_lb.grid(column=1,row=3, pady=4,sticky='w')

        self.scale = ttkb.Scale(self, from_=8, to=100, orient='horizontal', command=self.scale_update)
        self.scale.grid(column=2,row=3, pady=8, sticky='nsew')

        self.scale_label = ttkb.Label(self, text='', font=(18))
        self.scale_label.grid(column=2,row=2)

        # ЧЕКБОКС!!!!!!!!

        self.check_level = ttkb.Label(self, text='Выберите уровень', foreground="white", font=(24))
        self.check_level.grid(column=1,row=4, pady=8, sticky='w')

        self.var = IntVar()
        self.button1 = ttkb.Radiobutton(self, text='Простой', variable=self.var, value=0)
        self.button1.grid(column=2,row=4, sticky='w', padx=8, pady=8)
        self.button2 = ttkb.Radiobutton(self, text='Средний', variable=self.var, value=1)
        self.button2.grid(column=3,row=4, sticky='w', padx=2, pady=8)
        self.button3 = ttkb.Radiobutton(self, text='Сложный', variable=self.var, value=2)
        self.button3.grid(column=4,row=4, sticky='w', padx=2, pady=8)

        self.mail_lb = ttkb.Label(self, text='Почта', foreground="white", font=(18))
        self.mail_lb.grid(column=1,row=5, pady=8, sticky='w')

        items = ["Гугл", "Яндекс"]

        self.combobox_mail = ttkb.Combobox(self, values=items, textvariable=self.r1)
        self.combobox_mail.grid(column=2,row=5, sticky='e', pady=8)

        self.country_lb = ttkb.Label(self, text='Страна', foreground="white", font=(18))
        self.country_lb.grid(column=1,row=6, pady=8, sticky='w')
        countries = ['US', 'RUS']
        self.combobox_country = ttkb.Combobox(self, values=countries, textvariable=self.r2)
        self.combobox_country.grid(column=2,row=6, pady=8)

        self.password = ttkb.Button(self, text='Сгенерировать', command=self.open, state='disabled')
        self.password.grid(column=1,row=7, sticky='e', pady=8)

        self.save = ttkb.Button(self, text='Сохранённые записи', command=self.open1)
        self.save.grid(column=0,row=8, padx=10, pady=16, sticky='s')


        self.r1.trace('w', self.check)
        self.r2.trace('w', self.check)



    def open(self):
        child_window = ChildWindow(self.master,
                                   self.scale.get(),
                                   self.var.get(),
                                   self.combobox_mail.get(),
                                   self.combobox_country.get())

    def check(self, *args):
        if ((self.r1.get() == 'Гугл' or self.r1.get() == 'Яндекс')
                and (self.r2.get() == 'US' or self.r2.get() == 'RUS')
                and self.scale.get()):
            self.password.config(state='normal')

        else:
            self.password.config(state='disabled')

    def scale_update(self, e):
        self.scale_label.config(text=f'{int(self.scale.get())}')


    def open1(self):
        window = ChildWindow2(self)



class ChildWindow(tk.Toplevel):
    def __init__(self, parent, scale_value=8, var_value=1, combobox_male_value='uuu',
                 combobox_country_value='None'):
        super().__init__(parent)

        self.nick = self.generate_nick()
        self.combobox_country_value = combobox_country_value
        self.combobox_male_value = combobox_male_value
        self.scale_value = scale_value
        self.var_value = var_value

        self.title("Учётная запись")


        self.geometry(calculate_window())

        self.password_entry_lb = tk.Label(self, text='Ваш пароль')
        self.password_entry_lb.place(x=120, y=50)

        self.entry = tk.Entry(self)
        self.entry.insert(10, f'{self.generate_password()}')
        self.entry.place(x=250, y=50)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard, bootstyle='outline')
        self.copies.place(x=400, y=45)

        self.again = tk.Button(self, text='Сгенерировать заново', command=self.generate)
        self.again.place(x=250, y=350)

        self.nick_lb = tk.Label(self, text='Ваш ник')
        self.nick_lb.place(x=120, y=90)

        self.nick_entry = tk.Entry(self)
        self.nick_entry.insert(10, f'{self.nick}')
        self.nick_entry.place(x=250, y=90)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard1, bootstyle='outline')
        self.copies.place(x=400, y=85)

        self.fio_lb = tk.Label(self, text='Ваше ФИО')
        self.fio_lb.place(x=120, y=130)

        self.fio_entry = tk.Entry(self)
        self.fio_entry.insert(10, f'{self.get_fio()}')
        self.fio_entry.place(x=250, y=130)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard2, bootstyle='outline')
        self.copies.place(x=400, y=125)

        self.adress_lb = tk.Label(self, text='Адрес')
        self.adress_lb.place(x=120, y=170)

        self.adress_entry = tk.Entry(self)
        self.adress_entry.insert(10, f'{self.generate_adress()}')
        self.adress_entry.place(x=250, y=170)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard3, bootstyle='outline')
        self.copies.place(x=400, y=165)

        self.birth_lb = tk.Label(self, text='Дата рождения')
        self.birth_lb.place(x=120, y=210)

        self.birth_entry = tk.Entry(self)
        self.birth_entry.insert(10, f'{self.birth_date()}')
        self.birth_entry.place(x=250, y=210)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard4, bootstyle='outline')
        self.copies.place(x=400, y=205)

        self.gmail_lb = tk.Label(self, text='Ваша Почта')
        self.gmail_lb.place(x=120, y=250)

        self.gmail_entry = tk.Entry(self)
        self.gmail_entry.insert(10, f'{self.choose_mail()}')
        self.gmail_entry.place(x=250, y=250)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard5, bootstyle='outline')
        self.copies.place(x=400, y=245)

        self.phone_lb = tk.Label(self, text='Ном. телефона')
        self.phone_lb.place(x=120, y=290)

        self.phone_entry = tk.Entry(self)
        self.phone_entry.insert(10, f'{self.gen_phone()}')
        self.phone_entry.place(x=250, y=290)

        self.copies = ttkb.Button(self, text='Скопировать', command=self.copy_to_clipboard6, bootstyle='outline')
        self.copies.place(x=400, y=285)

        # Кнопка для закрытия дочернего окна
        self.btn_close = tk.Button(self, text='Close', command=lambda: self.destroy())
        self.btn_close.place(x=540, y=350)

        self.dbsave = tk.Button(self, text='Сохранить', command=self.save)
        self.dbsave.place(x=50, y=350)



    def copy_to_clipboard(self):
        copying = self.entry.get()
        pyperclip.copy(copying)

    def copy_to_clipboard1(self):
        copying = self.nick_entry.get()
        pyperclip.copy(copying)

    def copy_to_clipboard2(self):
        copying = self.fio_entry.get()
        pyperclip.copy(copying)

    def copy_to_clipboard3(self):
        copying = self.adress_entry.get()
        pyperclip.copy(copying)

    def copy_to_clipboard4(self):
        copying = self.birth_entry.get()
        pyperclip.copy(copying)

    def copy_to_clipboard5(self):
        copying = self.gmail_entry.get()
        pyperclip.copy(copying)

    def copy_to_clipboard6(self):
        copying = self.phone_entry.get()
        pyperclip.copy(copying)

    def generate_password(self):

        len = int(self.scale_value)
        CAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        low = 'abcdefghijklmnopqrstuvwxyz'
        signs = '!@#$%^&*()-_|+=;:,./?\`~[]{}'
        digits = '1234567890'
        allowed_chars = ''
        if self.var_value == 0:
            allowed_chars += low
        elif self.var_value == 1:
            allowed_chars += low + CAPS
        elif self.var_value == 2:
            allowed_chars += low + CAPS + signs + digits

        return ''.join(se.choice(allowed_chars) for _ in range(len))

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
        signs = ['_', ':', '.', '-', '|']
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        sign = random.choice(signs)
        result = first_name + sign + last_name
        return result

    def get_fio(self):
        lang = self.combobox_country_value
        if lang == 'RUS':
            return faker_rus.name()
        elif lang == 'US':
            return faker_us.name()
        else:
            return 'None'

    @staticmethod
    def birth_date():
        return faker.date('%d-%m-%Y')

    def generate_adress(self):
        lang = self.combobox_country_value
        if lang == 'RUS':
            return faker_rus.address()
        elif lang == 'US':
            return faker_us.address()

    def choose_mail(self):
        mail = self.combobox_male_value
        if mail == 'Яндекс':
            return self.generate_nick() + '@yandex.ru'
        elif mail == 'Гугл':
            return self.generate_nick() + '@gmail.com'
        else:
            return 'None'

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

    def generate(self):
        self.entry.delete(0, END)
        final_password = self.generate_password()
        self.entry.insert(10, final_password)
        self.adress_entry.delete(0, END)
        final_adress = self.generate_adress()
        self.adress_entry.insert(10, final_adress)
        self.nick_entry.delete(0, END)
        final_nick = self.generate_nick()
        self.nick_entry.insert(10, final_nick)
        self.gmail_entry.delete(0, END)
        final_mail = self.choose_mail()
        self.gmail_entry.insert(10, final_mail)
        self.birth_entry.delete(0, END)
        final_date = self.birth_date()
        self.birth_entry.insert(10, final_date)
        self.fio_entry.delete(0, END)
        final_fio = self.get_fio()
        self.fio_entry.insert(10, final_fio)
        self.phone_entry.delete(0, END)
        final_phone = self.gen_phone()
        self.phone_entry.insert(10, final_phone)

    def save(self):

        backend.enter(self.fio_entry.get(), self.nick_entry.get(),
                      self.gmail_entry.get(), self.entry.get(), self.phone_entry.get(),
                      self.adress_entry.get(), self.birth_entry.get())
        messagebox.showinfo("i", "Запись сохранена")




class ChildWindow2(tk.Toplevel):
    def __init__(self, parent):
        global your_copy
        super().__init__(parent)

        self.title('Сохранённые записи')

        self.geometry(calculate_window())

        self.button = ttkb.Button(self, text='Экспортировать', command=self.export)
        self.button.place(x=240,y=350)





        self.tree = ttk.Treeview(self, height=13)
        self.tree['columns'] = ('ФИО', 'Ник', 'Почта', 'Пароль', 'Номер телефона', 'Адрес', 'Дата рождения')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('ФИО', width=60, anchor=W)
        self.tree.column('Ник', width=60, anchor=W)
        self.tree.column('Почта', width=60, anchor=W)
        self.tree.column('Пароль', width=60, anchor=W)
        self.tree.column('Номер телефона', width=80, anchor=W)
        self.tree.column('Адрес', width=60, anchor=W)
        self.tree.column('Дата рождения', width=100, anchor=W)
        self.tree.heading('#0', text='')
        self.tree.heading('ФИО', text='ФИО')
        self.tree.heading('Ник', text='Ник')
        self.tree.heading('Почта', text='Почта')
        self.tree.heading('Пароль', text='Пароль')
        self.tree.heading('Номер телефона', text='Ном.телефона')
        self.tree.heading('Адрес', text='Адрес')
        self.tree.heading('Дата рождения', text='Дата рождения')
        self.tree.pack()

        for row in backend.show():
            self.tree.insert(parent='', text='', index='end',
                             values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        self.popup1 = tk.Menu(self, tearoff=False)
        self.popup1.add_command(
            command=self.your_copy,
            label="Копировать")
        self.popup1.add_command(
            command=self.delete_row,
            label="Удалить строку")
        self.popup1.add_command(
            command=self.delete_all,
            label="Удалить всё")
        self.popup1.add_command(
            command=self.quit,
            label="Выйти")
        self.tree.bind('<Button-3>', self.popup_menu)
    def your_copy(self):
        pass


    def delete_row(self):
        pass

    def delete_all(self):
        pass


    def popup_menu(self, event):
        self.tree.identify_row(event.y)
        self.popup1.post(event.x_root, event.y_root)

    def export(self):
        pop = Toplevel(self)
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


if __name__ == '__main__':
    app = MainWindow()
    style = ttkb.Style("vapor")

    def calculate_window():
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        # Вычисляем координаты окна приложения
        window_width = 600
        window_height = 400
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        return f"{window_width}x{window_height}+{x}+{y}"


    app.geometry(calculate_window())
    app.mainloop()