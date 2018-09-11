# coding=utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.modalview import ModalView
from Clients import EmpClient as func
import re
from kivy.uix.popup import Popup
import xlwt

emp = func.EmpClient()
PORT = 5920

Builder.load_string("""
#:import C kivy.utils.get_color_from_hex
#:import label kivy.uix.label
#:import sla kivy.adapters.simplelistadapter
<MyPopup>:
    size_hint: .3, .3
    auto_dismiss: False
    title: 'Hint'
    Button:
        id:button
        text: 'Wrong Password!'
        on_press: root.dismiss()
    
<ScreenManager>:
    
    LoginScreen
    MainEmScreen
    QueryEmScreen
    SettingsEmScreen

<BoxLayout>:
    padding: 10
    spacing: 10
    
<Label>:
    font_size: 15
    font_name:'UI/droid.ttf'

<Button>:
    font_name:'UI/droid.ttf'
    font_size: 18
    size_hint: (1, None)
    border: (2, 2, 2, 2)
    background_normal: 'UI/button1.png'
    background_down: 'UI/button2.png'

<TextInput>:
    font_size: 12
    multiline: False
    padding: [10, 0.5 * (self.height - self.line_height)]
    font_name:'UI/droid.ttf'

            
<LoginScreen>:
    name : 'loginem'
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
                font_size: 20
                size_hint: (0.25, 1/17)
                pos_hint: {'center_x': 0.21, 'y': 0.60}               #0.81   0.65
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            TextInput:
                id: password
                hint_text: "Password"
                password:True
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
                text:'Login'
                size_hint: (0.15, 1/17)
                pos_hint: {'center_x': 0.21, 'y': 0.2}
                background_normal: 'UI/button_normal.png'
                background_down: 'UI/button_down.png'
                on_release:root.Login()
                
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
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.52}
                background_normal: 'UI/mainAd-query2.png'
                background_down: 'UI/mainAd-query-down2.png'
                on_release:root.manager.current = 'queryEm'

            Button:
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.35}
                background_normal: 'UI/mainAd-setting.png'
                background_down:'UI/mainAd-setting-down.png'
<<<<<<< HEAD
                on_release: root.manager.current = 'settingsEm'
=======
                on_release: root.ShiftToSetting()
>>>>>>> 255ddba7b2d2a0e826d45822caa6097a0f6a70f4
                
            Button:                                                 #主界面退出登录按钮
                size_hint: (0.29, 0.13)
                pos_hint: {'center_x': 0.82, 'y': 0.18}
                background_normal: 'UI/mainEm-exit.png'
                background_down:'UI/mainEm-exit-down.png'
                on_release: root.exit()
                
            Button:                                                 #主界面退出按钮
                text:'退出'
                size_hint: (0.12, 1/17)
                pos_hint: {'center_x': 0.08, 'y': 0.03}
                background_normal: 'UI/button1.png'
                background_down: 'UI/button2.png'
                on_release:root.close()

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
                on_release: root.export()

                

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
                password:True
                password_mask:'●'
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
                password:True
                password_mask:'●'
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
                password:True
                password_mask:'●'
                pos_hint: {'center_x': 0.57, 'y': 0.3}
                background_normal: 'UI/input_line.png'
                background_active: 'UI/white.png'

            # Label:
            #     font_size:20
            #     text: '验证码:'
            #     size_hint: (0.15, 0.04)
            #     pos_hint: {'center_x': 0.3, 'y': 0.2}

            Label:                       
                id: code
                size_hint: (0.2, 0.05)
                pos_hint: {'center_x': 0.57, 'y': 0.2}
                # background_normal: 'UI/input_line.png'
                # background_active: 'UI/white.png'
                
            #Image:
                #size_hint: (0.18, 0.1)
                #pos_hint: {'center_x': 0.47, 'y': 0.07}

            Button:
                text: '确认修改'
                size_hint: (0.15, 0.06)
                pos_hint: {'center_x': 0.80, 'y': 0.06}
                background_normal: 'UI/button_normal.png'
                background_down:'UI/button_down.png'
                on_release: root.ChangeInfo()

""")


class MyPopup(Popup):
    def modify(self, text):
        self.ids.button.text = text


class ScreenManager(ScreenManager):
    pass


