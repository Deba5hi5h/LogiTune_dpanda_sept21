import os
import logging
import time
from pathlib import Path

from apps.collabos.nintendo.nintendo_methods import NintendoMethods
from testsuite_jasmine_ui.tc_methods_jasmine import JasmineTCMethods
from apps.collabos.coily.utilities import check_and_connect_device, remove_chromedriver_folder, \
    collect_logcat_logs_over_wifi
from base import global_variables
from common.usb_switch import disconnect_all
from base.base import Base
from base.base_ui import UIBase
from common.framework_params import NINTENDO_DESK_IP
from extentreport.report import Report


class JasmineBase(UIBase):
    elementName = ""
    test_flag = True
    rootPath = Path(os.path.dirname(__file__)).parent
    collabos_driver = None
    appium_service = None
    nintendo_methods = None
    jasmine_tc_methods = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls, start_winappdriver=False) -> None:
        global_variables.SYNC_ENV = 'raiden-latest1'
        # Logging for Webdriver set to Error only
        logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('urllib3.connectionpool')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('urllib3.util.retry')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('PIL.PngImagePlugin')
        logger.setLevel(logging.ERROR)
        logger = logging.getLogger('paramiko.transport')
        logger.setLevel(logging.INFO)
        remove_chromedriver_folder()
        check_and_connect_device(NINTENDO_DESK_IP)
        time.sleep(2)
        if global_variables.setupFlag:
            super(JasmineBase, cls).setUpClass(start_winappdriver=start_winappdriver)
        cls.nintendo_methods = NintendoMethods()
        cls.nintendo_methods.open_app()
        cls.jasmine_tc_methods = JasmineTCMethods(cls.nintendo_methods)


    @classmethod
    def tearDownClass(cls) -> None:
        super(JasmineBase, cls).tearDownClass()

    def setUp(self) -> None:
        Base.setUp(self)
        testcase_name = self.__getattribute__("_testMethodName")
        Report.logInfo(f'Test Case name: {testcase_name}')
        disconnect_all()
        self.nintendo_methods.open_app()


    def tearDown(self) -> None:
        Base.tearDown(self)


