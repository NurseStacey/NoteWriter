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

        MyDropDownBox(font_size,  self.input_frame,
                      name='interface_dropdown').grid(row=2, column=1, pady=20)

        self.add_interfaces()

        MyButton(font_size,  self.button_frame, text='Open Interface',
                 command=self.Open_Interface).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=0, column=2, padx=40)

    
    def add_interfaces(self):

        interface_names = self.Database_Obj.get_interface_names()

        if interface_names == 'Error':
                messagebox.showerror('Error','Error getting names of interfaces')
                return

        dropdown_box = self.input_frame.nametowidget('interface_dropdown')

        for one_line in interface_names:
            dropdown_box.add_item(one_line)

    def Open_Interface(self):
        
        interface_name = self.input_frame.nametowidget('interface_dropdown').get_selection()
        interface_fields = self.Database_Obj.get_interface_records(interface_name)
        self.winfo_toplevel().nametowidget('interface_dlg').InterfaceDLG_Class

class InterfaceDLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj
        
    def create_frame(self, interface_fields):
        pass



