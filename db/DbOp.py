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


def look_for(result, ed_time="23:59:59"):
    # print(result[0])
    last_rec = None
    for i in result:
        if (i[1][11:19] <= ed_time):
            last_rec = i
        else:
            break
    return last_rec


def am_state(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])
    day = str(time[8:10])

    new_date = year + "-" + month + "-" + day
    result = db.query(
        "select * from record_" + year + month + " where emp_id=" + emp_id + " and time like '" + new_date + "%'")
    result = sorted(result)
    state = ""

    # 是否旷工
    last_rec = look_for(result, time2)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id + " and time<'" + new_date + "'")
        re = sorted(re)
        la_rec = look_for(re)
        if (la_rec == None):
            state += "1"
        else:
            if (la_rec[3] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[1][11:19] < time1 and last_rec[3] == 0):
            state += "1"
        else:
            state += "0"
    if (state == "1"):
        return "111"

    # 是否迟到
    last_rec = look_for(result, time1)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        re = sorted(re)
        la_rec = look_for(re, time1)
        if (la_rec == None):
            state += "1"
        else:
            if (la_rec[3] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[3] == 1):
            state += "0"
        else:
            state += "1"

    # 是否早退
    last_rec = look_for(result, time2)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        re = sorted(re)
        la_rec = look_for(re, time2)
        if (la_rec == None):
            state += "0"
        else:
            if (la_rec[3] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[3] == 0):
            state += "1"
        else:
            state += "0"

    return state


def pm_state(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])
    day = str(time[8:10])

    new_date = year + "-" + month + "-" + day
    result = db.query(
        "select * from record_" + year + month + " where emp_id=" + emp_id + " and time like '" + new_date + "%'")
    result = sorted(result)
    state = ""

    # 是否旷工
    last_rec = look_for(result, time4)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id + " and time<'" + new_date + "'")
        re = sorted(re)
        la_rec = look_for(re)
        if (la_rec == None):
            state += "1"
        else:
            if (la_rec[3] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[1][11:19] < time3 and last_rec[3] == 0):
            state += "1"
        else:
            state += "0"
    if (state == "1"):
        return "111"

    # 是否迟到
    last_rec = look_for(result, time3)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        re = sorted(re)
        la_rec = look_for(re, time3)
        if (la_rec == None):
            state += "1"
        else:
            if (la_rec[3] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[3] == 1):
            state += "0"
        else:
            state += "1"

    # 是否早退
    last_rec = look_for(result, time4)
    if (last_rec == None):
        re = db.query(
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        re = sorted(re)
        la_rec = look_for(re, time4)
        if (la_rec == None):
            state += "0"
        else:
            if (la_rec[3] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[3] == 0):
            state += "1"
        else:
            state += "0"

    return state


def get_month_state_by_id(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])

    record_state = {}
    for i in range(31):
        state = am_state(emp_id, year + "-" + month + "-" + str(i + 1).zfill(2)) + \
                pm_state(emp_id, year + "-" + month + "-" + str(i + 1).zfill(2))
        record_state[i + 1] = state

    return record_state


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
    return result


def get_record_by_depart(department, time=None):
    year = str(time[0:4])
    month = str(time[5:7])
    result = db.query("select * from record_" + year + month + " where emp_id=" + department)
    return result


def get_record_by_name(name, time=None):
    year = str(time[0:4])
    month = str(time[5:7])
    result = db.query("select * from record_" + year + month + " where emp_id=" + name)
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


def add_emp_info(emp_id,emp_name,emp_department,emp_photo):
    db.update("INSERT INTO `facepro`.`empinfo` (`Emp_id`, `Emp_name`, `Emp_department`, `password`, `Emp_photo`) "
              "VALUES ('"+emp_id+"', '"+emp_name+"', '"+emp_department+"', '"+emp_id+"', '"+emp_photo+"')")
    return "true"


def get_record_and_state(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])
    monthRange = calendar.monthrange(int(year), int(month))

    record = get_record_by_id(emp_id, time)
    state = get_month_state_by_id(emp_id, time)
    a, b, c, d = 0, 0, 0, 0  # 对应正常,迟到,早退,旷工
    for i in range(monthRange[1]):
        x = state[i + 1]
        if x[0] == '1' or x[3] == '1':
            d += 1
        else:
            if x[1] == '1' or x[4] == '1':
                b += 1
            if x[2] == '1' or x[5] == '1':
                c += 1
            if x[0:3] == '000' and x[3:6] == '000':
                a += 1

    state = str(a) + "," + str(b) + "," + str(c) + "," + str(d)
    state = tuple(state.split(","))
    result = record + state
    result = str(result)
    return result


