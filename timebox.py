from logging import root
from turtle import pos
from kivy.app import App
from kivy.uix.widget import Widget
from numpy import size, source
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty,ListProperty
from fpdf import FPDF, HTMLMixin
from datetime import datetime
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from save_to_pdf import save_to_pdf,save_temp_csv,load_temp_csv


class LimitInput(TextInput):
    def keyboard_on_key_up(self, keycode, text):
        if text[0] == 'backspace':
            self.do_backspace()

    def on_text(self, instance, value):
        if len(self.text) >= 90:
            self.text = self.text[0:89]


# class DrawTimeBox(Widget):
#     def __init__(self, **kwargs):
#         super(DrawTimeBox, self).__init__(**kwargs)

#         with self.canvas:
#             self.rect = Rectangle(pos=(0,0), size=(50,50))

#     def on_touch_down(self, touch):
#         print("hej huj")
#         return super().on_touch_down(touch)

Builder.load_file('test2.kv')

class MyGridLayout(Widget):
    Window.size = (900, 1000)
    brain_dump_box = ObjectProperty(None)
    priorities_table = ListProperty([])
    timebox_table = ListProperty([])
    date_of_pdf = datetime.date(datetime.now())
    date = "Date: " + str(date_of_pdf)
    time_rectangle = []
    # rec_width = width * 0.04
    # rec_height = height * 0.04

    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

    def load_from_csv(self):
        load_temp_csv(self.date_of_pdf, self.brain_dump_box, self.priorities_table, self.timebox_table)

        # TEST CHANGE DAY! 
        # date_of_pdf = date_of_pdf.replace(day = 4)
        # print("day: ",date_of_pdf.day)
        print(self.date)

    def press_button(self):
        pass
        # save_to_pdf(self.date_of_pdf,self.brain_dump_box, self.priorities_table, self.timebox_table)
        # save_temp_csv(self.date_of_pdf,self.brain_dump_box, self.priorities_table, self.timebox_table)
        
    def press_texinput(self):
        print("cos ktos jak ")

    def on_size(self, *args):
        for elem in self.time_rectangle:
            elem.size = (self.width * 0.04, self.height * 0.04)

    def on_touch_down(self, touch):
        with self.canvas:
            self.time_rectangle.append(Rectangle(pos=(0,0), size=(self.width * 0.04, self.height * 0.04)))
            self.time_rectangle[-1].pos = touch.pos
            print('The touch is at position', touch.pos[1])

            self.time_rectangle[-1].pos = (0,touch.pos[1])


        print("hej huj")
        return super().on_touch_down(touch)

class TheTimeBox(App):
    spacing_numbers_column = NumericProperty(0.2)
    # font_size_array = NumericProperty(24)
    def build(self):
        self.gridLayout = MyGridLayout()
        return self.gridLayout

    def on_start(self, **kwargs):
        self.gridLayout.load_from_csv()


if __name__ == "__main__":
    TheTimeBox().run()