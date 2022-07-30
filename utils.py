# 定义断言公用方法
import json
import logging

import pymysql
import requests
from bs4 import BeautifulSoup



# 定义断言方法
import app


def assert_utils(self,response,status_code,status,desc):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))

# 定义第三方接口api
# 从form_data获取url/data，发送第三方接口请求，返回响应结果
def third_request_api(form_data):
    # 解析form表单的内容，并提取第三方请求的参数（url、data)
    soup = BeautifulSoup(form_data, 'html.parser')
    third_url = soup.form['action']
    logging.info('third request url={}'.format(third_url))
    data = {}
    for i in soup.find_all('input'):
        # 给字典赋值
        data.setdefault(i['name'], i['value'])
    logging.info('third request data={}'.format(data))
    # 发送第三方开户的接口请求
    response = requests.post(url=third_url, data=data)
    logging.info('third trust response={}'.format(response.text))
    return response


# 定义执行数据库sql语句的类
class DButils:
    @classmethod
    def get_conn(cls, db_name):
        conn=pymysql.connect(user=app.BASE_DB_USER_NAME,
                             password=app.BASE_DB_PASSWORD,
                             host=app.BASE_DB_HOST,
                             port=app.BASE_DB_PORT,
                             database=db_name,
                             charset="utf-8",
                             autocommit=True)
        return conn

    @classmethod
    def close(cls, cursor, conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls, db_name, sql):
        conn=None
        cursor=None
        try:
            conn= cls.get_conn(db_name)
            cursor=conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor, conn)

# 定义读取图片验证码的数据方法
def read_imgVerify_data(file_name):
    with open(file_name,encoding="utf-8") as f:
        verify_data=json.load(f)
        list_data=[]
        for d in verify_data.values():
            list_data.append((d.get("type"),d.get("status_code")))
        print("json_data={}".format(list_data))
        return list_data

# file_name=app.BASE_DIR + "/data/imgVerify.json"
# read_imgVerify_data(file_name)

# 定义读取注册的数据方法
def read_register_data(file_name):
    with open(file_name,encoding="utf-8") as f:
        register_data=json.load(f)
        list_data=[]
        for d in register_data.values():
            list_data.append((d.get("phone"),
                              d.get("password"),
                              d.get("verifycode"),
                              d.get("phone_code"),
                              d.get("dy_server"),
                              d.get("invite_phone"),
                              d.get("status_code"),
                              d.get("status"),
                              d.get("description")))
    print("json_data={}".format(list_data))
    return list_data

# register_file_name= app.BASE_DIR + "/data/register.json"
# register_data=read_register_data(register_file_name)

# 定义读取所有数据的方法
def read_data(file_name, method_name, param_names):
    """
    :param file_name: 数据文件名
    :param method_name: 测试数据列表名，如test_imgVerify
    :param param_names: 测试数据所有参数组成的字符串，"type,status_code"
    :return:
    """
    # 读取获取测试数据的所有列表
    with open(file_name,encoding="utf-8") as f:
        file_data=json.load(f)
        test_case_data=[]
        test_data_list = file_data.get(method_name)
        for test_data in test_data_list:
            test_params=[]
            for para in param_names.split(','):
                test_params.append(test_data.get(para))
            test_case_data.append(tuple(test_params))
    print(test_case_data)
    return test_case_data

# file_name= app.BASE_DIR + "/data/all.json"
# method_name="test_imgVerify"
# test_params="type,status_code"
# read_data(file_name,method_name,test_params)
#
# file_name= app.BASE_DIR + "/data/all.json"
# method_name="test_register"
# test_params="phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description"
# read_data(file_name,method_name,test_params)
#
# read_data(file_name,"test_register","phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description")