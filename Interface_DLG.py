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
        ListScrollCombo(5, 20, 20, None, self.input_frame,
                           name='interfaces').grid(row=this_row, column=7, sticky='NW', pady=(0, 10), padx=10)


        this_row += 1
        MyButton(font_size,  self.button_frame, text='Open Interface',
                 command=self.Open_Interface).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=0, column=2, padx=40)

    def populate_interface_box(self):

        interface_names = self.Database_Obj.get_interface_names_parent_none()

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
            10, 60, 20, None, self.input_frame, name='all_records').grid(row=1, column=1)

        self.input_frame.nametowidget(
            'all_records').set_double_click(self.Delete_Record)

        self.set_input_frame_columns(1)

        MyButton(font_size,  self.button_frame, text='New Record',
                 command=self.New_Record).grid(row=this_row, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Edit Record',
                 command=self.Edit_Record).grid(row=this_row, column=2, padx=40)
        MyButton(font_size,  self.button_frame, text='Delete Record',
                 command=self.Delete_Record).grid(row=this_row, column=3, padx=40)

        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel).grid(row=this_row, column=4, padx=40)

        self.interface_info = None

    def Populate_Records(self):
        pass

    def Delete_Record(self, event=None):

        self.Database_Obj.delete_record(
            self.interface_info, self.input_frame.nametowidget('all_records').get_selected_ID())

        self.Add_All_Records()


    def Edit_Record(self):
        selected_record = self.input_frame.nametowidget('all_records').get_selected_ID()

        Edit_Record_Frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg')

        Edit_Record_Frame.Set_Interface(self.interface_info)

        Edit_Record_Frame.Populate_Fields(selected_record)
        Edit_Record_Frame.tkraise()

    def New_Record(self):
        New_Record_Frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg')

        New_Record_Frame.Set_Interface(self.interface_info)
        New_Record_Frame.tkraise()
        

    def Set_Interface(self, this_interface):
        self.set_title(this_interface)

        self.interface_info = All_Interface_Info_Class(this_interface, self.Database_Obj.get_interface_info(
            this_interface), self.Database_Obj.get_interface_records(
            this_interface))

        self.Add_All_Records()

    def Add_All_Records(self):
        this_list_box = self.input_frame.nametowidget('all_records')

        this_list_box.remove_all_items
        this_list_box.add_item_list(
            self.Database_Obj.get_record_names(self.interface_info.interface_structure['interface_table'], self.interface_info.interface_structure['record_name_formula']))


class InterfaceDLG_One_Record_Class(MyFrame):
    def __init__(self, Database_Obj,   *args, **kwargs):
        
        super().__init__(Database_Obj, *args, **kwargs)

        self.interface_info = None

        self.Frame_For_Interface = None
        self.Scrolling_Frame = None


    def Populate_Fields(self, record_ID):
        self.Frame_For_Interface.Populate_Fields(record_ID)

    def create_frame(self):

        font_size = 24
        
        self.Scrolling_Frame=ScrollingFrame(self.input_frame)

        self.Frame_For_Interface = Frame_For_Interface_Class(self.Database_Obj,
            self.Scrolling_Frame.scrollable_frame, name='top_frame')

        self.Frame_For_Interface.Set_Interface(self.interface_info)

        self.Frame_For_Interface.Build_These_Fields(
            font_size)

        self.Scrolling_Frame.grid(row=0, column=0)

        self.Frame_For_Interface.grid(row=0, column=0, sticky='news')

        MyButton(font_size,  self.button_frame, text='Save Record',
                 command=self.Frame_For_Interface.Save_Record, underline=0).grid(row=0, column=1, padx=40)
        MyButton(font_size,  self.button_frame, text='Cancel',
                 command=self.Cancel, underline=0).grid(row=0, column=2, padx=40)

        self.winfo_toplevel().bind("<Alt-s>", self.Frame_For_Interface.Save_Record)
        self.winfo_toplevel().bind("<Alt-c>", self.Cancel)

    def Cancel(self):

        self.Frame_For_Interface.destroy()

        self.winfo_toplevel().nametowidget('interface_dlg').Add_All_Records()
        
        super().Cancel()

    def Set_Interface(self, interface_info):
        self.interface_info = interface_info
        self.create_frame()


