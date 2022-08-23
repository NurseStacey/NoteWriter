import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *
from Interface_Admin import InterfaceFieldClass


class Interface_Select_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(Database_Obj, *args, **kwargs)

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

        super().__init__(Database_Obj, *args, **kwargs)

        font_size = 24
        this_row = 1

        MyButton(font_size,  self.button_frame, text='New Record',
                 command=self.New_Record).grid(row=this_row, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Edit Record',
                 command=self.Edit_Record).grid(row=this_row, column=2, padx=40)
        MyButton(font_size,  self.button_frame, text='Delete Record',
                 command=self.Delete_Record).grid(row=this_row, column=3, padx=40)

        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=this_row, column=4, padx=40)

        self.the_interface = ''
        self.the_fields = []

    def Delete_Record(self):
        pass

    def Edit_Record(self):
        pass

    def New_Record(self):
        New_Record_Frame = self.winfo_toplevel().nametowidget('interface_new_record_dlg')

        New_Record_Frame.Set_Interface(self.the_interface)
        New_Record_Frame.tkraise()
        

    def Set_Interface(self, this_interface):
        self.set_title(this_interface)

        self.the_interface = this_interface



class InterfaceDLG_New_Record_Class(MyFrame):
    def __init__(self, Database_Obj,   *args, **kwargs):

        super().__init__(Database_Obj, *args, **kwargs)

        self.the_interface=''
        self.the_field_names=[]
        self.these_widgets=[]
                
    def create_frame(self):
        self.the_field = self.Database_Obj.get_interface_records(
            self.the_interface)

        font_size = 24
        this_row=1

        for one_field in self.the_field:
            self.the_field_names.append(one_field['Field_Name'])
            temp = MyLabel(font_size,self.input_frame, text=one_field['Field_Lable'])
            temp.grid(row=this_row, column=1)
            self.these_widgets.append(temp)
            temp = MyEntry(font_size, self.input_frame, validation_type=one_field['Field_Type'], name=one_field['Field_Name'])
            temp.grid(row=this_row, column=2)

            self.these_widgets.append(temp)
            this_row += 1

        MyButton(font_size,  self.button_frame, text='Save Record',
                 command=self.Save_Record).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=0, column=2, padx=40)

    def Save_Record(self):
        
        records_to_add = []

        for one_field in self.the_field:
            one_record = {}
            one_record['type'] = one_field['Field_Type']
            one_record['column'] = one_field['Field_Name']

            if one_field['Field_Type'] == 'string':
                one_record['value'] = self.input_frame.nametowidget(
                    one_field['Field_Name']).get()
                
            elif one_field['Field_Type'] == 'integer':
                one_record['value'] = int(self.input_frame.nametowidget(
                    one_field['Field_Name']).get())
            elif one_field['Field_Type'] == 'double':
                one_record['value'] = float(self.input_frame.nametowidget(
                    one_field['Field_Name']).get())

            records_to_add.append(one_record)

        interface_info = self.Database_Obj.get_interface_info(
            self.the_interface)

        self.Database_Obj.add_record(interface_info['Interface_Table'],records_to_add)



    def Cancel(self):

        for one_widget in self.these_widgets:
            one_widget.destroy()

        super().Cancel()

    def Set_Interface(self, this_interface):
        self.set_title(this_interface+'\nAdd Record')

        self.the_interface = this_interface


        self.create_frame()
