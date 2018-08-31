#coding=utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen


PORT = 5920

Builder.load_string("""
#:import C kivy.utils.get_color_from_hex

<BoxLayout>:
    padding: 10
    spacing: 10

<GridLayout>:
    rows: 2
    cols: 2
    spacing: 10
    row_default_height: 90
    row_force_default: True

<Label>:
    font_size: 25
    font_name:'UI/droid.ttf'

<Button>:
    font_name:'UI/droid.ttf'
    font_size: 18
    font_color:0,0,0
    height: 90
    size_hint: (1, None)
    background_normal: 'UI/button_normal.png'
    background_down: 'UI/button_down.png'
    border: (2, 2, 2, 2)

<TextInput>:
    font_size: 20
    multiline: False
    padding: [10, 0.5 * (self.height - self.line_height)]
    font_name:'UI/droid.ttf'

<ScrollView>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/Login-back.png"

        FloatLayout:
            TextInput:
                id: ID
                hint_text: "ID"
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.65}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: password
                hint_text: "Password"
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.53}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Button:
                text:'Login'
                size_hint: (0.15, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.25}

""")


class LoginScreen(Screen):
    pass


class LoginApp(App):
    def build(self):
        self.title = 'Login'
        return LoginScreen()


if __name__ == '__main__':
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')


LoginApp().run()
