from tkinter import font as tkfont


field_types = [
    "string",
    "text",
    "integer",
    "double",
    "date",
    "bool",
    "linked_table"
]

def font_return(this_size):
    return tkfont.Font(family="Arial", size=this_size)

