from app import BASE_URL


class tenderAPI():
    def __init__(self):
        self.tender_url=BASE_URL+"/trust/trust/tender"
        self.product_list_url=BASE_URL+"/common/loan/loaninfo"
        self.tender_list_url=BASE_URL+"/loan/loan/listtender"
        self.my_tender_list_url=BASE_URL+"/loan/tender/mytenderlist"

    def tender(self, session, id="970", amount="1000"):
        data={"id": id ,
              "depositCertificate": "-1",
              "amount": amount}
        response=session.post(url=self.tender_url,data=data)
        return response

    def product_list(self, session, id="970"):
        data={"id": id}
        response=session.post(url=self.product_list_url, data= data)
        return response


    def tender_list(self, session):
        response=session.post(url=self.tender_list_url)
        return response

    def my_tender_list(self, session):
        response=session.post(url=self.my_tender_list_url)
        return response