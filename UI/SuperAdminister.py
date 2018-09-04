# coding=utf-8
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
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.floatlayout import FloatLayout
import time
from Collection import imgCollection
import os
import numpy as np

PORT = 5920

Builder.load_string("""
#:import C kivy.utils.get_color_from_hex
#:import label kivy.uix.label
#:import sla kivy.adapters.simplelistadapter
<KivyCamera>

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
    ListView:
        size_hint: .9,.9
        #item_strings: [str(index) for index in range(100)]
        #adapter:
            #sla.SimpleListAdapter(
            #data=["Item #{0}".format(i) for i in range(100)],
            #cls=label.Label)

<ScrollView>:
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            
<ScreenManager>:
    MainAdScreen
    InputAdScreen
    QueryAdScreen
    QueryAdEmScreen
    AccountingAdScreen
    
<MainAdScreen>:
    id:s1
    name: 'mainAd'
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
                size_hint: (0.29, 0.13)                            #0.28    0.42
                pos_hint: {'center_x': 0.82, 'y': 0.55}          #0.195   0.171
                background_normal: 'UI/mainAd-luru2.png'
                background_down: 'UI/mainAd-luru-down2.png'
                on_release: root.manager.current = 'inputAd'

            Button:
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.38}
                background_normal: 'UI/mainAd-query2.png'
                background_down:'UI/mainAd-query-down2.png'
                on_release: root.manager.current = 'queryAd'

            Button:
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.21}
                background_normal: 'UI/mainAd-account2.png'
                background_down: 'UI/mainAd-account-down2.png'
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
            TextInput:
                id: ID
                hint_text: "ID"
                size_hint: (0.23, 1/17)
                pos_hint: {'center_x': 0.79, 'y': 0.63}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: name
                hint_text: "Name"
                size_hint: (0.23, 1/17)
                pos_hint: {'center_x': 0.79, 'y': 0.51}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
                
            TextInput:
                id: apartment
                hint_text: "Apartment"
                size_hint: (0.23, 1/17)
                pos_hint: {'center_x': 0.79, 'y': 0.39}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Button:
                text:'录入'
                size_hint: (0.14, 1/17)
                pos_hint: {'center_x': 0.79, 'y': 0.23}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release: root.fun()

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
                pos_hint: {'center_x': 0.39, 'y': 0.04}
                size_hint: (0.65, 0.65)
            Button:
                text: 'Search'
                size_hint: (0.10, 0.05)
                pos_hint: {'center_x': 0.1, 'y': 0.72}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.manager.current = 'queryAdEm'

            TextInput:
                id: ID
                hint_text: "ID"
                size_hint: (0.18, 0.05)
                pos_hint: {'center_x': 0.34, 'y': 0.72}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: password
                hint_text: "Password"
                size_hint: (0.18, 0.05)
                pos_hint: {'center_x': 0.62, 'y': 0.72}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

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
                # on_release: root.manager.current = 'queryAd'


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
                size_hint: (0.5, 0.75)
                pos_hint: {'center_x': 0.668, 'y': 0.11}
                
            Label:
                font_size:20
                text: '选择日期:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.45, 'y': 0.88}
            

            TextInput:                       #选择框
                id: ID
                hint_text: "ID"
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.62, 'y': 0.88}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:                       #选择框
                id: password
                hint_text: "Password"
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.82, 'y': 0.88}
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


""")


class ListViewModal(ModalView):
    def __init__(self, **kwargs):
        super(ListViewModal, self).__init__(**kwargs)


class KivyCamera(Image):
    capturing = False

    def __init__(self, fps, id):
        self.x = -300
        self.y = 0
        self.size = (100, 100)
        super(KivyCamera, self).__init__()

        self.classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
        self.path = "../TrainImage/" + id
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        KivyCamera.capturing = True
        self.capture = cv2.VideoCapture(0)
        self.index = 0
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self,dt):
        ret, frame = self.capture.read()
        if ret:
            if (self.index < 400):
                faces = self.classifier.detectMultiScale(frame, 1.1, 3, minSize=(120, 120))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face = frame[y:y + h, x:x + w]
                    face = cv2.resize(face, (64, 64))
                    cv2.imwrite(self.path + "/%d.png" % self.index,
                                imgCollection.relight(face, np.random.uniform(0.5, 1.5)))
                    self.index += 1
                # convert it to texture
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.texture = image_texture
            else:
                self.parent.remove_widget(self)
                self.capture.release()
                KivyCamera.capturing = False


# class YearSpinner(Spinner):
#     def show_selected_value(self, text):
#         print('The spinner', self, 'have text', text)
#
#     bind(text=show_selected_value)


class ScreenManager(ScreenManager):
    pass


class MainAdScreen(Screen):
    pass


class InputAdScreen(Screen):

    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")

    def fun(self):
        if not KivyCamera.capturing:
            id = self.ids["ID"].text
            if not id == "":
                camera = KivyCamera(144, id)
                self.add_widget(camera)


class QueryAdScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")


class QueryAdEmScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "queryAd"
        self.manager.transition = SlideTransition(direction="left")


class AccountingAdScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")


class SuperAdministerApp(App):
    def build(self):
        Window.fullscreen = "auto"
        self.title = 'SuperAdminister'
        return ScreenManager()


SuperAdministerApp().run()
