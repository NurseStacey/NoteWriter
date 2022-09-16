import datetime
import tkinter as tk
import tkinter.ttk as ttk
from universal_components import *
from tkinter import simpledialog
import dataclasses
from universal_components import *
from tkinter import messagebox
from tkinter import ttk

# class ListScrollCombo(tk.Frame):
#     def __init__(self, show_forward_backward_buttons, this_height, this_width, this_font, *args, **kwargs):

#         super().__init__(*args, **kwargs)
#     # ensure a consistent GUI size
#         self.grid_propagate(False)
#     # implement stretchability
#         # self.grid_rowconfigure(0, weight=1)
#         # self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(5, weight=1)
#         self.grid_columnconfigure(4, weight=1)

#         if show_forward_backward_buttons:
#             tk.Button(self, text='Backward ' + str(this_height), height=int(this_height/4), font=this_font,
#                       command=lambda: self.jump(-1)).grid(row=2, column=1, sticky='n')

#             tk.Button(self, text='Forward ' + str(this_height), height=int(this_height/4), font=this_font,
#                       command=lambda: self.jump(1)).grid(row=3, column=1, sticky='n')

#     # create a list widget
#         self.listbox = tk.Listbox(self, takefocus=False, name='list_box',
#                                   width=this_width, font=this_font, height=this_height, exportselection=0)
#         self.listbox.grid(row=1, column=2, rowspan=3,sticky="ne")

#     # create a Scrollbar and associate it with txt
#         scrollb = ttk.Scrollbar(self,  takefocus=False,
#                                 command=self.listbox.yview)
#         scrollb.grid(row=1, column=3, rowspan=3, sticky='ns')
#         self.listbox['yscrollcommand'] = scrollb.set

#         self.config(width=(self.listbox.winfo_reqwidth()+scrollb.winfo_reqwidth()), height=(self.listbox.winfo_reqheight()+scrollb.winfo_reqheight()))

#     def do_nothing(self, event):
#         return True

#     def list_box_bind(self, function):
#         self.listbox.bind('<Double-1>', function)

#     def jump(self, direction):
#         self.listbox.yview_scroll(direction, "pages")

#     def get_listbox(self):
#         return self.nametowidget('list_box')
    
#     def remove_item(self, text):

#         ID = self.listbox.get(0, tk.END).index(text)
#         self.listbox.delete(ID)
        
#     def listboxclicked(self, event):
#         pass

#     def add_item(self, thistext):
#         self.listbox.insert(tk.END, thistext)

#     def get_item(self, which):
#         return self.listbox.get(which)

#     def get_selected_text(self):

#         return_value = []

#         this_array = self.getselections()

#         for index in this_array:
#             return_value.append(self.get_item(index))

#         return return_value


#     def getselections(self):
#         return self.listbox.curselection()

#     def set_selection(self, index):
#         self.listbox.selection_set(index)

#     def set_selected_items(self, item_list):

#         for index in range(self.listbox.size()):
#             if self.get_item(index) in item_list:
#                 self.listbox.selection_set(index)

#     def set_selection_mode(self, which):
#         self.listbox.config(selectmode=which)

#     def clear_listbox(self):
#         self.listbox.delete(0, tk.END)

#     def selection_clear(self):
#         self.listbox.selection_clear(0, tk.END)

#     def get_all_items(self):
#         all_items = []
#         for index in range(self.listbox.size()):
#             all_items.append(self.listbox.get(index))

#         return all_items

#     def set_state(self, this_state):
#         self.listbox.configure(state=this_state)

#     def order_items(self):

#         all_items = self.get_all_items()

#         all_items.sort()
#         self.clear_listbox()

#         for this_item in all_items:
#             self.add_item(this_item)

