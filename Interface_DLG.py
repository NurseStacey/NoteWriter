import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *
from Interface_Admin import InterfaceFieldClass


class Interface_Select_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj
        font_size = 24

        this_row =1
        ListScrollComboTwo(5, 20, 20, None, self.input_frame,
                           name='interfaces').grid(row=this_row, column=7, sticky='NW', pady=(0, 10), padx=10)


        this_row += 1
        MyButton(font_size,  self.button_frame, text='Open Interface',
                 command=self.Open_Interface).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=0, column=2, padx=40)

    def populate_interface_box(self):

        interface_names = self.Database_Obj.get_interface_names()

        if interface_names == 'Error':
            messagebox.showerror('Error', 'Error getting names of interfaces')
            return

        self.input_frame.nametowidget(
            'interfaces').add_item_list(interface_names)
            
    def tkraise(self):
        self.populate_interface_box()
        
        super().tkraise()

    def Open_Interface(self):

        self.winfo_toplevel().nametowidget('interface_dlg').Set_Interface(self.input_frame.nametowidget(
            'interfaces').get_selected_text())
        self.winfo_toplevel().nametowidget('interface_dlg').tkraise()

class InterfaceDLG_DoWhat_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.Database_Obj = Database_Obj
        font_size = 24
        this_row = 1
        MyButton(font_size,  self.button_frame, text='New Record',
                 command=self.New_Record).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=0, column=2, padx=40)

        self.the_interface = ''
        self.the_fields = []

    def New_Record(self):
        pass

    def Set_Interface(self, this_interface):
        self.set_title(this_interface)

        self.the_interface = this_interface

        self.the_fields = self.Database_Obj.get_interface_records(
            this_interface)

class InterfaceDLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj
        
    def create_frame(self, interface_fields):
        pass



