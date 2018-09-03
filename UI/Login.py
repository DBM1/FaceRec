# coding=utf-8
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.animation import Animation
import socket

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


<Node>:
    canvas:
        Color:
            rgba: self.rgba1
        Line:
            circle: (self.x, self.y,self.size1 / 2 )
            width: self.size1 / 33
        Color:
            rgba: self.rgba
        Line:
            circle: (self.x, self.y ,self.size1 / 10)
            width: self.size1 / 8


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
                on_press: root.pressed()

""")


class Node(Widget):
    def __init__(self, x=10, y=10, size=150, rgba=(.2, .2, .7, 1), type=0):
        self.rgba = rgba
        self.rgba1 = rgba[0:3] + tuple([rgba[3] * 0.5])
        self.size1 = size
        self.x = x
        self.y = y
        if type == 0:
            anim = Animation(x=x + 50, y=y + 50, size1=size * 0.8, t="in_out_back", duration=4) + Animation(x=x,
                                                                                                            y=y + 100,
                                                                                                            t="in_out_back",
                                                                                                            size1=size * 1.1,
                                                                                                            duration=4) + Animation(
                x=x, y=y, t="in_out_back", size1=size, duration=4)
        anim.repeat = True
        anim.start(self)
        super(Node, self).__init__()


class Nodes(Widget):
    def __init__(self, x=240, y=200, size=120, alpha=1):
        self.x = x
        self.y = y
        self.size1 = size
        self.alpha = alpha
        self.rate = size / 145
        super(Nodes, self).__init__()

    def build(self):
        root = GridLayout()
        node1 = Node(self.x + 50 * self.rate, self.y + 140 * self.rate, self.size1 - 50 * self.rate,
                     rgba=(.8, .8, .8, 1))
        node2 = Node(self.x - 100 * self.rate, self.y + 50 * self.rate, self.size1 + 50 * self.rate,
                     rgba=(.5, .1, .4, 1))
        node3 = Node(self.x + 100 * self.rate, self.y - 50 * self.rate, self.size1)
        root.add_widget(node1)
        root.add_widget(node2)
        root.add_widget(node3)
        return root


class LoginScreen(Screen):
    def __init__(self):
        FloatLayout.__init__(self)
        self.add_widget(Nodes().build())

    def pressed(self):
        s = socket.socket()
        adr = '192.168.43.14'
        port = 12345
        s.connect((adr, port))
        s.send(("login," + self.ids['ID'].text + ',' + self.ids['password'].text).encode())
        print(s.recv(1024))

        s.close()
        return


class LoginApp(App):
    def build(self):
        self.title = 'Login'
        return LoginScreen()


if __name__ == '__main__':
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')

LoginApp().run()
