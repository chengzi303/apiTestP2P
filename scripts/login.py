import logging
import random
import time
import unittest

import requests

from api.loginAPI import loginAPI
from utils import assert_utils


class loginTest(unittest.TestCase):
    phone1 = "15688886618"
    phone2 = "15688886613"
    phone3 = "15688886614"
    phone4 = "15688886615"
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

    # 随机小数，获取图片验证码成功
    def test01_getImgCode_random_float(self):
        # 定义参数（随机小数）
        r=random.random()
        # 调用接口类中的接口
        response=self.login_api.getImgCode(self.session,str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200,response.status_code)

    # 随机整数，获取图片验证码成功
    def test02_getImgCode_random_int(self):
        # 定义参数（随机整数）
        r=random.randint(100000000,900000000)
        # 调用接口类中的接口
        response=self.login_api.getImgCode(self.session,str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200,response.status_code)

    # 参数为空，获取图片验证码失败
    def test03_getImgCode_no_para(self):
        # 定义参数（无）
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, "")
        # 接收接口返回结果，进行断言
        self.assertEqual(404, response.status_code)

    # 参数为字母，获取图片验证码失败
    def test04_getImgCode_string(self):
        # 定义参数（随机字母）
        r=random.sample("abcdefghijklmn",10)
        rand="".join(r)
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, rand)
        # 接收接口返回结果，进行断言
        self.assertEqual(400,response.status_code)

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
        response = self.login_api.getSms(self.session, self.phone1, self.imgVerifyCode1)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")

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
        error_code = "1111"
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
        response = self.login_api.getSms(self.session, "", self.imgVerifyCode1)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

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
        response = self.login_api.getSms(self.session, self.phone1, self.imgVerifyCode1)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "图片验证码错误")

    # 正确填写仅必填参数，注册成功
    def test10_register_success(self):
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
        response = self.login_api.getSms(self.phone1, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（正确填写仅必填参数）
        # 调用注册的接口
        response=self.login_api.register(self.session, self.phone1, self.password1)
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "注册成功")

    # 正确填写所有参数，注册成功
    def test11_register_success_all(self):
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
        response = self.login_api.getSms(self.phone2, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（正确填写所有参数，注册成功）
        # 调用注册的接口
        response = self.login_api.register(self.session, self.phone2, self.password1, invite_phone="13012345678")
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "注册成功")

    # 图片验证码错误，注册失败
    def test12_register_imgCode_error(self):
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
        response = self.login_api.getSms(self.phone3, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（图片验证码错误，注册失败）
        # 调用注册的接口
        response = self.login_api.register(self.session, self.phone3, self.password1, verifycode='1111')
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "验证码错误!")


    # 短信验证码错误，注册失败
    def test13_register_Sms_error(self):
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
        response = self.login_api.getSms(self.phone3, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（短信验证码错误，注册失败）
        # 调用注册的接口
        response = self.login_api.register(self.session, self.phone3, self.password1, phone_code='111111')
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "验证码错误")


    # 手机已存在，注册失败
    def test14_register_phone_is_exist(self):
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
        response = self.login_api.getSms(self.phone1, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（手机已存在，注册失败）
        # 调用注册的接口
        response = self.login_api.register(self.session, self.phone1, self.password1)
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "手机已存在!")

    # 密码为空，注册失败(bug)
    def test15_register_password_is_null(self):
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
        response = self.login_api.getSms(self.phone3, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（密码为空，注册失败）
        # 调用注册的接口
        response = self.login_api.register(self.session, self.phone3, password="")
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 未勾选请同意我们的条款，注册失败(bug)
    def test16_register_disagree_protocol(self):
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
        response = self.login_api.getSms(self.phone4, self.imgVerifyCode1, self.session)
        # logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（未勾选请同意我们的条款，注册失败）
        # 调用注册的接口
        response = self.login_api.register(self.session, self.phone4, self.password1, dy_server='off')
        # logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 100, "请同意我们的条款")

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




