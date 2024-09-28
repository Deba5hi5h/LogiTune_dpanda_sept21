import os
import logging
import time
from pathlib import Path

from apps.collabos.nintendo.nintendo_methods import NintendoMethods
from apps.collabos.nintendo.room_booking_test_methods import RoomBookingTests
from apps.collabos.coily.utilities import check_and_connect_device, remove_chromedriver_folder, \
    collect_logcat_logs_over_wifi
from base import global_variables
from common.usb_switch import disconnect_all
from base.base import Base
from base.base_ui import UIBase
from common.framework_params import NINTENDO_DESK_IP
from extentreport.report import Report
from apps.tune.TunesAppInstall import TunesUIInstall
from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS
from common.platform_helper import get_custom_platform
from common.framework_params import INSTALLER


WIN_APP_BAT_PATH = "\\WinApp\\winapp.bat"
WIN_APP_CLOSE_BAT_PATH = "\\WinApp\\winapp_close.bat"

class NintendoBase(UIBase):
    elementName = ""
    test_flag = True
    rootPath = Path(os.path.dirname(__file__)).parent
    collabos_driver = None
    appium_service = None
    nintendo_methods = None
    nintendo_test_methods = None

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
            super(NintendoBase, cls).setUpClass(start_winappdriver=start_winappdriver)
        cls.nintendo_methods = NintendoMethods()
        cls.nintendo_methods.open_app()
        cls.nintendo_test_methods = RoomBookingTests(cls.nintendo_methods)


    @classmethod
    def tearDownClass(cls) -> None:
        super(NintendoBase, cls).tearDownClass()

    def setUp(self) -> None:
        Base.setUp(self)
        testcase_name = self.__getattribute__("_testMethodName")
        Report.logInfo(f'Test Case name: {testcase_name}')
        disconnect_all()
        self.nintendo_methods.open_app()
        if get_custom_platform() == 'windows':
            app = TunesUIInstall()
            if not app.check_for_app_installed_win("Logi Tune"):
                Report.logInfo("Tune not installed, Installing")
                os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)
                self.nintendo_test_methods.tune_methods.tc_install_logitune(version=INSTALLER, disconnect_devices=False)
            else:
                Report.logInfo("Tune installed before test")
        else:
            app = TunesUIInstallMacOS()
            if not app.check_tune_installed_macos():
                Report.logInfo("Tune not installed, Installing")
                self.nintendo_test_methods.tune_methods.tc_install_logitune(version=INSTALLER, disconnect_devices=False)
            else:
                Report.logInfo("Tune installed before test")

    def tearDown(self, tune_installed=True) -> None:
        if global_variables.testStatus == "Fail":
            name = self.__getattribute__("_testMethodName").split("_")
            file_name = f'{name[0]}_{name[1]}_logcat.txt'
            file_path = os.path.join(self.logdirectory, file_name)
            collect_logcat_logs_over_wifi(device_ip=NINTENDO_DESK_IP, file_path=file_path)

        Base.tearDown(self)
        if NintendoBase.test_flag != True:
            assert False

