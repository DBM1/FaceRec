# coding=utf-8
import sys

sys.path.append('../')
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from Collection import imgCollection
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

from Clients import EmpClient
import numpy as np
import os
import re
import xlwt

Builder.load_string("""
<MyPopup>:
    size_hint: .3, .3
    auto_dismiss: False
    title: 'Hint'
    Button:
        id:button
        text: 'Wrong Password!'
        on_press: root.dismiss()
<BoxLayout>:
    padding: 10
    spacing: 10
<Label>:
    font_size: 15
    font_name:'UI/droid.ttf'
<Button>:
    font_name:'UI/droid.ttf'
    font_size: 18
    font_color:1,1,0
    size_hint: (1, None)
    border: (2, 2, 2, 2)
    background_normal: 'UI/button1.png'
    background_down: 'UI/button2.png'
<TextInput>:
    font_size: 12
    multiline: False
    padding: [10, 0.5 * (self.height - self.line_height)]
    font_name:'UI/droid.ttf'

<ScreenManager>:
    LoginScreen
    MainAdScreen
    InputAdScreen
    QueryAdScreen
    QueryAdEmScreen
    AccountingAdScreen
    SettingsEmScreen
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
                pos_hint: {'center_x': 0.82, 'y': 0.6}          #0.195   0.171
                background_normal: 'UI/mainAd-luru2.png'
                background_down: 'UI/mainAd-luru-down2.png'
                on_release: root.manager.current = 'inputAd'
            Button:
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.43}
                background_normal: 'UI/mainAd-query2.png'
                background_down:'UI/mainAd-query-down2.png'
                on_release: root.manager.current = 'queryAd'
            Button:
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.26}
                background_normal: 'UI/mainAd-account2.png'
                background_down: 'UI/mainAd-account-down2.png'
                on_release: root.manager.current = 'accountingAd'

            Button:
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.09}
                background_normal: 'UI/mainAd-setting.png'
                background_down:'UI/mainAd-setting-down.png'
                on_release: root.manager.current = 'settingsEm'

            Button:                                                 #主界面退出按钮
                text:'退出'
                size_hint: (0.12, 1/17)
                pos_hint: {'center_x': 0.08, 'y': 0.03}
                background_normal: 'UI/button1.png'
                background_down: 'UI/button2.png'
                on_release: root.close()                
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
                hint_text: "账号"
                text: "管理员"
                readonly: True
                font_size: 20
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.21, 'y': 0.60}               #0.81   0.65
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            TextInput:
                id: password
                hint_text: "密码"
                password: True
                password_mask:'●'
                font_size: 20
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.21, 'y': 0.48}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            Label:
                id: boarder
                font_size: 20
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.21, 'y': 0.36}
            Button:
                text:'登录'
                size_hint: (0.15, 1/17)
                pos_hint: {'center_x': 0.21, 'y': 0.2}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release:root.Login()
<SettingsEmScreen>:
    id:Setting
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
            Label:
                font_size:20
                text: '原密码:'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.3, 'y': 0.5}
            TextInput:                       
                id: previousPass
                password: True
                password_mask:'●'
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
                password: True
                password_mask:'●'
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
                password: True
                password_mask:'●'
                size_hint: (0.32, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.3}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            Label:                       
                id: code
                size_hint: (0.2, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.2}
                # background_normal: 'UI/input_line.png'
                # background_active: 'UI/white.png'

            Image:
                size_hint: (0.18, 0.1)
                pos_hint: {'center_x': 0.47, 'y': 0.07}
            Button:
                text: '确认修改'
                size_hint: (0.15, 0.06)
                pos_hint: {'center_x': 0.80, 'y': 0.06}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.ChangeInfo()
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
                hint_text: "工号"
                readonly: True
                size_hint: (0.23, 1/17)
                pos_hint: {'center_x': 0.79, 'y': 0.63}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            TextInput:
                id: name
                hint_text: "姓名"
                size_hint: (0.23, 1/17)
                pos_hint: {'center_x': 0.79, 'y': 0.51}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: apartment
                hint_text: "部门"
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
            ListView:
                id : lists
                pos_hint: {'center_x': 0.39, 'y': 0.04}
                size_hint: (0.65, 0.65)
            Button:
                text: '查找'
                size_hint: (0.10, 0.05)
                pos_hint: {'center_x': 0.1, 'y': 0.72}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.fun()
            TextInput:
                id: ID
                hint_text: "工号"
                size_hint: (0.18, 0.05)
                pos_hint: {'center_x': 0.34, 'y': 0.72}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'
            TextInput:
                id: name
                hint_text: "姓名"
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
            ListView:
                id:list
                pos_hint: {'center_x': 0.39, 'y': 0.1}
                size_hint: (0.63, 0.61)
                item_strings: 

            Label:
                id:name
                font_size:25
                size_hint: (0.2, 0.1)
                pos_hint:{'center_x': 0.7, 'y': 0.85}
                text: ' '

            Label:
                font_size:20
                text: '选择日期:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.11, 'y': 0.73}

            Spinner:
                id:Year
                text: '2018'
                values: ['2018', '2017', '2016']
                size_hint: (None, None)
                size:(150,34)
                pos_hint: {'center_x': 0.27, 'y': 0.73} 
            Spinner:
                id:Month
                text: '01'
                values: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                size_hint: (None, None)
                size:(150,34)
                pos_hint: {'center_x': 0.45, 'y': 0.73} 
            Button:
                text: '查询'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.66, 'y': 0.73}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.Query()

            Label:
                font_size:14
                text: '迟到/天'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.07, 'y': 0.04}

            TextInput:                       
                id: late
                # hint_text: "late"
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
                # hint_text: 'off'
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
                # hint_text: 'early'
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
                # hint_text: 'normal'
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
                on_release: root.export()


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
            ListView:
                id: list
                size_hint: (0.5, 0.75)
                pos_hint: {'center_x': 0.668, 'y': 0.11}

            Label:
                font_size:20
                text: '选择日期:'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.45, 'y': 0.88}

            Spinner:
                id:year
                text: '2018'
                values: ['2018', '2017', '2016']
                size_hint: (None, None)
                size:(150,34)
                pos_hint: {'center_x': 0.60, 'y': 0.88} 
            Spinner:
                id:month
                text: '01'
                values: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                size_hint: (None, None)
                size:(150,34)
                pos_hint: {'center_x': 0.72, 'y': 0.88} 

            Label:
                font_size:14
                text: '共计/人次'
                size_hint: (0.15, 0.04)
                pos_hint: {'center_x': 0.53, 'y': 0.04}

            TextInput:                       
                id: late
                # hint_text: "num"
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
                on_release: root.export()
            Button:
                text: '查询'
                size_hint: (0.10, 0.04)
                pos_hint: {'center_x': 0.85, 'y': 0.88} 
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.fun()
""")

