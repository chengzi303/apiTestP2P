from app import BASE_URL


class approveAPI():
    def __init__(self):
        self.approve_url=BASE_URL+"/member/realname/approverealname"
        self.getAppprove_url=BASE_URL+"/member/member/getapprove"

    def approve(self,session,realname,card_id):
        data={"realname":realname, "card_id":card_id}
        response=session.post(url=self.approve_url, data=data, files={'x':'y'})
        return response

    def getApprove(self,session):
        response=session.post(url=self.getAppprove_url)
        return response

