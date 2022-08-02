
import tkinter as tk
from HomeScreen import HomeScreen_DLG_Class
from Database_Class_File import MyDatabaseClass
from Database_Admin import Database_Admin_DLG_Class, New_Database_Table_DLG_Class, Alter_Database_Table_DLG_Class

The_Window = tk.Tk()
The_Window.title('My EHR program')
The_Window.state('zoomed')

The_Window.grid_columnconfigure(0,weight=1)
The_Window.grid_columnconfigure(1, weight=1)
The_Window.grid_columnconfigure(2, weight=1)

The_Window.grid_rowconfigure(2, weight=1)

HomeScreen_DLG_Class(The_Window, name='homescreen').grid(
    row=1, column=1, sticky='news')



Database_Obj = MyDatabaseClass()
Database_Admin_DLG_Class(Database_Obj,
    The_Window, name='database_admin').grid(row=1, column=1, sticky='news')


New_Database_Table_DLG_Class(Database_Obj,
    The_Window, name='new_table').grid(row=1, column=1, sticky='news')

Alter_Database_Table_DLG_Class(Database_Obj,
    The_Window, name='alter_table').grid(row=1, column=1, sticky='news')

The_Window.nametowidget('homescreen').tkraise()

The_Window.mainloop()

