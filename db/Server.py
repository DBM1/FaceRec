import sys
sys.path.append('../')
import socketserver
import configparser
import DbOp


def login(info):
    emp_id = info[1]
    psw = info[2]
    result = DbOp.login(emp_id, psw)
    return result


def change_psw(info):
    emp_id = info[1]
    ori_psw = info[2]
    new_psw = info[3]
    result = DbOp.change_psw(emp_id, ori_psw, new_psw)
    return result


def get_info(info):
    emp_id = info[1]
    result = DbOp.get_info(emp_id)
    return result


def get_info_by_name(info):
    emp_name = info[1]
    result = DbOp.get_info_by_name(emp_name)
    return result


def get_record_and_state(info):
    emp_id = info[1]
    time = info[2]
    result = DbOp.get_record_and_state(emp_id, time)
    return result


def add_emp_info(info):
    emp_id = info[1]
    emp_name = info[2]
    emp_department = info[3]
    emp_photo = info[4]
    result = DbOp.add_emp_info(emp_id, emp_name, emp_department, emp_photo)
    return result


def get_info_by_name(info):
    emp_name = info[1]
    result = DbOp.get_info_by_name(emp_name)
    return result


def get_except_record(info):
    time = info[1]
    num, result_record = DbOp.get_except_record(time)
    if num == 0:
        return str(result_record)
    result = str(num) + str(result_record)
    return result


def get_last_id(info):
    result=DbOp.get_last_id()
    return result


def add_record_info(info):
    emp_id=info[1]
    time=info[2]
    result=DbOp.add_record_info(emp_id,time)
    return result


class FaceProServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.send("1".encode())

        flag = True
        try:
            while flag:
                info = conn.recv(4096).decode()
                info = tuple(info.split(","))
                result = func[info[0]](info)
                conn.send(result.encode())

        except Exception as data:
            print(data)


if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("Server.conf")
    server_host = cf.get("Server", "host")
    server_port = int(cf.get("Server", "port"))

    func = {"login": login, "change_psw": change_psw, "get_info": get_info, "get_record": get_record_and_state,
            "add_emp_info": add_emp_info, "get_info_by_name": get_info_by_name, "get_except_record": get_except_record,
            "get_last_id":get_last_id,"add_record_info":add_record_info
            }

    socketserver.ThreadingTCPServer((server_host, server_port), FaceProServer).serve_forever()
