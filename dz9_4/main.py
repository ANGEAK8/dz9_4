import tkinter as tk
from tkinter import ttk
import sqlite3


# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # хранение и инициализация объектов GUI
    def init_main(self):
        # создаем панель инструментов (тулбар)
        # bg - фон
        # bd - границы
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        # упаковка
        # side закрепляет вверху окна
        # fill растягивает по X (горизонтали)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./dz9_4/img/add.png')
        # создание кнопки добавления
        # command - функция по нажатию
        # bg - фон
        # bd - граница
        # compound - ориентация текста (tk.CENTER , tk.LEFT , tk.RIGHT , tk.TOP или tk.BOTTOM.)
        # image - иконка кнопки
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img, command=self.open_dialog)
        # упаковка и выравнивание по левому краю
        btn_open_dialog.pack(side=tk.LEFT)

        # создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./dz9_4/img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                    image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./dz9_4/img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./dz9_4/img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./dz9_4/img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавляем Treeview
        # columns - столбцы
        # height - высота таблицы
        # show='headings' скрываем нулевую (пустую) колонку таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45, show='headings')
        # добавляем параметры колонкам
        # width - ширина
        # anchor - выравнивание текста в ячейке
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("phone", text='Телефон')
        self.tree.heading("email", text='E-mail')

        # упаковка
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # добавление данных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()


    # вывод данных в виджет таблицы
    def view_records(self):
        # выбираем информацию из БД
        self.db.c.execute('''SELECT * FROM users''')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]
        
    # обновление (изменение) данных
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.c.execute('''UPDATE users SET name=?, phone=?, email=? WHERE ID=?''',
                          (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()
        
    # удаление записей
    def delete_records(self):
        # цикл по выделенным записям
        for row in self.tree.selection():
            # удаление из БД
            id = self.tree.set(self.tree.selection()[0], '#1')
            self.db.c.execute('''DELETE FROM users WHERE id=?''', (id, ))
        # сохранение изменений в БД
        self.db.conn.commit()
        # обновление виджета таблицы
        self.view_records()

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    # метод отвечающий за вызов дочернего окна
    def open_dialog(self):
        Child()

    # метод отвечающий за вызов окна для изменения данных
    def open_update_dialog(self):
        Update()

    # метод отвечающий за вызов окна для поиска
    def open_search_dialog(self):
        Search()

# класс дочерних окон
# Toplevel - окно верхнего уровня
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # заголовок окна
        self.title('Добавить')
        # размер окна
        self.geometry('400x220')
        # ограничение изменения размеров окна
        self.resizable(False, False)

        # перехватываем все события происходящие в приложении
        self.grab_set()
        # захватываем фокус
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)

        # добавляем строку ввода для наименования
        self.entry_name = ttk.Entry(self)
        # меняем координаты объекта
        self.entry_name.place(x=200, y=50)

        # добавляем строку ввода для email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # добавляем строку ввода для телефона
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=110)

        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(
            self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        # срабатывание по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_phone.get()))
    

# класс окна для обновления, наследуемый от класса дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_phone.get()))

        # закрываем окно редактирования
        # add='+' позваляет на одну кнопку вешать более одного события
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (id, ))
        # получаем доступ к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone.insert(0, row[3])


# класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app


    def init_search(self):
        self.title('Поиск по контактам')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set
        self.focus_set

        label_search = tk.Label(self, text='ФИО: ')
        label_search.place(x=20, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=70, y=20)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=50)

        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))


# класс БД
class DB:
    def __init__(self):
        # создаем соединение с БД
        self.conn = sqlite3.connect('contacts.db')
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.c = self.conn.cursor()
        # выполнение запроса к БД
        self.c.execute('''CREATE TABLE IF NOT EXISTS users(
                       id integer primary key, 
                       name text, 
                       phone text, 
                       email text)''')
        # сохранение изменений БД
        self.conn.commit()

    # метод добавления в БД
    def insert_data(self, name, phone, email):
        self.c.execute('''INSERT INTO users (name, phone, email) 
                       VALUES (?, ?, ?)''', (name, phone, email))
        self.conn.commit()




if __name__ == '__main__':
    root = tk.Tk()
    # экземпляр класса DB
    db = DB()
    app = Main(root)
    app.pack()
    # заголовок окна
    root.title('Телефонная книга')
    # размер окна
    root.geometry('665x450')
    # ограничение изменения размеров окна
    root.resizable(False, False)
    root.configure(bg='White')
    root.mainloop()