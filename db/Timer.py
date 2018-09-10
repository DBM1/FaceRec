import DbOp
import datetime
import time

while True:
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        DbOp.update_record()
    if now.hour == 11 and now.minute == 30:
        DbOp.update_am()
    if now.hour == 17 and now.minute == 30:
        DbOp.update_pm()
    time.sleep(60)