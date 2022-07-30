import requests

from app import BASE_URL


class loginAPI():
    def __init__(self):
        self.img_code_url=BASE_URL+"/common/public/verifycode1/"
        self.sms_url=BASE_URL+"/member/public/sendSms"
        self.register_url=BASE_URL+"/member/public/reg"
        self.login_url=BASE_URL+"/member/public/login"

    def getImgCode(self,session,r):
        url=self.img_code_url + r
        response=session.get(url)
        return response

    def getSms(self, session, phone, imgVerifyCode):
        # 准备参数
        data={'phone':phone,'imgVerifyCode':imgVerifyCode,'type':'reg'}
        # 发送请求
        response=session.post(url=self.sms_url,data=data)
        # 返回响应
        return response

    def register(self, session, phone, password, verifycode='8888', phone_code='666666', dy_server='on', invite_phone=""):
        # 准备参数
        data={"phone":phone,
              "password":password,
              "verifycode":verifycode,
              "phone_code":phone_code,
              "dy_server":dy_server,
              "invite_phone":invite_phone}
        # 发送请求
        response = session.post(url=self.register_url, data=data)
        # 返回响应
        return response

    def login(self, session, keywords="15688886631", password="a123456"):
        # 准备参数
        data={
            "keywords": keywords,
            "password": password
        }
        # 发送请求
        response=session.post(url=self.login_url,data=data)
        # 返回响应
        return response