empclient = EmpClient.EmpClient()


class MyPopup(Popup):
    def modify(self, text):
        self.ids.button.text = text


class KivyCamera(Image):
    capturing = False

    def __init__(self, fps, id):
        self.x = -300
        self.y = 0
        self.size = (100, 100)
        super(KivyCamera, self).__init__()

        self.classifier = cv2.CascadeClassifier('../Collection/haarcascade_frontalface_alt2.xml')
        self.path = "../NewImage/" + id
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        KivyCamera.capturing = True
        self.capture = cv2.VideoCapture(0)
        self.index = 0
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            if (self.index < 400):
                faces = self.classifier.detectMultiScale(frame, 1.1, 3, minSize=(150, 150))
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


class ScreenManager(ScreenManager):
    pass


class MainAdScreen(Screen):
    def close(self):
        Window.close()


class LoginScreen(Screen):
    def Login(self):
        id = self.ids.ID.text
        psw = self.ids.password.text
        if not (id == "" or psw == ""):
            res = empclient.login(emp_id="000001", psw=psw)
            if (res == 'success'):
                self.manager.current = 'mainAd'
            elif (res == 'no such id'):  # 已修改为弹框
                s = '账号不存在'
                p = MyPopup()
                p.modify(s)
                p.open()
            elif (res == 'wrong password'):  # 已修改为弹框
                s = '密码错误'
                p = MyPopup()
                p.modify(s)
                p.open()
        else:
            s = "请输入账号密码"
            p = MyPopup()
            p.modify(s)
            p.open()


class SettingsEmScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")

    def ChangeInfo(self):
        ori_psw = self.ids.previousPass.text
        new_psw = self.ids.newPass.text
        iden_psw = self.ids.idetiNewPass.text
        if (ori_psw == "" or new_psw == "" or iden_psw == ""):
            s = "密码不能为空"
            p = MyPopup()
            p.modify(s)
            p.open()
        else:
            if (new_psw == iden_psw):  # 已修改为弹框
                if (empclient.change_psw(ori_psw, new_psw) == "wrong psw"):
                    # self.ids.code.text = "密码修改成功"
                    s = "原密码错误"
                    p = MyPopup()
                    p.modify(s)
                    p.open()
                else:
                    s = "密码修改成功"
                    p = MyPopup()
                    p.modify(s)
                    p.open()
            else:  # 已修改为弹框
                # self.ids.code.text = '两次密码不一致'
                s = '两次密码不一致'
                p = MyPopup()
                p.modify(s)
                p.open()


class InputAdScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")

    def fun(self):
        if not KivyCamera.capturing:
            self.ids["ID"].text = empclient.get_last_id()
            id = self.ids["ID"].text
            name = self.ids["name"].text
            department = self.ids["apartment"].text
            if not (id == "" or name == "" or department == ""):
                camera = KivyCamera(144, id)
                self.add_widget(camera)
                if (empclient.add_emp_info(id, name, department, "None")):
                    print("Adding employee information successful!")
                else:
                    s = "录入信息失败，请检查数据"
                    p = MyPopup()
                    p.modify(s)
                    p.open()
            else:
                s = "请输入员工信息"
                p = MyPopup()
                p.modify(s)
                p.open()


