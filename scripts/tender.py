import logging
import unittest

import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from utils import assert_utils, third_request_api


class tender(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.tender_api=tenderAPI()
        self.session=requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 必填项填写正确，投资成功
    def test01_tender_success(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、必填项填写正确，投资成功
        # 调用投资的接口
        response = self.tender_api.tender(self.session)
        logging.info("tender response={}".format(response.json()))
        # 对响应数据断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 3、发送第三方投资请求
        form_data=response.json().get("description").get("form")
        response=third_request_api(form_data)
        logging.info("third tender response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual("InitiativeTender OK", response.text)

    # 投资金额为空，投资失败(bug)
    def test02_tender_amount_is_null(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、投资金额为空，投资失败
        # 调用投资的接口
        response = self.tender_api.tender(self.session, amount="")
        logging.info("tender response={}".format(response.json()))
        # 对响应数据断言
        assert_utils(self, response, 200, 100, "投资⾦额不能为空")

    # 投资产品详情
    def test03_tender_product_list(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、投资产品详情
        # 调用投资的接口
        response=self.tender_api.product_list(self.session)
        logging.info("tender product list response={}".format(response.json()))
        # 对响应数据断言
        assert_utils(self, response, 200, 200, "OK")

    # 查询投资产品列表成功
    def test04_tender_list(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、查询投资产品列表成功
        # 调用投资的接口
        response = self.tender_api.tender_list(self.session)
        logging.info("tender list response={}".format(response.json()))
        # 对响应数据断言
        self.assertEqual(200, response.status_code)

    # 我的投资列表
    def test05_my_tender_list(self):
        # 1、登录成功
        # 调用登录的接口
        response = self.login_api.login(self.session)
        # logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、我的投资列表
        # 调用投资的接口
        response = self.tender_api.my_tender_list(self.session)
        logging.info("my tender list response={}".format(response.json()))
        # 对响应数据断言
        self.assertEqual(200, response.status_code)
