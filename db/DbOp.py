import DataBase
import datetime
import SetLogger
import time
import configparser
import calendar

db = DataBase.DataBase()
logger = SetLogger.logger

cf = configparser.ConfigParser()
cf.read("database.conf")
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
            if (la_rec[2] == 1):
                db.update(sql + "'0')")
            else:
                db.update(sql + "'1')")
    else:
        db.update(sql + "'" + str(int(not bool(last_rec[0][2]))) + "')")


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
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        re = sorted(re)
        la_rec = look_for(re, time2)
        if (la_rec == None):
            state += "1"
        else:
            if (la_rec[2] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[1][11:19] < time1 and last_rec[2] == 0):
            state += "1"
        else:
            state += "0"
    if(state=="1"):
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
            if (la_rec[2] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[2] == 1):
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
            if (la_rec[2] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[2] == 0):
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
            "select * from record_" + year + month + " where emp_id=" + emp_id)
        re = sorted(re)
        la_rec = look_for(re, time4)
        if (la_rec == None):
            state += "1"
        else:
            if (la_rec[2] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[1][11:19] < time3 and last_rec[2] == 0):
            state += "1"
        else:
            state += "0"
    if(state=="1"):
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
            if (la_rec[2] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[2] == 1):
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
            if (la_rec[2] == 1):
                state += "0"
            else:
                state += "1"
    else:
        if (last_rec[2] == 0):
            state += "1"
        else:
            state += "0"

    return state


def get_month_state_by_id(emp_id, time):
    year = str(time[0:4])
    month = str(time[5:7])

    record_state={}
    for i in range(31):
        state=am_state(emp_id,year+"-"+month+"-"+str(i+1)).zfill(2)\
              +pm_state(emp_id,year+"-"+month+"-"+str(i+1).zfill(2))
        record_state[i]=state

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


def test():
    re = db.query("select emp_department from empinfo where Emp_id='000001'")
    print(re[0][0])