class TextScrollCombo(tk.Frame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    # ensure a consistent GUI size
        self.grid_propagate(False)
    # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = tk.Text(self, wrap=tk.WORD)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

        self.the_state = tk.NORMAL

    def set_font(self, font_size):
        self.txt.config(font=font_return(font_size))

    def get(self):
        # I seem to always get an extra '\n' this is how I'm correcting this
        temp=self.txt.get("1.0", tk.END)
        return temp[:len(temp)-1]

    def gettextaslines(self):
        return self.txt.get('1.0',tk.END).splitlines()

    def cleartext(self):

        if not(self.the_state==tk.NORMAL):
            self.setstate(tk.NORMAL)

        self.txt.delete(1.0, tk.END)

        self.setstate(self.the_state)

    def settext(self, thistext):
        self.cleartext()
        self.txt.insert(tk.END, thistext)

    def setstate(self, newstate):
        self.txt.config(state=newstate)
        self.the_state = newstate

    def appendtext(self, thistext):
        self.txt.insert(tk.END, thistext + "\n")

# making a list box with tkinter base class to store location  information
class My_List_Box(tk.Listbox):
    def __init__(self, this_row, this_column, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.this_row = this_row
        self.this_column = this_column

class MyMultiListBox(tk.Frame):
    def __init__(self, fields, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.image_object = Image_Class(os.getcwd())
        

        self.fields = fields

        self.number_columns = len(fields)
        self.list_boxes = []
        self.header_labels = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text=' ').grid(row=1, column=2)
        tk.Button(self, image=self.image_object.double_up, command=lambda: self.shift(
            'double_up')).grid(row=2, column=2, sticky='n')

        tk.Button(self, image=self.image_object.up, command=lambda: self.shift(
            'up')).grid(row=3, column=2, sticky='n')

        tk.Button(self, image=self.image_object.down, command=lambda: self.shift(
            'down')).grid(row=4, column=2, sticky='s')

        tk.Button(self, image=self.image_object.double_down, command=lambda: self.shift(
            'double_down')).grid(row=5, column=2, sticky='s')

        self.listboxframe = tk.Frame(self)
        self.listboxframe.grid_rowconfigure(0, weight=1)
        self.listboxframe.grid_columnconfigure(0, weight=1)
        self.listboxframe.grid(row=1, column=1, rowspan=5)

        self.the_scrollbar = tk.Scrollbar(self.listboxframe)
        self.the_scrollbar.config(command=self.yview)


        this_row = 0
        this_column = 1
        for one_field in fields:
            temp = tk.Label(self.listboxframe, anchor='w', takefocus=False, text=one_field.capitalize(
            ), name=one_field.lower() + 'label')
            temp.grid(row=this_row, column=this_column, sticky='news')
            self.header_labels.append(temp)

            temp = My_List_Box(this_row+1, this_column, self.listboxframe, takefocus=False,
                               name=one_field.lower(), selectmode=tk.SINGLE, exportselection=False, yscrollcommand=self.listboxscroll)  # need to add a command for scrolling)
            temp.config(yscrollcommand=self.listboxscroll)
            temp.bind('<<ListboxSelect>>', self.listboxclicked)
            
            temp.grid(row=this_row+1, column=this_column, sticky='news')

            self.list_boxes.append(temp)
            this_column+=1

        this_row = this_row + 1

        self.the_scrollbar.grid(row=this_row, column=self.number_columns+2, sticky='ns')

        this_row = this_row + 1
        self.listboxframe.grid_rowconfigure(this_row, weight=1)
        self.listboxframe.grid_columnconfigure(self.number_columns+3, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.single_click=None

        self.the_data = []
        self.last_selection = 0

    #this is for changing position of an element
    def shift(self, which):

        selection = self.list_boxes[0].curselection()
        if len(selection)==0:
            return

        selection = selection[0]

        number_of_items = self.list_boxes[0].size()

        if (which=='up' or which=='double_up') and selection==0:
            return

        if (which=='down' or which=='double_down') and selection==(number_of_items-1):
            return

        record_to_swap = 0
        if which=='up':
            record_to_swap=  selection - 1
        if which=='down':
            record_to_swap=  selection + 1
        if which=='double_down':
            record_to_swap=  number_of_items - 1

        first_data_item = next(x for x in self.the_data if x['field_order']==selection)
        second_data_item = next(x for x in self.the_data if x['field_order'] == record_to_swap)

        first_data_item['field_order']=record_to_swap
        second_data_item['field_order']=selection

        item_one = []
        item_two = []

        for one_list_box in self.list_boxes:
            item_one.append(one_list_box.get(selection))
            item_two.append(one_list_box.get(record_to_swap))

        for index, one_list_box in enumerate(self.list_boxes):
            one_list_box.delete(selection)
            if which=='up' or which=='down':
                one_list_box.insert(selection, item_two[index])
                one_list_box.delete(record_to_swap)
                
            one_list_box.insert(record_to_swap, item_one[index])

        self.set_selection_by_index(record_to_swap)

    def set_selection_by_index(self, index):

        for one_list_box in self.list_boxes:
            one_list_box.select_set(index)

    def set_state(self, the_state):
        self.last_selection = self.get_selection()

        for one_box in self.list_boxes:
            one_box.config(state=the_state)

    def set_single_click(self, function):
        self.single_click = function

    def set_double_click(self,function):
        for one_listbox in self.list_boxes:
            one_listbox.bind('<Double-Button-1>', function)

    def set_height(self, this_height):
        for one_list_box in self.list_boxes:
            one_list_box.config(height=this_height)

    def set_font_size(self, font_size):
        this_font = font_return(font_size)
        for one_list_box in self.list_boxes:
            one_list_box.config(font=this_font)

        for one_label in self.header_labels:
            one_label.config(font=this_font)

    def change_lable_text(self, labelname, newlabletext):
        this_label = self.listboxframe.nametowidget(labelname + 'label')

        this_label['text'] = newlabletext

    def listboxclicked(self, event=None):

        if len(event.widget.curselection())==0:
            return

        which = event.widget.curselection()[0]
        for temp in self.list_boxes:
            temp.select_clear(0, tk.END)
            temp.select_set(which)

        if not self.single_click==None:
            self.single_click()

    def hide_column(self, which):
        self.listboxframe.nametowidget(which).grid_remove()
        self.listboxframe.nametowidget(which + 'label').grid_remove()

    def set_width(self, which, this_width):
        this_listbox = self.listboxframe.nametowidget(which)
        this_button = self.listboxframe.nametowidget(which+'label')
        this_listbox.grid(row=this_listbox.this_row, column=this_listbox.this_column)
        this_listbox.configure(width=this_width)

        this_button.grid(row=this_listbox.this_row-1, column=this_listbox.this_column)
        this_button.configure(width=this_width)

    def listboxscroll(self, *args):
        for temp in self.list_boxes:
            temp.yview_moveto(args[0])

        self.the_scrollbar.set(*args)

    def yview(self, *args):
        for temp in self.list_boxes:
            temp.yview(*args)

    def scrolljump(self, direction):

        for this_listbox in self.list_boxes:
            this_listbox.yview_scroll(direction, "pages")

    def numberitems(self):
        return self.list_boxes[0].size()

    def clear_list_boxes(self):
        for this_list_box in self.list_boxes:
            this_list_box.delete(0, tk.END)
        
        self.the_data = []
            
    def delete_one_item_from_box(self, which):
        for temp in self.list_boxes:
            temp.delete(which)

    def delete_one_item(self, which):

        self.delete_one_item_from_box(which)

        item_to_delete = next(x for x in self.the_data if x['field_order']==which)
        item_to_delete['field_order']=-1

        for one_data_item in self.the_data:
            if one_data_item['field_order'] > which:
                one_data_item['field_order'] -= 1

    def clear_all_selections(self):

        for this_list_box in self.list_boxes:
            this_list_box.selection_clear(0, tk.END)

    def get_item(self, which, index):
        temp = self.listboxframe.nametowidget(which)
        return temp.get(index)
    
    def value_in_list(self, which, value):
        return (value in self.listboxframe.nametowidget(which).get(0, tk.END))

    # def get_index(self, which, value):
    #     return self.listboxframe.nametowidget(which).index(0, tk.END)

    def get_one_value_in_list(self, which, record):
        return (self.listboxframe.nametowidget(which).index(record))

    def get_all_records(self):

        return self.the_data
        # return_value = []
        # for which in range(self.numberitems()):
        #     return_value.append(self.get_one_record(which))

        # return return_value

    def get_current_selection_this_column(self,which):
        which_item = self.list_boxes[0].curselection()[0]

        return (next(x[which] for x in self.the_data if x['field_order'] == which_item))

    def get_current_selection(self):

        which_item = self.list_boxes[0].curselection()[0]

        return next(x for x in self.the_data if x['field_order'] == which_item)
        # return_value = {}
        # field_names = []

        # for one_box in self.list_boxes:
        #     return_value[one_box._name] = one_box.get(
        #         one_box.curselection()[0])

        # return_value['order'] = self.list_boxes[0].curselection()[0]

        # return return_value

    def get_one_record(self, which):
        
        this_record = {}

        for one_box in self.list_boxes:
            field_name = one_box._name
            this_record[field_name] = one_box.get(which)


        this_record['field_order']=which
        return this_record

    def delete_one_record(self,which,value):
        index = self.listboxframe.nametowidget(which).get(0, tk.END).index(value)
        self.delete_one_item(index)


    def get_values_in_column(self, which):
        return self.listboxframe.nametowidget(which).get(0, tk.END)

    def get_current_selection_value(self, which):
        return next(
            x for x in self.the_data if x['field_order'] == self.get_selection())[which]


    def update_selected_record(self, record):
        item_to_be_updated = next(
            x for x in self.the_data if x['field_order'] == self.get_selection())

        for key in record:
            item_to_be_updated[key]=record[key]

        self.delete_one_item_from_box(item_to_be_updated['field_order'])
        self.insert_one_record_to_listboxes(
            item_to_be_updated, item_to_be_updated['field_order'])

    def insert_one_record_to_listboxes(self, record, where):
        
        for one_box in self.list_boxes:
            list_box_name = one_box._name

            if list_box_name in record:
                value = record[list_box_name]
                if isinstance(value, datetime.date):
                    text = value.strftime('%m/%d/%Y')
                    one_box.insert(where, text)
                elif isinstance(value, bool):
                    if value:
                        one_box.insert(where, 'Yes')
                    else:
                        one_box.insert(where, 'No')
                else:
                    one_box.insert(where, value)

    def add_one_record(self, record):

        one_data_item = {}
        position=self.numberitems()
        if 'field_order' in record:
            position=record['field_order']

        for key  in record:
            one_data_item[key]=record[key]

        one_data_item['field_order'] = position
        self.the_data.append(one_data_item)

        self.insert_one_record_to_listboxes(record, position)
        # for one_box in self.list_boxes:
        #     list_box_name = one_box._name
            
        #     if list_box_name in record:
        #         value = record[list_box_name]
        #         if isinstance(value, datetime.date):
        #             text = value.strftime('%m/%d/%Y')
        #             one_box.insert(position, text)
        #         elif isinstance(value, bool):
        #             if value:
        #                 one_box.insert(position, 'Yes')
        #             else:
        #                 one_box.insert(position, 'No')
        #         else:
        #             one_box.insert(position, value)

    def get_selection(self):
        return self.list_boxes[0].curselection()[0]

    def get_current_selection_which(self, which):
        return self.listboxframe.nametowidget(which).get(self.listboxframe.nametowidget(which).curselection()[0])

    #this moves the actual list boxes
    def change_position(self, which, whereto):
        swap = ""

        for temp in self.list_boxes:
            if temp.grid_info()['column'] == whereto:
                swap = temp.winfo_name()


        if swap == "":
            return

        this_row = self.listboxframe.nametowidget(which).grid_info()['row']
        fromwhere =  self.listboxframe.nametowidget(which).grid_info()['column']

        self.listboxframe.nametowidget(which).grid(row=this_row, column=whereto)
        self.listboxframe.nametowidget(swap).grid(row=this_row, column=fromwhere)
        self.listboxframe.nametowidget(which + 'button').grid(row=this_row-1, column=whereto)
        self.listboxframe.nametowidget(swap + 'button').grid(row=this_row-1, column=fromwhere)



class MyButton(tk.Button):
    def __init__(self, font_size,  *args, **kwargs):

        kwargs['font'] = font_return(font_size)

        super().__init__(*args, **kwargs)  
            
class MyLabel(tk.Label):
    def __init__(self, font_size,  *args, **kwargs):

        kwargs['font'] = font_return(font_size)

        super().__init__(*args, **kwargs)  

class MyEntry(tk.Frame):    
    def __init__(self, font_size, *args, **kwargs):
        
        validate_type='key'
        validation_field_function=self.do_nothing
        this_is_date = False
        this_is_phone = False
        
        if 'validation_type' in kwargs:
            if kwargs['validation_type'] == 'DB_string':
                validation_field_function = self.MySQL_Field_Name
                
            elif kwargs['validation_type'] == 'digit_only':
                validation_field_function = self.only_numbers  
      
            elif kwargs['validation_type'] == 'integer':
                validate_type='focusout'
                validation_field_function = self.only_integer  
            elif kwargs['validation_type'] == 'double':
                validate_type='focusout'
                validation_field_function = self.only_double  
            elif kwargs['validation_type'] == 'phone':                
                this_is_phone = True
                validation_field_function = self.valid_phone
                validate_type = 'focusout'                    
            elif kwargs['validation_type'] == 'date':                
                this_is_date = True
                validation_field_function = self.valid_date
                validate_type = 'focusout'
            del kwargs['validation_type']

        super().__init__(*args, **kwargs)

        validation_field = self.register(validation_field_function)
        kwargs['validate'] = validate_type
        kwargs['font'] = font_return(font_size)

        if validate_type in ['all','focusout']:
            kwargs['validatecommand']=(validation_field,'%P')
        else:
            kwargs['validatecommand']=(validation_field,'%S')

        self.Entry_Box = tk.Entry(self, **kwargs)

        self.Entry_Box.grid(row=0, column=0)

        if this_is_date:
            self.Entry_Box.bind('<KeyRelease>', self.only_date) 
            self.date_is_valid = False
        elif this_is_phone:
            self.Entry_Box.bind('<KeyRelease>', self.only_phone)
            self.phone_is_valid = False

        self.allowed_charactors = [chr(i+ord('a')) for i in range(26)] +\
            ['_'] +\
            [chr(i+ord('0')) for i in range(10)]


    def valid_phone(self, text):
        if self.phone_is_valid or text=='':
            return True
        else:
            messagebox.showerror('error', 'That is not a valid date. Either clear the box or fix the date.')
            return False

    def valid_date(self, text):

        if self.date_is_valid or text=='':
            return True
        else:
            messagebox.showerror('error', 'That is not a valid date. Either clear the box or fix the date.')
            return False

    def only_phone(self, event):

        if event.keycode==8:
            return

        self.phone_is_valid = False
        text=self.Entry_Box.get()
        if not event.char.isdigit():
            text = text[0:len(text)-1]
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)

        if len(text)==1:
            text = '(' + text
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)
            return
        
        if len(text)==4:
            text = text + ') '
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)
            return
        
        if len(text)==9:
            text = text + '-'
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)
            return

        if len(text)==14:
            self.phone_is_valid = True

        if len(text)==15:
            text = text[0:len(text)-1]
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)
            self.phone_is_valid = True
            return


    def only_date(self, event):

        if event.keycode==8:
            return

        text=self.Entry_Box.get()
        #nothing here
        if text == '':
            self.date_is_valid = True
            return

        self.date_is_valid = False

        last_char = text[len(text)-1:]
        if not last_char.isdigit():
            text=text[0:len(text)-1]
            self.Entry_Box.delete(0,tk.END)
            self.Entry_Box.insert(0,text)
            return

        if len(text)==3:
            pass
        #month
        if len(text)<3:
            if len(text)==1 and not text in ['0','1']:
                self.Entry_Box.delete(0, tk.END)
                text= '0' + text + '\\'
                self.Entry_Box.insert(0,text)
                
            elif len(text)==2:
                if text[0]=='0' and not text[1]=='0':
                    self.Entry_Box.delete(0, tk.END)
                    text=text + '\\'
                    self.Entry_Box.insert(0, text)
                  
                elif text[0]=='1' and text[1] in ['0','1','2']:
                    self.Entry_Box.delete(0, tk.END)
                    text = text + '\\'
                    self.Entry_Box.insert(0, text)
                    
                else:
                    text=text[0:len(text)-1]
                    self.Entry_Box.delete(0,tk.END)
                    self.Entry_Box.insert(0,text)
            return


        #day
        if len(text)<6:
            month = text[0:2]
            allowed_first_digits = ['0','1','2']
            if not month=='02':
                allowed_first_digits += ['3']

            if len(text) == 4 and not text[3] in allowed_first_digits:
                self.Entry_Box.delete(0, tk.END)
                day = text[3]
                text = text[0:3] + '0' + day + '\\'
                self.Entry_Box.insert(0, text)
                
            elif len(text)==5:
                day = int(text[3:5])
                month = text[0:2]
                if not(day > days_in_month[month]):
                    self.Entry_Box.delete(0, tk.END)
                    text = text + '\\'
                    self.Entry_Box.insert(0, text)
                else:
                    text=text[0:len(text)-1]
                    self.Entry_Box.delete(0,tk.END)
                    self.Entry_Box.insert(0,text)                    
                
            return

        #year
        if len(text)==8:
            year = text[6:]
            if year in ['19', '20']:
                return
            century='19'
            if int(year)<19:
                century='20'

            text = text[0:6] + century + year
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)
            self.date_is_valid = True

        #check year is valid - leap days
        if len(text)==10:
            month=text[:2]
            day = text[3:5]
            year = text[6:10]

            if int(month)==2 and int(day)==29:
                if not(int(year)%4==0 and not int(year)==2000):
                    messagebox.showerror('error', 'That is not a valid date.')
                    self.date_is_valid = False
                    return

            self.date_is_valid = True


        if len(text)>10:
            text = text[0:10]
            self.Entry_Box.delete(0, tk.END)
            self.Entry_Box.insert(0, text)
            self.date_is_valid = True


    def only_double(self, text):

        try:
            float(text)
        except ValueError:
            messagebox.showerror('Error', 'Must be numberic value')
            # self.Entry_Box.focus() do I need this?
            return False
        
        return True

    def only_integer(self, text):
        
        if text=='':
            return True

        try:
            int(text)
        except ValueError:
            messagebox.showerror('Error', 'Must be an integer value')
            # self.Entry_Box.focus() do I need this?
            return False

        return True

    def get(self):

        return self.Entry_Box.get() 
    
    def delete(self, *args):

        self.Entry_Box.delete(*args)
    
    def set_state(self, this_state):
        self.Entry_Box.config(state=this_state)

    def insert(self, *args):

        self.Entry_Box.insert(*args)

    def only_numbers(self, char):
        return char.isdigit()

    def MySQL_Field_Name(self, char):
            #doesn't seem like the right work around
        return (char in self.allowed_charactors or len(char)>1) 

    def do_nothing(self, char):
        return True

