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


#this is for loading all images
class Image_Class():

    def __init__(self, location):

        self.load_icons()
        # self.location = location + '\\exercises\\'
        # self.the_exercises = []

        # self.build_array()

    # def is_a_png_file(self, file):

    #     if not(os.path.isfile(self.location+file)):
    #         return False

    #     if not(file.partition('.')[2].lower() == 'png'):
    #         return False

    #     #should also check somehow if it's a valid png file
    #     return True

    # def build_array(self):

    #     for one_item in os.listdir(self.location):
    #         if self.is_a_png_file(one_item):
    #             self.the_exercises.append(One_Exercise_Class(one_item))

    # def get_image(self, image_object, dimensions):
    #     if image_object.is_an_exercise:
    #         return(self.get_exercise_image(image_object.exercise, dimensions))
    #     else:
    #         return(self.get_from_image_folder(image_object.exercise, dimensions))

    # def get_exercise_image(self, which_exercise, dimensions):

    #     file_name = which_exercise + '.png'
    #     img = Image.open(self.location+file_name)
    #     resized_image = img.resize(
    #         (dimensions[0], dimensions[1]), Image.ANTIALIAS)
    #     return ImageTk.PhotoImage(resized_image)

    # def get_from_image_folder(self, which_image, dimensions):

    #     file_name = os.getcwd() + '\\image_files\\' + which_image + '.png'
    #     img = Image.open(file_name)
    #     resized_image = img.resize(
    #         (dimensions[0], dimensions[1]), Image.ANTIALIAS)
    #     return ImageTk.PhotoImage(resized_image)

    def load_icons(self):
        img = Image.open('Image_Files\\double_up.png')
        self.double_up = ImageTk.PhotoImage(img)

        img = Image.open('Image_Files\\up.png')
        self.up = ImageTk.PhotoImage(img)

        img = Image.open('Image_Files\\down.png')
        self.down = ImageTk.PhotoImage(img)

        img = Image.open('Image_Files\\double_down.png')
        self.double_down = ImageTk.PhotoImage(img)
