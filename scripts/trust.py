import logging
import random
import unittest
import requests
from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from utils import assert_utils, third_request_api


class trust(unittest.TestCase):
    phone1 = "15688886637"
    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.trust_api=trustAPI()
        self.session=requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 发送开户请求，开户成功
    def test01_trust_register(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、发送开户请求
        # 调用开户的接口
        response = self.trust_api.trustRegister(self.session)
        logging.info("trust register response={}".format(response.json()))
        # 对响应结果断言
        self.assertEqual(200, response.status_code)
        # 3、发送第三方开户请求
        form_data=response.json().get('description').get('form')
        response=third_request_api(form_data)
        # 断言
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

    # 风险测评
    def test02_risk(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone1)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、发送风险测评请求
        # 调用风险测评的接口
        response=self.trust_api.risk(self.session)
        assert_utils(self, response, 200 ,200, "OK")
        self.assertEqual("提交成功", response.json().get("data"))

    # 随机数小数，获取充值验证码成功
    def test03_recharge_verifyCode_random_float(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、随机数小数，获取充值验证码成功
        # 定义参数（随机小数）
        r=random.random()
        # 调用接口类中的接口
        response=self.trust_api.recharge_verifyCode(self.session,str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)

    # 随机数整数，获取充值验证码成功
    def test04_recharge_verifyCode_random_int(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session, keywords=self.phone1)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、随机数整数，获取充值验证码成功
        # 定义参数（随机整数）
        r=random.randint(1000000, 9000000)
        # 调用接口类中的接口
        response=self.trust_api.recharge_verifyCode(self.session,str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)

    # 参数填写正确，充值成功
    def test05_recharge_success(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、随机数小数，获取充值验证码成功
        # 定义参数（随机小数）
        r=random.random()
        # 调用接口类中的接口
        response=self.trust_api.recharge_verifyCode(self.session,str(r))
        # logging.info("recharge verifyCode response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 3、参数填写正确，充值成功
        # 定义参数（参数填写正确）
        # 调用充值接口类中的接口
        response=self.trust_api.recharge(self.session)
        logging.info("recharge response={}".format(response.json()))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 4、发送第三方充值请求
        form_data=response.json().get("description").get("form")
        response=third_request_api(form_data)
        logging.info("third recharge response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual("NetSave OK", response.text)

    # 验证码错误，充值失败
    def test06_recharge_verifyCode_error(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、随机数小数，获取充值验证码成功
        # 定义参数（随机小数）
        r=random.random()
        # 调用接口类中的接口
        response=self.trust_api.recharge_verifyCode(self.session,str(r))
        # logging.info("recharge verifyCode response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 3、验证码错误，充值失败
        # 定义参数（验证码错误）
        # 调用接口类中的接口
        response=self.trust_api.recharge(self.session, valicode="1111")
        logging.info("recharge response={}".format(response.json()))
        # 接收接口返回结果，进行断言
        assert_utils(self, response, 200, 100, "验证码错误")

    # 验证码为空，充值失败
    def test07_recharge_verifyCode_is_null(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、随机数小数，获取充值验证码成功
        # 定义参数（随机小数）
        r=random.random()
        # 调用接口类中的接口
        response=self.trust_api.recharge_verifyCode(self.session,str(r))
        # logging.info("recharge verifyCode response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 3、验证码为空，充值失败
        # 定义参数（验证码为空）
        # 调用接口类中的接口
        response=self.trust_api.recharge(self.session, valicode="")
        logging.info("recharge response={}".format(response.json()))
        # 接收接口返回结果，进行断言
        assert_utils(self, response, 200, 100, "验证码错误")




