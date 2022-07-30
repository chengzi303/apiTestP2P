import logging
import random
import unittest

import requests

import app
from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI
from utils import assert_utils, third_request_api, DButils


class tender_process(unittest.TestCase):
    phone6 = "15688886619"
    imgVerifyCode1 = "8888"
    password1 = "a123456"
    realname = "卫寒凝"
    card_id = "429006198902135782"
    def setUp(self) -> None:
        self.login_api=loginAPI()
        self.approve_api = approveAPI()
        self.trust_api = trustAPI()
        self.tender_api=tenderAPI()
        self.session=requests.Session()

    def tearDown(self) -> None:
        self.session.close()
        # sql1 = "delete from mb_member_register_log where phone = '15688886619' or phone = '15688886618' or phone = '15688886617' or phone = '15688886616';"
        # DButils.delete(app.BASE_MEMBER, sql1)
        # logging.info("delete sql={}".format(sql1))
        # sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone = '15688886619' or m.phone = '15688886618' or m.phone = '15688886617' or m.phone = '15688886616';"
        # DButils.delete(app.BASE_MEMBER, sql2)
        # logging.info("delete sql={}".format(sql2))
        # sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone = '15688886619' or m.phone = '15688886618' or m.phone = '15688886617' or m.phone = '15688886616';"
        # DButils.delete(app.BASE_MEMBER, sql3)
        # logging.info("delete sql={}".format(sql3))
        # sql4 = "delete from mb_member WHERE phone = '15688886619' or phone = '15688886618' or phone = '15688886617' or phone = '15688886616';"
        # DButils.delete(app.BASE_MEMBER, sql4)
        # logging.info("delete sql={}".format(sql4))

    def test01_tender_process(self):
        # 1、 定义参数（随机小数）
        r = random.random()
        # 获取图片验证码
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、获取短信验证码
        # 定义参数（正确的手机号、验证码）
        # 调用获取短信验证码的接口
        response = self.login_api.getSms(self.session, self.phone6, self.imgVerifyCode1)
        logging.info("get sms code response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、注册
        # 定义参数（正确填写仅必填参数）
        # 调用注册的接口
        response=self.login_api.register(self.session, self.phone6, self.password1)
        logging.info("register response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "注册成功")
        # 4、登录
        # 调用登录的接口
        response = self.login_api.login(self.session,keywords=self.phone6)
        logging.info("login response={}".format(response.json()))
        # 对返回的响应断言
        assert_utils(self, response, 200, 200, "登录成功")
        # 5、认证成功
        # 准备参数
        # 调用接口脚本定义的方法发送请求
        response = self.approve_api.approve(self.session, realname=self.realname, card_id=self.card_id)
        logging.info("get approve response={}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "提交成功!")
        # 6、发送开户请求
        # 调用开户的接口
        response = self.trust_api.trustRegister(self.session)
        logging.info("trust register response={}".format(response.json()))
        # 对响应结果断言
        self.assertEqual(200, response.status_code)
        # 7、发送第三方开户请求
        form_data = response.json().get('description').get('form')
        response = third_request_api(form_data)
        # 断言
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)
        # 8、发送风险测评请求
        # 调用风险测评的接口
        response = self.trust_api.risk(self.session)
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual("提交成功", response.json().get("data"))
        # 9、随机数小数，获取充值验证码成功
        # 定义参数（随机小数）
        r = random.random()
        # 调用接口类中的接口
        response = self.trust_api.recharge_verifyCode(self.session, str(r))
        logging.info("recharge verifyCode response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 10、参数填写正确，充值成功
        # 定义参数（参数填写正确）
        # 调用充值接口类中的接口
        response = self.trust_api.recharge(self.session)
        logging.info("recharge response={}".format(response.json()))
        # 接收接口返回结果，进行断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 11、发送第三方充值请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        logging.info("third recharge response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual("NetSave OK", response.text)
        # 12、必填项填写正确，投资成功
        # 调用投资的接口
        response = self.tender_api.tender(self.session)
        logging.info("tender response={}".format(response.json()))
        # 对响应数据断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 13、发送第三方投资请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        logging.info("third tender response={}".format(response.text))
        # 接收接口返回结果，进行断言
        self.assertEqual("InitiativeTender OK", response.text)
        # 14、我的投资列表
        # 调用投资的接口
        response = self.tender_api.my_tender_list(self.session)
        logging.info("my tender list response={}".format(response.json()))
        # 对响应数据断言
        self.assertEqual(200, response.status_code)



