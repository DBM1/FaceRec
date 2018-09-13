import DataBase
import datetime
import SetLogger
import time
import configparser
import calendar
import os

db = DataBase.DataBase()
logger = SetLogger.logger

cf = configparser.ConfigParser()
cf.read(os.path.dirname(os.getcwd()) + "\config.conf")
time1 = cf.get("work_time", "time1")
time2 = cf.get("work_time", "time2")
time3 = cf.get("work_time", "time3")
time4 = cf.get("work_time", "time4")
time5 = cf.get("work_time", "time5")


def add_record_info(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])
    day = str(time[8:10])

    new_date = year + "-" + month + "-" + day
    department = db.query("select emp_department from empinfo where Emp_id='" + emp_id + "'")[0][0]

    result = db.query(
        "select * from record_" + year + month + " where emp_id=" + emp_id + " and time like '" + new_date + "%'")
    if result==():
        return "False"
    result = sorted(result)
    sql = "INSERT INTO `facepro`.`record_" + year + month + "` (`emp_id`, `time`,`department`, `state`) " \
                                                            "VALUES ('" + emp_id + "', '" + time + "','" + department + "',"

    last_rec = look_for(result, time1)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        la_rec = look_for(re)
        if (la_rec == None):
            db.update(sql + "'1')")
        else:
            if (la_rec[3] == 1):
                db.update(sql + "'0')")
            else:
                db.update(sql + "'1')")
    else:
        db.update(sql + "'" + str(int(not bool(last_rec[0][3]))) + "')")
    return "True"


def update_record(time=str(datetime.datetime.now())):
    year = str(time[0:4])
    month = str(time[5:7])
    day = str(time[8:10])

    if int(day) > 1:
        last_day = str(int(day) - 1)
        last_month = month
        last_year = year
    else:
        if int(month) > 1:
            last_month = str(int(month) - 1)
            last_day = str(calendar.monthrange(int(year), int(month))[1])
            last_year = year
        else:
            last_year = str(int(year) - 1)
            last_month = str(12)
            last_day = str(31)

    last_record = db.query("select * from record_" + last_year + last_month + " where time like "
                                                                              "'" + last_year + "-" + last_month + "-" + last_day + "%' and state=1")
    for i in last_record:
        db.update("INSERT INTO `facepro`.`record_" + year + month + "` (`emp_id`, `time`,`department`, `state`) "
                                                                    "VALUES ('" + i[0] + "', '" + time[0:19] + "','" +
                  i[2] + "'," + "1")


def update_am():
    time = str(datetime.datetime.now())
    year = str(time[0:4])
    month = str(time[5:7])
    day = str(time[8:10])

    emp = db.query("select * from empinfo")
    for i in emp:
        new_date = year + "-" + month + "-" + day
        result = db.query(
            "select * from record_" + year + month + " where emp_id=" + i[0] + " and time like '" + new_date + "%'")
        result = sorted(result)

        last_rec = look_for(result, time2)
        if last_rec == ():
            # 旷工
            db.update("INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                        "VALUES ('" + i[
                          0] + "', '" + new_date + "', '" + i[2] + "', '3')")
        else:
            la_rec = look_for(result, time1)
            if la_rec == ():
                db.update(
                    "INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                      "VALUES ('" + i[0] + "', '" + result[0][
                        1] + "', '" + i[2] + "', '1')")
            if last_rec[3] == 0:
                db.update(
                    "INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                      "VALUES ('" + i[0] + "', '" + last_rec[
                        3] + "', '" + i[2] + "', '2')")


def update_pm():
    time = str(datetime.datetime.now())
    year = str(time[0:4])
    month = str(time[5:7])
    day = str(time[8:10])
    emp = db.query("select * from empinfo")
    for i in emp:
        new_date = year + "-" + month + "-" + day
        result = db.query(
            "select * from record_" + year + month + " where emp_id=" + i[0] + " and time like '" + new_date + "%'")
        result = sorted(result)

        last_rec = look_for(result, time4)
        if last_rec == ():
            # 旷工
            db.update("INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                        "VALUES ('" + i[
                          0] + "', '" + new_date + "', '" + i[2] + "', '3')")
        else:
            if last_rec[1] < new_date + " " + time3:
                # 旷工
                if last_rec[3] == 0:
                    db.update(
                        "INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                          "VALUES ('" + i[
                            0] + "', '" + new_date + "', '" + i[2] + "', '3')")
                else:
                    # 正常
                    pass
            else:
                if last_rec[3] == 0:
                    # 早退
                    db.update(
                        "INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                          "VALUES ('" + i[0] + "', '" + last_rec[
                            3] + "', '" + i[2] + "', '2')")
                la_rec = look_for(result, time3)
                if la_rec == ():
                    # 迟到
                    db.update(
                        "INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                          "VALUES ('" + i[0] + "', '" + result[0][
                            1] + "', '" + i[2] + "', '1')")
                else:
                    if last_rec[3] == 1:
                        pass
                    else:
                        db.update(
                            "INSERT INTO `facepro`.`except_" + year + month + "` (`emp_id`, `time`, `department`, `state`) "
                                                                              "VALUES ('" + i[0] + "', '" + result[0][
                                1] + "', '" + i[2] + "', '1')")


def look_for(result, ed_time="23:59:59"):
    # print(result[0])
    last_rec = None
    for i in result:
        if (i[1][11:19] <= ed_time):
            last_rec = i
        else:
            break
    return last_rec