class MyFrame(tk.Frame):
    def __init__(self, Database_Obj, *args, **kwargs):
        title_text = ''
        if 'title_text' in kwargs:
            title_text = kwargs['title_text']
            del kwargs['title_text']

        font_size=36
        if 'font_size' in kwargs:
            font_size = kwargs['font_size']
            del kwargs['font_size']

        self.Database_Obj = Database_Obj
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)       
    
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0, column=1, pady=10, sticky='news')
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_columnconfigure(2, weight=1)
        MyLabel(font_size, self.title_frame, name='title',
                text=title_text).grid(row=0, column=1)

        self.input_frame = tk.Frame(
            self)
        self.input_frame.grid(row=1, column=1, pady=30, sticky='news')
        self.input_frame.grid_columnconfigure(0, weight=1)
        

        self.button_frame = tk.Frame(
            self)
#, highlightbackground="blue", highlightthickness=2
        self.button_frame.grid(row=3, column=1, pady=10, sticky='news')
        self.button_frame.grid_columnconfigure(0, weight=1)

    def set_title(self, title):

        self.title_frame.nametowidget('title').config(text=title)
        
    def set_input_frame_columns(self, num_columns):
        self.input_frame.grid_columnconfigure(num_columns+1, weight=1)

    def set_button_frame_columns(self, num_columns):
        self.button_frame.grid_columnconfigure(num_columns+1, weight=1)

    def raise_frame(self, which_frame):
        self.winfo_toplevel().nametowidget(which_frame).tkraise()

    def Cancel(self):
        self.lower()


