import pymysql
import configparser
import SetLogger
import os

# 从配置文件中读取数据库参数
DB = "database"
cf = configparser.ConfigParser()
cf.read(os.path.dirname(os.getcwd())+"\config.conf")
db_host = cf.get(DB, "db_host")
db_port = cf.get(DB, "db_port")
db_user = cf.get(DB, "db_user")
db_psw = cf.get(DB, "db_psw")
db_name = cf.get(DB, "db_name")

class DataBase:
    """mysql数据库类
    封装sql的基本操作"""

    def __init__(self, dbname=None, dbhost=None):
        """初始化函数,提供默认构造参数,dbname数据库名,dbhost主机地址"""
        self._logger = SetLogger.logger
        self._logger.info("database class is creating...")
        if dbname is None:
            self._dbname = db_name
        else:
            self._dbname = dbname
        if dbhost is None:
            self._dbhost = db_host
        else:
            self._dbhost = db_host

        self._dbport = db_port
        self._dbuser = db_user
        self._dbpsw = db_psw

        """数据库连接"""
        self._conn = self.connect()
        self._cursor = self._conn.cursor()

    def connect(self):
        try:
            conn = pymysql.connect(host=self._dbhost,  # 主机地址
                                   user=self._dbuser,  # 用户名
                                   password=self._dbpsw,  # 密码
                                   db=self._dbname)  # 数据库名

        except Exception as data:
            self._logger.error("connect database failed, %s" % data)
            conn = False
        self._logger.info("database is connecting...")
        return conn

    def query(self, sql):
        """获取结果集"""
        self._logger.info(sql)
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
        except Exception as data:
            result = False
            self._logger.error("query database exception, %s" % data)

        return result

    def update(self, sql):
        self._logger.info(sql)
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            self.close()
            self._conn = self.connect()
            self._cursor = self._conn.cursor()
            flag = True
        except Exception as data:
            if (str(data)[1:5] == '1060'):
                flag = True
            else:
                flag = False
                self._logger.error("update database exception, %s" % data)
        return flag

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as data:
            self._logger.error("close database exception, %s, %s, %s"
                               % (data, type(self._cursor), type(self._conn)))
        self._logger.debug("database is closing")
