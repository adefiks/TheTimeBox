from kivy.app import App
from kivy.uix.widget import Widget
from numpy import source
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty,ListProperty
from fpdf import FPDF, HTMLMixin
from datetime import datetime
from kivy.uix.textinput import TextInput
from save_to_pdf import save_to_pdf,save_temp_csv,load_temp_csv

class LimitInput(TextInput):
    def keyboard_on_key_up(self, keycode, text):
        if text[0] == 'backspace':
            self.do_backspace()

    def on_text(self, instance, value):
        if len(self.text) >= 90:
            self.text = self.text[0:89]

Builder.load_file('test2.kv')

class MyGridLayout(Widget):
    Window.size = (900, 1000)
    brain_dump_box = ObjectProperty(None)
    priorities_table = ListProperty([])
    timebox_table = ListProperty([])
    date_of_pdf = datetime.date(datetime.now())
    date = "Date: " + str(date_of_pdf)

    def load_from_csv(self):
        load_temp_csv(self.date_of_pdf, self.brain_dump_box, self.priorities_table, self.timebox_table)

        # TEST CHANGE DAY! 
        # date_of_pdf = date_of_pdf.replace(day = 4)
        # print("day: ",date_of_pdf.day)
        print(self.date)

    def press_button(self):
        save_to_pdf(self.date_of_pdf,self.brain_dump_box, self.priorities_table, self.timebox_table)
        save_temp_csv(self.date_of_pdf,self.brain_dump_box, self.priorities_table, self.timebox_table)
        
    def press_texinput(self):
        print("cos ktos jak ")

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
    # app = TheTimeBox()
    # app.run()