class MyCheckBox(tk.Checkbutton):
    def __init__(self,  *args, **kwargs):

        super().__init__(*args, **kwargs)

    def set_state(self, this_state):
        self.config(state=this_state)

class FunctionOnSelect():
    def __init__(self, values, function_call):
        self.function_call = function_call
        self.values = values

class ListScrollCombo(tk.Frame):
    def __init__(self, this_height, this_width, this_font, selection_made, *args, **kwargs):


        super().__init__(*args, **kwargs)

        self.listbox = tk.Listbox(self, name='list_box', selectmode='single',
                                  width=this_width, font=this_font, height=this_height, exportselection=0)

        self.listbox.bind('<KeyRelease>', self.key_pressed)
        self.listbox.bind('<ButtonRelease-1>', self.selection_made)
        if not selection_made == None:
            self.listbox.bind('<FocusOut>', selection_made)

        self.listbox.grid(row=1, column=1, sticky="ne")

    # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.listbox.yview)
        scrollb.grid(row=1, column=2, sticky='ns')
        self.listbox['yscrollcommand'] = scrollb.set
        
        self.list_box_items = []
        self.the_text=''
        self.current_selection = 0
        self.listbox.selection_set(0)
        self.function_on_select = []

    def get_all_elements(self):
        return self.listbox.get(0, tk.END)
        
    def set_function_on_select(self, values, function):
        self.function_on_select.append(FunctionOnSelect(values, function))

    def set_double_click(self, function):
        self.listbox.bind('<Double-Button-1>', function)

    def add_item_list(self, item_list):
        self.clear_listbox()
        self.list_box_items = []

        for one_item in item_list:
            #self.list_box_items.append(one_item.lower())
            self.list_box_items.append(one_item)
            self.listbox.insert(tk.END, one_item)

    def get_all_selected_texts(self):
        selections = self.listbox.curselection()
        return_value = []

        for one_selection in selections:
            return_value.append(self.listbox.get(one_selection))

        return return_value

    def get_selected_text(self):

        selections = self.listbox.curselection()
        if len(selections)==0:
            return self.listbox.get(0)

        return self.listbox.get(selections[0])

    def selection_made(self, e=None):

        for one_select_function in self.function_on_select:
            if self.get_selected_text() in one_select_function.values:
                one_select_function.function_call()
                
    def update_displayed_list(self):

        self.listbox.delete(0, tk.END)
        for x in self.list_box_items:
            if x[:len(self.the_text)].lower() == self.the_text:
                self.listbox.insert(tk.END,  x)
        
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(0)
        self.selection_made()


    def set_selection_mode(self, which):
        self.listbox.config(selectmode=which)

    def reset(self):
        self.the_text=''
        self.update_displayed_list()

    def key_pressed(self, e):

        if e.keycode == 9:
            return

        if len(self.listbox.curselection())==0:
            current_selection=0
        else:
            current_selection = self.listbox.curselection()[0]

        if e.keycode == 40 and current_selection < self.listbox.size():
            current_selection += 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(current_selection)
            return

        if e.keycode == 38 and current_selection > 0:
            current_selection -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(current_selection)
            return

        if e.char.isalpha():
            self.the_text += e.char
        elif e.keycode==8:
            self.the_text = ''

        self.update_displayed_list()

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)
        self.list_box_items = []

    def remove_item(self, text):

        if self.listbox.get(0, tk.END)==():
            return

        try:
            ID = self.listbox.get(0, tk.END).index(text)
        except ValueError:
            return

        if ID<0:
            return
            
        self.listbox.delete(ID)
        self.list_box_items.remove(text)
        
    def set_state(self, this_state):
        self.listbox.configure(state=this_state)

    def set_selection(self, which):
        self.listbox.selection_clear(0, tk.END)
        new_selection= self.listbox.get(0,tk.END).index(which)
        self.listbox.selection_set(new_selection)

