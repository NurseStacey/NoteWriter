import datetime
import tkinter as tk
import tkinter.ttk as ttk
from universal_components import *
from tkinter import simpledialog
import dataclasses
from universal_components import *

class ListScrollCombo(tk.Frame):
    def __init__(self, show_forward_backward_buttons, this_height, this_width, this_font, *args, **kwargs):

        super().__init__(*args, **kwargs)
    # ensure a consistent GUI size
        self.grid_propagate(False)
    # implement stretchability
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(4, weight=1)

        if show_forward_backward_buttons:
            tk.Button(self, text='Backward ' + str(this_height), height=int(this_height/4), font=this_font,
                      command=lambda: self.jump(-1)).grid(row=2, column=1, sticky='n')

            tk.Button(self, text='Forward ' + str(this_height), height=int(this_height/4), font=this_font,
                      command=lambda: self.jump(1)).grid(row=3, column=1, sticky='n')

    # create a list widget
        self.listbox = tk.Listbox(self, takefocus=False, name='list_box',
                                  width=this_width, font=this_font, height=this_height, exportselection=0)
        self.listbox.grid(row=1, column=2, rowspan=3,sticky="ne")

    # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self,  takefocus=False,
                                command=self.listbox.yview)
        scrollb.grid(row=1, column=3, rowspan=3, sticky='ns')
        self.listbox['yscrollcommand'] = scrollb.set

        self.config(width=(self.listbox.winfo_reqwidth()+scrollb.winfo_reqwidth()), height=(self.listbox.winfo_reqheight()+scrollb.winfo_reqheight()))

    def do_nothing(self, event):
        return True

    def list_box_bind(self, function):
        self.listbox.bind('<Double-1>', function)

    def jump(self, direction):
        self.listbox.yview_scroll(direction, "pages")

    def get_listbox(self):
        return self.nametowidget('list_box')
    
    def remove_item(self, text):

        ID = self.listbox.get(0, tk.END).index(text)
        self.listbox.delete(ID)
        
    def listboxclicked(self, event):
        pass

    def add_item(self, thistext):
        self.listbox.insert(tk.END, thistext)

    def get_item(self, which):
        return self.listbox.get(which)

    def get_selected_text(self):

        return_value = []

        this_array = self.getselections()

        for index in this_array:
            return_value.append(self.get_item(index))

        return return_value


    def getselections(self):
        return self.listbox.curselection()

    def set_selection(self, index):
        self.listbox.selection_set(index)

    def set_selected_items(self, item_list):

        for index in range(self.listbox.size()):
            if self.get_item(index) in item_list:
                self.listbox.selection_set(index)

    def set_selection_mode(self, which):
        self.listbox.config(selectmode=which)

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)

    def selection_clear(self):
        self.listbox.selection_clear(0, tk.END)

    def get_all_items(self):
        all_items = []
        for index in range(self.listbox.size()):
            all_items.append(self.listbox.get(index))

        return all_items

    def set_state(self, this_state):
        self.listbox.configure(state=this_state)

    def order_items(self):

        all_items = self.get_all_items()

        all_items.sort()
        self.clear_listbox()

        for this_item in all_items:
            self.add_item(this_item)

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

    def gettext(self):
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
    def __init__(self, record_class, fields_to_include, include_forward_backward, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.record_class = record_class
        #temp = self.record_class()
        self.fields_to_include = fields_to_include
        headers = []

        #for attribute in  vars(temp):
        for attribute in vars(record_class)['__annotations__']:
            #if not (callable(getattr(temp, attribute))) and not attribute.startswith('__') and 
            if attribute in self.fields_to_include:
                headers.append(attribute)

        self.selection_mode_multi = False
        self.which_last_sort = ''
        self.direction_last_sort = -1

        self.number_columns = len(headers)
        self.list_boxes = []
        #self.list_box_grid_info = []
        self.header_button = []


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if(include_forward_backward):
            forward_button = tk.Button(self, text='Jump Forward', width=10, height=6,
                                    font=font_return(16), wraplength=90,
                                    command=lambda: self.scrolljump(1))
            forward_button.grid(row=2, column=2)
            spacer = tk.Label(self, text='')

            backward_button = tk.Button(self, text='Jump Backward', width=10, height=6,
                                    font=font_return(16), wraplength=90,
                                    command=lambda: self.scrolljump(-1))
            backward_button.grid(row=1, column=2)

        self.listboxframe = tk.Frame(self)
        self.listboxframe.grid_rowconfigure(0, weight=1)
        self.listboxframe.grid_columnconfigure(0, weight=1)
        self.listboxframe.grid(row=1, column=1, rowspan=2)

        self.the_scrollbar = tk.Scrollbar(self.listboxframe)
        self.the_scrollbar.config(command=self.yview)


        this_row = 0
        for x in range(self.number_columns):
            temp = tk.Button(self.listboxframe, anchor='w', takefocus=False, text=headers[x].capitalize(
            ), name=headers[x] + 'button', command=lambda y=headers[x]: self.sort(y))
            temp.grid(row=this_row, column=x+1, sticky='news')
            # temp.grid(row=this_row, column=x + 1)
            self.header_button.append(temp)
            temp = My_List_Box(this_row+1, x+1, self.listboxframe, takefocus=False,
                               name=headers[x], exportselection=False, yscrollcommand=self.listboxscroll)  # need to add a command for scrolling)
            temp.config(yscrollcommand=self.listboxscroll)
            temp.bind('<<ListboxSelect>>', self.listboxclicked)
            
            
            temp.grid(row=this_row+1, column=x+1, sticky='news')

            self.list_boxes.append(temp)

        this_row = this_row + 1

        self.the_scrollbar.grid(row=this_row, column=self.number_columns+2, sticky='ns')

        this_row = this_row + 1
        self.listboxframe.grid_rowconfigure(this_row, weight=1)
        self.listboxframe.grid_columnconfigure(self.number_columns+3, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.single_click=None

    def set_single_click(self, function):
        self.single_click = function

    def get_selection(self):

        return self.list_boxes[0].curselection()

    def set_state(self, the_state):
        for one_box in self.list_boxes:
            one_box.config(state=the_state)

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

        for one_button in self.header_button:
            one_button.config(font=this_font)

    def get_widget(self, which):
        return(self.listboxframe.nametowidget(which))

    def clear_list_boxes(self):
        for this_list_box in self.list_boxes:
            this_list_box.delete(0, tk.END)

    #this is to get only the first one selected
    def get_current_selection_first(self, which):
        return self.listboxframe.nametowidget(which).get(self.listboxframe.nametowidget(which).curselection()[0])

    def get_current_selection(self):
        return_value = []
        field_names = []

        for one_box in self.list_boxes:
            return_value.append(one_box.get(one_box.curselection()[0]))
            field_names.append(one_box._name)

        return dict(zip(field_names,return_value))

    def get_current_selection_all(self, which):
        selection_list = self.listboxframe.nametowidget(which).curselection()

        return_value = []
        for one_selection in selection_list:
            return_value.append(self.listboxframe.nametowidget(which).get(one_selection))

        return return_value

    def change_button_text(self, buttonname, newbuttontext):
        this_button = self.listboxframe.nametowidget(buttonname + 'button')

        this_button['text'] = newbuttontext

    def delete_one_item(self, which):

        for temp in self.list_boxes:
            temp.delete(which)

    def listboxclicked(self, event=None):

        if len(event.widget.curselection())==0:
            return

        which = event.widget.curselection()[0]
        for temp in self.list_boxes:
            temp.select_clear(0, tk.END)
            temp.select_set(which)

        if not self.single_click==None:
            self.single_click()

    #if you are to allow multiple lines to be selected
    def listboxclicked_multi(self, event=None):

        all_selections = event.widget.curselection()
        for temp in self.list_boxes:
            temp.select_clear(0, tk.END)
            for which in all_selections:
                temp.select_set(which)

    def hide_column(self, which):
        self.listboxframe.nametowidget(which).grid_remove()
        self.listboxframe.nametowidget(which + 'button').grid_remove()

    def set_width(self, which, this_width):
        this_listbox = self.listboxframe.nametowidget(which)
        this_button = self.listboxframe.nametowidget(which+'button')
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

    def get_item(self, which, index):
        temp = self.listboxframe.nametowidget(which)
        return temp.get(index)
    
    def value_in_list(self, which, value):
        return (value in self.listboxframe.nametowidget(which).get(0, tk.END))

    def get_index(self, which, value):
        return self.listboxframe.nametowidget(which).index(0, tk.END)

    def get_one_value_in_list(self, which, record):
        return (self.listboxframe.nametowidget(which).index(record))

    def get_all_records(self):

        return_value = []
        for which in range(self.numberitems()):
            return_value.append(self.get_one_record(which))

        return return_value
        
    def get_one_record(self, which):
        
        this_record = []
        for attribute in dataclasses.fields(self.record_class):
            this_record.append(
                self.listboxframe.nametowidget(attribute.name).get(which))

        return self.record_class(*this_record)

    def delete_one_record(self,which,value):
        index = self.listboxframe.nametowidget(which).get(0, tk.END).index(value)
        self.delete_one_item(index)

    def add_one_record(self, record):

        size = 0
        for attribute, value in vars(record).items():
            # if not (callable(getattr(record, attribute))) and not attribute.startswith('__'):
                try:
                    temp = self.listboxframe.nametowidget(attribute)

                    if isinstance(value, datetime.date):
                        text = value.strftime('%m/%d/%Y')
                        temp.insert(tk.END, text)
                    elif isinstance(value, bool):
                        if value:
                            temp.inser(tk.END,'Yes')
                        else:
                            temp.inser(tk.END,'No')
                    else:
                        temp.insert(tk.END, value)

                except KeyError:
                    pass

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

    def numberitems(self):
        return self.list_boxes[0].size()

    def sort(self, which):

        direction = 1
        if which == self.which_last_sort:
            direction = -1 * self.direction_last_sort
        else:
            self.which_last_sort = which

        self.direction_last_sort = direction

        this_list_box = self.listboxframe.nametowidget(which)

        number_of_items = self.numberitems()
        temporary_records = []

        #element_names=vars(self.record_class())

        for index in range(number_of_items):
            
            this_record = []
            for attribute in dataclasses.fields(self.record_class):
                this_record.append(
                    self.listboxframe.nametowidget(attribute.name).get(index))
            #for attribute in element_names:

             #   if not (callable(getattr(temp_record, attribute))) and not attribute.startswith('__') and attribute in self.fields_to_include:
#                    this_value = self.listboxframe.nametowidget(attribute).get(index)
#                    setattr(temp_record, attribute, this_value)

            temporary_records.append(self.record_class(*this_record))

        self.clear_list_boxes()

        def sort_function(one_record):
            nonlocal which
            return getattr(one_record, which)

        reverse_sort = not(self.direction_last_sort==1)

        temporary_records.sort(key=sort_function, reverse=reverse_sort)

        for one_record in temporary_records:
            self.add_one_record(one_record)



    def set_selection_mode(self, which):

        if which == tk.MULTIPLE:
            self.selection_mode_multi = True
            for one_list_box in self.list_boxes:
                one_list_box.config(selectmode=which)
                one_list_box.bind('<<ListboxSelect>>', self.listboxclicked_multi)
        else:
            for one_list_box in self.list_boxes:
                one_list_box.config(selectmode=which)

    def clear_all_selections(self):

        for this_list_box in self.list_boxes:
            this_list_box.selection_clear(0, tk.END)

class MyButton(tk.Button):
    def __init__(self, font_size,  *args, **kwargs):

        kwargs['font'] = font_return(font_size)

        super().__init__(*args, **kwargs)  
            
class MyLabel(tk.Label):
    def __init__(self, font_size,  *args, **kwargs):

        kwargs['font'] = font_return(font_size)

        super().__init__(*args, **kwargs)  

#class MyEntry(tk.Entry):
class MyEntry(tk.Frame):    
    def __init__(self, font_size, *args, **kwargs):

        validation_field_function=self.do_nothing
        if 'validation_type' in kwargs:
            if kwargs['validation_type'] == 'DB_string':
                validation_field_function = self.MySQL_Field_Name
                
            elif kwargs['validation_type'] == 'digit_only':
                validation_field_function = self.only_numbers           
            del kwargs['validation_type']

       

        super().__init__(*args, **kwargs)

        validation_field = self.register(validation_field_function)
        kwargs['validate']='key'
        kwargs['font'] = font_return(font_size)
        kwargs['validatecommand']=(validation_field,'%S')

        self.Entry_Box = tk.Entry(self, **kwargs)
        self.Entry_Box.grid(row=0, column=0)

        
        self.allowed_charactors = [chr(i+ord('a')) for i in range(26)] +\
            [chr(i+ord('A')) for i in range(26)] +\
                ['_'] +\
            [chr(i+ord('0')) for i in range(10)]

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

        self.Database_Obj = Database_Obj
        super().__init__(*args, **kwargs)


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)       
    
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0, column=1, pady=10, sticky='news')
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_columnconfigure(2, weight=1)
        MyLabel(36, self.title_frame, name='title',
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

class MyDropDownBox(tk.Frame):
    def __init__(self, font_size, function_on_leave, *args, **kwargs):
#, highlightbackground="blue", highlightthickness=2

        # kwargs['validatecommand'] = (self.register(self.leave_widget), '%P')
        # kwargs['validate'] = 'focusout'

        super().__init__(*args, **kwargs)


        self.entry_box = tk.Entry(self, font=font_return(
            font_size), width=20, validate='focusout', validatecommand=(self.register(self.leave_widget),'%P'))

        self.entry_box.grid(row=0, column=0, sticky='W')
        self.entry_box.bind('<KeyRelease>', self.key_pressed)
        self.list_box = ListScrollCombo(False, 5, 18, font_return(
            font_size), self)

        self.list_box.grid(row=1,column=0)

        self.list_box_items = []
        self.list_box.list_box_bind(self.list_box_selected)
        self.grid_rowconfigure(2,weight=1)

        self.current_selection = -1
        self.function_on_leave = function_on_leave

    def add_item(self, item):
        self.list_box_items.append(item.lower())
        self.list_box.add_item(item)

    def add_item_list(self, item_list):
        for one_item in item_list:
            self.list_box_items.append(one_item.lower())
            self.list_box.add_item(one_item)

    def list_box_selected(self,e):
        new_text = self.list_box.get_selected_text()
        self.entry_box.delete(0, tk.END)
        self.entry_box.insert(0, new_text[0])
        self.entry_box.focus_set()

    def leave_widget(self, value):
        self.entry_box.delete(0, tk.END)
        self.entry_box.insert(0,self.get_selection())   
        if not self.function_on_leave==None:
            self.function_on_leave()

        return True  

    def set_state(self, this_state):
        self.entry_box.config(state=this_state)
        self.list_box.set_state(this_state)

    def key_pressed(self, e):
        
        current_text = self.entry_box.get().lower()

        if e.keycode == 40:
            self.current_selection += 1
            self.list_box.selection_clear()
            self.list_box.set_selection(self.current_selection)
            return
        
        if e.keycode == 38:
            self.current_selection -= 1
            self.list_box.selection_clear()
            self.list_box.set_selection(self.current_selection)
            return
            
        self.add_list_box_items(current_text)

    def clear_box(self):
        self.entry_box.delete(0,tk.END)
        self.add_list_box_items('')
        self.list_box.selection_clear()

    def add_list_box_items(self, text):
        self.list_box.clear_listbox()
        for x in self.list_box_items:
            if x[:len(text)].lower() == text:
                self.list_box.add_item(x)

        self.current_selection = 0
        self.list_box.selection_clear()
        self.list_box.set_selection(self.current_selection)

    def get_selection(self):

        if len(self.list_box.get_selected_text())==0:
            return ''

        return self.list_box.get_selected_text()[0]

class MyCheckBox(tk.Checkbutton):
    def __init__(self,  *args, **kwargs):

        super().__init__(*args, **kwargs)


class ListScrollComboTwo(tk.Frame):
    def __init__(self, this_height, this_width, this_font, selection_made, *args, **kwargs):


        super().__init__(*args, **kwargs)

        self.listbox = tk.Listbox(self, name='list_box', selectmode='single',
                                  width=this_width, font=this_font, height=this_height, exportselection=0)

        self.listbox.bind('<KeyRelease>', self.key_pressed)

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

    def add_item_list(self, item_list):
        self.clear_listbox()
        self.list_box_items = []

        for one_item in item_list:
            self.list_box_items.append(one_item.lower())
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

    def update_displayed_list(self):

        self.listbox.delete(0, tk.END)
        for x in self.list_box_items:
            if x[:len(self.the_text)].lower() == self.the_text:
                self.listbox.insert(tk.END,  x)

        
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(0)

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
            self.the_text = self.the_text[:max(0,len(self.the_text)-1)]

        self.update_displayed_list()

    def clear_listbox(self):
        self.listbox.delete(0, tk.END)

    def remove_item(self, text):

        ID = self.listbox.get(0, tk.END).index(text)
        self.listbox.delete(ID)
        
    def set_state(self, this_state):
        self.listbox.configure(state=this_state)

    def set_selection(self, which):
        self.listbox.selection_clear(0, tk.END)
        new_selection= self.listbox.get(0,tk.END).index(which)
        self.listbox.selection_set(new_selection)
