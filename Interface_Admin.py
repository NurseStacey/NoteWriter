import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *



@dataclass
class InterfaceFieldClass:
    name: str
    label: str
    type: str
    length: int
    order: int

class Interface_Admin_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj

        font_size = 24
        MyButton(font_size,  self.button_frame, command=self.new_interface,
                 text='New\nInterface', height=3, width=10).grid(row=1,  padx=5, column=2)
        MyButton(font_size, self.button_frame, command=self.delete_interface,
                 text='Delete\nInterface', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(font_size, self.button_frame, command=self.alter_interface,
                 text='Alter\nInterface', height=3, width=10).grid(row=2,  padx=5, column=2)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 height=3, width=10, command=self.Cancel).grid(row=2, column=3, padx=5)

        ListScrollCombo(False, 10, 25, font_return(16), self.button_frame,
                        name='interface_list_box').grid(row=1, column=1, pady=30, rowspan=2)

        self.button_frame.nametowidget('interface_list_box').set_selection_mode('multiple')

        # self.button_frame.nametowidget(
        #     'interface_list_box').config(width=350, height=450)

    def tkraise(self):

        super().tkraise()

    def alter_interface(self):
        interface_list_box = self.button_frame.nametowidget(
            'interface_list_box')
        interface_name = interface_list_box.get_selected_text()
        if len(interface_name) == 0:
            messagebox.showerror('error', 'Must choose an interface')
            return
        if len(interface_name) > 1:
            messagebox.showerror('error', 'Please choose just one interface')
            return
        interface_name = interface_name[0]

        ###need to retrieve information regarding interface

        interface_records = self.Database_Obj.get_interface_records(
            interface_name)
        if interface_records == 'Error':
            messagebox.showerror('error', 'Error loading interface')
            return

        self.winfo_toplevel().nametowidget(
            'alter_interface').set_current_interface_info(interface_records)

        self.raise_frame('alter_interface')

    def delete_interface(self):
        interface_list_box = self.button_frame.nametowidget(
            'interface_list_box')
        interface_list = interface_list_box.get_selected_text()

        for one_interface in interface_list:
            if self.Database_Obj.delete_interface(one_interface) == 'Error':
                messagebox.showerror('Error', 'Error removing interface')
                return
                
            interface_list_box.remove_item(one_interface)

    def populate_interface_box(self):

        interface_list = self.Database_Obj.get_interface_names()
        if interface_list == 'Error':
            messagebox.showerror('Error', 'Error retrieving interface list')
            return
        interface_list_box = self.button_frame.nametowidget(
            'interface_list_box')
        interface_list_box.clear_listbox()

        for one_interface in interface_list:
            interface_list_box.add_item(one_interface)

    def new_interface(self):
        self.raise_frame('new_interface')

    def tkraise(self):

        self.populate_interface_box()
        super().tkraise()

