import tkinter as tk
from universal_components import *
from tkinter import messagebox
from WidgetControls import *
from Database_Class_File import MyDatabaseClass


class New_Clinic_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj

        MyButton(24,  self.button_frame, command=self.new_clinic,
                 text='Add\nClinic', height=3, width=10).grid(row=1,  padx=5, column=1)
        MyButton(24, self.button_frame, text='Cancel',
                 height=3, width=10, command=self.Cancel).grid(row=1, column=2, padx=5)


    def new_clinic(self):
        pass
