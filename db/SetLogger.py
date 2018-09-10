import configparser
import logging
import time
import os.path


# 设置日志输出
cf = configparser.ConfigParser()
cf.read(os.path.dirname(os.getcwd())+"\config.conf")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logpath = cf.get("path", "logpath")
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + logpath + "\database"
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
