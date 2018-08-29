import DataBase
import datetime
import SetLogger
import time
import configparser
import calendar

db = DataBase.DataBase()
logger = SetLogger.logger


def get_all_record_table():
    return db.query("SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema='facepro' and table_name like 'record%'")


def update_record_emp(year=None, month=None):
    """更新当前月份及以后的考勤表,加入新的员工信息"""
    # 如果没有指定年月则使用当前日期
    if month is None:
        month = datetime.datetime.now().strftime('%m')
    if year is None:
        year = datetime.datetime.now().strftime('%Y')
        # 返回符合条件的表名

    record_tables = db.query("SELECT table_name FROM information_schema.tables "
                             "WHERE table_schema='facepro' and table_name like 'record%'"
                             "and table_name>='record_" + year + month + "_01'")
    # 两重循环插入员工信息
    emp_id = db.query("select emp_id from empinfo")
    for j in range(len(record_tables)):
        for i in range(len(emp_id)):
            flag = db.update("ALTER TABLE " + record_tables[j][0] + " ADD `" + emp_id[i][0] + "` varchar(5) NULL")
    return flag


def add_emp(_id, _name, _department, _psw, _photo):
    flag = db.update(
        "INSERT INTO `facepro`.`empinfo` (`Emp_id`, `Emp_name`, `Emp_department`, `password`, `Emp_photo`) "
        "VALUES ('" + _id + "','" + _name + "','" + _department + "','" + _psw + "','" + _photo + "')")


def create_record_table(year=None, month=None):
    """添加新的考勤表"""
    # 如果没有指定年月则使用当前日期
    if month is None:
        month = datetime.datetime.now().strftime('%m')
        day_now = time.localtime()
        wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
        day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
        days = day_end[8:10]
    if year is None:
        year = datetime.datetime.now().strftime('%Y')
    cf = configparser.ConfigParser()
    cf.read("database.conf")
    num = cf.get("record", "number")
    table_name = "record_" + year + month + "_"  # 缺少最后的num编号在循环中添加

    if(month[0]=="0"):
        month=month[1]
    monthRange = calendar.monthrange(int(year), int(month))
    days=monthRange[1]

    for i in range(int(num)):
        sql="CREATE TABLE "+table_name+str(i+1)+" (date int PRIMARY KEY NOT NULL)"
        db.update(sql)
        for j in range(int(days)):
            sql="INSERT INTO `facepro`."+table_name+str(i+1)+" (`date`) VALUES ('"+str(j+1)+"')"
            db.update(sql)