class ListScrollWithRecordID(ListScrollCombo):
    def __init__(self, this_height, this_width, this_font, selection_made, *args, **kwargs):

        super().__init__(this_height, this_width, this_font, selection_made, *args, **kwargs)

    def add_item_list(self, item_list):
        self.clear_listbox()
        self.list_box_items = []

        for one_item in item_list:
            #self.list_box_items.append(one_item.lower())
            self.list_box_items.append(one_item)
            self.listbox.insert(tk.END, one_item['Name'])

    def remove_item(self, item):
        ID = self.listbox.get(0, tk.END).index(item['Name'])
        self.listbox.delete(ID)
        self.list_box_items.remove(item)        

    def remove_all_items(self):
        self.list_box_items=[]
        self.listbox.delete(0, tk.END)
        
    def update_displayed_list(self):

        self.listbox.delete(0, tk.END)

        for x in self.list_box_items:
            if x['Name'][:len(self.the_text)].lower() == self.the_text.lower():
                self.listbox.insert(tk.END,  x['Name'])

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(0)

    def clear_selection(self):
        self.listbox.selection_clear(0, tk.END)
        
    def get_selected_ID(self):

        selections = self.listbox.curselection()
        if len(selections)==0:
            return self.listbox.get(0)

        return next(x['Record_ID'] for x in self.list_box_items if x['Name'] == self.listbox.get(selections[0]))

class ScrollingFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                       command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, name='base_frame')

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0), width=1500, window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set, height=450, width=500)

        self.canvas.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # for index in range(50):
        #     tk.Label(self.scrollable_frame, text='I want to be able to display a very very long line here. I want to be able to display a very very long line here. I want to be able to display a very very long line here').grid(
        #         row=index, column=1)            
        # this_file = open('fruit.txt', 'r')
        # the_fruit = []

        # for one_line in this_file.readlines():
        #     the_fruit.append(one_line.replace('\n', ''))

        # for index, one_fruit in enumerate(the_fruit):
        #     tk.Label(self.scrollable_frame, text=one_fruit).grid(
        #         row=index, column=1)

    def get_inner_frame(self):

        return self.scrollable_frame


# class MyDropDownBox(tk.Frame):
#     def __init__(self, font_size, function_on_leave, *args, **kwargs):
# #, highlightbackground="blue", highlightthickness=2

#         # kwargs['validatecommand'] = (self.register(self.leave_widget), '%P')
#         # kwargs['validate'] = 'focusout'

#         super().__init__(*args, **kwargs)


#         self.entry_box = tk.Entry(self, font=font_return(
#             font_size), width=20, validate='focusout', validatecommand=(self.register(self.leave_widget),'%P'))

#         self.entry_box.grid(row=0, column=0, sticky='W')
#         self.entry_box.bind('<KeyRelease>', self.key_pressed)
#         self.list_box = ListScrollCombo(False, 5, 18, font_return(
#             font_size), self)