def get_info(emp_id):
    result = db.query("select * from empinfo where Emp_id=" + emp_id)
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
    result = db.query("select * from empinfo where Emp_name='" + emp_name+"'")
    if result==():
        return "None"
    re = ""
    for i in result:
        re += i[0] + "," + i[1] + "," + i[2] + "," + i[3] + "," + i[4] + ","
    return re


def get_except_record(time):
    year = str(time[0:4])
    month = str(time[5:7])
    monthRange = calendar.monthrange(int(year), int(month))

    result_record=()
    emp=db.query("select * from empinfo")
    num=0
    for i in emp:
        for j in range(monthRange[1]):
            print(j)
            day=str(j+1).zfill(2)
            new_date = year + "-" + month + "-" + day
            result = db.query(
                "select * from record_" + year + month + " where emp_id=" + i[0] + " and time like '" + new_date + "%'")
            result = sorted(result)
            state = ""

            # 是否旷工
            last_rec = look_for(result, time2)
            if (last_rec == None):
                re = db.query(
                    "select * from record_" + year + month + " where emp_id=" + i[0] + " and time<'" + new_date + "'")
                re = sorted(re)
                la_rec = look_for(re)
                if (la_rec == None):
                    result_record=result_record+(i[0],new_date,i[2],"1")
                    num+=1
                else:
                    """"""
                    if (la_rec[3] == 0):
                        result_record += (i[0], new_date, i[2], "1")
                        num += 1
            else:
                if (last_rec[1][11:19] < time1 and last_rec[3] == 0):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1

            #print(result_record)
            # 迟到
            last_rec = look_for(result, time1)
            if (last_rec == None):
                re = db.query(
                    "select * from record_" + year + month + " where emp_id=" + i[0])
                re = sorted(re)
                la_rec = look_for(re, time1)
                if (la_rec == None):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1
                else:
                    if (la_rec[3] == 1):
                        pass
                    else:
                        result_record += (i[0], new_date, i[2], "1")
                        num += 1
            else:
                if (last_rec[3] == 1):
                    pass
                else:
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1

                # 是否早退
            last_rec = look_for(result, time2)
            if (last_rec == None):
                re = db.query(
                    "select * from record_" + year + month + " where emp_id=" + i[0])
                re = sorted(re)
                la_rec = look_for(re, time2)
                if (la_rec == None):
                    pass
                else:
                    if (la_rec[3] == 1):
                        pass
                    else:
                        result_record += (i[0], new_date, i[2], "1")
                        num += 1
            else:
                if (last_rec[3] == 0):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1
                else:
                    pass


            # 下午
            # 是否旷工
            last_rec = look_for(result, time4)
            if (last_rec == None):
                re = db.query(
                    "select * from record_" + year + month + " where emp_id=" + i[0] + " and time<'" + new_date + "'")
                re = sorted(re)
                la_rec = look_for(re)
                if (la_rec == None):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1
                else:
                    if (la_rec[3] == 1):
                        pass
                    else:
                        result_record += (i[0], new_date, i[2], "1")
                        num += 1
            else:
                if (last_rec[1][11:19] < time3 and last_rec[3] == 0):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1
                else:
                    pass


            # 是否迟到
            last_rec = look_for(result, time3)
            if (last_rec == None):
                re = db.query(
                    "select * from record_" + year + month + " where emp_id=" + i[0])
                re = sorted(re)
                la_rec = look_for(re, time3)
                if (la_rec == None):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1
                else:
                    if (la_rec[3] == 1):
                       pass
                    else:
                        result_record += (i[0], new_date, i[2], "1")
                        num += 1
            else:
                if (last_rec[3] == 1):
                    pass
                else:
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1

            # 是否早退
            last_rec = look_for(result, time4)
            if (last_rec == None):
                re = db.query(
                    "select * from record_" + year + month + " where emp_id=" + i[0])
                re = sorted(re)
                la_rec = look_for(re, time4)
                if (la_rec == None):
                    pass
                else:
                    if (la_rec[3] == 1):
                        pass
                    else:
                        result_record += (i[0], new_date, i[2], "1")
                        num += 1
            else:
                if (last_rec[3] == 0):
                    result_record += (i[0], new_date, i[2], "1")
                    num += 1
                else:
                    pass

    return num,result_record


def test():
    re = db.query("select emp_department from empinfo where Emp_id='000001'")
    print(re[0][0])
