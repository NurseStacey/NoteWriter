
import tkinter as tk
from HomeScreen import HomeScreen_DLG_Class
from Database_Class_File import MyDatabaseClass
from Database_Admin import *
from Clinic_Admin import New_Clinic_DLG_Class
from Interface_Admin import *
from Interface_DLG import *

The_Window = tk.Tk()
The_Window.title('My EHR program')
The_Window.state('zoomed')

The_Window.grid_columnconfigure(0,weight=1)
The_Window.grid_columnconfigure(1, weight=1)
The_Window.grid_columnconfigure(2, weight=1)

The_Window.grid_rowconfigure(2, weight=1)

Database_Obj = MyDatabaseClass()

HomeScreen_DLG_Class(Database_Obj, The_Window, title_text='Home Screen', name='homescreen').grid(
    row=1, column=1, sticky='news')

Database_Admin_DLG_Class(Database_Obj,
    The_Window, title_text='Database Management', name='database_admin').grid(row=1, column=1, sticky='news')

New_Database_Table_DLG_Class(Database_Obj,
    The_Window, title_text='New Table', name='new_table').grid(row=1, column=1, sticky='news')

Alter_Database_Table_DLG_Class(Database_Obj,
                               The_Window, title_text='Alter Table', name='alter_table').grid(row=1, column=1, sticky='news')

New_Clinic_DLG_Class(Database_Obj,
                     The_Window, title_text='Create Clinic', name='new_clinic').grid(row=1, column=1, sticky='news')

Interface_Admin_DLG_Class(Database_Obj,
                          The_Window, title_text='Interface Management', name='interface_admin').grid(row=1, column=1, sticky='news')

New_Interface_DLG_Class(Database_Obj,
                     The_Window, title_text='Create New Interface', name='new_interface').grid(row=1, column=1, sticky='news')

Alter_Interface_DLG_Class(Database_Obj,
                          The_Window, title_text='Alter Interface', name='alter_interface').grid(row=1, column=1, sticky='news')

Interface_Select_DLG_Class(Database_Obj,
                          The_Window, title_text='Select Interface', name='select_interface').grid(row=1, column=1, sticky='news')

InterfaceDLG_Class(Database_Obj,
                           The_Window, title_text='', name='interface_dlg').grid(row=1, column=1, sticky='news')

InterfaceDLG_DoWhat_Class(Database_Obj,
                          The_Window, title_text='', name='interface_dlg').grid(row=1, column=1, sticky='news')

The_Window.nametowidget('homescreen').tkraise()

The_Window.mainloop()

