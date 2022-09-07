import tkinter as tk
from universal_components import *
from dataclasses import dataclass
from tkinter import messagebox
from WidgetControls import *
#from Interface_Admin import InterfaceFieldClass
from datetime import datetime
from template import *

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
        self.Frame_For_Interface = None
        self.Scrolling_Frame = None
        
        self.multi_value_fields = {}
        self.multi_value_interface_info = {}
        self.multi_value_records = []
        self.multi_value_record_IDs = {}
                
    def create_frame(self):
        self.these_widgets = []
        self.multi_value_record_IDs = {}
        self.multi_value_records = []
        self.the_fields = self.Database_Obj.get_interface_records(
            self.the_interface)

        font_size = 24
        
        self.Scrolling_Frame=ScrollingFrame(self.input_frame)

        self.Frame_For_Interface = Frame_For_Interface_Class(self.Database_Obj,
            self.Scrolling_Frame.scrollable_frame)

        self.Frame_For_Interface.Build_These_Fields(
            font_size, self.the_fields, self.the_interface)

        self.Scrolling_Frame.grid(row=0, column=0)

        self.Frame_For_Interface.grid(row=0, column=0)

        MyButton(font_size,  self.button_frame, text='Save Record',
                 command=self.Save_Record, underline=0).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel, underline=0).grid(row=0, column=2, padx=40)

        self.winfo_toplevel().bind("<Alt-s>", self.Save_Record)
        self.winfo_toplevel().bind("<Alt-c>", self.Cancel)

    # def Build_These_Fields(self, this_frame, font_size, the_fields):

    #     fields_to_save = []
    #     these_widgets = []

    #     for this_row, one_field in enumerate(the_fields, start=1):
    #         self.the_field_names.append(one_field['field_name'])

    #         if not one_field['field_type']=='multi_linked_table':

    #             one_widget = {}

    #             temp = MyLabel(font_size, this_frame,
    #                         text=one_field['field_label'])
    #             one_widget['the_widget']=temp
    #             kwargs = {}
    #             kwargs['row']=this_row
    #             kwargs['column']=1
    #             kwargs['pady']=10
    #             one_widget['kwargs']=kwargs

    #             these_widgets.append(one_widget)

    #         if one_field['field_type'] == 'linked_table':
    #             temp = ListScrollWithRecordID(
    #                 5, 20, 20, None, this_frame, name=one_field['field_name'])
    #             linked_interface_info = self.Database_Obj.get_interface_info(
    #                 one_field['Linked_Table'])
    #             temp.add_item_list(
    #                 self.Database_Obj.get_record_names(linked_interface_info['interface_table'], linked_interface_info['Record_Name_Formula']))
    #         elif one_field['field_type'] == 'text':
    #             temp = TextScrollCombo(
    #                 this_frame, name=one_field['field_name'])
    #             temp.config(width=500, height=150)
    #             temp.set_font(16)

    #         elif one_field['field_type'] == 'bool':
    #             temp_var = tk.IntVar()
    #             self.Checkbox_var[one_field['field_name']] = temp_var
    #             temp = MyCheckBox(this_frame, width=4,
    #                               name=one_field['field_name'], variable=temp_var)
    #             temp_var.set(0)
    #         elif one_field['field_type']=='multi_linked_table':
    #             #not sure why MyFrame won't work with this but I don't need it
    #             #temp = MyFrame(None, this_frame, font_size = font_size, name=one_field['field_name'], title_text=one_field['field_label'])
    #             name_of_field = this_frame._name + '*' + one_field['field_name']
    #             temp = tk.Frame(this_frame,  name=name_of_field)
    #             these_fields = self.Database_Obj.get_interface_records(
    #                 one_field['field_label'])
    #             interface_info = self.Database_Obj.get_interface_info(
    #                 one_field['field_label'])
    #             self.multi_value_fields[name_of_field] = these_fields
    #             self.multi_value_interface_info[name_of_field] = interface_info

    #             temp_fields = [
    #                 x for x in these_fields if not x['linked_table'] == self.the_interface]

    #             self.Build_These_Fields(temp, font_size, [x for x in these_fields if not x['linked_table'] == self.the_interface])
    #             MyLabel(font_size, temp, text=one_field['field_label']).grid(
    #                 row=0, column=1, columnspan=2)

    #             tk.Listbox(temp, name='*list_box', font=font_return(font_size), height=4, width=20).grid(row=3,  column=1, columnspan=2)

    #             MyButton(font_size-8, temp, text='Add Values', command=lambda: self.Add_Value_Mutli_Value_Box(name_of_field)).grid(
    #                 row=4, column=1, columnspan=2)
    #         else:
    #             temp = MyEntry(
    #                 font_size, this_frame, validation_type=one_field['field_type'], name=one_field['field_name'], width=10)

    #         fields_to_save.append(temp)
    #         one_widget = {}
    #         kwargs = {}
    #         kwargs['row'] = this_row
    #         one_widget['the_widget'] = temp
    #         kwargs['pady'] = 10
            
    #         if not one_field['field_type']=='multi_linked_table':
    #             kwargs['column'] = 2
    #         else:
    #             kwargs['column'] = 1
    #             kwargs['columnspan'] = 2

    #         one_widget['kwargs'] = kwargs

    #         these_widgets.append(one_widget)
    #         this_row += 1

    #     for one_widget in these_widgets:
    #         one_widget['the_widget'].grid(one_widget['kwargs'])

    #     self.the_fields = fields_to_save

    def Add_Value_Mutli_Value_Box(self, field_name):
        these_fields = self.multi_value_fields[field_name]
        interface_info = self.multi_value_interface_info[field_name]

        this_multi_value_field = [
            x['the_widget'] for x in self.these_widgets if x['the_widget']._name == field_name][0]

        this_record_values = {}

        for one_field in these_fields:
            if one_field['linked_table']==self.the_interface:
                field_name_for_record_id = one_field['field_name']
            else:
                this_record_values[one_field['field_name']] = this_multi_value_field.nametowidget(one_field['field_name']).get()
        
        this_record_values['Record_ID'] = 0

        this_name = get_names([this_record_values],
                              interface_info['record_name_formula'])[0]['Name']
        this_record_values['*record_name']=this_name

        this_multi_value_field.nametowidget(
            '*list_box').insert(tk.END, this_name)

        this_record_values['field_name'] = field_name.split(
            '*')[len(field_name.split('*'))-1]

        this_record = {}
        this_record['table'] = interface_info['interface_table']
        this_record['values'] = this_record_values
        self.multi_value_record_IDs[interface_info['interface_table']]=field_name_for_record_id

        self.multi_value_records.append(this_record)

    def Save_Record(self):
        
        record_to_add = []

        for one_field in self.the_fields:
            if not one_field['field_type'] == 'multi_linked_table':
                one_field_record = {}
                one_field_record['type'] = one_field['field_type']
                #one_record['column'] = one_field['field_name']
                one_field_record['field_name'] = one_field['field_name']

                if one_field['field_type'] in ['text','string']:
                    one_field_record['value'] = self.Frame_For_Interface.nametowidget(
                        one_field['field_name']).get()
                elif one_field['field_type'] == 'date':
                    one_field_record['value'] = datetime.strptime(self.Frame_For_Interface.nametowidget(
                        one_field['field_name']).get(),'%m\\%d\\%Y')
                elif one_field['field_type'] == 'integer':
                    one_field_record['value'] = int(self.Frame_For_Interface.nametowidget(
                        one_field['field_name']).get())
                elif one_field['field_type'] == 'double':
                    one_field_record['value'] = float(self.Frame_For_Interface.nametowidget(
                        one_field['field_name']).get())
                elif one_field['field_type'] == 'linked_table':
                    one_field_record['value'] = self.Frame_For_Interface.nametowidget(
                        one_field['field_name']).get_selected_ID()[0]
                elif one_field['field_type'] == 'bool':
                    one_field_record['value'] = self.Frame_For_Interface.Checkbox_var[one_field['field_name']].get(
                    )

                record_to_add.append(one_field_record)

        interface_info = self.Database_Obj.get_interface_info(
            self.the_interface)

        record_id = self.Database_Obj.add_record(
            interface_info['interface_table'], record_to_add)
        
        if record_id=='Error':
            messagebox.showerror('Error', "Error adding record")

        the_tables_for_multivalues = set(x['table'] for x in self.multi_value_records)
        for one_table in the_tables_for_multivalues:
            these_records = [x['values'] for x in self.multi_value_records if x['table']==one_table]
            for one_record in these_records:
                one_record[self.multi_value_record_IDs[one_table]] = record_id
                record_id = self.Database_Obj.add_record(
                    one_table, one_record)
                
                if record_id == 'Error':
                    messagebox.showerror('Error', "Error adding record")

        self.winfo_toplevel().nametowidget('interface_dlg').Set_Interface(self.the_interface)
        self.lower()

    def Cancel(self):

        self.these_widgets = []
        self.Frame_For_Interface.destroy()

        super().Cancel()

    def Set_Interface(self, this_interface):
        #self.set_title(this_interface+'\nAdd Record')

        self.the_interface = this_interface
        self.the_interface_info = self.Database_Obj.get_interface_info(self.the_interface)


        self.create_frame()


