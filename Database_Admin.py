import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *
from Database_Class_File import MyDatabaseClass

@dataclass
class FieldClass:
    name:str
    type:str
    length:int


@dataclass
class InterfaceFieldClass:
    name: str
    label: str
    type: str
    length: int
    order: int



class Database_Admin_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.Database_Obj = Database_Obj

        font_size = 24
        MyButton(font_size, self.winfo_toplevel(), self.button_frame, command=self.new_table, text='New\nTable', height=3, width=10).grid(row=1,  padx=5, column=2)
        MyButton(font_size, self.winfo_toplevel(), self.button_frame, command=self.delete_table, text='Delete\nTable', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(font_size, self.winfo_toplevel(), self.button_frame, command=self.alter_table, text='Alter\nTable', height=3, width=10).grid(row=2,  padx=5, column=2)
        MyButton(font_size, self.winfo_toplevel(), self.button_frame, text='Cancel', height=3, width=10, command=self.Cancel).grid(row=2, column=3, padx=5)

        ListScrollCombo(False, 10, 25, font_return(16), self.button_frame,
                        name='table_list_box').grid(row=1, column=1, pady=30, rowspan=2)
        self.button_frame.nametowidget(
            'table_list_box').config(width=350, height=450)
        


    def tkraise(self):

        self.populate_table_box()
        super().tkraise()

    def alter_table(self):
        table_list_box = self.button_frame.nametowidget('table_list_box')
        table_name = table_list_box.get_selected_text()
        if len(table_name)==0:
            messagebox.showerror('error', 'That field name already used')
            return
        if len(table_name) > 1:
            messagebox.showerror('error', 'Please choose just one table')
            return

        table_info = self.Database_Obj.get_column_info(table_name[0])
        self.winfo_toplevel().nametowidget(
            'alter_table').set_current_table_info(table_info, table_name[0])
        self.raise_frame('alter_table')

    def delete_table(self):
        table_list_box = self.button_frame.nametowidget('table_list_box')
        table_name_list = table_list_box.get_selected_text()

        for one_table in table_name_list:
            _SQL = 'DROP TABLE ' + one_table
            mycursor = self.Database_Obj.get_cursor()
            mycursor.execute(_SQL)
            table_list_box.remove_item(one_table)

    def populate_table_box(self):

        table_list = self.Database_Obj.get_list_current_tables()
        table_list_box = self.button_frame.nametowidget('table_list_box')
        table_list_box.clear_listbox()

        for one_table in table_list:
            table_list_box.add_item(one_table)

    def new_table(self):
        self.raise_frame('new_table')


class New_Database_Table_DLG_Class(MyFrame):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(*args, **kwargs)
        ####################

        def type_chosen(event):

            if self.field_type_value.get() in ['string']:
                self.input_frame.nametowidget(
                    'field_length').config(state='normal')
            else:
                self.input_frame.nametowidget(
                    'field_length').config(state='disabled')

        self.Database_Obj = Database_Obj
        self.Table_Name = '' 

        font_size = 24
        MyLabel(font_size, self.winfo_toplevel(),self.input_frame, text='Table Name').grid(row=0, column=0, pady=20)
        
        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='table_name', validation_type='DB_string').grid(row=0, column=1, columnspan=2, pady=20)

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame, text='Field Name').grid(row=1, column=0, pady=20)

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame, text='Field Type').grid(row=1, column=1, pady=20)

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame, text='Field\nLength').grid(row=1, column=2, pady=20)

        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='field_name',
                validation_type='DB_string').grid(row=2, column=0, pady=20)

        field_types = [
            "string",
            "text",
            "integer",
            "double",
            "date",
        ]

        self.field_type_value = tk.StringVar()

        self.field_type_value.set('string')

        field_menu = tk.OptionMenu(
            self.input_frame, self.field_type_value, *field_types, command=type_chosen)
        field_menu.grid(row=2, column=1, pady=20)
        field_menu.config(font=font_return(font_size))
 
        self.input_frame.nametowidget(
            field_menu.menuname).config(font=font_return(font_size))

        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='field_length',
                validation_type='digit_only').grid(row=2, column=2, pady=20)

        headers = ['name', 'type', 'length']
        self.FieldList = MyMultiListBox(FieldClass, headers, False, self)
        self.FieldList.set_font_size(16)
        self.FieldList.grid(row=2, column=1, columnspan=3, pady=20, sticky='news')
        self.FieldList.set_height(5)
        self.set_input_frame_columns(2)

        MyButton(font_size, self.winfo_toplevel(),self.button_frame, text='Add Field', command=self.Add_Field).grid(row=0, column=1, padx=40)
        MyButton(font_size, self.winfo_toplevel(),self.button_frame, text='Add Table', name='add_table_button', command=self.Add_Table).grid(row=0, column=2, padx=40)
        MyButton(font_size, self.winfo_toplevel(),self.button_frame, text='Cancel', command=self.Cancel).grid(row=0, column=3, padx=40)
        self.set_button_frame_columns(3)

    def raise_frame(self, which_frame):
        #in case there are things to do when leaving the frame
        self.FieldList.clear_list_boxes()
        super().raise_frame(which_frame)

    def tkraise(self):
        super().tkraise()
        
    def Add_Field(self):

        field_name = self.input_frame.nametowidget('field_name').get()

        if self.FieldList.value_in_list('name', field_name):
            messagebox.showerror('error', 'That field name already used')
            return

        this_field = FieldClass(
            field_name,
            self.field_type_value.get(),
            self.input_frame.nametowidget('field_length').get()
        )
        
        self.field_type_value.set('string')
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_length').config(state='normal')
        
        self.FieldList.add_one_record(this_field)


    def Add_Table(self):
        
        table_name = self.input_frame.nametowidget('table_name').get()

        if table_name in self.Database_Obj.get_list_current_tables():
            messagebox.showerror('error', 'That table name already used')
            return

        all_fields = self.FieldList.get_all_records()
        self.Database_Obj.add_new_table(table_name, all_fields)

        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('table_name').delete(0,tk.END)
        self.field_type_value.set('string')
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_length').config(state='normal')
        self.input_frame.nametowidget('field_name').delete(0, tk.END)

        self.winfo_toplevel().nametowidget('database_admin').populate_table_box()

