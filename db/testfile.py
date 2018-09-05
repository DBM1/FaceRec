import DbOp
import datetime

time=datetime.datetime.now()
time=str(time)[0:19]
#DbOp.add_record_info("000002","2018-08-29 13:48:34")
# print(DbOp.am_state("111111","2018-08-31"))


DbOp.get_except_record("2018-08")







# import calendar
# str="09"
# int=int(str)
# print(int)
# monthRange = calendar.monthrange(2016,9)
# print(monthRange)

# DbOp.create_record_table("2018-09")

#DbOp.test()

# print(DbOp.get_record_by_id("111111","2018-08-31"))

# a=DbOp.get_month_state_by_id("111111","2018-08-28")
# print(a)
# DbOp.log_in("000001","pw1")