class Frame_For_Interface_Class(tk.Frame):
    def __init__(self, Database_Obj, *args, **kwargs):


        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj
        self.the_field_names = []
        self.Checkbox_var = []

    def Build_These_Fields(self, font_size, the_fields, parent_interface):

        these_widgets = []

        for this_row, one_field in enumerate(the_fields, start=1):
            self.the_field_names.append(one_field['field_name'])

            if not one_field['field_type'] == 'multi_linked_table':

                one_widget = {}

                temp = MyLabel(font_size, self,
                               text=one_field['field_label'])
                one_widget['the_widget'] = temp
                kwargs = {}
                kwargs['row'] = this_row
                kwargs['column'] = 1
                kwargs['pady'] = 10
                one_widget['kwargs'] = kwargs

                these_widgets.append(one_widget)

            if one_field['field_type'] == 'linked_table':
                temp = ListScrollWithRecordID(
                    5, 20, 20, None, self, name=one_field['field_name'])
                linked_interface_info = self.Database_Obj.get_interface_info(
                    one_field['Linked_Table'])
                temp.add_item_list(
                    self.Database_Obj.get_record_names(linked_interface_info['interface_table'], linked_interface_info['Record_Name_Formula']))
            elif one_field['field_type'] == 'text':
                temp = TextScrollCombo(
                    self, name=one_field['field_name'])
                temp.config(width=500, height=150)
                temp.set_font(16)

            elif one_field['field_type'] == 'bool':
                temp_var = tk.IntVar()
                self.Checkbox_var[one_field['field_name']] = temp_var
                temp = MyCheckBox(self, width=4,
                                  name=one_field['field_name'], variable=temp_var)
                temp_var.set(0)
            elif one_field['field_type'] == 'multi_linked_table':
                #not sure why MyFrame won't work with this but I don't need it
                #temp = MyFrame(None, this_frame, font_size = font_size, name=one_field['field_name'], title_text=one_field['field_label'])
                # name_of_field = this_frame._name + \
                #     '*' + one_field['field_name']
                temp = Frame_For_Interface_Class(self.Database_Obj,
                    self,  name=one_field['field_name'])
                these_fields = self.Database_Obj.get_interface_records(
                    one_field['field_label'])
                interface_info = self.Database_Obj.get_interface_info(
                    one_field['field_label'])
                # self.multi_value_fields[name_of_field] = these_fields
                # self.multi_value_interface_info[name_of_field] = interface_info

                fields_to_show = [
                    x for x in these_fields if not x['linked_table'] == parent_interface]

                temp.Build_These_Fields(
                    font_size, fields_to_show, one_field['field_label'])
                # self.Build_These_Fields(temp, font_size, [
                #                         x for x in these_fields if not x['linked_table'] == self.the_interface])
                MyLabel(font_size, temp, text=one_field['field_label']).grid(
                    row=0, column=1, columnspan=2)

                tk.Listbox(temp, name='*list_box', font=font_return(font_size),
                           height=4, width=20).grid(row=len(fields_to_show)+1,  column=1, columnspan=2)

                MyButton(font_size-8, temp, text='Add Values', command=lambda: self.Add_Value_Mutli_Value_Box(name_of_field)).grid(
                    row=len(fields_to_show)+2, column=1, columnspan=2)
            else:
                temp = MyEntry(
                    font_size, self, validation_type=one_field['field_type'], name=one_field['field_name'], width=10)

            #self.the_fields.append(temp)
            one_widget = {}
            kwargs = {}
            kwargs['row'] = this_row
            one_widget['the_widget'] = temp
            kwargs['pady'] = 10

            if not one_field['field_type'] == 'multi_linked_table':
                kwargs['column'] = 2
            else:
                kwargs['column'] = 1
                kwargs['columnspan'] = 2

            one_widget['kwargs'] = kwargs

            these_widgets.append(one_widget)
            this_row += 1

        for one_widget in these_widgets:
            one_widget['the_widget'].grid(one_widget['kwargs'])