class New_Interface_DLG_Class(MyFrame):

    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(*args, **kwargs)
        ####################

        def type_chosen(event):
            if self.input_frame.nametowidget('field_type').add_item_list(field_types).get_selection() in ['string']:
                self.input_frame.nametowidget('field_length').set_state('normal')          
            else:
                self.input_frame.nametowidget(
                    'field_length').set_state('disabled')
            pass
            # - dropdown
            # if self.field_type_value.get() in ['string']:
            #     self.input_frame.nametowidget(
            #         'field_length').config(state='normal')
            # else:
            #     self.input_frame.nametowidget(
            #         'field_length').config(state='disabled')

        self.Database_Obj = Database_Obj
        self.Table_Name = ''

        font_size = 18

        ## Row 1
        this_row=0
        MyLabel(font_size,  self.input_frame,
                text='Interface Name').grid(row=this_row, column=2, columnspan=1, pady=10)

        MyLabel(font_size,  self.input_frame,
                text='Table Name').grid(row=this_row, column=4, columnspan=1, pady=10)

        MyLabel(font_size,   self.input_frame,
                text='Field Type').grid(row=this_row, column=5,  sticky='W', columnspan=2,  pady=10, padx=10)

        MyLabel(font_size,   self.input_frame,
                text='Linked Table').grid(row=this_row, column=7,  sticky='W', rowspan=1,  columnspan=1, pady=10, padx=10)

        # row 2
        this_row += 1
        MyEntry(font_size, self.input_frame, name='interface_name').grid(
            row=this_row, column=2,  columnspan=1, pady=10, sticky='N')

        MyEntry(font_size, self.input_frame, name='table_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1,  pady=10, sticky='N')

        MyDropDownBox(font_size,  self.input_frame, name='field_type').grid(
            row=this_row, column=5, columnspan=2, sticky='NW', pady=10, padx=10)

        field_types = [
            "string",
            "text",
            "integer",
            "double",
            "date",
        ]

        self.input_frame.nametowidget('field_type').add_item_list(field_types)

        MyDropDownBox(font_size, self.input_frame,
                      name='interface_dropdown').grid(row=this_row, column=7, sticky='NW', pady=10, padx=10)
        # row 3
        this_row += 1

        MyLabel(font_size,   self.input_frame,
                text='Field Label').grid(row=this_row, column=2, columnspan=1, pady=10, sticky='N')

        MyLabel(font_size,   self.input_frame,
                text='Field Name').grid(row=this_row, column=4, columnspan=1, pady=10, sticky='N')

        MyLabel(font_size,   self.input_frame,
                text='Field\nLength').grid(row=this_row, column=5,  sticky='W',  columnspan=1, pady=10, padx=10)

        MyLabel(font_size,  self.input_frame,
                text='Order').grid(row=this_row, column=6,  sticky='W',  columnspan=1, pady=10, padx=10)


        # row 4 
        this_row += 1
        MyEntry(font_size, self.input_frame, name='field_label').grid(row=this_row, column=2,  columnspan=1,  pady=10, sticky='N')

        MyEntry(font_size, self.input_frame, name='field_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1, pady=10, sticky='N')

        MyEntry(font_size,  self.input_frame, width=4,  name='field_length',
                validation_type='digit_only').grid(row=this_row, column=5,   sticky='N', columnspan=1, pady=10, padx=10)

        MyEntry(font_size,  self.input_frame, width=4,  name='field_order',
                validation_type='digit_only').grid(row=this_row, column=6,  sticky='NW',  columnspan=1, pady=10, padx=10)

        self.input_frame.nametowidget('field_order').insert(0, '1')
        # row 5
        this_row += 1




        # row 6
        this_row += 1


        field_types = [
            "string",
            "text",
            "integer",
            "double",
            "date",
        ]

        # self.field_type_value = tk.StringVar()

        # self.field_type_value.set('string')

        # field_menu = tk.OptionMenu(
        #     self.input_frame, self.field_type_value, *field_types, command=type_chosen)
        # field_menu.grid(row=this_row, column=1,
        #                 columnspan=2,   sticky='NW', pady=15, padx=10)
        # field_menu.config(font=font_return(font_size))

        # self.input_frame.nametowidget(
        #     field_menu.menuname).config(font=font_return(font_size))
        


        #columnspan=1, pady=15, padx=10)

        self.add_interfaces()

        #row 7
        this_row += 1
        headers = ['name', 'type', 'length', 'order', 'label']
        self.FieldList = MyMultiListBox(
            InterfaceFieldClass, headers, False, self.input_frame)
        self.FieldList.set_font_size(16)
        self.FieldList.grid(row=this_row, column=2, columnspan=6,
                            pady=15, sticky='news')
        self.FieldList.set_height(5)

        self.set_input_frame_columns(5)

        MyButton(font_size,  self.button_frame, text='Add Field',
                 command=self.Add_Field).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Add Interface',
                 name='add_interface_button', command=self.Add_Interface).grid(row=0, column=2, padx=40)
        MyButton(font_size,  self.button_frame,
                 text='Cancel', command=self.Cancel).grid(row=0, column=3, padx=40)
        self.set_button_frame_columns(3)

    
    def add_interfaces(self):

        interface_names = self.Database_Obj.get_interface_names()

        if interface_names == 'Error':
                messagebox.showerror('Error','Error getting names of interfaces')
                return

        dropdown_box = self.input_frame.nametowidget('interface_dropdown')

        for one_line in interface_names:
            dropdown_box.add_item(one_line)

    def Add_Interface(self):

        table_name = self.input_frame.nametowidget('table_name').get()
        table_list = self.Database_Obj.get_list_current_tables()
        if table_list=='Error':
            messagebox.showerror('Error','Not able to list of current tables')
            return

        if table_name in table_list:
            messagebox.showerror('error', 'That table name already used')
            return


        interface_name = self.input_frame.nametowidget('interface_name').get()

        all_fields = self.FieldList.get_all_records()
        if self.Database_Obj.add_new_table(table_name, all_fields) == 'Error':
            messagebox.showerror('Error', 'Error adding table')
            return

        if self.Database_Obj.add_new_interface(interface_name, table_name, all_fields) == 'Error':
            messagebox.showerror('Error', 'Error adding interface')
            return

        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        #self.field_type_value.set('string') - dropdown
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_length').set_state('normal')
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_order').delete(0, tk.END)

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
            # self.field_type_value.get(), - dropdow
            self.input_frame.nametowidget('field_type').get_selection(), #- dropdow
            self.input_frame.nametowidget('field_length').get(),
            field_order
        )

        #self.field_type_value.set('string')
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_label').delete(0, tk.END)
        self.input_frame.nametowidget('field_order').delete(0, tk.END)
        self.input_frame.nametowidget('field_order').insert(0, str(int(field_order)+1))
        self.input_frame.nametowidget('field_length').set_state('normal')

        self.FieldList.add_one_record(this_field)



    def Cancel(self):

        self.clear_widgets()
        self.winfo_toplevel().nametowidget('interface_admin').populate_interface_box()
        super().Cancel()

    def clear_widgets(self):
        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        # self.field_type_value.set('string') - dropdown
        self.input_frame.nametowidget('field_length').delete(0, tk.END)
        self.input_frame.nametowidget('field_length').set_state('normal')
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_order').delete(0, tk.END)