class QueryAdScreen(Screen):
    recordTuple = ""

    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")

    def fun(self):
        id = self.ids["ID"].text
        name = self.ids["name"].text
        QueryAdScreen.recordTuple = ""
        self.ids["lists"].item_strings = ""
        showList = []
        if id == "":
            if not name == "":
                QueryAdScreen.recordTuple = empclient.get_info_by_name(name)
            else:
                s = "请输入工号或姓名"
                p = MyPopup()
                p.modify(s)
                p.open()
        else:
            QueryAdScreen.recordTuple = empclient.get_info(id)
        if not QueryAdScreen.recordTuple == "":
            if not QueryAdScreen.recordTuple[0] == "None":
                len1 = len(QueryAdScreen.recordTuple)
                for i in range(len1 // 5):
                    record = QueryAdScreen.recordTuple[0 + 5 * i] + "    " + QueryAdScreen.recordTuple[
                        1 + 5 * i] + "    " + \
                             QueryAdScreen.recordTuple[2 + 5 * i]
                    showList.append(record)
                list = self.ids["lists"]
                list.item_strings = showList
                if len1 == 5:
                    self.manager.current = 'queryAdEm'
            else:
                s = "工号或姓名不存在"
                p = MyPopup()
                p.modify(s)
                p.open()


class QueryAdEmScreen(Screen):
    record = []
    Time = ""

    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "queryAd"

    def Query(self):
        year = self.ids.Year.text
        month = self.ids.Month.text
        time = year + '-' + month
        QueryAdEmScreen.Time = time
        res = empclient.get_record_and_state(time, QueryAdScreen.recordTuple[0])
        if (res == "wrong time") or (res == "None"):
            s = "数据查询失败"
            p = MyPopup()
            p.modify(s)
            p.open()
            self.ids.list.item_strings = ""
        else:
            r = res[1:-1]
            comp = re.split(r"[(](.*?)[)]", r)
            date = re.findall('\d+', comp[-1])
            if not date == []:
                self.ids.late.text = date[1]
                self.ids.off.text = date[3]
                self.ids.early.text = date[2]
                self.ids.normal.text = date[0]
                record = QueryAdEmScreen.record
                for i in range(len(comp)):
                    if i % 2 == 1:
                        comp[i] = comp[i].replace("'", '')
                        record.append(comp[i])
                self.ids.list.item_strings = record
                info = empclient.get_info(QueryAdScreen.recordTuple[0])
                self.ids.name.text = info[1] + ',' + info[0] + ',' + info[2]
            else:
                self.ids.late.text = ""
                self.ids.off.text = ""
                self.ids.early.text = ""
                self.ids.normal.text = ""
                # s = "该月无数据"
                # p = MyPopup()
                # p.modify(s)
                # p.open()

    def export(self):
        record = QueryAdEmScreen.record
        if not record == []:
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet1")
            for i in range(len(record)):
                item = record[i].split(',')
                for j in range(len(item)):
                    sheet.write(i, j, item[j])
            sheet.col(1).width = 22 * 256
            sheet.col(2).width = 12 * 256
            wbk.save("../ExportFile/" + QueryAdScreen.recordTuple[0] + '-' + QueryAdEmScreen.Time + ".xls")
        else:
            s = "导出记录为空"
            p = MyPopup()
            p.modify(s)
            p.open()


class AccountingAdScreen(Screen):
    record = []
    date = ""

    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainAd"
        self.manager.transition = SlideTransition(direction="left")

    def fun(self):
        year = self.ids["year"].text
        month = self.ids["month"].text
        AccountingAdScreen.date = year + "-" + month
        receive = empclient.get_except_record(AccountingAdScreen.date)
        if (receive == "wrong time") or (receive == "None"):
            # s = "数据查询失败"
            # p = MyPopup()
            # p.modify(s)
            # p.open()
            self.ids["list"].item_strings = ""
        else:
            par = r'\((.*)\)'
            receive = receive.replace("\'", '')
            records = re.findall(par, receive)
            records = records[0].split(",")
            records = np.array(records).reshape(len(records) // 4, 4)
            AccountingAdScreen.record = records
            showList = []
            for i in range(records.shape[0]):
                showList.append("")
                for j in range(records.shape[1]):
                    showList[i] += records[i][j] + "    "
            self.ids["late"].text = str(records.shape[0])
            self.ids["list"].item_strings = showList

    def export(self):
        records = AccountingAdScreen.record
        if not records == []:
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet1")
            for i in range(records.shape[0]):
                for j in range(records.shape[1]):
                    sheet.write(i, j, records[i][j])
            sheet.col(1).width = 22 * 256
            sheet.col(2).width = 12 * 256
            wbk.save("../ExportFile/" + "Records-" + AccountingAdScreen.date + ".xls")
        else:
            s = "导出记录为空"
            p = MyPopup()
            p.modify(s)
            p.open()


class SuperAdministerApp(App):
    def build(self):
        Window.fullscreen = "auto"
        self.title = 'SuperAdminister'
        return ScreenManager()


SuperAdministerApp().run()