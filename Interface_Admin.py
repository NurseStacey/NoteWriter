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
    # length: int
    order: int
    linked_table: str
    immutable: bool

class Interface_Admin_DLG_Class(MyFrame):
    def __init__(self, Database_Obj,  *args, **kwargs):

        super().__init__(Database_Obj, *args, **kwargs)

        font_size = 24
        MyButton(font_size,  self.button_frame, command=self.new_interface,
                 text='New\nInterface', height=3, width=10).grid(row=1,  padx=5, column=2)
        MyButton(font_size, self.button_frame, command=self.delete_interface,
                 text='Delete\nInterface', height=3, width=10).grid(row=1,  padx=5, column=3)
        MyButton(font_size, self.button_frame, command=self.alter_interface,
                 text='Alter\nInterface', height=3, width=10).grid(row=2,  padx=5, column=2)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 height=3, width=10, command=self.Cancel).grid(row=2, column=3, padx=5)

        ListScrollComboTwo(10, 20, 25, None, self.button_frame,
                        name='interface_list_box').grid(row=1, column=1, pady=30, rowspan=2)

        self.button_frame.nametowidget('interface_list_box').set_selection_mode('multiple')


    def tkraise(self):
        self.populate_interface_box()
        
        super().tkraise()

    def alter_interface(self):
        interface_list_box = self.button_frame.nametowidget(
            'interface_list_box')
        interface_name = interface_list_box.get_all_selected_texts()
        if len(interface_name) == 0:
            messagebox.showerror('error', 'Must choose an interface')
            return
        if len(interface_name) > 1:
            messagebox.showerror('error', 'Please choose just one interface')
            return
        interface_name = interface_name[0]

        ###need to retrieve information regarding interface

        interface_fields = self.Database_Obj.get_interface_records(
            interface_name)
        if interface_fields == 'Error':
            messagebox.showerror('error', 'Error loading interface')
            return

        interface_info = self.Database_Obj.get_interface_info(interface_name)

        self.winfo_toplevel().nametowidget(
            'alter_interface').set_current_interface_info(interface_fields, interface_info)

        self.raise_frame('alter_interface')

    def delete_interface(self):
        interface_list_box = self.button_frame.nametowidget(
            'interface_list_box')
        interface_list = interface_list_box.get_all_selected_texts()

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

        self.button_frame.nametowidget(
            'interface_list_box').clear_listbox()
        self.button_frame.nametowidget(
            'interface_list_box').add_item_list(interface_list)

    def new_interface(self):
        self.raise_frame('new_interface')

    def tkraise(self):

        self.populate_interface_box()
        super().tkraise()

