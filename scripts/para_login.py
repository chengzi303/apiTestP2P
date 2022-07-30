import logging
import random
import time
import unittest

import requests
from parameterized import parameterized

import app
from api.loginAPI import loginAPI
from utils import assert_utils, read_imgVerify_data, read_register_data, read_data

# img_file_name= app.BASE_DIR + "/data/imgVerify.json"
# img_data=read_imgVerify_data(img_file_name)
# register_file_name= app.BASE_DIR + "/data/register.json"
# register_data=read_register_data(register_file_name)
file_name=app.BASE_DIR + "/data/all.json"


class loginTest_para(unittest.TestCase):
    phone1 = "15688886618"
    phone2 = "15688886613"
    # phone3 = "15688886614"
    # phone4 = "15688886615"
    phone5 = "15688886616"
    imgVerifyCode1 = "8888"
    password1="a123456"

    def setUp(self) -> None:
        # 实例化loginAPI
        self.login_api=loginAPI()
        # 实例化session
        self.session=requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 获取图片验证码
    @parameterized.expand(read_data(file_name,"test_imgVerify","type,status_code"))
    def test01_get_img_verify(self, type, status_code):
        r = ''
        # 根据不同类型，准备不同参数数据
        if type == "float":
            r = str(random.random())
        elif type == "int":
            r = str(random.randint(100000000,900000000))
        elif type == "string":
            rand = random.sample("abcdefghijklmn",8)
            r = "".join(rand)
        # 发送请求
        response = self.login_api.getImgCode(self.session, r)
        # 接收接口返回结果，进行断言
        self.assertEqual(status_code,response.status_code)


    # 参数正确，获取短信验证码成功
    def test05_getSms_success(self):
        # 1、获取图片验证码
        # 定义参数（随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数（正确的手机号、验证码）
        # 调用获取短信验证码的接口
        response=self.login_api.getSms(self.session, self.phone1,self.imgVerifyCode1)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self,response,200,200,"短信发送成功")

    # 图片验证码错误，获取短信验证码失败
    def test06_getSms_imgCode_error(self):
        # 1、获取图片验证码
        # 定义参数（随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数（错误的验证码）
        error_code="1111"
        # 调用获取短信验证码的接口
        response = self.login_api.getSms(self.session, self.phone1, error_code)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 手机号为空，获取短信验证码失败
    def test07_getSms_phone_is_null(self):
        # 1、获取图片验证码
        # 定义参数（随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数（手机号为空）
        # 调用获取短信验证码的接口
        response = self.login_api.getSms( self.session, "", self.imgVerifyCode1)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        self.assertEqual(200,response.status_code)
        self.assertEqual(100,response.json().get("status"))

    # 图片验证码为空，获取短信验证码失败
    def test08_getSms_imgCode_is_null(self):
        # 1、获取图片验证码
        # 定义参数（随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数（图片验证码为空）
        # 调用获取短信验证码的接口
        response = self.login_api.getSms(self.session, self.phone1, "")
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 未调用图片验证码，参数正确，获取短信验证码失败
    def test09_getSms_no_use_ImgCode(self):
        # 1、未调用图片验证码
        # 2、获取短信验证码
        # 定义参数（正确的手机号、验证码）
        # 调用获取短信验证码的接口
        response = self.login_api.getSms(self.session, self.phone1, self.imgVerifyCode1 )
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 注册，参数化方式
    @parameterized.expand(read_data(file_name,"test_register","phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description"))
    def test10_register(self,  phone, password, verifycode, phone_code, dy_server, invite_phone, status_code, status, description):
        # 1、获取图片验证码
        # 定义参数（随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数（正确的手机号、验证码）
        # 调用获取短信验证码的接口
        response = self.login_api.getSms(self.session, phone, imgVerifyCode='8888')
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 使用参数化的数据进行注册，并返回对应的结果
        response = self.login_api.register(self.session, phone, password, verifycode, phone_code, dy_server, invite_phone)
        logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, status_code, status, description)

    # 参数正确，登录成功
    def test17_login_success(self):
        # 定义参数(参数正确)
        # 调用登录的接口
        response=self.login_api.login(self.session)
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self,response, 200, 200, "登录成功")

    # 用户不存在，登录失败
    def test18_login_user_is_not_exist(self):
        # 定义参数(用户不存在)
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone5, password="a123456")
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "用户不存在")

    # 密码为空，登录失败
    def test19_login_password_is_null(self):
        # 定义参数(密码为空)
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone2, password="")
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 密码错误1/2/3次，
    def test20_login_password_error(self):
        # 1、密码错误1次，提示
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone1, password="error")
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")

        # 2、密码错误2次
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone1, password="error")
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")

        # 3、密码错误3次
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone1, password="error")
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        # 4、密码错误3次，未等待1分钟后，填写参数正确，登录失败
        # 调用登录的接口
        response=self.login_api.login(self.session, keywords=self.phone1 ,password=self.password1)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self,response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")

        time.sleep(60)
        # 5、密码错误3次，等待1分钟后，填写参数正确，登录成功
        # 调用登录的接口
        response=self.login_api.login(self.session, keywords=self.phone1,password=self.password1)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")




