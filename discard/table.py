from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import weakref
from kivy.clock import Clock

kv = """

#:import FadeTransition kivy.uix.screenmanager.FadeTransition
ScreenManager:
    transition: FadeTransition()
    ShipmentsScreen:

<TextInput@TextInput>
    size_hint_y: None
    height: 20

<Row>:
    cols: 3
    TextInput:
    TextInput:
    TextInput:

<Rows>:
    orientation: 'vertical' 

<ShipmentsScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Store'
            size_hint_y: None
            height: 20 
            on_press: rows.store()
        Rows:
            id: rows

"""


class Row(GridLayout):
    pass


class Rows(BoxLayout):
    def __init__(self, **kwargs):
        super(Rows, self).__init__(**kwargs)
        Clock.schedule_once(self.fill)
        self._rows = {}

    def fill(self, dt):
        for i in range(30):
            row = Row()
            self.add_widget(row)
            self._rows["row"+str(i)] = weakref.ref(row)

    def store(self):
        #loop that will access each textinput and print its content
        print("textinput content by id or coordinates x, y")
        for id, row in self._rows.items():
            print(id)
            children = row().children
            col = len(children) - 1
            for ti in children:
                print('\tcol#', col, ti.text)
                col -= 1


class ShipmentsScreen(Screen):
    pass


sm = Builder.load_string(kv)


class TestApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    TestApp().run()
