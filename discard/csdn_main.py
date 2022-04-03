from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class MainApp(App):
    def build(self):
        label = Label(text='Hello World', size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})

        return label


class boxLayoutExample1(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=15, padding=10)  # 创建Layout
        buttons = [str(i) for i in range(7)]  # 设置按键的标签
        for i in range(7):
            button = Button(text=buttons[i], size_hint=(.5, .5),
                            pos_hint={"center_x": .5, "center_y": .5})
            button.bind(on_press=self.on_press_button)
            layout.add_widget(button)  # 将按键加入到Layout中
        return layout

    def on_press_button(self, instance):
        print('You pressed {} key.'.format(instance.text))


Builder.load_string('''
<myLayout>
    BoxLayout:
        orientation:'vertical'
        spacing:15
        padding:38
        Button:
            id:0
            text:'0'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}
            on_press:root.on_press_button(self.text)
        Button:
            id:1
            text:'1'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}            
            on_press:root.on_press_button(self.text)
        Button:
            id:2
            text:'2'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}            
            on_press:root.on_press_button(self.text)
        Button:
            id:3
            text:'3'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}            
            on_press:root.on_press_button(self.text)
        Button:
            id:4
            text:'4'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}            
            on_press:root.on_press_button(self.text)   
        Button:
            id:5
            text:'5'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}            
            on_press:root.on_press_button(self.text)
        Button:
            id:6
            text:'6'
            size_hint:(.5, .5)
            pos_hint:{"center_x": .5, "center_y": .5}            
            on_press:root.on_press_button(self.text)                                 
''')


class myLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(myLayout, self).__init__(**kwargs)

    def on_press_button(self, instance):
        print('You pressed {} key.'.format(instance))


class boxLayoutExample2(App):
    def build(self):
        return myLayout()


if __name__ == '__main__':
    # app = MainApp()
    # app = boxLayoutExample1()
    app = boxLayoutExample2()
    app.run()
