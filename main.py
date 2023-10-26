import tkinter as tk
from tkinter import ttk
import sqlite3 


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records() 


# функция поиска
    def search_records(self, name):
        name = ('%' + name + '%')  
        self.db.c.execute("""SELECT * FROM db WHERE name LIKE ?""", (name,))   
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


# функция открытия диалогового окна для поиска
    def open_search_dialog(self):
        Search()


# функция удаления выбранной строки
    def delite_records(self):
        for selection_items in self.tree.selection():
            self.db.c.execute("""DELETE FROM db 
                              WHERE id=?""", (self.tree.set(selection_items, '#1')))
            self.db.conn.commit()
            self.view_records()


# функция редактирования выбранной строки
    def update_record(self, name, tel, email, salary):
        self.db.c.execute("""UPDATE db SET name=?, tel=?, email=?, salary=? 
                          WHERE ID=?""", (name, tel, email, salary,
                                          self.tree.set(self.tree.selection()[0],'#1')),)
        self.db.conn.commit()
        self.view_records()


# диалоговое окно для редактирования
    def open_update_dialog(self):
        Update()

    

    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()



    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)      # bg - фон / bd - граница
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./ikons/add.png')    # создание кнопки добавления
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog) 
        btn_open_dialog.pack(side=tk.LEFT)      # упаковка и выравнивание по левому краю


        #  ДАЛЕЕ СОЗДАНИЕ И ОТОБРАЖЕНИЕ ТАБЛИЦЫ      
        # создание таблицы
        self.tree = ttk.Treeview(columns=('ID', 'name', 'tel', 'email', 'salary'), height=45, show='headings')  # self - del
        
        # добавление параметров колонам
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # добавляем наименование колонок для шапки таблицы
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        

        # упаковка виджета
        self.tree.pack(side=tk.LEFT)
    

    # ДАЛЕЕ КНОПКИ
# создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./ikons/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0',
                                    bd=0, image=self.update_img,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

# создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./ikons/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img,
                               command=self.delite_records)
        btn_delete.pack(side=tk.LEFT)

# кнопка для поиска
        self.search_img = tk.PhotoImage(file='./ikons/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

# кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./ikons/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.refresh_img,
                               command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)


# метод открытия дочернего окна
    def open_dialog(self):       
        Child()


        # функция обновления таблицы
    def view_records(self):
        self.db.c.execute('''SELECT * FROM db''')               
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)for row in self.db.c.fetchall()]                        # добавляем в виджет таблицы всю информауию из БД




class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app



    def init_child(self):
        self.title('Добавить')          # текст
        self.geometry('400x260')        # размер окна
        self.resizable(False, False)    # заблокировано увеличение X/Y

        self.grab_set()                 # метод для перехватывания все событий в приложении
        self.focus_set()                # дает пользоваться только дочерним окном

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)

        label_select = tk.Label(self, text='Телефон:')
        label_select.place(x=50, y=80)

        label_sum = tk.Label(self, text='E-mail:')
        label_sum.place(x=50, y=110)

        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=140)


         # добавляем строку ввода для ФИО
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)  

        # добаляем строку ввода для E-mail 
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80) 

        # добаляем строку ввода для Телефона 
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110) 

        # добаляем строку ввода для Зарплаты 
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=150) 


        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=220, y=170)
        

        # кнопка добавления 
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=300, y=170)


        # срабатывание по ЛКП 
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_salary.get()), )



# КЛАСС ВЫЗОВА ОКНА ОБНОВЛЕНИЯ
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()


        # окно обновления
    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                  self.entry_email.get(),
                                                  self.entry_tel.get(),
                                                  self.entry_salary.get() ))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')   
        self.btn_ok.destroy()      



    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1')),)
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])



# КЛАСС ОКНА ПОИСКА ЗАПИСИ  
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)
        
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)
        
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)
        
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)
        
        btn_search = ttk.Button(self, text='Поиск') 
        btn_search.place(x=105, y=50)

        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()),)
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')



# КЛАСС БД
class DB():
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS db (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       tel TEXT,
                       email TEXT,
                       salary REAL);
                       """)
        self.conn.commit()



    def insert_data(self, name, tel, email, salary):
        self.c.execute("""INSERT INTO db (name, tel, email, salary)
                       VALUES (?, ?, ?, ?);""", (name, tel, email, salary))
        self.conn.commit()


# проверка
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('860x540')
    root.resizable(False, False)
    root.mainloop()