class New_Interface_DLG_Class(MyFrame):

    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

        self.record_name_formula = ''
        self.Table_Name = ''
        self.field_to_update = ''
        font_size = 18
        self.FieldList = None
        self.Checkbox_var = None

        self.interface_name = ''

        self.build_input_frame(font_size)
  
        self.set_input_frame_columns(5)

        self.build_buttond_frame(font_size)
        

    def enable_edit_field_button(self):
        self.button_frame.nametowidget('edit_field').config(state='normal')
        self.winfo_toplevel().bind("<Alt-e>", self.Edit_Field)

    def Edit_Field(self, event=None):
        this_field = self.FieldList.get_current_selection()
        self.reset_all_fields()

        self.button_frame.nametowidget('edit_field').config(text='Update Field')
        self.button_frame.nametowidget('edit_field').config(command=self.Update_Field)
        self.button_frame.nametowidget('cancel').config(command=self.Cancel_Field_Update)

        self.field_to_update = this_field['name']
        self.input_frame.nametowidget('field_name').insert(0, this_field['name'])
        #self.input_frame.nametowidget('field_order').delete(0,tk.END)

        #self.input_frame.nametowidget('field_order').insert(0, this_field['order'])
        self.input_frame.nametowidget(
            'field_label').insert(0, this_field['label'])
        if this_field['immutable']=='Yes':
            self.Checkbox_var.set(1)
        linked_table = this_field['linked_table']
        if not linked_table=='':
            self.input_frame.nametowidget['linked_table'].set_selection(
                linked_table)

        self.FieldList.set_state('disabled')
        self.winfo_toplevel().bind("<Alt-u>", self.Edit_Field)
        self.winfo_toplevel().unbind("<Alt-e>")

    def Cancel_Field_Update(self):
        self.reset_edit_field_button()
        
        
    def reset_edit_field_button(self):
        self.button_frame.nametowidget(
            'edit_field').config(command=self.Edit_Field)
        self.button_frame.nametowidget(
            'edit_field').config(text='Edit Field')
        self.button_frame.nametowidget(
            'edit_field').config(state='disabled')
        self.button_frame.nametowidget('cancel').config(
            command=self.Cancel)
        self.FieldList.clear_all_selections()
        
    def build_input_frame(self,font_size):

        def type_chosen(e):
            if self.input_frame.nametowidget('field_type').get_selected_text() in ['linked_table']:
                self.input_frame.nametowidget(
                    'linked_table').set_state('normal')
                self.input_frame.nametowidget(
                    'linked_table').focus_set()
            else:
                self.input_frame.nametowidget(
                    'linked_table').reset()
                self.input_frame.nametowidget(
                    'linked_table').set_state('disabled')
                self.input_frame.nametowidget(
                    'field_label').focus_set()
        ## Row 1
        this_row = 0
        MyLabel(font_size,  self.input_frame,
                text='Interface Name').grid(row=this_row, column=2, columnspan=1, pady=10)

        MyLabel(font_size,  self.input_frame,
                text='Table Name').grid(row=this_row, column=4, columnspan=1, pady=(0, 10))

        MyLabel(font_size,   self.input_frame,
                text='Field Type').grid(row=this_row, column=5,  sticky='W', columnspan=2,  pady=(0, 10), padx=10)

        MyLabel(font_size,   self.input_frame,
                text='Linked Table').grid(row=this_row, column=7,  sticky='W', rowspan=1,  columnspan=1, pady=(0, 10), padx=10)

        # row 2
        this_row += 1
        MyEntry(font_size, self.input_frame, name='interface_name').grid(
            row=this_row, column=2,  columnspan=1, pady=(0, 10), sticky='nw')

        MyEntry(font_size, self.input_frame, name='table_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1,  pady=(0, 10), sticky='N')

        ListScrollComboTwo(5, 20, 20, type_chosen, self.input_frame, name='field_type').grid(
            row=this_row, column=5, columnspan=2, sticky='NW', pady=(0, 10), padx=10)

        self.input_frame.nametowidget('field_type').add_item_list(field_types)

        ListScrollComboTwo(5, 20, 20, None, self.input_frame,
                           name='linked_table').grid(row=this_row, column=7, sticky='NW', pady=(0, 10), padx=10)

        this_row += 1

        MyLabel(font_size,   self.input_frame,
                text='Field Label').grid(row=this_row, column=2, columnspan=1, sticky='N')

        MyLabel(font_size,   self.input_frame,
                text='Field Name').grid(row=this_row, column=4, columnspan=1, sticky='N')

        # MyLabel(font_size,  self.input_frame,
        #         text='Order').grid(row=this_row, column=6,  sticky='W',  columnspan=1,  padx=10)

        MyLabel(font_size,  self.input_frame,
                text='Is Immutable').grid(row=this_row, column=7,  sticky='W',  columnspan=1,  padx=10)
        # row 4
        this_row += 1
        MyEntry(font_size, self.input_frame, name='field_label').grid(
            row=this_row, column=2,  columnspan=1,  pady=(0, 10), sticky='N')

        MyEntry(font_size, self.input_frame, name='field_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1, pady=(0, 10), sticky='N')

        # MyEntry(font_size,  self.input_frame, width=4,  name='field_order',
        #         validation_type='digit_only').grid(row=this_row, column=6,  sticky='NW',  columnspan=1, pady=(0, 10), padx=10)

        self.Checkbox_var = tk.IntVar()
        MyCheckBox(self.input_frame, width=4, name='immutable', variable=self.Checkbox_var).grid(
            row=this_row, column=7,  sticky='NW',  columnspan=1, pady=(0, 10), padx=10)
        self.Checkbox_var.set(0)

        # row 5
        this_row += 1
        MyLabel(font_size, self.input_frame,  text='Name Formula:', name='record_name_formula').grid(
            row=this_row, column=2, columnspan=5, sticky='NW', pady=(0, 10), padx=10)
        # row 6
        this_row += 1

        self.populate_interface_box()

        #row 7
        this_row += 1

        headers = ['field_name', 'field_type',
                   'field_label', 'linked_table', 'immutable']

        # headers = ['name', 'type', 'order',
        #            'label', 'linked_table', 'immutable']     
        self.FieldList = MyMultiListBox(
            headers, self.input_frame)              
        # self.FieldList = MyMultiListBox(
        #     InterfaceFieldClass, headers, False, self.input_frame)

        self.FieldList.change_lable_text('field_name', 'Field Name')
        self.FieldList.change_lable_text('field_type', 'Field Type')
        self.FieldList.change_lable_text('field_label', 'Field Label')
        self.FieldList.change_lable_text('linked_table', 'Linked Table')
        self.FieldList.change_lable_text('immutable', 'Immutable Name')

        self.FieldList.set_font_size(16)
        self.FieldList.grid(row=this_row, column=2, columnspan=6,
                            pady=15, sticky='news')
        self.FieldList.set_height(5)
        self.FieldList.set_width('field_type', 10)
        self.FieldList.set_width('immutable', 8)
        self.FieldList.set_width('field_name', 10)
        self.FieldList.set_width('field_label', 10)
        self.FieldList.set_width('linked_table', 10)
        self.FieldList.set_double_click(self.delete_record)
        self.FieldList.set_single_click(self.enable_edit_field_button)

    def build_buttond_frame(self, font_size):

        column=1
        MyButton(font_size,  self.button_frame, text='Add Field',
                 command=self.Add_Field, underline=4).grid(row=0, column=column, padx=40)

        column += 1
        MyButton(font_size,  self.button_frame, text='Add Interface',
                 name='add_interface_button', command=self.Add_Interface, underline=0).grid(row=0, column=column, padx=40)

        column += 1
        MyButton(font_size,  self.button_frame,
                 text='Edit Field', command=self.Edit_Field, name='edit_field', underline=0).grid(row=0, column=column, padx=40)

        column += 1
        MyButton(font_size,  self.button_frame,
                 text='Create Name', command=self.create_name, name='create_name', underline=7).grid(row=0, column=column, padx=40)
        self.button_frame.nametowidget('edit_field').config(state='disabled')

        column += 1
        MyButton(font_size,  self.button_frame,
                 text='Cancel', command=self.Cancel, name='cancel', underline=0).grid(row=0, column=column, padx=40)
        
        column += 1
        
        self.set_button_frame_columns(column)

    def delete_record_to_update(self):
        self.FieldList.delete_one_record('name', self.field_to_update)
        

    def Update_Field(self):

        self.winfo_toplevel().bind("<Alt-e>", self.Edit_Field)
        self.winfo_toplevel().unbind("<Alt-u>")
        
        self.FieldList.set_state('normal')
        self.delete_record_to_update()
        self.Add_Field()

        self.reset_edit_field_button()
        self.reset_all_fields()

    def delete_record(self, event=None):

        which = self.FieldList.get_selection()[0]
        #which = event.widget.curselection()[0]

        self.FieldList.delete_one_item(which)

    def create_name(self, event=None):
        
        build_name_gui = BuildName_DLG_Class(self)
        build_name_gui.build_gui(self.FieldList.get_values_in_column(
            'field_name'), self.set_name_formula)
        build_name_gui.grab_set()

    def set_name_formula(self, new_formula):
        self.record_name_formula = new_formula
        self.input_frame.nametowidget('record_name_formula')[
            'text'] = 'Name Formula:' + new_formula

    def tkraise(self):
        self.winfo_toplevel().bind("<Alt-f>", self.Add_Field)
        self.winfo_toplevel().bind("<Alt-i>", self.Add_Interface)
        self.winfo_toplevel().bind("<Alt-c>", self.Cancel)
        self.winfo_toplevel().bind("<Alt-n>", self.create_name)
        self.winfo_toplevel().bind("<Alt-a>", self.Add_Interface)
        self.populate_interface_box()
        # self.input_frame.nametowidget('field_order').insert(0, '1')
        self.reset_edit_field_button()

        super().tkraise()
    
    def populate_interface_box(self):

        interface_names = self.Database_Obj.get_interface_names()
        
        if interface_names == 'Error':
                messagebox.showerror('Error','Error getting names of interfaces')
                return

        self.input_frame.nametowidget(
            'linked_table').add_item_list(interface_names)

    def Add_Interface(self, event=None):

        table_name = self.input_frame.nametowidget('table_name').get()
        table_list = self.Database_Obj.get_list_current_tables()
        if table_list=='Error':
            messagebox.showerror('Error','Not able to list of current tables')
            return

        if table_name in table_list:
            messagebox.showerror('error', 'That table name already used')
            return


        interface_name = self.input_frame.nametowidget('interface_name').get().strip()

        #temp till I fix this code
        all_fields = self.FieldList.get_all_records()
        if self.Database_Obj.add_new_table(table_name, all_fields) == 'Error':
            messagebox.showerror('Error', 'Error adding table')
            return

        if self.Database_Obj.add_new_interface(interface_name, table_name, self.record_name_formula, all_fields) == 'Error':
            messagebox.showerror('Error', 'Error adding interface')
            self.Database_Obj.delete_table(table_name)
            return

        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        #self.field_type_value.set('string') - dropdown
        # self.input_frame.nametowidget('field_length').delete(0, tk.END)
        # self.input_frame.nametowidget('field_length').set_state('normal')
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        #self.input_frame.nametowidget('field_order').delete(0, tk.END)
        self.input_frame.nametowidget('field_type').reset()
        self.input_frame.nametowidget('linked_table').reset()

    def Add_Field(self, event=None):

        field_name = self.input_frame.nametowidget('field_name').get()
        field_type = self.input_frame.nametowidget('field_type').get_selected_text()
        linked_table=''
        if field_type=='linked_table':
            linked_table = self.input_frame.nametowidget(
                'linked_table').get_selected_text()

        if field_type=='linked_table' and linked_table =='':
            messagebox.showerror('error', 'Need to select a table to link to')
            return 'Fail'

        # if field_type == 'string' and field_length == '':
        #     messagebox.showerror('error', 'Need to enter a field length')
        #     return        

        if self.FieldList.value_in_list('field_name', field_name):
            messagebox.showerror('error', 'That field name already used')
            return 'Fail'

        field_label = self.input_frame.nametowidget('field_label').get()
        if self.FieldList.value_in_list('field_label', field_label):
            messagebox.showerror('error', 'That field label already used')
            return 'Fail'

        # field_order = self.input_frame.nametowidget('field_order').get()
        # if self.FieldList.value_in_list('order', field_order):
        #     messagebox.showerror('error', 'Another field has that order value')
        #     return 'Fail'
        # if field_order == '':
        #     messagebox.showerror('error', 'Need value for field order')
        #     return 'Fail'

        immutable = 'Yes'
        if self.Checkbox_var.get()==0:
            immutable = 'No'

        # this_field = InterfaceFieldClass(
        #     field_name,
        #     field_label,
        #     field_type,  
        #     # field_length,
        #     0,
        #     linked_table,
        #     immutable,
        # )
        #         headers = ['name', 'type',
        #            'label', 'linked_table', 'immutable']
        this_field={}
        this_field['field_name'] = field_name
        this_field['field_type'] = field_type
        this_field['field_label'] = field_label
        this_field['linked_table'] = linked_table
        this_field['immutable'] = immutable



        self.FieldList.add_one_record(this_field)
        self.input_frame.nametowidget('field_type').focus_set()
        self.reset_all_fields()


    def reset_all_fields(self):
        #self.field_type_value.set('string')
        # self.input_frame.nametowidget('field_length').delete(0, tk.END)
        #field_order = self.input_frame.nametowidget('field_order').get()
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_label').delete(0, tk.END)
        # self.input_frame.nametowidget('field_order').delete(0, tk.END)
        # self.input_frame.nametowidget('field_order').insert(
        #     0, str(int(field_order)+1))
        # self.input_frame.nametowidget('field_length').set_state('normal')
        self.input_frame.nametowidget('field_type').reset()
        self.input_frame.nametowidget('linked_table').reset()
        self.Checkbox_var.set(0)
        self.FieldList.clear_all_selections()

    def Cancel(self, event=None):
        self.winfo_toplevel().unbind("<Alt-f>")
        self.winfo_toplevel().unbind("<Alt-i>")
        self.winfo_toplevel().unbind("<Alt-c>")
        self.winfo_toplevel().unbind("<Alt-n>")
        self.winfo_toplevel().unbind("<Alt-a>")
        self.clear_widgets()
        self.winfo_toplevel().nametowidget('interface_admin').populate_interface_box()
        super().Cancel()

    def clear_widgets(self):
        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        # self.field_type_value.set('string') - dropdown
        # self.input_frame.nametowidget('field_length').delete(0, tk.END)
        # self.input_frame.nametowidget('field_length').set_state('normal')
        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        #self.input_frame.nametowidget('field_order').delete(0, tk.END)
        self.input_frame.nametowidget('field_type').reset()
        self.Checkbox_var.set(0)



class Alter_Interface_DLG_Class(New_Interface_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):

        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

        self.current_interface_info = []
        self.current_interface_name = ''
        self.current_table_name = ''
        self.current_name_formula = ''

    def tkraise(self):

        temp_button = self.button_frame.nametowidget('add_interface_button')
        temp_button.config(text='Update Interface')
        temp_button.config(command=self.update_interface)

        super().tkraise()
        self.input_frame.nametowidget('linked_table').remove_item(
            self.current_interface_name)

    def update_interface(self):

        record_ID = {'column_name': 'interface_name', 'value':self.current_interface_name, 'type':'string'}
        columns_to_update = []
        update_interface_info = False
        #check if interface name has changed
        interface_name = self.input_frame.nametowidget('interface_name').get()
        if not interface_name == self.current_interface_name:
            if interface_name in self.Database_Obj.get_interface_names():
                messagebox.ERROR('Error', 'Interface name already being used')
                return


            one_column_to_update = {}
            one_column_to_update['column_name'] = 'interface_name'
            one_column_to_update['type'] = 'string'
            one_column_to_update['value'] = interface_name
            self.Database_Obj.update_one_record(
                'interface_fields', record_ID, [one_column_to_update])

            columns_to_update.append(one_column_to_update)

            self.current_interface_name = interface_name
            update_interface_info = True


        #check if table name has changed
        table_name = self.input_frame.nametowidget('table_name').get()
        if not table_name == self.current_table_name:
            one_column_to_update = {}
            one_column_to_update['column_name'] = 'interface_table'
            one_column_to_update['type'] = 'string'
            one_column_to_update['value'] = table_name
            columns_to_update.append(one_column_to_update)

            
            update_interface_info = True
            if self.Database_Obj.change_table_name(
                self.current_table_name, table_name) == 'Error':
                messagebox.showerror('Error', 'Problem changing table name')
                return
            self.current_table_name = table_name
            

        #check if record name formula has changed
        record_name_formula = self.record_name_formula

        if not record_name_formula == self.current_name_formula:
            one_column_to_update = {}
            one_column_to_update['column_name'] = 'record_name_formula'
            one_column_to_update['type'] = 'string'
            one_column_to_update['value'] = record_name_formula
            columns_to_update.append(one_column_to_update)

            self.current_name_formula = record_name_formula
            update_interface_info = True
            # if self.Database_Obj.change_name_formula(
            #         self.current_interface_name, record_name_formula) == 'Error':
            #     messagebox.ERROR('Error', 'Problem making the table')
            #     return
        
        if update_interface_info:
            self.Database_Obj.update_one_record(
                'interfaces', record_ID, columns_to_update)

        #check if there are new fields
        fields_from_multibox = self.FieldList.get_all_records()

        new_fields = []
        fields_to_remove = []

        for one_field in fields_from_multibox:
            if not(one_field in self.current_interface_info):    
                fields_to_remove = fields_to_remove + \
                    [x for x in self.current_interface_info if x['field_name']
                        == one_field['field_name']]
                new_fields.append(one_field)
                self.current_interface_info.append(one_field)

        #check if fields were removed.
        
        for one_field in self.current_interface_info:
            if next((x for x in fields_from_multibox if x['field_name'] == one_field['field_name']), None) == None:
                fields_to_remove.append(one_field)

        if not fields_to_remove == []:
            if self.Database_Obj.remove_fields_interface(self.current_interface_name,
                                                         self.current_table_name, [x['field_name'] for x in fields_to_remove]) == 'Error':
                messagebox.showerror('Error', 'Error removing fields')
                return

        if not new_fields == []:
            if self.Database_Obj.add_new_fields_interface(self.current_interface_name,
                                                          self.current_table_name, new_fields) == 'Error':
                messagebox.showerror(
                    'Error', 'Error adding one of the new fields')
                return

        #if we wanted to allow fields to be changed we would do it here

    def Cancel(self):
        #in case there are things to do when leaving the frame
        temp_button = self.button_frame.nametowidget('add_interface_button')
        temp_button.config(text='Add Table')
        temp_button.config(command=self.Add_Interface)

        super().Cancel()
    
    def set_current_interface_info(self, interface_records, interface_info):
        
        self.current_name_formula= interface_info['record_name_formula']
        self.record_name_formula = interface_info['record_name_formula']
        self.current_interface_name = interface_records[0]['interface_name']
        self.current_table_name = interface_info['interface_table']

        self.current_interface_info = []

        self.input_frame.nametowidget('record_name_formula')[
            'text'] = self.current_name_formula
        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.input_frame.nametowidget('table_name').insert(
            0, self.current_table_name)

        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        self.input_frame.nametowidget('interface_name').insert(
            0, self.current_interface_name)

        for one_item in interface_records:
            is_mutable = 'Yes'
            if one_item['immutable']==0:
                is_mutable = 'No'

            # one_field = InterfaceFieldClass(one_item['Field_Name'], one_item['Field_Lable'],
            #                                 one_item['Field_Type'],  one_item['Field_Order'], one_item['Linked_Table'], is_mutable)
            # # one_field = InterfaceFieldClass(one_item['Field_Name'], one_item['Field_Lable'], one_item['Field_Type'],
            #                                 one_item['Field_Length'], one_item['Field_Order'], one_item['Linked_Table'], one_item['Immutable'])
            del one_item['Record_ID']
            del one_item['interface_name']
            self.FieldList.add_one_record(one_item)
            self.current_interface_info.append(one_item)


class BuildName_DLG_Class(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.the_frame = None

    def build_gui(self, field_names, update_record_name):

        font_size=14
        self.update_record_name = update_record_name

        MyLabel(font_size, self, text='Build a Name for the Interface').grid(
            row=1, column=1, columnspan=2, pady=15)

        ListScrollComboTwo(10, 20, 25, None, self,
                           name='field_list_box').grid(row=2, column=1, columnspan=2)

        self.nametowidget('field_list_box').add_item_list(field_names)
        self.nametowidget('field_list_box').set_double_click(self.field_chosen)

        MyEntry(font_size, self, width=75, name='edit_box').grid(
            row=3, column=1, columnspan=2, pady=15)
        #self.nametowidget('edit_box').is_build_name()

        MyButton(font_size, self, text='Save',
                 command=self.done).grid(row=4, column=1)
        MyButton(font_size,self,text='Cancel',command=self.destroy).grid(row=4, column=2)

    def done(self):
        self.update_record_name(self.nametowidget('edit_box').get())
        # interface_name = self.nametowidget('edit_box').get()
        # self.interface_name_widget['text'] = 'Name Formula: ' + interface_name
        # record_name = interface_name
        self.destroy()

    def field_chosen(self, e):

        current_text = self.nametowidget('edit_box').get()
        field_to_add = self.nametowidget('field_list_box').get_selected_text()

        current_text += '<!-'
        current_text += field_to_add
        current_text += '-!>'

        self.nametowidget('edit_box').delete(0, tk.END)
        self.nametowidget('edit_box').insert(0, current_text)
