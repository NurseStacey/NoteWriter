import tkinter as tk
from universal_components import *
from WidgetControls import *


class HomeScreen_DLG_Class(MyFrame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        MyButton(24, self.winfo_toplevel(), self.button_frame, command=self.new_clinic, text='New\nClinic', height=3, width=10).grid(row=1,  padx=5, column=1)
        MyButton(24, self.winfo_toplevel(), self.button_frame, command=self.clinic_admin, text='Clinic\nAdmin',  height=3, width=10).grid(row=1, padx=5,column=2)
        MyButton(24, self.winfo_toplevel(), self.button_frame, command=self.provider_admin, text='Provider\nAdmin', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(24, self.winfo_toplevel(), self.button_frame, command=self.database_admin, text='Database\nAdmin', height=3, width=10).grid(row=1,  padx=5, column=4)
        MyButton(24, self.winfo_toplevel(), self.button_frame, command=self.new_interface, text='New\nInterface', height=3, width=10).grid(row=1,  padx=5, column=5)
        


    def tkraise(self):
        super().tkraise()

    def new_clinic(self):
        self.raise_frame('new_clinic')

    def new_interface(self):
        self.raise_frame('new_interface')

    def clinic_admin(self):
        pass

    def provider_admin(self):
        pass

    def database_admin(self):
        self.raise_frame('database_admin')
