import socket
import configparser


class EmpClient:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read("Client.conf")
        self.server_host = self.cf.get("Server", "host")
        self.server_port = int(self.cf.get("Server", "port"))

        self.socket = socket.socket()
        self.socket.connect((self.server_host, self.server_port))
        self.conn = self.recv()
        self.emp_id = ""

    def send(self, info):
        self.socket.send(info.encode())

    def recv(self, size=1024):
        return self.socket.recv(size).decode()

    def connected(self):
        return self.conn

    def close(self):
        self.socket.close()

    def login(self, emp_id, psw):
        info = "login" + "," + emp_id + "," + psw
        self.send(info)
        result = self.recv()
        if result == "success":
            self.emp_id = emp_id
        return result

    def change_psw(self, ori_psw, new_psw, emp_id=None):
        if emp_id is None:
            emp_id = self.emp_id
        info = "change_psw," + emp_id + "," + ori_psw + "," + new_psw
        self.send(info)
        return self.recv()

    def get_info(self, emp_id=None):
        if emp_id is None:
            emp_id = self.emp_id

        info = "get_info," + emp_id
        self.send(info)
        result = self.recv()
        result = tuple(result.split(","))
        return result

    def get_record_and_state(self, time, emp_id=None):
        if emp_id is None:
            emp_id = self.emp_id

        info = "get_record," + emp_id + "," + time
        self.send(info)
        result = self.recv(102400)
        return result

    def add_emp_info(self,emp_id,emp_name,emp_department,emp_photo):
        info="add_emp_info,"+emp_id+","+emp_name+","+emp_department+","+emp_photo
        self.send(info)
        result=self.recv()
        return result

