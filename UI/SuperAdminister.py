#coding=utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.uix.modalview import ModalView


PORT = 5920

Builder.load_string("""
#:import C kivy.utils.get_color_from_hex
#:import label kivy.uix.label
#:import sla kivy.adapters.simplelistadapter

<ScreenManager>:
    MainAdScreen
    InputAdScreen
    QueryAdScreen
    QueryAdEmScreen
    AccountingAdScreen
    
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

<MainAdScreen>:
    name: 'mainAd'
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/mainAd-back.png"

        FloatLayout:
            Button:
                size_hint: (0.28, 0.42)
                pos_hint: {'center_x': 0.195, 'y': 0.171}
                background_normal: 'UI/mainAd-luru.png'
                background_down: 'UI/mainAd-luru-down.png'
                on_release: root.manager.current = 'inputAd'

            Button:
                size_hint: (0.28, 0.42)
                pos_hint: {'center_x': 0.5, 'y': 0.171}
                background_normal: 'UI/mainAd-query.png'
                background_down:'UI/mainAd-query-down.png'
                on_release: root.manager.current = 'queryAd'

            Button:
                size_hint: (0.28, 0.42)
                pos_hint: {'center_x': 0.808, 'y': 0.171}
                background_normal: 'UI/mainAd-account.png'
                background_down: 'UI/mainAd-account-down.png'
                on_release: root.manager.current = 'accountingAd'

<InputAdScreen>:
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
            Camera:
                resolution: (128, 128)
                pos_hint: {'center_x': 0.3, 'y': -0.03}
                play:False
                
            TextInput:
                id: ID
                hint_text: "ID"
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.65}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: name
                hint_text: "Name"
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.53}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            TextInput:
                id: apartment
                hint_text: "Apartment"
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.41}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Button:
                text:'录入'
                size_hint: (0.15, 1/17)
                pos_hint: {'center_x': 0.81, 'y': 0.25}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                
            Button:
                text: 'Return'
                size_hint: (0.1, 0.1)
                pos_hint: {'center_x': 0.1, 'y': 0.02}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release: root.manager.current = 'mainAd'

<QueryAdScreen>:
    name: 'queryAd'
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
                pos_hint: {'center_x': 0.53, 'y': 0.04}
                size: 600, 380
            Button:
                text: 'Search'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.2, 'y': 0.72}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.manager.current = 'queryAdEm'

            TextInput:
                id: ID
                hint_text: "ID"
                size_hint: (0.2, 0.04)
                pos_hint: {'center_x': 0.5, 'y': 0.72}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: password
                hint_text: "Password"
                size_hint: (0.2, 0.04)
                pos_hint: {'center_x': 0.77, 'y': 0.72}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Button:
                text: 'Return'
                size_hint: (0.1, 0.1)
                pos_hint: {'center_x': 0.05, 'y': 0.02}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release: root.manager.current = 'mainAd'
                
            

<QueryAdEmScreen>:
    name: 'queryAdEm'
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
                pos_hint: {'center_x': 0.53, 'y': 0.1}
                
            Image:
                size_hint: (0.1, 0.1)
                pos_hint:{'center_x': 0.9, 'y': 0.85}
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
                pos_hint: {'center_x': 0.21, 'y': 0.73}
            

            TextInput:                       #选择框
                id: ID
                hint_text: "ID"
                size_hint: (0.2, 0.04)
                pos_hint: {'center_x': 0.5, 'y': 0.73}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:                       #选择框
                id: password
                hint_text: "Password"
                size_hint: (0.2, 0.04)
                pos_hint: {'center_x': 0.77, 'y': 0.73}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '迟到/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.21, 'y': 0.04}
                
            TextInput:                       
                id: late
                hint_text: "late"
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.28, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            
            Label:
                font_size:14
                text: '请假/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.36, 'y': 0.04}
                
            TextInput:                       
                id: off
                hint_text: 'off'
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.43, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '早退/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.51, 'y': 0.04}
                
            TextInput:                       
                id: early
                hint_text: 'early'
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.58, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '正常/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.66, 'y': 0.04}
                
            TextInput:                       
                id: normal
                hint_text: 'normal'
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.73, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Button:
                text: '导出'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.85, 'y': 0.04}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                #on_release: root.manager.current = 'queryAd'
                
            Button:
                text: 'Return'
                size_hint: (0.1, 0.1)
                pos_hint: {'center_x': 0.05, 'y': 0.02}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release: root.manager.current = 'queryAd'

<AccountingAdScreen>:
    name: 'accountingAd'
    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "UI/AccountingAd-back.png"

        FloatLayout:
            ListViewModal:
                size:450, 430
                pos_hint: {'center_x': 0.68, 'y': 0.09}
                
            Label:
                font_size:20
                text: '选择日期:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.45, 'y': 0.85}
            

            TextInput:                       #选择框
                id: ID
                hint_text: "ID"
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.62, 'y': 0.85}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:                       #选择框
                id: password
                hint_text: "Password"
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.82, 'y': 0.85}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            Label:
                font_size:14
                text: '共计/人次'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.53, 'y': 0.04}
                
            TextInput:                       
                id: late
                hint_text: "num"
                size_hint: (0.06, 0.04)
                pos_hint: {'center_x': 0.61, 'y': 0.04}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            
            Button:
                text: '导出'
                size_hint: (0.11, 0.05)
                pos_hint: {'center_x': 0.85, 'y': 0.04}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                #on_release: root.manager.current = 'queryAd'
                
            Button:
                text: 'Return'
                size_hint: (0.1, 0.1)
                pos_hint: {'center_x': 0.05, 'y': 0.02}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release: root.manager.current = 'mainAd'

""")


class ListViewModal(ModalView):
    def __init__(self, **kwargs):
        super(ListViewModal, self).__init__(**kwargs)


class KivyCamera(Image):
    def __init__(self, capture, fps):
        super(KivyCamera, self).__init__()
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=10)
        self.title="人脸数据采集"
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()



class ScreenManager(ScreenManager):
    pass


class MainAdScreen(Screen):
    pass


class InputAdScreen(Screen):
    pass


class QueryAdScreen(Screen):
    pass


class QueryAdEmScreen(Screen):
    pass


class AccountingAdScreen(Screen):
    pass


class SuperAdministerApp(App):
    def build(self):
        self.title = 'SuperAdminister'
        return ScreenManager()


if __name__ == '__main__':
    Config.set('graphics', 'width', '800')
    Config.set('graphics', 'height', '600')


SuperAdministerApp().run()
