# coding=utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

Builder.load_string("""
#:import FloatLayout kivy.uix.floatlayout
#:import label kivy.uix.label

<Button>:
    font_name:'UI/droid.ttf'
    font_size: 18
    font_color:1,1,0
    # height: 90
    size_hint: (1, None)
    border: (2, 2, 2, 2)
    background_normal: 'UI/button1.png'
    background_down: 'UI/button2.png'

<TextInput>:
    font_size: 12
    multiline: False
    padding: [10, 0.5 * (self.height - self.line_height)]
    font_name:'UI/droid.ttf'

<RecognizeScreen>:
    name: 'inputAd'
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/InputAd-back.png"

        FloatLayout:
            TextInput:
                id: ID
                hint_text: "ID"
                size_hint: (0.23, 1 / 17)
                pos_hint: {'center_x': 0.79, 'y': 0.63}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            
            TextInput:
                id: name
                hint_text: "Name"
                size_hint: (0.23, 1 / 17)
                pos_hint: {'center_x': 0.79, 'y': 0.51}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            
            TextInput:
                id: apartment
                hint_text: "Apartment"
                size_hint: (0.23, 1 / 17)
                pos_hint: {'center_x': 0.79, 'y': 0.39}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            
            Button:
                text: '开始识别'
                size_hint: (0.14, 1 / 17)
                pos_hint: {'center_x': 0.79, 'y': 0.23}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                #on_release: 
                    
""")


class RecognizeScreen(Screen):
    pass


class RecognizeApp(App):
    def build(self):
        Window.fullscreen = "auto"
        self.title = 'SuperAdminister'
        return RecognizeScreen()


RecognizeApp().run()
