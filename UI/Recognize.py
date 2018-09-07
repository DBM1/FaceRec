# coding=utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

import os
import numpy as np
from Core import CNN
import tensorflow as tf

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
    background_color: (1,1,1,0.8)
    readonly: True
    
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
            
            # Button:
            #     text: '开始识别'
            #     size_hint: (0.14, 1 / 17)
            #     pos_hint: {'center_x': 0.79, 'y': 0.23}
            #     background_normal: 'UI/button_normal.png'
            #     background_down: 'UI/button_down.png'
            #     on_release: root.rec()
                    
""")


class KivyCamera(Image):
    capturing = False

    def __init__(self, fps):
        self.x = -300
        self.y = 0
        self.size = (100, 100)
        super(KivyCamera, self).__init__()

        self.classifier = cv2.CascadeClassifier('../Collection/haarcascade_frontalface_alt2.xml')
        self.path = "../TrainImage"
        self.filename = os.listdir(self.path)
        self.jugement = np.zeros([classnum])

        KivyCamera.capturing = True
        self.capture = cv2.VideoCapture(0)
        self.index = 0
        Clock.schedule_interval(self.update, 1.0 / fps)

    def remove(self):
        self.parent.remove_widget(self)
        self.capture.release()

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            if (self.index < 100):
                faces = self.classifier.detectMultiScale(frame, 1.1, 3, minSize=(150, 150))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    face = frame[y:y + h, x:x + w]
                    face = cv2.resize(face, (64, 64))
                    face = np.expand_dims(face, 0)
                    result = sess.run(output,
                                      feed_dict={CNN.x_data: face, CNN.keep_porb1: 1.0, CNN.keep_porb2: 1.0})
                    self.jugement[[np.argmax(result)]] += 1
                    self.index += 1
            else:
                rate = self.jugement[np.argmax(self.jugement)] / 100.0
                if rate > 0.85:
                    self.parent.showResult(self.filename[np.argmax(self.jugement)])
                else:
                    self.parent.showResult("Not include!")
                self.jugement = np.zeros([classnum])
                self.index = 0
                # self.parent.remove_widget(self)
                # self.capture.release()
                KivyCamera.capturing = False
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class RecognizeScreen(Screen):
    def rec(self):
        if not KivyCamera.capturing:
            camera = KivyCamera(60)
            self.add_widget(camera)

    def showResult(self, id):
        self.ids["ID"].text = id


class RecognizeApp(App):
    def build(self):
        Window.fullscreen = "auto"
        self.title = 'SuperAdminister'
        screen = RecognizeScreen()
        screen.rec()
        return screen


with tf.Session() as sess:
    classnum = 2
    output = CNN.cnnlayer(classnum)
    saver = tf.train.Saver()
    saver.restore(sess, "../Core/model/testmodel1")
    app = RecognizeApp()
    app.run()
