import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *
from template import *


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

        ListScrollCombo(10, 20, 25, None, self.button_frame,
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
            this_interface_info = self.Database_Obj.get_interface_info(one_interface)
            if not this_interface_info['parent_interface']=='':
                messagebox.showerror('Error', 'Cannot remove ' + one_interface +'.  Remove parent interface that links to it and it will be removed.')
                interface_list.remove(one_interface)

        counter = 0
        while counter<len(interface_list):
            interface_list = interface_list + \
                self.Database_Obj.get_child_interface_names(interface_list[counter])
            counter += 1

        for one_interface in reversed(interface_list):
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
        #self.field_to_update = ''
        font_size = 18
        self.FieldList = None
        self.Required_checkbox_var = None
        self.current_interface_name = ''
        self.current_table_name = ''

        self.interface_name = ''

        self.multi_value_frames = []

        self.build_input_frame(font_size)
  
        self.set_input_frame_columns(5)

        self.build_button_frame(font_size)
        self.from_frame=''
        self.parent_interface = ''


    def enable_edit_field_button(self):
        self.button_frame.nametowidget('edit_field').config(state='normal')
        self.winfo_toplevel().bind("<Alt-e>", self.Edit_Field)

    def Edit_Field(self, event=None):
        this_field = self.FieldList.get_current_selection()

        self.reset_all_fields()

        self.button_frame.nametowidget('edit_field').config(text='Update Field')
        self.button_frame.nametowidget('edit_field').config(
            command=self.Update_Field_Clicked)
        self.button_frame.nametowidget('add_interface_button').config(state='disabled')
        self.button_frame.nametowidget('cancel').config(command=self.Cancel_Field_Update)
        self.button_frame.nametowidget('add_field').config(
            state='disabled')

        self.input_frame.nametowidget('field_type').set_selection(this_field['field_type'])

        #self.field_to_update = this_field
        self.input_frame.nametowidget('field_name').insert(
            0, this_field['field_name'])
        self.input_frame.nametowidget(
            'field_label').insert(0, this_field['field_label'])

        linked_table = this_field['linked_table']
        if not linked_table == '' and not this_field['field_type'] == 'multi_linked_table':
            self.input_frame.nametowidget['linked_table'].set_selection(
                linked_table)

        self.FieldList.set_state('disabled')
        self.winfo_toplevel().bind("<Alt-u>", self.Update_Field)
        self.winfo_toplevel().unbind("<Alt-e>")

    def Cancel_Field_Update(self):
        self.reset_edit_field_button()
        
        
    def reset_edit_field_button(self):
        self.button_frame.nametowidget(
            'edit_field').config(command=self.Edit_Field)
        self.button_frame.nametowidget(
            'edit_field').config(text='Edit Field')
        self.button_frame.nametowidget(
            'add_interface_button').config(state='normal')
        self.button_frame.nametowidget(
            'edit_field').config(state='disabled')
        self.button_frame.nametowidget('cancel').config(
            command=self.Cancel)
        self.FieldList.clear_all_selections()
        
    def build_input_frame(self,font_size):

        ## Row 1
        this_row = 0
        MyLabel(font_size,  self.input_frame,
                text='Interface Name').grid(row=this_row, column=2, columnspan=1, pady=10)

        MyLabel(font_size,  self.input_frame,
                text='Table Name').grid(row=this_row, column=4, columnspan=1, pady=(0, 10))

        MyLabel(font_size,  self.input_frame,
                text='Is Required').grid(row=this_row, column=7,  sticky='W',  columnspan=1,  padx=10)

        # row 2
        this_row += 1
        MyEntry(font_size, self.input_frame, name='interface_name').grid(
            row=this_row, column=2,  columnspan=1, pady=(0, 10), sticky='nw')

        MyEntry(font_size, self.input_frame, name='table_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1,  pady=(0, 10), sticky='N')

        self.Required_checkbox_var = tk.IntVar()

        self.Required_checkbox_var.set(0)

        MyCheckBox(self.input_frame, width=4, name='required_interface', variable=self.Required_checkbox_var).grid(
            row=this_row, column=7,  sticky='NW',  columnspan=1, pady=(0, 10), padx=10)


        # row 3
        this_row += 1

        MyLabel(font_size,   self.input_frame,
                text='Field Label').grid(row=this_row, column=2, columnspan=1, sticky='N')

        MyLabel(font_size,   self.input_frame,
                text='Field Name').grid(row=this_row, column=4, columnspan=1, sticky='N')

        MyLabel(font_size,   self.input_frame,
                text='Field Type').grid(row=this_row, column=5,  sticky='W', columnspan=2, pady=(0, 10), padx=10)

        MyLabel(font_size,   self.input_frame,
                text='Linked Table').grid(row=this_row, column=7,  sticky='W', rowspan=1, columnspan=1, pady=(0, 10), padx=10)

        # row 4
        this_row += 1

        MyEntry(font_size, self.input_frame, name='field_label').grid(
            row=this_row, column=2,  columnspan=1,  pady=(0, 10), sticky='N')

        MyEntry(font_size, self.input_frame, name='field_name',
                validation_type='DB_string').grid(row=this_row, column=4,  columnspan=1, pady=(0, 10), sticky='N')

        ListScrollCombo(5, 20, 20, None, self.input_frame, name='field_type').grid(
            row=this_row, column=5, columnspan=2,  rowspan=3, sticky='NW', pady=(0, 10), padx=10)

        ListScrollCombo(5, 20, 20, None, self.input_frame,
                           name='linked_table').grid(row=this_row,  rowspan=3, column=7, sticky='NW', pady=(0, 10), padx=10)

        self.input_frame.nametowidget('field_type').add_item_list(field_types)

        self.input_frame.nametowidget('field_type').set_function_on_select(
            ['linked_table'], self.enable_linked_table)

        self.input_frame.nametowidget('field_type').set_function_on_select(
            ['multi_linked_table'], self.multi_linked_table)

        self.input_frame.nametowidget('field_type').set_function_on_select(
            field_types_without_linked_table, self.disable_linked_table)

        # # row 5
        this_row += 1
        # MyLabel(font_size,   self.input_frame,
        #         text='Linked Interface Name').grid(row=this_row, column=2, columnspan=1, sticky='N')

        # # row 6
        this_row += 1

        # MyEntry(font_size, self.input_frame, name='new_linked_interface').grid(
        #     row=this_row, column=2,  columnspan=1,  pady=(0, 10), sticky='N')
        # self.input_frame.nametowidget('new_linked_interface').set_state('disabled')

        # row 7
        this_row += 1
        MyLabel(font_size, self.input_frame,  text='Name Formula:', name='record_name_formula').grid(
            row=this_row, column=2, columnspan=5, sticky='NW', pady=(0, 10), padx=10)

        # row 8
        this_row += 1

        self.populate_interface_box()

        #row 7
        this_row += 1

        headers = ['field_name', 'field_type',
                   'field_label', 'linked_table']
        # all_variables = headers + ['order']
        # all_variables = headers + [x+'-original' for x in all_variables]

        self.FieldList = MyMultiListBox(
            headers, self.input_frame)

        self.FieldList.change_lable_text('field_name', 'Field Name')
        self.FieldList.change_lable_text('field_type', 'Field Type')
        self.FieldList.change_lable_text('field_label', 'Field Label')
        self.FieldList.change_lable_text('linked_table', 'Linked Table')

        # fields_to_hide = [x for x in all_variables if x not in headers]

        # for one_field in fields_to_hide:
        #     self.FieldList.hide_column(one_field)

        self.FieldList.set_font_size(16)
        self.FieldList.grid(row=this_row, column=2, columnspan=6,
                            pady=15, sticky='news')
        self.FieldList.set_height(5)
        self.FieldList.set_width('field_type', 10)
        #self.FieldList.set_width('immutable', 8)
        self.FieldList.set_width('field_name', 10)
        self.FieldList.set_width('field_label', 10)
        self.FieldList.set_width('linked_table', 10)
        self.FieldList.set_double_click(self.delete_record)
        self.FieldList.set_single_click(self.enable_edit_field_button)

    def multi_linked_table(self):
        self.input_frame.nametowidget('linked_table').set_state('disabled')
        # self.input_frame.nametowidget(
        #     'new_linked_interface').set_state('normal')

    def disable_linked_table(self):
        self.input_frame.nametowidget('linked_table').set_state('disabled')
        #self.input_frame.nametowidget('new_linked_interface').set_state('disabled')

    def enable_linked_table(self):
        self.input_frame.nametowidget('linked_table').set_state('normal')
        # self.input_frame.nametowidget(
        #     'new_linked_interface').set_state('disabled')

    def build_button_frame(self, font_size):

        column=1
        MyButton(font_size,  self.button_frame, text='Add Field', name='add_field',
                 command=self.Add_Field_Button_Clicked, underline=4).grid(row=0, column=column, padx=40)

        column += 1
        MyButton(font_size,  self.button_frame, text='Add Interface',
                 name='add_interface_button', command=self.Done, underline=0).grid(row=0, column=column, padx=40)

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
        self.FieldList.delete_one_record('field_name', self.field_to_update['field_name'])
        

    def Update_Field_Clicked(self):

        self.winfo_toplevel().bind("<Alt-e>", self.Edit_Field)
        self.winfo_toplevel().unbind("<Alt-u>")
        
        self.FieldList.set_state('normal')
        self.button_frame.nametowidget('add_field').config(
            state='normal')


        #self.delete_record_to_update()

        for one_MV_interface in self.multi_value_frames:
            if one_MV_interface._name == self.FieldList.get_current_selection_this_column('field_name'):
                one_MV_interface.set_interface_name(self.input_frame.nametowidget(
                    'field_label').get())
                one_MV_interface.tkraise()
            
        self.Update_Field()

        #self.Add_Field()

        self.reset_edit_field_button()
        self.reset_all_fields()

    def delete_record(self, event=None):

        which = self.FieldList.get_selection()
        #which = event.widget.curselection()[0]

        self.FieldList.delete_one_item(which)

        pass

    def create_name(self, event=None):
        
        build_name_gui = BuildName_DLG_Class(self)
        build_name_gui.build_gui(self.FieldList.get_values_in_column(
            'field_name'), self.set_name_formula)
        build_name_gui.grab_set()

    def set_name_formula(self, new_formula):
        self.record_name_formula = new_formula
        self.input_frame.nametowidget('record_name_formula')[
            'text'] = 'Name Formula:' + new_formula

    def do_binding(self):
        self.winfo_toplevel().bind("<Alt-f>", self.Add_Field_Button_Clicked)
        #self.winfo_toplevel().bind("<Alt-i>", self.Add_Interface)
        self.winfo_toplevel().bind("<Alt-c>", self.Cancel)
        self.winfo_toplevel().bind("<Alt-n>", self.create_name)
        self.winfo_toplevel().bind("<Alt-a>", self.Done)

    def tkraise(self):
        self.do_binding()
        self.populate_interface_box()
        # self.input_frame.nametowidget('field_order').insert(0, '1')
        self.reset_edit_field_button()

        super().tkraise()
    
    def populate_interface_box(self):

        interface_names = self.Database_Obj.get_interface_names()
        
        if interface_names == 'Error':
                messagebox.showerror('Error','Error getting names of interfaces')
                return

        linked_table_list_box = self.input_frame.nametowidget('linked_table')
        self.enable_linked_table()
        linked_table_list_box.add_item_list(interface_names)
        self.disable_linked_table()

    def Validate(self, table_name, interface_name, is_required):

        if self.record_name_formula.strip() == '':
            messagebox.showerror('Error', 'Need a record name entered')
            return 'Error'

        if get_fields_for_record_name_formula(self.record_name_formula) == 0:
            messagebox.showerror(
                'Error', 'Must use at least one field in record name')
            return 'Error'

        if not table_name==self.current_table_name or self.current_table_name=='':
            if table_name.strip() == '':
                messagebox.showerror('Error', 'Need a table name entered')
                return 'Error'

            table_list = self.Database_Obj.get_list_current_tables()
            if table_list == 'Error':
                messagebox.showerror('Error', 'Not able to list of current tables')
                return 'Error'

            if table_name in table_list:
                messagebox.showerror('error', 'That table name already used')
                return 'Error'

        if not self.current_interface_name==interface_name:
            if interface_name.strip() == '':
                messagebox.showerror('Error', 'Need an interface name entered')
                return 'Error'

            interface_list = self.Database_Obj.get_interface_names()
            if interface_list == 'Error':
                messagebox.showerror('Error', 'Not able to list of current interface')
                return 'Error'

            if interface_name in interface_list:
                messagebox.showerror('error', 'That interface name already used')
                return 'Error'


    def Done(self, event=None):

        is_required = (self.Required_checkbox_var.get() == 1)
        table_name = self.input_frame.nametowidget('table_name').get()
        interface_name = self.input_frame.nametowidget(
            'interface_name').get().strip()
        if self.Validate(table_name, interface_name, is_required) == 'Error':
            return

        self.Add_Interface(table_name, interface_name, is_required)

        self.reset_frame()

    def reset_frame(self):
        self.input_frame.nametowidget('table_name').delete(0, tk.END)
        self.input_frame.nametowidget('interface_name').delete(0, tk.END)

        self.input_frame.nametowidget('field_name').delete(0, tk.END)

        self.input_frame.nametowidget('field_type').reset()
        self.input_frame.nametowidget('linked_table').reset()
        self.disable_linked_table()

    def Add_Interface(self, table_name, interface_name, is_required):
        #temp till I fix this code
        all_fields = self.FieldList.get_all_records()
        if self.Database_Obj.add_new_table(table_name, all_fields, False) == 'Error':
            messagebox.showerror('Error', 'Error adding table')
            return

        if self.Database_Obj.add_new_interface(interface_name, table_name, self.record_name_formula, all_fields, is_required, self.parent_interface) == 'Error':
            messagebox.showerror('Error', 'Error adding interface')
            self.Database_Obj.delete_table(table_name)
            return

        for one_multi_value in self.multi_value_frames:
            one_multi_value.set_parent_interface(interface_name, is_required)
            one_multi_value.Add_Interface()
            
        self.multi_value_frames=[]
        self.FieldList.clear_list_boxes()



    def Validate_Field(self,field_name, field_type, field_label, linked_table):

        if field_name.strip()=='':
            messagebox.showerror('error', 'Need a name for the field')
            return 'Error'

        if field_name.strip() in field_names_not_allowed:
            messagebox.showerror('error', 'Cannot use that field name')
            return 'Error'

        if field_label.strip() == '':
            messagebox.showerror('error', 'Need a label for the field')
            return 'Error'

        if field_type=='linked_table' and linked_table =='':
            messagebox.showerror('error', 'Need to select a table to link to')
            return 'Error'



        if field_type=='multi_linked_table':

            interface_list = self.Database_Obj.get_interface_names()
            if interface_list == 'Error':
                messagebox.showerror(
                    'Error', 'Not able to list of current interface')
                return 'Error'

            if field_label in interface_list:
                messagebox.showerror('error', 'That interface name already used.  You cannot use it for a field name with multi link')
                return 'Error'

    def Update_Field(self):
        field_name = self.input_frame.nametowidget('field_name').get()
        field_type = self.input_frame.nametowidget(
            'field_type').get_selected_text()
        field_label = self.input_frame.nametowidget('field_label').get()
        linked_table = ''
        if field_type == 'linked_table':
            linked_table = self.input_frame.nametowidget(
                'linked_table').get_selected_text()

        if self.Validate_Field(field_name, field_type, field_label, linked_table) == 'Error':
            return


        #this validation needs to be done here - different than when you update a field
        if not field_name == self.FieldList.get_current_selection_this_column('field_name') and self.FieldList.value_in_list('field_name', field_name):
            messagebox.showerror('error', 'That field name already used')
            return 'Error'

        if not field_label == self.FieldList.get_current_selection_this_column('field_label') and self.FieldList.value_in_list('field_label', field_label):
            messagebox.showerror('error', 'That field label already used')
            return 'Error'

        updated_field = {}
        updated_field['field_name']=field_name
        updated_field['field_type']=field_type
        updated_field['field_label'] = field_label
        updated_field['linked_table'] = linked_table

        original_field_name = self.FieldList.get_current_selection_value(
                'field_name-original')



        original_field_type = self.FieldList.get_current_selection_value(
                'field_type-original')

        self.FieldList.update_selected_record(updated_field)

        self.reset_edit_field_button()
        self.reset_all_fields()



        if field_type == 'multi_linked_table':


            if not original_field_type == 'multi_linked_table':
                new_frame = New_Interface_DLG_Class_For_Multi_Value(self.Database_Obj,
                                                                    self.winfo_toplevel(), title_text='Create Linked Interface', name=field_name)
                new_frame.grid(row=1, column=1, sticky='news')
                new_frame.set_from(self._name)
                new_frame.set_interface_name(field_label)
                self.multi_value_frames.append(new_frame)
                new_frame.tkraise()
            else:
                this_frame = next(x for x in self.multi_value_frames if x._name==original_field_name)
                this_frame.set_from(self._name)
                this_frame.set_interface_name(field_label)
                this_frame.tkraise()

    def Add_Field_Button_Clicked(self, event=None):
        field_name = self.input_frame.nametowidget('field_name').get()
        field_type = self.input_frame.nametowidget(
            'field_type').get_selected_text()
        field_label = self.input_frame.nametowidget('field_label').get()
        linked_table = ''
        if field_type == 'linked_table':
            linked_table = self.input_frame.nametowidget(
                'linked_table').get_selected_text()

        if self.Validate_Field(field_name, field_type, field_label, linked_table)=='Error':
            return

        #this validation needs to be done here - different than when you update a field

        if self.FieldList.value_in_list('field_label', field_label):
            messagebox.showerror('error', 'That field label already used')
            return 'Error'

        if self.FieldList.value_in_list('field_name', field_name):
            messagebox.showerror('error', 'That field name already used')
            return 'Error'

        self.Add_Field()

        if field_type == 'multi_linked_table':
            new_frame = New_Interface_DLG_Class_For_Multi_Value(self.Database_Obj,
                                                                self.winfo_toplevel(), title_text='Create Linked Interface', name=field_name)
            new_frame.grid(row=1, column=1, sticky='news')
            new_frame.set_from(self._name)
            new_frame.set_interface_name(self.input_frame.nametowidget(
                'field_label').get())
            self.multi_value_frames.append(new_frame)
            new_frame.tkraise()
        
        self.reset_all_fields()
        # else:
        #     self.Add_Field()
    #def Add_Field(self, event=None):

    def Add_Field(self):

        field_name = self.input_frame.nametowidget('field_name').get()
        field_type = self.input_frame.nametowidget(
            'field_type').get_selected_text()
        field_label = self.input_frame.nametowidget('field_label').get()
        linked_table = ''
        if field_type == 'linked_table':
            linked_table = self.input_frame.nametowidget(
                'linked_table').get_selected_text()

        this_field={}
        this_field['field_name'] = field_name
        this_field['field_type'] = field_type
        this_field['field_label'] = field_label
        this_field['linked_table'] = linked_table

        self.FieldList.add_one_record(this_field)

        self.input_frame.nametowidget('field_label').focus_set()
        

    def reset_all_fields(self):

        self.input_frame.nametowidget('field_name').delete(0, tk.END)
        self.input_frame.nametowidget('field_label').delete(0, tk.END)

        self.input_frame.nametowidget('field_type').reset()
        self.input_frame.nametowidget('linked_table').reset()
        #self.Required_checkbox_var.set(0)
        #self.FieldList.clear_all_selections()

    def Cancel(self, event=None):
        self.winfo_toplevel().unbind("<Alt-f>")
        self.winfo_toplevel().unbind("<Alt-i>")
        self.winfo_toplevel().unbind("<Alt-c>")
        self.winfo_toplevel().unbind("<Alt-n>")
        self.winfo_toplevel().unbind("<Alt-a>")
        self.clear_widgets()
        self.winfo_toplevel().nametowidget('interface_admin').populate_interface_box()

        for one_multi_value in self.multi_value_frames:
            one_multi_value.destroy()
            
        super().Cancel()

    def clear_widgets(self):
        self.FieldList.clear_list_boxes()

        self.input_frame.nametowidget('interface_name').delete(0, tk.END)
        self.input_frame.nametowidget('table_name').delete(0, tk.END)

        self.input_frame.nametowidget('field_name').delete(0, tk.END)

        self.input_frame.nametowidget('field_type').reset()
        self.Required_checkbox_var.set(0)



class Alter_Interface_DLG_Class(New_Interface_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):

        #self.current_interface_info = []

        self.current_name_formula = ''
        ####################
        #always have super()     at the top
        super().__init__(Database_Obj, *args, **kwargs)
        ####################

    def Done(self, event=None):

        is_required = (self.Required_checkbox_var.get() == 1)
        table_name = self.input_frame.nametowidget('table_name').get()
        interface_name = self.input_frame.nametowidget(
            'interface_name').get().strip()
        if self.Validate(table_name, interface_name, is_required) == 'Error':
            return

        if self.Update_Interface()=='Error':
            return

        self.reset_frame()

    def set_current_interface_info(self, interface_records, interface_info):

        self.current_name_formula = interface_info['record_name_formula']
        self.record_name_formula = interface_info['record_name_formula']
        self.current_interface_name = interface_info['interface_name']
        self.current_table_name = interface_info['interface_table']
        self.input_frame.nametowidget(
            'linked_table').remove_item(self.current_interface_name)

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
            if not one_item['field_name'] == 'parent_id':

                one_item_for_fieldlist = {}
                del one_item['Record_ID']
                del one_item['interface_name']
                
                for key in one_item:
                    one_item_for_fieldlist[key]=one_item[key]
                    one_item_for_fieldlist[key+'-original']=one_item[key]


                self.FieldList.add_one_record(one_item_for_fieldlist)
                #self.current_interface_info.append(one_item)

                if one_item['field_type'] == 'multi_linked_table':
                    self.set_this_MV_frame(
                        one_item['field_label'], one_item['field_name'])

    def tkraise(self):

        self.button_frame.nametowidget(
            'add_interface_button').config(text='Update Interface')

        # self.button_frame.nametowidget(
        #     'add_interface_button').config(command=self.update_interface)

        super().tkraise()
        self.enable_linked_table()
        self.input_frame.nametowidget('linked_table').remove_item(
            self.current_interface_name)
        self.disable_linked_table()

    def Update_Interface(self):

        record_ID = {'column_name': 'interface_name', 'value':self.current_interface_name, 'type':'string'}
        columns_to_update = []
        update_interface_info = False
        #check if interface name has changed
        interface_name = self.input_frame.nametowidget('interface_name').get()
        if not interface_name == self.current_interface_name:
            if interface_name in self.Database_Obj.get_interface_names():
                messagebox.ERROR('Error', 'Interface name already being used')
                return 'Error'


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
                return 'Error'
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
        
        fields_from_multibox = self.FieldList.get_all_records()
        fields_needed_for_name_formula = get_fields_for_record_name_formula(self.current_name_formula)

        fields_to_remove = [x for x in fields_from_multibox if x['field_order']==-1]
        fields_from_multibox = [x for x in fields_from_multibox if x not in fields_to_remove]

        #if field_name-original not in the dictionar it must not be in the table so doesn't need to really be removed.
        fields_to_remove = [
            x for x in fields_to_remove if 'field_name-original' in x]

        new_fields = [x for x in fields_from_multibox if not 'field_name-original' in x]
        original_fields = [x for x in fields_from_multibox if not x in new_fields]
        headers = ['field_name', 'field_type',
                   'field_label', 'linked_table', 'field_order']


        #get the original fields that have been altered
        #this is so we don't lose data
        original_fields_with_changes =[]
        [original_fields_with_changes.append(
            x) for x in original_fields for y in headers if not x[y] == x[y+'-original'] and x not in original_fields_with_changes]
        
       
        if not [x for x in fields_needed_for_name_formula if x not in [y['field_name'] for y in fields_from_multibox]]==[]:
            messagebox.showerror('Error', 'Missing fields that are in the name formula')
            return 'Error'                        
       

        if update_interface_info:
            self.Database_Obj.update_one_record(
                'interfaces', record_ID, columns_to_update)

        #add new fields
        if not new_fields == []:
            if self.Database_Obj.add_new_fields_interface(self.current_interface_name,
                                                          self.current_table_name, new_fields) == 'Error':
                messagebox.showerror(
                    'Error', 'Error adding one of the new fields')
                return 'Error'

        #change altered fields
        if not original_fields_with_changes == []:
            if self.Database_Obj.alter_fields_interface(self.current_interface_name,
                                                          self.current_table_name, original_fields_with_changes) == 'Error':
                messagebox.showerror(
                    'Error', 'Error adding one of the new fields')
                return 'Error'

        #remove fields
        if not fields_to_remove == []:
            if self.Database_Obj.remove_fields_interface(self.current_interface_name,
                                                         self.current_table_name, fields_to_remove) == 'Error':
                messagebox.showerror('Error', 'Error removing fields')
                return 'Error'

        for one_multi_value in self.multi_value_frames:
            one_multi_value.set_parent_interface(interface_name, False)
            if type(one_multi_value).__name__== 'New_Interface_DLG_Class_For_Multi_Value':
                one_multi_value.Add_Interface()
            else:
                one_multi_value.new_parent_interface_name(self.current_interface_name)

                one_multi_value.Update_Interface()                
            # elif not columns_to_update==[]:
            #     if not next(x for x in columns_to_update if x['column_name']=='interface_name')==None:
            #         one_multi_value.new_parent_interface_name(self.current_interface_name)

            #         one_multi_value.Update_Interface()
            
        self.multi_value_frames=[]
        self.FieldList.clear_list_boxes()
        self.winfo_toplevel().nametowidget('interface_admin').populate_interface_box()
        self.lower()

    def Cancel(self):
        #in case there are things to do when leaving the frame
        temp_button = self.button_frame.nametowidget('add_interface_button')
        temp_button.config(text='Add Table')
        temp_button.config(command=self.Done)

        for one_multi_value in self.multi_value_frames:
            one_multi_value.destroy()

        super().Cancel()
    
    def set_this_MV_frame(self, this_interface, field_name):
        interface_fields = self.Database_Obj.get_interface_records(
            this_interface)
        if interface_fields == 'Error':
            messagebox.showerror('error', 'Error loading interface')
            return 'Error'

        interface_info = self.Database_Obj.get_interface_info(this_interface)

        new_frame = Alter_Interface_DLG_Class_For_Multi_Value(self.Database_Obj,
                                                            self.winfo_toplevel(), title_text='Alter Multi Value', name=field_name)
        new_frame.grid(row=1, column=1, sticky='news')
        new_frame.set_from(self._name)
        new_frame.set_interface_name(self.input_frame.nametowidget(
            'field_label').get())
        new_frame.set_current_interface_info(interface_fields,interface_info)
        self.multi_value_frames.append(new_frame)

class BuildName_DLG_Class(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.the_frame = None

    def build_gui(self, field_names, update_record_name):

        font_size=14
        self.update_record_name = update_record_name

        MyLabel(font_size, self, text='Build a Name for the Interface').grid(
            row=1, column=1, columnspan=2, pady=15)

        ListScrollCombo(10, 20, 25, None, self,
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

        this_name = self.nametowidget('edit_box').get()

        fields_needed = get_fields_for_record_name_formula(this_name)

        fields_available = self.nametowidget('field_list_box').get_all_elements()

        if [x for x in fields_needed if x in fields_available]==[]:
            messagebox.showerror('Error', 'Need to choose at least one field from this interface')
            return

        self.update_record_name(this_name)


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


class Alter_Interface_DLG_Class_For_Multi_Value(Alter_Interface_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):
        super().__init__(Database_Obj, *args, **kwargs)

        self.button_frame.nametowidget(
            'add_interface_button').config(text="Done")
        self.button_frame.nametowidget('add_interface_button').config(
            command=self.Done)
        self.button_frame.nametowidget('cancel').config(
            command=self.lower())
        self.title_frame.nametowidget('title').config(
            text='New Multi Value Table')

        self.input_frame.nametowidget(
            'required_interface').set_state('disabled')

        self.is_required = False

    def Done(self, event=None):

        is_required = (self.Required_checkbox_var.get() == 1)
        table_name = self.input_frame.nametowidget('table_name').get()
        interface_name = self.input_frame.nametowidget(
            'interface_name').get().strip()
        if self.Validate(table_name, interface_name, is_required) == 'Error':
            return
        else:
            #self.winfo_toplevel().nametowidget(self.from_frame).Add_Field()
            pass

            self.current_interface_name = interface_name
            self.current_table_name = table_name
            self.winfo_toplevel().nametowidget(self.from_frame).do_binding()
            self.lower()

    def tkraise(self):

        super().tkraise()

        self.button_frame.nametowidget(
            'add_interface_button').config(text='Done')

        self.button_frame.nametowidget(
            'add_interface_button').config(command=self.Done)

    def set_interface_name(self, interface_name):
        self.input_frame.nametowidget(
            'interface_name').delete(0, tk.END)

        self.input_frame.nametowidget(
            'interface_name').insert(0, interface_name)

        self.title_frame.nametowidget('title')['text'] = 'Update ' + interface_name

    def set_from(self, from_frame):
        self.from_frame = from_frame

    def new_parent_interface_name(self, interface_name):
        this_field = {}
        this_field['field_name'] = 'parent_id'
        this_field['field_type'] = 'linked_table'
        this_field['field_label'] = ''
        this_field['linked_table'] = interface_name
        this_field['field_order']=0
        this_field['field_name-original'] = 'parent_id'
        this_field['field_type-original'] = 'linked_table'
        this_field['field_label-original'] = ''
        this_field['linked_table-original'] = ''
        this_field['field_order-original'] = 0
        self.FieldList.add_one_record(this_field)

    def set_parent_interface(self, interface_name, is_required):
        self.is_required = is_required

        # this_field = {}
        # this_field['field_name'] = 'parent_id'
        # this_field['field_type'] = 'linked_table'
        # this_field['field_label'] = ''
        # this_field['linked_table'] = interface_name
        self.parent_interface = interface_name
        #self.FieldList.add_one_record(this_field)

class New_Interface_DLG_Class_For_Multi_Value(New_Interface_DLG_Class):
    def __init__(self, Database_Obj, *args, **kwargs):
        super().__init__(Database_Obj, *args, **kwargs)

        self.button_frame.nametowidget(
            'add_interface_button').config(text="Done")
        self.button_frame.nametowidget('add_interface_button').config(
            command=self.Done)
        self.button_frame.nametowidget('cancel').config(
            command=self.lower())
        self.title_frame.nametowidget('title').config(text='New Multi Value Table')

        self.input_frame.nametowidget(
            'required_interface').set_state('disabled')

        self.input_frame.nametowidget('table_name').focus_set()
        self.is_required=False

    def Done(self, event=None):

        is_required = (self.Required_checkbox_var.get() == 1)
        table_name = self.input_frame.nametowidget('table_name').get()
        interface_name = self.input_frame.nametowidget(
            'interface_name').get().strip()
        if self.Validate(table_name, interface_name, is_required) == 'Error':
            return
        else:
            #self.winfo_toplevel().nametowidget(self.from_frame).Add_Field()
            pass

            self.current_interface_name = interface_name
            self.current_table_name = table_name
            self.winfo_toplevel().nametowidget(self.from_frame).do_binding()
            self.lower()

    def set_interface_name(self, interface_name):
        self.input_frame.nametowidget('interface_name').insert(0, interface_name)

    def set_from(self, from_frame):
        self.from_frame=from_frame
    
    def set_parent_interface(self, interface_name, is_required):
        self.is_required = is_required

        this_field = {}
        this_field['field_name'] = 'parent_id'
        this_field['field_type'] = 'linked_table'
        this_field['field_label'] = ''
        this_field['linked_table'] = interface_name
        self.parent_interface = interface_name
        self.FieldList.add_one_record(this_field)

    def Add_Interface(self):
        
        table_name = self.input_frame.nametowidget('table_name').get()
        interface_name = self.input_frame.nametowidget(
            'interface_name').get().strip()

        super().Add_Interface(table_name, interface_name, self.is_required)