class Frame_For_Interface_Class(tk.Frame):
    def __init__(self, Database_Obj, *args, **kwargs):


        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj

        self.the_records = []

        self.interface_info = []
        self.top_frame = None

        #these are for the multivalue so that we can tie them back correctly
        self.current_record=0
        self.current_parent_record=0

    def Set_Interface(self, interface_info):
        self.interface_info = interface_info
    
    def Set_top_frame(self, top_frame):
        self.top_frame=top_frame

    def Populate_Fields(self, record_ID):

        this_record = self.Database_Obj.get_one_record(
            self.interface_info.interface_structure['interface_table'], record_ID)

        for one_field in self.interface_info.the_fields:
            if one_field['field_type'] == 'linked_table':
                pass
            elif one_field['field_type'] == 'multi_linked_table':
                pass
            elif one_field['field_type'] == 'bool':
                pass
            elif one_field['field_type'] == 'date':
                self.nametowidget(one_field['field_name']).insert(
                    0, this_record[one_field['field_name']].strftime('%m/%d/%Y'))
            elif one_field['field_type'] in ['integer', 'double']:
                if not this_record[one_field['field_name']]==None:
                    self.nametowidget(one_field['field_name']).insert(
                        0, str(this_record[one_field['field_name']]))
            else:
                if not this_record[one_field['field_name']]==None:
                    self.nametowidget(one_field['field_name']).insert(
                        0, this_record[one_field['field_name']])


        # these_multi_linked_tables = [
        #     x['field_name'] for x in self.the_fields if x['field_type'] == 'multi_linked_table']

        # multi_linked_tables_records = {}
        # for one_table in multi_linked_tables_records:
        #     multi_linked_tables_records[one_table] = self.Database_Obj.get_multi_linked_records(
        #         one_table, selected_record)



    # def set_name_formula(self, Record_Name_Formula):
    #     self.Record_Name_Formula = Record_Name_Formula


    def Build_These_Fields(self, font_size):

        #self.interface_name = interface_name
        these_widgets = []

        self.interface_info.the_fields.sort(key=Sort_By_Order)

        for this_row, one_field in enumerate(self.interface_info.the_fields, start=1):
            #self.the_fields.append(one_field)

            if not one_field['field_type'] in fields_to_skip_in_interface:

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

            if one_field['field_type']=='title':
                temp = MyLabel(
                    font_size, self, name=one_field['field_name'], text=one_field['field_label'])
            elif one_field['field_type']=='MV_buttons':
                field_name=copy.deepcopy(one_field['field_name'])
                temp=tk.Frame(self)

                MyButton(font_size-8, temp, text='Done',
                         command=self.Collect_Data_and_Lower).grid(row=1, column=1)
                MyButton(font_size-8, temp, text='Cancel',
                         command=self.Lower).grid(row=1, column=2)

            elif one_field['field_type'] == 'linked_table':
                temp = ListScrollWithRecordID(
                    5, 20, 20, None, self, name=one_field['field_name'])
                linked_interface_info = self.Database_Obj.get_interface_info(
                    one_field['Linked_Table'])
                temp.add_item_list(
                    self.Database_Obj.get_record_names(linked_interface_info['interface_table'], linked_interface_info['record_name_formula']))
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

                above_frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg')
                this_frame = Frame_For_Interface_Class(self.Database_Obj,
                                               above_frame.Scrolling_Frame.scrollable_frame,  name=one_field['field_name'])

                # this_frame = Multi_Value_Frame(self.Database_Obj,
                #                                above_frame.Scrolling_Frame.scrollable_frame,  name=one_field['field_name'])
                this_frame.grid(row=0, column=0, sticky='news')
                

                temp = tk.Frame(self,  name=one_field['field_name'])

                # temp = Frame_For_Interface_Class(self.Database_Obj,
                #     self,  name=one_field['field_name'])

                MyLabel(font_size, temp, text=one_field['field_label']).grid(
                    row=0, column=1, columnspan=2)


                these_fields = self.Database_Obj.get_interface_records(
                    one_field['field_label'])
                # interface_info = self.Database_Obj.get_interface_info(
                #     one_field['field_label'])

                #temp.set_name_formula(interface_info['record_name_formula'])
                # self.multi_value_fields[name_of_field] = these_fields
                # self.multi_value_interface_info[name_of_field] = interface_info

                fields_to_show = [
                    x for x in these_fields if not x['field_name'] == 'parent_id']

                field_name = copy.deepcopy(one_field['field_name'])
                title_field = {}
                title_field['field_order']=-2
                title_field['field_label'] = one_field['field_label']
                title_field['field_type']='title'
                title_field['field_name'] = '*title'
                fields_to_show.append(title_field)

                title_field = {}
                title_field['field_order'] = -1
                title_field['field_type'] = 'MV_buttons'
                title_field['field_name'] = field_name
                fields_to_show.append(title_field)

                this_multi_interface_info = All_Interface_Info_Class(one_field['field_label'], self.Database_Obj.get_interface_info(
                    one_field['field_label']), fields_to_show )

                this_frame.Set_Interface(this_multi_interface_info)
                this_frame.Set_top_frame(self._name)

                this_frame.Build_These_Fields(font_size)
                this_frame.lower()
                #temp.Build_These_Fields(font_size)
                # self.Build_These_Fields(temp, font_size, [
                #                         x for x in these_fields if not x['linked_table'] == self.the_interface])
                
                # MyButton(font_size-8, temp, text='Add Values', command=lambda: self.Add_Value_Mutli_Value_Box(field_name)).grid(
                #     row=len(fields_to_show)+1, column=1, columnspan=2)
                MyButton(font_size-8, temp, text='Add Values', command=lambda: self.Lift_Frame(field_name)).grid(
                    row=len(fields_to_show)+1, column=1, columnspan=2)

                tk.Listbox(temp, name='list_box', font=font_return(font_size),
                           height=4, width=20).grid(row=len(fields_to_show)+2,  column=1, columnspan=2)


            else:
                temp = MyEntry(
                    font_size, self, validation_type=one_field['field_type'], width=15, name=one_field['field_name'])

            #self.the_fields.append(temp)
            one_widget = {}
            kwargs = {}
            kwargs['row'] = this_row
            one_widget['the_widget'] = temp
            kwargs['pady'] = 10

            if not one_field['field_type'] in fields_to_skip_in_interface:
                kwargs['column'] = 2
            else:
                kwargs['column'] = 1
                kwargs['columnspan'] = 2

            one_widget['kwargs'] = kwargs

            these_widgets.append(one_widget)
            this_row += 1

        for one_widget in these_widgets:
            one_widget['the_widget'].grid(one_widget['kwargs'])

    def Lower(self):
        self.lower()

    def Collect_Data_and_Lower(self):
        
        new_record = {}
        for one_field in self.interface_info.the_fields:
            if not one_field['field_type'] in fields_to_skip_in_interface:
                new_record[one_field['field_name']] = self.nametowidget(
                     one_field['field_name']).get()
                #self.nametowidget(one_field['field_name']).delete(0,tk.END)

        new_record['*record_name'] = get_name(new_record,
                                                  self.interface_info.interface_structure['record_name_formula'])
        new_record['*parent_record']=self.current_parent_record
        new_record['*current_record']=self.current_record

        self.the_records.append(new_record)

        #     this_frame.nametowidget(
        #         '*list_box').insert(tk.END, new_record['*record_name'])

        above_frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg').Scrolling_Frame.scrollable_frame.nametowidget(
            self.top_frame)



        above_frame.nametowidget(self._name).nametowidget(
            'list_box').insert(tk.END, new_record['*record_name'])

        self.clear_fields()

        self.Lower()

    def set_current_parent_record(self, current_parent_record):
        self.current_parent_record = current_parent_record

    def Lift_Frame(self, this_frame):

        above_frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg')
        this_frame = above_frame.Scrolling_Frame.scrollable_frame.nametowidget(
            this_frame)
        # we are increasing this by one each time the frame gets raised
        this_frame.current_record += 1
        #may not always have a record associated with it if they hit cancel

        #then we have to set the parent_record in the MV_fields to match the current record here
        for one_field in this_frame.interface_info.the_fields:
            if one_field['field_type'] == 'multi_linked_table':

                above_frame.Scrolling_Frame.scrollable_frame.nametowidget(
                    one_field['field_name']).set_current_parent_record(this_frame.current_record)

        above_frame.Scrolling_Frame.scrollable_frame.nametowidget(
                                           this_frame).tkraise()
        #self.tkraise()

    # def Add_Value_Mutli_Value_Box(self, frame_name):

    #     this_frame = self.nametowidget(frame_name)

    #     new_record = {}
    #     for one_field in this_frame.interface_info.the_fields:

    #         new_record[one_field['field_name']] = this_frame.nametowidget(
    #             one_field['field_name']).get()

    #     new_record['*record_name'] = get_name(new_record,
    #                                           this_frame.interface_info.interface_structure['record_name_formula'])

    #     this_frame.the_records.append(new_record)

    #     this_frame.nametowidget(
    #         '*list_box').insert(tk.END, new_record['*record_name'])


    def Save_Record(self, record_id=-1):
        #record_id=-1 means it is the main interface, not a multi_value field

        record_to_add = []

        for one_field in self.interface_info.the_fields:
            if not one_field['field_type'] in fields_to_skip_in_interface:
                one_field_record = {}
                one_field_record['type'] = one_field['field_type']
                one_field_record['field_name'] = one_field['field_name']
                one_field_record['value']  = self.get_one_field_value(
                    one_field_record['field_name'], one_field['field_type'])

                record_to_add.append(one_field_record)

        record_id = self.Database_Obj.add_record(
            self.interface_info.interface_structure['interface_table'], record_to_add)
        
        if record_id=='Error':
            messagebox.showerror('Error', "Error adding record")

        above_frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg')
        for one_field in self.interface_info.the_fields:
            if one_field['field_type']=='multi_linked_table':
              
                above_frame.Scrolling_Frame.scrollable_frame.nametowidget(
                    one_field['field_name']).Save_Record_Multi_Value(record_id, 0)
                #self.nametowidget(one_field['field_name']).Save_Record_Multi_Value(record_id)

        self.clear_fields()

    def clear_fields(self):

        for one_field in self.interface_info.the_fields:
            if one_field['field_type'] == 'linked_table':
                self.nametowidget(one_field['field_name']).clear_selection()
            elif one_field['field_type'] == 'multi_linked_table':
                
                self.nametowidget(one_field['field_name']).nametowidget(
                    'list_box').delete(0, tk.END)
            elif not one_field['field_type'] in ['MyLabel', 'MV_buttons', 'title']:
                self.nametowidget(one_field['field_name']).delete(0,tk.END)        
    
    def get_one_field_value(self, field_name, field_type):

        if field_type in ['text', 'string','phone']:
            return self.nametowidget(
                field_name).get()
        elif field_type == 'multi_linked_table':
            pass
        elif field_type == 'date':
            return datetime.strptime(self.nametowidget(
                field_name).get(), '%m\\%d\\%Y')
        elif field_type == 'integer':
            return  int(self.nametowidget(
                field_name).get())
        elif field_type == 'double':
            return float(self.nametowidget(
                field_name).get())
        elif field_type == 'linked_table':
            return self.nametowidget(
                field_name).get_selected_ID()
        elif field_type == 'bool':
            return self.Checkbox_var[field_name].get(
            )

        return None

    def Save_Record_Multi_Value(self, parent_id, parent_record=0):

        # interface_info = self.Database_Obj.get_interface_info(
        #     self.interface_name)

        
        for one_record in self.the_records:
            if one_record['*parent_record']==parent_record:
                one_record_to_add = []
                
                for one_field in self.interface_info.the_fields:
                    one_value_to_add ={}
                    if not one_field['field_type'] in fields_to_skip_in_interface:
                        one_value_to_add['field_name']=one_field['field_name']
                        one_value_to_add['type'] = one_field['field_type']
                        one_value_to_add['value'] = one_record[one_field['field_name']]
                        one_record_to_add.append(one_value_to_add)

                one_value_to_add ={}        
                one_value_to_add['field_name']='parent_id'
                one_value_to_add['type']='integer'
                one_value_to_add['value']=parent_id
                one_record_to_add.append(one_value_to_add)

                record_id = self.Database_Obj.add_record(
                    self.interface_info.interface_structure['interface_table'], one_record_to_add)

                if record_id == 'Error':
                    messagebox.showerror('Error', "Error adding record")
                    return

                above_frame = self.winfo_toplevel().nametowidget('interface_one_record_dlg')
                for one_field in self.interface_info.the_fields:
                    if one_field['field_type'] == 'multi_linked_table':

                        above_frame.Scrolling_Frame.scrollable_frame.nametowidget(
                            one_field['field_name']).Save_Record_Multi_Value(record_id, one_record['*current_record'])
                

class Multi_Value_Frame(tk.Frame):

    def __init__(self, Database_Obj, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.Database_Obj = Database_Obj
        self.interface_info = None

        tk.Label(self, name='title', text = '').grid(row=1, column=1)

    def Set_Interface(self, this_interface):

        self.interface_info = this_interface


        self.nametowidget('title')['text']=self.interface_info.interface_name
