import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *
from Interface_Admin import InterfaceFieldClass
from datetime import datetime

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

        ListScrollWithRecordID(
            5, 20, 20, None, self.input_frame, name='all_records').grid(row=1, column=1)

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

    def Populate_Records(self):
        pass

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

        interface_info = self.Database_Obj.get_interface_info(
            self.the_interface)
        self.input_frame.nametowidget('all_records').add_item_list(
            self.Database_Obj.get_record_names(interface_info['interface_table'], interface_info['record_name_formula']))


class InterfaceDLG_New_Record_Class(MyFrame):
    def __init__(self, Database_Obj,   *args, **kwargs):

        super().__init__(Database_Obj, *args, **kwargs)

        self.the_interface=''
        self.the_interface_info = None
        self.the_field_names=[]
        self.these_widgets=[]
        self.Checkbox_var = {}
                
    def create_frame(self):
        self.the_fields = self.Database_Obj.get_interface_records(
            self.the_interface)

        font_size = 24
        this_row=1

        for one_field in self.the_fields:
            self.the_field_names.append(one_field['field_name'])
            temp = MyLabel(font_size,self.input_frame, text=one_field['field_label'])
            temp.grid(row=this_row, column=1)
            self.these_widgets.append(temp)

            if one_field['field_type'] == 'linked_table':
                temp = ListScrollWithRecordID(
                    5, 20, 20, None, self.input_frame, name=one_field['field_name'])
                linked_interface_info = self.Database_Obj.get_interface_info(one_field['Linked_Table'])
                temp.add_item_list(
                    self.Database_Obj.get_record_names(linked_interface_info['interface_table'], linked_interface_info['Record_Name_Formula']))
            elif one_field['field_type'] == 'text':
                temp = TextScrollCombo(self.input_frame, name=one_field['field_name'])
                temp.config(width=150, height=100)

            elif one_field['field_type'] == 'bool':
                temp_var = tk.IntVar()
                self.Checkbox_var[one_field['field_name']] = temp_var
                temp = MyCheckBox(self.input_frame, width=4,
                                  name=one_field['field_name'], variable=temp_var)
                temp_var.set(0)
            else:
                temp = MyEntry(font_size, self.input_frame, validation_type=one_field['field_type'], name=one_field['field_name'])

            temp.grid(row=this_row, column=2)

            self.these_widgets.append(temp)
            this_row += 1

        MyButton(font_size,  self.button_frame, text='Save Record',
                 command=self.Save_Record).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=0, column=2, padx=40)

    def Save_Record(self):
        
        records_to_add = []

        for one_field in self.the_fields:
            one_record = {}
            one_record['type'] = one_field['field_type']
            one_record['column'] = one_field['field_name']

            if one_field['field_type'] in ['text','string']:
                one_record['value'] = self.input_frame.nametowidget(
                    one_field['field_name']).get()
            elif one_field['field_type'] == 'date':
                one_record['value'] = datetime.strptime(self.input_frame.nametowidget(
                    one_field['field_name']).get(),'%m\\%d\\%Y')
            elif one_field['field_type'] == 'integer':
                one_record['value'] = int(self.input_frame.nametowidget(
                    one_field['field_name']).get())
            elif one_field['field_type'] == 'double':
                one_record['value'] = float(self.input_frame.nametowidget(
                    one_field['field_name']).get())
            elif one_field['field_type'] == 'linked_table':
                one_record['value'] = self.input_frame.nametowidget(
                    one_field['field_name']).get_selected_ID()[0]
            elif one_field['field_type'] == 'bool':
                one_record['value'] = self.Checkbox_var[one_field['field_name']].get()

            records_to_add.append(one_record)

        interface_info = self.Database_Obj.get_interface_info(
            self.the_interface)

        self.Database_Obj.add_record(interface_info['interface_table'], records_to_add)

        self.winfo_toplevel().nametowidget('interface_dlg').Set_Interface(self.the_interface)
        self.lower()

    def Cancel(self):

        for one_widget in self.these_widgets:
            one_widget.destroy()

        super().Cancel()

    def Set_Interface(self, this_interface):
        self.set_title(this_interface+'\nAdd Record')

        self.the_interface = this_interface
        self.the_interface_info = self.Database_Obj.get_interface_info(self.the_interface)


        self.create_frame()
