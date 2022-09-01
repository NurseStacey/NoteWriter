import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *

class Database_Admin_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(Database_Obj, *args, **kwargs)

        font_size = 24
        MyButton(font_size,  self.button_frame, command=self.new_table, text='New\nTable', height=3, width=10).grid(row=1,  padx=5, column=2)
        MyButton(font_size,self.button_frame, command=self.delete_table, text='Delete\nTable', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(font_size,  self.button_frame, command=self.alter_table, text='Alter\nTable', height=3, width=10).grid(row=2,  padx=5, column=2)
        MyButton(font_size,  self.button_frame, text='Cancel', height=3, width=10, command=self.Cancel).grid(row=2, column=3, padx=5)

        ListScrollComboTwo(10, 20, 25, None, self.button_frame,
                           name='table_list_box').grid(row=1, column=1, pady=30, sticky='NW', rowspan=2)
        
        self.button_frame.nametowidget(
            'table_list_box').set_selection_mode('multiple')

    def tkraise(self):

        self.populate_table_box()
        super().tkraise()

    def alter_table(self):
        table_list_box = self.button_frame.nametowidget('table_list_box')
        table_name = table_list_box.get_all_selected_texts()
        if len(table_name)==0:
            messagebox.showerror('error', 'That field name already used')
            return
        if len(table_name) > 1:
            messagebox.showerror('error', 'Please choose just one table')
            return

        table_info = self.Database_Obj.get_column_info(table_name[0])
        if table_info == 'Error':
            messagebox.showerror('Error','Not able to list of current tables')
            return

        self.winfo_toplevel().nametowidget(
            'alter_table').set_current_table_info(table_info, table_name[0])
        self.raise_frame('alter_table')

    def delete_table(self):
        table_list_box = self.button_frame.nametowidget('table_list_box')
        table_name_list = table_list_box.get_all_selected_texts()

        for one_table in table_name_list:
            if self.Database_Obj.delete_table(one_table)=='Error':
                messagebox.showerror('Error','Not able to delete table')
                return

            table_list_box.remove_item(one_table)

    def populate_table_box(self):

        table_list = self.Database_Obj.get_list_current_tables()
        if table_list=='Error':
            messagebox.showerror('Error','Not able to list of current tables')
            return

        table_list_box = self.button_frame.nametowidget('table_list_box')
        table_list_box.add_item_list(table_list)

    def new_table(self):
        self.raise_frame('new_table')


class New_Database_Table_DLG_Class(MyFrame):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

        self.Table_Name = '' 

        font_size = 24
        MyLabel(font_size, self.input_frame, text='Table Name').grid(
            row=0, column=0, pady=(0, 10))
        
        MyEntry(font_size, self.input_frame, name='table_name', validation_type='DB_string').grid(
            row=0, column=1, columnspan=2, pady=(0, 10))

        MyLabel(font_size,   self.input_frame, text='Field Name').grid(row=1, column=0)

        MyLabel(font_size,  self.input_frame, text='Field Type').grid(row=1, column=1)

        MyLabel(font_size,   self.input_frame, text='Required').grid(row=1, column=2)

        MyEntry(font_size,  self.input_frame, name='field_name',
                validation_type='DB_string').grid(sticky='n', row=2, column=0, pady=(0, 10))

        ListScrollComboTwo(5, 20, 20, None, self.input_frame, name='field_type').grid(
            sticky='n', row=2, column=1, pady=(0, 10))

        self.Required_checkbox_var = tk.IntVar()
        MyCheckBox(self.input_frame, width=4, name='required', variable=self.Required_checkbox_var).grid(
            row=2, column=2,  pady=(0, 10), padx=10)
        self.Required_checkbox_var.set(0)

        self.input_frame.nametowidget('field_type').add_item_list(field_types)

        headers = ['field_name', 'field_type']
        self.FieldList = MyMultiListBox(
            headers, self.input_frame)
        self.FieldList.set_font_size(16)
        self.FieldList.grid(row=3, column=0, columnspan=3, sticky='news')
        self.FieldList.set_height(5)
        self.set_input_frame_columns(2)
        self.FieldList.set_double_click(self.delete_record)

        MyButton(font_size, self.button_frame, text='Add Field', command=self.Add_Field).grid(row=0, column=1, padx=40)
        MyButton(font_size,self.button_frame, text='Add Table', name='add_table_button', command=self.Add_Table).grid(row=0, column=2, padx=40)
        MyButton(font_size,self.button_frame, text='Cancel', command=self.Cancel).grid(row=0, column=3, padx=40)
        self.set_button_frame_columns(3)

    def delete_record(self, event):
        which = event.widget.curselection()[0]

        if self.FieldList.get_one_value_in_list('name', which)=='Record_ID': 
            messagebox.showerror('Error','Cannot delete Record_ID')
            return

        self.FieldList.delete_one_item(which)

    def raise_frame(self, which_frame):
        #in case there are things to do when leaving the frame
        self.FieldList.clear_list_boxes()
        super().raise_frame(which_frame)

    def tkraise(self):
        super().tkraise()
        
    def Add_Field(self):

        field_name = self.input_frame.nametowidget('field_name').get()

        if self.FieldList.value_in_list('field_name', field_name):
            messagebox.showerror('error', 'That field name already used')
            return

        field_type = self.input_frame.nametowidget(
            'field_type').get_selected_text()

        this_field={}
        this_field['field_name']=field_name
        this_field['field_type'] = field_type
        
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        
        self.input_frame.nametowidget('field_type').reset()
        self.FieldList.add_one_record(this_field)


    def Add_Table(self):
        
        required_table=(self.Required_checkbox_var.get() == 1)

        table_name = self.input_frame.nametowidget('table_name').get()
        table_list =self.Database_Obj.get_list_current_tables()

        if table_list=='Error':
                messagebox.showerror('Error','Error getting current table list')
                return

        if table_name in table_list:
            messagebox.showerror('error', 'That table name already used')
            return

        all_fields = self.FieldList.get_all_records()
        if self.Database_Obj.add_new_table(table_name, all_fields, required_table) == 'Error':
            messagebox.showerror('Error','Error adding table')
            return

        self.clear_widgets()

        self.winfo_toplevel().nametowidget('database_admin').populate_table_box()

    def clear_widgets(self):
        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('table_name').delete(0,tk.END)
        
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        
    def Cancel(self):

        self.clear_widgets()

        super().Cancel()

class Alter_Database_Table_DLG_Class(New_Database_Table_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

        self.current_table_info = []
        self.current_table_name = ''

    def tkraise(self):

        temp_button = self.button_frame.nametowidget('add_table_button')
        temp_button.config(text='Update Table')
        temp_button.config(command=self.update_table)

        super().tkraise()

    def update_table(self):

        #check if name has changed
        table_name = self.input_frame.nametowidget('table_name').get()
        if not table_name == self.current_table_name:
            if self.Database_Obj.change_table_name(
                self.current_table_name, table_name) == 'Error':
                messagebox.ERROR('Error', 'Problem making the table')
                return
            self.current_table_name = table_name

        #check if there are new fields
        fields_from_multibox = self.FieldList.get_all_records()

        new_fields = []
        for one_field in fields_from_multibox:
            if next((x for x in self.current_table_info if x['field_name'] == one_field['field_name']), None) == None:
                new_fields.append(one_field)

        if not new_fields == []:
            if self.Database_Obj.add_new_fields(
                    self.current_table_name, new_fields) == 'Error':
                messagebox.showerror('Error', 'Error adding one of the new fields')
                return

        #check if fields were removed.
        fields_to_remove = []
        for one_field in self.current_table_info:
            if next((x for x in fields_from_multibox if x['field_name'] == one_field['field_name']), None) == None:
                fields_to_remove.append(one_field)

        if not fields_to_remove == []:
            if self.Database_Obj.remove_fields(
                    self.current_table_name,  [x['field_name'] for x in fields_to_remove]) == 'Error':
                messagebox.showerror('Error', 'Error removing fields')
                return

        #if we wanted to allow fields to be changed we would do it here

    def raise_frame(self, which_frame):
        #in case there are things to do when leaving the frame
        temp_button = self.button_frame.nametowidget('add_table_button')
        temp_button.config(text='Add Table')
        temp_button.config(command=self.Add_Table)

        super().raise_frame(which_frame)

    def set_current_table_info(self, table_info, table_name):

        self.current_table_name = table_name
        self.current_table_info = []

        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.input_frame.nametowidget('table_name').insert(0, table_name)

        for one_item in table_info:
            field_name = one_item[0]
            field_type_temp = one_item[1].decode('utf-8')

            if field_type_temp == 'mediumtext':
                field_type = 'text'
            elif field_type_temp == 'smallint':
                field_type = 'integer'
            elif field_type_temp[:5] == 'float':
                field_type = 'integer'
            elif field_type_temp[:3] == 'int':
                field_type = 'integer'
            elif field_type_temp == 'datetime':
                field_type = 'date'
            elif field_type_temp[:7] == 'varchar':
                field_type = 'string'

            one_field={}
            one_field['field_name']=field_name
            one_field['field_type']=field_type
            self.current_table_info.append(one_field)
            self.FieldList.add_one_record(one_field)
