from tkinter import font as tkfont
import os
from PIL import Image, ImageTk

field_types = [
    "string",
    "text",
    "integer",
    "double",
    "date",
    "bool",
    "linked_table",
    "multi_linked_table",
]
field_types_with_linked_table = ['linked_table', 'multi_linked_table']
field_types_without_linked_table = [
    x for x in field_types if x not in field_types_with_linked_table]
    
def font_return(this_size):
    return tkfont.Font(family="Arial", size=this_size)

days_in_month = {
    '01':31,
    '02':29,
    '03':31,
    '04':30,
    '05':31,
    '06':30,
    '07':31,
    '08':31,
    '09':30,
    '10':31,
    '11':30,
    '12': 31,
}


#this is for loading all images
class Image_Class():

    def __init__(self, location):

        self.load_icons()

    def load_icons(self):
        img = Image.open('Image_Files\\double_up.png')
        self.double_up = ImageTk.PhotoImage(img)

        img = Image.open('Image_Files\\up.png')
        self.up = ImageTk.PhotoImage(img)

        img = Image.open('Image_Files\\down.png')
        self.down = ImageTk.PhotoImage(img)

        img = Image.open('Image_Files\\double_down.png')
        self.double_down = ImageTk.PhotoImage(img)

def dict1_in_dict2(dict1, dict2):

    keys = list(dict1.keys())
    for one_key in keys:

        if not one_key in dict2:
            return False
        elif not dict1[one_key] == dict2[one_key]:
            return False
    return True