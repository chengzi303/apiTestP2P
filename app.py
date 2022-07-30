#初始化日志配置
import logging
import time
from logging import handlers
import os

BASE_DIR=os.path.dirname(__file__)
BASE_URL="http://user-p2p-test.itheima.net/"
BASE_DB_HOST="52.83.144.39"
BASE_DB_PORT="3306"
BASE_DB_USER_NAME="root"
BASE_DB_PASSWORD="Itcast_p2p_20191228"
BASE_MEMBER="czbk_member"
BASE_FINANCE="czbk_finance"

def init_log_config():
    #1、初始化日志对象
    logger=logging.getLogger()
    #2、设置日志级别
    logger.setLevel(logging.INFO)
    #3、创建控制台日志处理器和文件日志处理器
    sh=logging.StreamHandler()
    # logfile=BASE_DIR+"/log/p2p-{}.log".format(time.strftime("%Y%m%d%H%M%S"))
    logfile=BASE_DIR+os.sep+"log"+os.sep+"p2p-{}.log".format(time.strftime("%Y%m%d%H%M%S"))
    fh=logging.handlers.TimedRotatingFileHandler(logfile,when="M",interval=5,backupCount=5,encoding="UTF-8")
    #4、设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter=logging.Formatter(fmt=fmt)
    #5、将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    #6、将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)