class Alter_Interface_DLG_Class(New_Interface_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

        self.current_interface_info = []
        self.current_interface_name = ''
        self.current_table_name = ''

    def tkraise(self):

        temp_button = self.button_frame.nametowidget('add_interface_button')
        temp_button.config(text='Update Interface')
        temp_button.config(command=self.update_interface)

        super().tkraise()

    def update_interface(self):

        #check if table name has changed
        table_name = self.input_frame.nametowidget('table_name').get()
        if not table_name == self.current_table_name:
            if self.Database_Obj.change_table_name_interface(self.current_interface_name,
                self.current_table_name, table_name) == 'Error':
                messagebox.showerror('Error', 'Problem changing table name')
                return
            self.current_table_name = table_name

        #check if interface name has changed
        interface_name = self.input_frame.nametowidget('interface_name').get()
        if not interface_name == self.current_interface_name:
            if self.Database_Obj.change_interface_name(
                    self.current_interface_name, interface_name) == 'Error':
                messagebox.ERROR('Error', 'Problem making the table')
                return
            self.current_table_name = table_name

        #check if there are new fields
        fields_from_multibox = self.FieldList.get_all_records()

        new_fields = []
        for one_field in fields_from_multibox:
            if next((x for x in self.current_interface_info if x.name == one_field.name), None) == None:
                new_fields.append(one_field)

        if not new_fields == []:
            if self.Database_Obj.add_new_fields_interface(self.current_interface_name,
                    self.current_table_name, new_fields) == 'Error':
                messagebox.showerror(
                    'Error', 'Error adding one of the new fields')
                return

        #check if fields were removed.
        fields_to_remove = []
        for one_field in self.current_interface_info:
            if next((x for x in fields_from_multibox if x.name == one_field.name), None) == None:
                fields_to_remove.append(one_field)

        if not fields_to_remove == []:
            if self.Database_Obj.remove_fields_interface(self.current_interface_name,
                    self.current_table_name, [x.name for x in fields_to_remove]) == 'Error':
                messagebox.showerror('Error', 'Error removing fields')
                return

        #if we wanted to allow fields to be changed we would do it here

    def Cancel(self):
        #in case there are things to do when leaving the frame
        temp_button = self.button_frame.nametowidget('add_interface_button')
        temp_button.config(text='Add Table')
        temp_button.config(command=self.Add_Interface)

        super().Cancel()
    
    def set_current_interface_info(self, interface_records):
        
        self.current_interface_name = interface_records[0]['Interface_Name']
        self.current_table_name = interface_records[0]['Table_Name']

        self.current_interface_info = []

        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.input_frame.nametowidget('table_name').insert(
            0, self.current_table_name)

        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        self.input_frame.nametowidget('interface_name').insert(
            0, self.current_interface_name)

        for one_item in interface_records:

            one_field = InterfaceFieldClass(one_item['Field_Name'], one_item['Field_Lable'], one_item['Field_Type'], one_item['Field_Length'], one_item['Field_Order'])
            self.FieldList.add_one_record(one_field)
            self.current_interface_info.append(one_field)

