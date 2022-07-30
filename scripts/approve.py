import logging
import unittest

import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils


class approveTest(unittest.TestCase):
    realname = "卫寒凝"
    card_id = "429006198902135782"
    phone1 = "15688886631"
    phone2 = "15688886632"
    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.approve_api=approveAPI()
        self.session=requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 必填项填写正确，认证成功
    def test01_approve_success(self):
        # 1、用户登录
        # 调用获取短信验证码的接口
        response = self.login_api.login(self.session)
        logging.info("get login code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、认证成功
        # 准备参数
        # 调用接口脚本定义的方法发送请求
        response = self.approve_api.approve(self.session,realname=self.realname,card_id=self.card_id)
        logging.info("get approve response={}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "提交成功!")


    # 姓名为空，认证失败(bug)
    def test02_approve_realName_is_null(self):
        # 1、用户登录
        # 调用获取短信验证码的接口
        response = self.login_api.login(self.session, self.phone2)
        logging.info("get login code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、姓名为空，认证失败
        # 准备参数（姓名为空，认证失败）
        # 调用接口脚本定义的方法发送请求
        response = self.approve_api.approve(self.session, realname="", card_id=self.card_id)
        logging.info("get approve response={}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "姓名不能为空")

    # 身份证号为空，认证失败(bug)
    def test03_approve_card_id_is_null(self):
        # 1、用户登录
        # 调用获取短信验证码的接口
        response = self.login_api.login(self.session, self.phone2)
        logging.info("get login code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、身份证号为空，认证失败
        # 准备参数（身份证号为空，认证失败）
        # 调用接口脚本定义的方法发送请求
        response = self.approve_api.approve(self.session, realname=self.realname, card_id="")
        logging.info("get approve response={}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 100, "身份证号不能为空")

    # 获取认证信息
    def test04_getApprove_success(self):
        # 1、用户登录
        # 调用获取短信验证码的接口
        response = self.login_api.login(self.session, self.phone1)
        logging.info("get login code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 2、获取认证信息
        # 调用接口脚本定义的方法发送请求
        response=self.approve_api.getApprove(self.session)
        logging.info("get approve response={}".format(response.json()))
        # 对返回的响应断言
        self.assertEqual(200, response.status_code)