def create_record_table(time):
    last_year = year = str(time[0:4])
    last_month = month = str(time[5:7])
    if (int(month) - 1 > 0):
        last_month = str(int(month) - 1).zfill(2)
    else:
        last_year = str(int(year) - 1)
        last_month = "12"

    # 复制表结构
    db.update("create table record_" + year + month + " like record_201808")

    # 处理跨月问题
    emp = db.update("insert into record_" + year + month + "(emp_id,time,department,state) "
                                                           "select emp_id,time,department,state from record_" + last_year + last_month + " where state=1;")


def get_record_by_id(emp_id, time=None):
    year = str(time[0:4])
    month = str(time[5:7])
    result = db.query("select * from record_" + year + month + " where emp_id=" + emp_id)
    if result == ():
        return "None"
    return result


def get_record_by_depart(department, time=None):
    year = str(time[0:4])
    month = str(time[5:7])
    result = db.query("select * from record_" + year + month + " where emp_id=" + department)
    if result == ():
        return "None"
    return result


def get_record_by_name(name, time=None):
    year = str(time[0:4])
    month = str(time[5:7])
    result = db.query("select * from record_" + year + month + " where emp_id=" + name)
    if result == ():
        return "None"
    return result


def login(emp_id, psw):
    check_id = db.query("select * from empinfo where Emp_id=" + emp_id)
    if check_id == ():
        return "no such id"
    else:
        check_psw = db.query("select password from empinfo where Emp_id=" + emp_id)
        if check_psw[0][0] == psw:
            return "success"
        else:
            return "wrong password"


def add_emp_info(emp_id, emp_name, emp_department, emp_photo):
    db.update("INSERT INTO `facepro`.`empinfo` (`Emp_id`, `Emp_name`, `Emp_department`, `password`, `Emp_photo`) "
              "VALUES ('" + emp_id + "', '" + emp_name + "', '" + emp_department + "', '" + emp_id + "', '" + emp_photo + "')")
    return "true"


def get_record_and_state(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])
    re = db.query("SELECT table_name FROM information_schema.TABLES WHERE table_name ='record_" + year + month + "'")
    if re == ():
        return "None"

    monthRange = calendar.monthrange(int(year), int(month))

    record = get_record_by_id(emp_id, time)
    if record == ():
        return "None"
    except_record = db.query("select * from except_" + year + month + " where emp_id=" + emp_id)
    a, b, c, d = monthRange[1], 0, 0, 0
    for i in except_record:
        if i[3] == 1:
            b += 1
            a -= 1
        if i[3] == 2:
            c += 1
            a -= 1
        if i[3]:
            d += 1
            a -= 1

    state = str(a) + "," + str(b) + "," + str(c) + "," + str(d)
    state = tuple(state.split(","))
    result = record + state
    result = str(result)
    return result


def get_info(emp_id):
    result = db.query("select * from empinfo where Emp_id=" + emp_id)
    if result == ():
        return "None"
    result = result[0]
    re = result[0] + "," + result[1] + "," + result[2] + "," + result[3] + "," + result[4]
    return re


def change_psw(emp_id, ori_psw, new_psw):
    check_psw = db.query("select password from empinfo where Emp_id=" + emp_id)
    print(check_psw)
    if check_psw[0][0] == ori_psw:
        db.update("update empinfo set password='" + new_psw + "' where emp_id='" + emp_id + "'")
        return "true"
    else:
        return "wrong psw"


def get_info_by_name(emp_name):
    result = db.query("select * from empinfo where Emp_name='" + emp_name + "'")
    if result == ():
        return "None"
    re = ""
    for i in result:
        re += i[0] + "," + i[1] + "," + i[2] + "," + i[3] + "," + i[4] + ","
    return re


def get_except_record(time):
    year = str(time[0:4])
    month = str(time[5:7])

    re = db.query("SELECT table_name FROM information_schema.TABLES WHERE table_name ='record_" + year + month + "'")
    if re == ():
        return 0, "None"

    result = db.query("select * from except_" + year + month)
    re = ()
    for i in result:
        re += i
    num = len(result)
    result = str(num) + str(re)
    print(num, result)
    return num, result


def get_last_id():
    result=db.query("select * from empinfo")
    result=str(int(result[-1][0])+1).zfill(6)
    return result


# def test():
#     emp = db.query("select * from empinfo")
#     for j in emp:
#         for i in range(31):
#             db.update("INSERT INTO `facepro`.`record_201808` (`emp_id`, `time`,`department`, `state`) "
#                       "VALUES ('" + j[0] + "', '2018-08-" + str(i + 1).zfill(2) + " 08:00:00','department',1)")
#             db.update("INSERT INTO `facepro`.`record_201808` (`emp_id`, `time`,`department`, `state`) "
#                       "VALUES ('" + j[0] + "', '2018-08-" + str(i + 1).zfill(2) + " 11:40:00','department',0)")
#             db.update("INSERT INTO `facepro`.`record_201808` (`emp_id`, `time`,`department`, `state`) "
#                       "VALUES ('" + j[0] + "', '2018-08-" + str(i + 1).zfill(2) + " 13:30:00','department',1)")
#             db.update("INSERT INTO `facepro`.`record_201808` (`emp_id`, `time`,`department`, `state`) "
#                       "VALUES ('" + j[0] + "', '2018-08-" + str(i + 1).zfill(2) + " 18:00:00','department',0)")
#         print(j[0] + "," + str(i + 1))
