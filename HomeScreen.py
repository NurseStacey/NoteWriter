import tkinter as tk
from universal_components import *
from WidgetControls import *


class HomeScreen_DLG_Class(MyFrame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        temp_listbox = ListScrollComboTwo(5, 20, 20, self.input_frame)
        temp_listbox.grid(row=1, column=1)
        fruit_list = []
        with open('fruit.txt', 'r') as this_file:
            for one_line in this_file.readlines():
                fruit_list.append(one_line.replace('\n',''))

        temp_listbox.add_item_list(fruit_list)

        MyButton(24, self.button_frame, command=self.new_clinic, text='New\nClinic', height=3, width=10).grid(row=1,  padx=5, column=1)
        MyButton(24,  self.button_frame, command=self.clinic_admin, text='Clinic\nAdmin',  height=3, width=10).grid(row=1, padx=5,column=2)
        MyButton(24, self.button_frame, command=self.provider_admin, text='Provider\nAdmin', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(24,  self.button_frame, command=self.database_admin, text='Database\nAdmin', height=3, width=10).grid(row=1,  padx=5, column=4)
        MyButton(24,  self.button_frame, command=self.interface_management,
                 text='Interface\nManagement', height=3, width=10).grid(row=1,  padx=5, column=5)
        
        MyButton(24,  self.button_frame, command=self.select_interface,
                 text='Select\nInterface', height=3, width=10).grid(row=2,  padx=5, column=1)


    def tkraise(self):
        super().tkraise()

    def new_clinic(self):
        self.raise_frame('new_clinic')

    def interface_management(self):
        self.raise_frame('interface_admin')

    def select_interface(self):
        self.raise_frame('select_interface')
        
    def new_interface(self):
        self.raise_frame('new_interface')

    def clinic_admin(self):
        pass

    def provider_admin(self):
        pass

    def database_admin(self):
        self.raise_frame('database_admin')

