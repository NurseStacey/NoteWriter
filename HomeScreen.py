import tkinter as tk
from universal_components import *
from WidgetControls import *

class HomeScreen_DLG_Class(tk.Frame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)



        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        

        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=1, pady=10, sticky='news')
        MyLabel(36, self.winfo_toplevel(),  title_frame, width=30, text='Welcome to the EHR').grid(row=0, column=0)

        button_frame = tk.Frame(
            self, name='button_frame')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid(row=1, column=1, pady=40, sticky='news')

        MyButton(24, self.winfo_toplevel(), button_frame, command=self.new_clinic, text='New\nClinic', height=3, width=10).grid(row=1,  padx=5, column=1)
        MyButton(24, self.winfo_toplevel(),button_frame, command=self.clinic_admin, text='Clinic\nAdmin',  height=3, width=10).grid(row=1, padx=5,column=2)
        MyButton(24, self.winfo_toplevel(), button_frame, command=self.provider_admin, text='Provider\nAdmin', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(24, self.winfo_toplevel(), button_frame, command=self.database_admin, text='Database\nAdmin', height=3, width=10).grid(row=1,  padx=5, column=4)
        


    def tkraise(self):
        
        super().tkraise()

    def new_clinic(self):
        pass

    def clinic_admin(self):
        pass

    def provider_admin(self):
        pass

    def raise_frame(self, which_frame):
        self.winfo_toplevel().unbind_all(['<Tab>'])
        self.winfo_toplevel().nametowidget(which_frame).tkraise()

    def database_admin(self):
        self.raise_frame('database_admin')