class LoginScreen(Screen):
    def Login(self):
        id = self.ids.ID.text
        psw = self.ids.password.text
        a = 0
        if (id == ''):
            s = 'ID输入为空'
            p = MyPopup()
            p.modify(s)
            p.open()
            a = 1
        elif (psw == ''):
            s = '密码输入为空'
            p = MyPopup()
            p.modify(s)
            p.open()
            a = 1
        if (a == 0):
            res = emp.login(emp_id=id, psw=psw)
            if (res == 'success'):
                self.ids.ID.text = ""
                self.ids.password.text = ""
                self.manager.current = 'mainEm'
            elif (res == 'no such id'):  # 已修改为弹框
                # self.ids.boarder.text = "no such id"
                s = 'no such id'
                p = MyPopup()
                p.modify(s)
                p.open()
            elif (res == 'wrong password'):
                # self.ids.boarder.text = 'wrong password'                                    #已修改为弹框
                s = 'wrong password'
                p = MyPopup()
                p.modify(s)
                p.open()


class MainEmScreen(Screen):
    def ShiftToSetting(self):
        self.manager.current = 'settingsEm'
        s = self.manager.get_screen('settingsEm')
        info = emp.get_info()
        s.ids.ID.text = info[1]
        s.ids.name.text = info[0]
        s.ids.apartment.text = info[2]

    def exit(self):
        self.manager.current = 'loginem'

    def close(self):
        Window.close()


class QueryEmScreen(Screen):
    record = []
    time = ''

    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainEm"
        self.manager.transition = SlideTransition(direction="left")

    def Query(self):
        year = self.ids.Year.text
        month = self.ids.Month.text
        QueryEmScreen.time = year + '-' + month
        res = emp.get_record_and_state(QueryEmScreen.time)
        print(res)
        if (res == 'None'):
            self.ids.late.text = '0'
            self.ids.off.text = '0'
            self.ids.early.text = '0'
            self.ids.normal.text = '0'
            self.ids.list.item_strings = []
        else:
            r = res[1:-1]
            comp = re.split(r"[(](.*?)[)]", r)
            date = re.findall('\d+', comp[-1])

            self.ids.late.text = date[1]
            self.ids.off.text = date[3]
            self.ids.early.text = date[2]
            self.ids.normal.text = date[0]

            for i in range(len(comp)):
                if i % 2 == 1:
                    comp[i] = comp[i].replace("'", '')
                    QueryEmScreen.record.append(comp[i])
            self.ids.list.item_strings = QueryEmScreen.record
            info = emp.get_info()
            self.ids.name.text = info[1] + ',' + info[0] + ',' + info[2]

    def export(self):
        l = self.manager.get_screen('loginem')
        id = l.ids.ID.text
        record = QueryEmScreen.record
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet1")
        for i in range(len(record)):
            item = record[i].split(',')
            for j in range(len(item)):
                sheet.write(i, j, item[j])
        if not record == []:
            wbk.save("../ExportFile/" + id + '_' + QueryEmScreen.time + ".xls")


class SettingsEmScreen(Screen):
    def on_touch_move(self, touch):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "mainEm"
        self.manager.transition = SlideTransition(direction="left")

    def ChangeInfo(self):
        ori_psw = self.ids.previousPass.text
        new_psw = self.ids.newPass.text
        iden_psw = self.ids.idetiNewPass.text
        if (ori_psw == ''):
            s = "请输入原密码"
            p = MyPopup()
            p.modify(s)
            p.open()
        elif (new_psw == ''):
            s = "请输入新密码"
            p = MyPopup()
            p.modify(s)
            p.open()
        elif (iden_psw == ''):
            s = "请确认新密码"
            p = MyPopup()
            p.modify(s)
            p.open()
        elif (new_psw == iden_psw):  # 已修改为弹框
            if (emp.change_psw(ori_psw, new_psw) == 'true'):
                # self.ids.code.text = "密码修改成功"
                s = "密码修改成功"
                p = MyPopup()
                p.modify(s)
                p.open()
            else:
                s = "原密码输入不正确"
                p = MyPopup()
                p.modify(s)
                p.open()
        else:  # 已修改为弹框
            # self.ids.code.text = '两次密码不一致'
            s = '两次密码不一致'
            p = MyPopup()
            p.modify(s)
            p.open()


class EmployeeApp(App):
    def build(self):
        Window.fullscreen = "auto"
        self.title = 'Employee'
        return ScreenManager()


# if __name__ == '__main__':
#    Config.set('graphics', 'width', '800')
#    Config.set('graphics', 'height', '600')

EmployeeApp().run()
