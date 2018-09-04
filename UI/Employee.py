# coding=utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.modalview import ModalView

PORT = 5920

Builder.load_string("""
#:import C kivy.utils.get_color_from_hex
#:import label kivy.uix.label
#:import sla kivy.adapters.simplelistadapter

<ScreenManager>:
    MainEmScreen
    QueryEmScreen
    SettingsEmScreen

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
    font_size: 15
    font_name:'UI/droid.ttf'

<Button>:
    font_name:'UI/droid.ttf'
    font_size: 18
    font_color:0,0,0
    height: 90
    size_hint: (1, None)
    border: (2, 2, 2, 2)

<TextInput>:
    font_size: 12
    multiline: False
    padding: [10, 0.5 * (self.height - self.line_height)]
    font_name:'UI/droid.ttf'

<ListViewModal>:
    size_hint: None, None
    size: 600,360
    ListView:
        size_hint: .9,.9
        #item_strings: [str(index) for index in range(100)]

<ScrollView>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

<MainEmScreen>:
    name: 'mainEm'
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/back1.png"

        FloatLayout:
            Button:
                size_hint: (0.29, 0.15)
                pos_hint: {'center_x': 0.82, 'y': 0.52}
                background_normal: 'UI/mainEm-query.png'
                background_down: 'UI/mainEm-query-down.png'
                on_release:root.manager.current = 'queryEm'

            Button:
                size_hint: (0.29, 0.15)
                pos_hint: {'center_x': 0.82, 'y': 0.28}
                background_normal: 'UI/mainEm-settings.png'
                background_down:'UI/mainEm-settings-down.png'
                on_release: root.manager.current = 'settingsEm'

<QueryEmScreen>:
    name: 'queryEm'
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/QueryAd-back.png"

        FloatLayout:
            ListViewModal:
                pos_hint: {'center_x': 0.39, 'y': 0.1}
                size_hint: (0.63, 0.61)
                
            Image:
                size_hint: (0.1, 0.1)
                pos_hint:{'center_x': 0.82, 'y': 0.85}
                source: 'UI/icon.png'
                
            Label:
                font_size:25
                size_hint: (0.2, 0.1)
                pos_hint:{'center_x': 0.7, 'y': 0.85}
                text: 'XXX,123456,市场部'
                
            Label:
                font_size:20
                text: '选择日期:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.11, 'y': 0.73}
            

            TextInput:                       #选择框
                id: ID
                hint_text: "ID"
                size_hint: (0.2, 0.04)
                pos_hint: {'center_x': 0.3, 'y': 0.73}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:                       #选择框
                id: password
                hint_text: "Password"
                size_hint: (0.2, 0.04)
                pos_hint: {'center_x': 0.56, 'y': 0.73}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '迟到/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.07, 'y': 0.04}
                
            TextInput:                       
                id: late
                hint_text: "late"
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.12, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            
            Label:
                font_size:14
                text: '旷工/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.21, 'y': 0.04}
                
            TextInput:                       
                id: off
                hint_text: 'off'
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.26, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '早退/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.35, 'y': 0.04}
                
            TextInput:                       
                id: early
                hint_text: 'early'
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.40, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '正常/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.49, 'y': 0.04}
                
            TextInput:                       
                id: normal
                hint_text: 'normal'
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.54, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Button:
                text: '导出'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.66, 'y': 0.04}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                #on_release: 

<SettingsEmScreen>:
    name: 'settingsEm'
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/settingsEm-back.png"

        FloatLayout:

            Image:
                size_hint: (0.15, 0.15)
                pos_hint:{'center_x': 0.87, 'y': 0.65}
                source: 'UI/icon.png'

            Label:
                font_size:20
                text: 'ID:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.16, 'y': 0.68}
                
            TextInput:                       
                id: ID
                hint_text: "ID"
                size_hint: (0.11, 0.04)
                pos_hint: {'center_x': 0.235, 'y': 0.68}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:20
                size_hint: (0.10, 0.04)
                pos_hint:{'center_x': 0.36, 'y': 0.68}
                text: 'Name:'

            TextInput:                       
                id: name
                hint_text: "Name"
                size_hint: (0.11, 0.04)
                pos_hint: {'center_x': 0.445, 'y': 0.68}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:20
                text: 'Apartment:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.59, 'y': 0.68}

            TextInput:                       #选择框
                id: apartment
                hint_text: "Apartment"
                size_hint: (0.11, 0.04)
                pos_hint: {'center_x': 0.713, 'y': 0.68}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Label:
                font_size:20
                text: '原密码:'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.3, 'y': 0.5}

            TextInput:                       
                id: previousPass
                size_hint: (0.32, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.5}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Label:
                font_size:20
                text: '新密码:'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.3, 'y': 0.4}

            TextInput:                       
                id: newPass
                size_hint: (0.32, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.4}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Label:
                font_size:20
                text: '确认新密码:'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.3, 'y': 0.3}

            TextInput:                       
                id: idetiNewPass
                size_hint: (0.32, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.3}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Label:
                font_size:20
                text: '验证码:'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.3, 'y': 0.2}

            TextInput:                       
                id: code
                size_hint: (0.2, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.2}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Image:
                size_hint: (0.18, 0.1)
                pos_hint: {'center_x': 0.47, 'y': 0.07}

            Button:
                text: '确认修改'
                size_hint: (0.15, 0.06)
                pos_hint: {'center_x': 0.80, 'y': 0.06}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                #on_release: root.manager.current = 'queryAd'

""")


class ListViewModal(ModalView):
    def __init__(self, **kwargs):
        super(ListViewModal, self).__init__(**kwargs)


class ScreenManager(ScreenManager):
    pass


class MainEmScreen(Screen):
    pass


class QueryEmScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainEm"
        self.manager.transition = SlideTransition(direction="left")


class SettingsEmScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainEm"
        self.manager.transition = SlideTransition(direction="left")


class EmployeeApp(App):
    def build(self):
        Window.fullscreen = "auto"
        self.title = 'Employee'
        return ScreenManager()


#if __name__ == '__main__':
#    Config.set('graphics', 'width', '800')
#    Config.set('graphics', 'height', '600')

EmployeeApp().run()
