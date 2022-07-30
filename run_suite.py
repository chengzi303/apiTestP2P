import time
import unittest

from app import BASE_DIR
from lib.HTMLTestRunner import HTMLTestRunner
from scripts.approve import approveTest
from scripts.login import loginTest
from scripts.para_login import loginTest_para
from scripts.tender import tender
from scripts.tender_process import tender_process
from scripts.trust import trust

suite=unittest.TestSuite()
# suite.addTest(unittest.makeSuite(loginTest))
suite.addTest(unittest.makeSuite(loginTest_para))
suite.addTest(unittest.makeSuite(approveTest))
suite.addTest(unittest.makeSuite(trust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(tender_process))

# report_file=BASE_DIR + "/report/p2p-{}.html".format(time.strftime("%Y%m%d%H%M%S"))
report_file=BASE_DIR + "/report/index.html"
with open(report_file,"wb") as f:
    runner=HTMLTestRunner(f,title="P2P金融项目接口测试报告",description="test")
    runner.run(suite)