class Alter_Database_Table_DLG_Class(New_Database_Table_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

        self.current_table_info = []
        self.current_table_name=None

    def tkraise(self):

        temp_button = self.button_frame.nametowidget('add_table_button')
        temp_button.config(text='Update Table')
        temp_button.config(command=self.update_table)

        super().tkraise()

    def update_table(self):

        #check if name has changed
        table_name = self.input_frame.nametowidget('table_name').get()
        if not table_name == self.current_table_name:
            self.Database_Obj.change_table_name(
                self.current_table_name, table_name)
            self.current_table_name = table_name

        #check if there are new fields
        fields_from_multibox = self.FieldList.get_all_records()

        new_fields = []
        for one_field in fields_from_multibox:
            if next((x for x in self.current_table_info if x.name == one_field.name), None) == None:
                new_fields.append(one_field)

        if not new_fields == []:
            self.Database_Obj.add_new_fields(self.current_table_name, new_fields)

        #check if fields were removed.
        fields_to_remove = []
        for one_field in self.current_table_info:
            if next((x for x in fields_from_multibox if x.name == one_field.name), None) == None:
                fields_to_remove.append(one_field)

        if not fields_to_remove == []:
            self.Database_Obj.removed_fields(self.current_table_name, fields_to_remove)

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
            field_length = 0
            
            if field_type_temp=='mediumtext':
                field_type='text'
            elif field_type_temp == 'smallint':
                field_type = 'integer'
            elif field_type_temp[:5] == 'float':
                field_type = 'integer'
            elif field_type_temp == 'datetime':
                field_type = 'date'
            elif field_type_temp[:7] == 'varchar':
                field_type = 'string'
                field_length = int(field_type_temp[8:len(
                    field_type_temp)-1])

            one_field = FieldClass(field_name, field_type, field_length)
            self.current_table_info.append(one_field)
            self.FieldList.add_one_record(one_field)


class New_Interface_DLG_Class(MyFrame):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(*args, **kwargs)
        ####################

        def type_chosen(event):

            if self.field_type_value.get() in ['string']:
                self.input_frame.nametowidget(
                    'field_length').config(state='normal')
            else:
                self.input_frame.nametowidget(
                    'field_length').config(state='disabled')

        self.Database_Obj = Database_Obj
        self.Table_Name = ''

        font_size = 18

        ## Row 1
        this_row=0
        MyLabel(font_size, self.winfo_toplevel(), self.input_frame,
                text='Interface Name').grid(row=this_row, column=2, columnspan=1, pady=10)

        MyLabel(font_size, self.winfo_toplevel(), self.input_frame,
                text='Table Name').grid(row=this_row, column=4, columnspan=1, pady=10)

        # row 2
        this_row += 1
        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='interface_name').grid(
            row=this_row, column=2,  columnspan=1, pady=15)

        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='table_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1,  pady=10)

        # row 3
        this_row += 1

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame,
                text='Field Label').grid(row=this_row, column=2, columnspan=1, pady=10)

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame,
                text='Field Name').grid(row=this_row, column=4, columnspan=1, pady=10)



        # row 4 
        this_row += 1
        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='field_label').grid(row=this_row, column=2,  columnspan=1,  pady=10)

        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, name='field_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1, pady=15)


        # row 5
        this_row += 1

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame,
                text='Field Type').grid(row=this_row, column=2,  columnspan=1,  pady=15, padx=10)

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame,
                text='Field\nLength').grid(row=this_row, column=3,  columnspan=1, pady=15, padx=10)

        MyLabel(font_size, self.winfo_toplevel(),  self.input_frame,
                text='Order').grid(row=this_row, column=4,  columnspan=1, pady=15, padx=10)

        # row 6
        this_row += 1


        field_types = [
            "string",
            "text",
            "integer",
            "double",
            "date",
        ]

        self.field_type_value = tk.StringVar()

        self.field_type_value.set('string')

        field_menu = tk.OptionMenu(
            self.input_frame, self.field_type_value, *field_types, command=type_chosen)
        field_menu.grid(row=this_row, column=1,
                        columnspan=2,  pady=15, padx=10)
        field_menu.config(font=font_return(font_size))

        self.input_frame.nametowidget(
            field_menu.menuname).config(font=font_return(font_size))

        MyEntry(font_size, self.winfo_toplevel(), self.input_frame, width=4,  name='field_length',
                validation_type='digit_only').grid(row=this_row, column=3,  columnspan=1, pady=15, padx=10)

        MyEntry(font_size, self.winfo_toplevel(), self.input_frame,width=4,  name='field_order',
                validation_type='digit_only').grid(row=this_row, column=4,  columnspan=1, pady=15, padx=10)
        self.input_frame.nametowidget('field_order').insert(0,'1')

        #row 7
        this_row += 1
        headers = ['name', 'type', 'length', 'order', 'label']
        self.FieldList = MyMultiListBox(
            InterfaceFieldClass, headers, False, self.input_frame)
        self.FieldList.set_font_size(16)
        self.FieldList.grid(row=this_row, column=1, columnspan=5,
                            pady=15, sticky='news')
        self.FieldList.set_height(5)

        self.set_input_frame_columns(5)

        MyButton(font_size, self.winfo_toplevel(), self.button_frame, text='Add Field',
                 command=self.Add_Field).grid(row=0, column=1, padx=40)
        MyButton(font_size, self.winfo_toplevel(), self.button_frame, text='Add Table',
                 name='add_table_button', command=self.Add_Interface).grid(row=0, column=2, padx=40)
        MyButton(font_size, self.winfo_toplevel(), self.button_frame,
                 text='Cancel', command=self.Cancel).grid(row=0, column=3, padx=40)
        self.set_button_frame_columns(3)

    def Add_Interface(self):

        table_name = self.input_frame.nametowidget('table_name').get()

        if table_name in self.Database_Obj.get_list_current_tables():
            messagebox.showerror('error', 'That table name already used')
            return


        interface_name = self.input_frame.nametowidget('interface_name').get()

        # if interface_name in self.Database_Obj.get_list_current_tables():
        #     messagebox.showerror('error', 'That table name already used')
        #     return

        all_fields = self.FieldList.get_all_records()
        self.Database_Obj.add_new_table(table_name, all_fields)

        self.Database_Obj.add_new_interface(interface_name, table_name, all_fields)

        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.field_type_value.set('string')
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_length').config(state='normal')
        self.input_frame.nametowidget('field_name').delete(0, tk.END)

    def Add_Field(self):

        field_name = self.input_frame.nametowidget('field_name').get()
        

        if self.FieldList.value_in_list('name', field_name):
            messagebox.showerror('error', 'That field name already used')
            return

        field_label = self.input_frame.nametowidget('field_label').get()
        if self.FieldList.value_in_list('label', field_label):
            messagebox.showerror('error', 'That field label already used')
            return

        field_order = self.input_frame.nametowidget('field_order').get()
        if self.FieldList.value_in_list('order', field_order):
            messagebox.showerror('error', 'Another field has that order value')
            return
        if field_order == '':
            messagebox.showerror('error', 'Need value for field order')
            return

        this_field = InterfaceFieldClass(
            field_name,
            field_label,
            self.field_type_value.get(),
            self.input_frame.nametowidget('field_length').get(),
            field_order
        )

        self.field_type_value.set('string')
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_label').delete(0, tk.END)
        self.input_frame.nametowidget('field_order').delete(0, tk.END)
        self.input_frame.nametowidget('field_order').insert(0, str(int(field_order)+1))

        self.FieldList.add_one_record(this_field)
