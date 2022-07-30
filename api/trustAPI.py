from app import BASE_URL


class trustAPI():
    def __init__(self):
        self.trust_register_url=BASE_URL+"/trust/trust/register"
        self.risk_url=BASE_URL+"/risk/answer/submit"
        self.recharge_verifyCode_url=BASE_URL+"/common/public/verifycode/"
        self.recharge_url=BASE_URL+"/trust/trust/recharge"

    def trustRegister(self,session):
        response=session.post(url=self.trust_register_url)
        return response

    def risk(self, session):
        # 准备参数
        data = {"answers_1": "D", "answers_2": "D", "answers_3": "D", "answers_4": "D",
              "answers_5": "D", "answers_6": "D", "answers_7": "D", "answers_8": "D",
              "answers_9": "D", "answers_10": "D"}
        response = session.post(url=self.risk_url, data=data)
        return response

    def recharge_verifyCode(self, session, r):
        url = self.recharge_verifyCode_url + r
        response = session.get(url)
        return response

    def recharge(self, session, amount="200000", valicode="8888"):
        data={"paymentType": "chinapnrTrust",
              "amount": amount,
              "formStr": "reForm",
              "valicode": valicode}
        response=session.post(url=self.recharge_url, data=data)
        return response