#         self.list_box.grid(row=1,column=0)

#         self.list_box_items = []
#         self.list_box.list_box_bind(self.list_box_selected)
#         self.grid_rowconfigure(2,weight=1)

#         self.current_selection = -1
#         self.function_on_leave = function_on_leave

#     def add_item(self, item):
#         self.list_box_items.append(item.lower())
#         self.list_box.add_item(item)

#     def add_item_list(self, item_list):
#         for one_item in item_list:
#             self.list_box_items.append(one_item.lower())
#             self.list_box.add_item(one_item)

#     def list_box_selected(self,e):
#         new_text = self.list_box.get_selected_text()
#         self.entry_box.delete(0, tk.END)
#         self.entry_box.insert(0, new_text[0])
#         self.entry_box.focus_set()

#     def leave_widget(self, value):
#         self.entry_box.delete(0, tk.END)
#         self.entry_box.insert(0,self.get_selection())
#         if not self.function_on_leave==None:
#             self.function_on_leave()

#         return True

#     def set_state(self, this_state):
#         self.entry_box.config(state=this_state)
#         self.list_box.set_state(this_state)

#     def key_pressed(self, e):

#         current_text = self.entry_box.get().lower()

#         if e.keycode == 40:
#             self.current_selection += 1
#             self.list_box.selection_clear()
#             self.list_box.set_selection(self.current_selection)
#             return

#         if e.keycode == 38:
#             self.current_selection -= 1
#             self.list_box.selection_clear()
#             self.list_box.set_selection(self.current_selection)
#             return

#         self.add_list_box_items(current_text)

#     def clear_box(self):
#         self.entry_box.delete(0,tk.END)
#         self.add_list_box_items('')
#         self.list_box.selection_clear()

#     def add_list_box_items(self, text):
#         self.list_box.clear_listbox()
#         for x in self.list_box_items:
#             if x[:len(text)].lower() == text:
#                 self.list_box.add_item(x)

#         self.current_selection = 0
#         self.list_box.selection_clear()
#         self.list_box.set_selection(self.current_selection)

#     def get_selection(self):

#         if len(self.list_box.get_selected_text())==0:
#             return ''

#         return self.list_box.get_selected_text()[0]
