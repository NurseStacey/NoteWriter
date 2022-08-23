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