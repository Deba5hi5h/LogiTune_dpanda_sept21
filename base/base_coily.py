import os
import logging
import time
from pathlib import Path

from apps.collabos.coily.coily_methods import TuneCoilyMethods
from apps.collabos.coily.tune_coily_test_methods import TuneCoilyTests
from apps.collabos.coily.tune_coily_config import GOOGLE, MICROSOFT
from apps.tune.TuneElectron import TuneElectron
from apps.collabos.coily.utilities import check_and_connect_device, remove_chromedriver_folder, \
    collect_logcat_logs_over_wifi
from base import global_variables
from common.usb_switch import disconnect_all
from base.base import Base
from base.base_ui import UIBase
from common.framework_params import COILY_DESK_IP
from apps.collabos.coily.utilities import prepare_work_account_credentials
from extentreport.report import Report
from apps.tune.TunesAppInstall import TunesUIInstall
from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS
from common.platform_helper import get_custom_platform
from common.framework_params import INSTALLER
from common.logs_storer import store_failed_testcase_logs_on_server


WIN_APP_BAT_PATH = "\\WinApp\\winapp.bat"
WIN_APP_CLOSE_BAT_PATH = "\\WinApp\\winapp_close.bat"

class CoilyBase(UIBase):
    elementName = ""
    test_flag = True
    rootPath = Path(os.path.dirname(__file__)).parent
    coily_driver = None
    appium_service = None
    coily_methods = None
    coily_test_methods = None
    google_credentials = prepare_work_account_credentials(GOOGLE)
    microsoft_credentials = prepare_work_account_credentials(MICROSOFT)

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
        check_and_connect_device(COILY_DESK_IP)
        time.sleep(2)
        if global_variables.setupFlag:
            super(CoilyBase, cls).setUpClass(start_winappdriver=start_winappdriver)
        cls.coily_methods = TuneCoilyMethods()
        cls.coily_methods.open_app()
        cls.coily_test_methods = TuneCoilyTests(cls.coily_methods)


    @classmethod
    def tearDownClass(cls) -> None:
        super(CoilyBase, cls).tearDownClass()

    def setUp(self) -> None:
        Base.setUp(self)
        testcase_name = self.__getattribute__("_testMethodName")
        Report.logInfo(f'Test Case name: {testcase_name}')
        disconnect_all()
        self.coily_methods.open_app()
        if get_custom_platform() == 'windows':
            app = TunesUIInstall()
            if not app.check_for_app_installed_win("Logi Tune"):
                Report.logInfo("Tune not installed, Installing")
                os.system(str(UIBase.rootPath) + WIN_APP_BAT_PATH)
                self.coily_test_methods.tune_methods.tc_install_logitune(version=INSTALLER, disconnect_devices=False)
            else:
                Report.logInfo("Tune installed before test")
        else:
            app = TunesUIInstallMacOS()
            if not app.check_tune_installed_macos():
                Report.logInfo("Tune not installed, Installing")
                self.coily_test_methods.tune_methods.tc_install_logitune(version=INSTALLER, disconnect_devices=False)
            else:
                Report.logInfo("Tune installed before test")

        for account_type, credentials in (
                {GOOGLE: self.google_credentials, MICROSOFT: self.microsoft_credentials}.items()):
            self.coily_test_methods.delete_active_reservations_for_user(credentials)
            self.coily_test_methods.delete_all_calendar_event_for_the_user(account_type, credentials)
        self.coily_test_methods.delete_active_reservations_for_desk()
        self.coily_test_methods.sync_portal_services.set_coily_settings(privacy_mode_enabled=False)
        self.coily_test_methods.clean_tune_connected_account()
        self.coily_test_methods.clean_existing_reservation_on_the_desk()
        self.verify_coily_displays_idle_page()

    def verify_coily_displays_idle_page(self):
        self.coily_methods.open_app(force=True)
        try:
            self.coily_methods.home.verify_time_idle_page()
            Report.logInfo("Idle Page before test start is present, continuing")
        except Exception:
            Report.logInfo('Restarting Coily because IDLE Page not found')
            self.coily_methods.appium_service.restart_collabos_device_and_wait_for_boot()
            self.coily_methods.open_app(force=True)

    def tearDown(self, tune_installed=True) -> None:
        self.coily_test_methods.clean_existing_reservation_on_the_desk()
        if tune_installed:
            self.coily_test_methods.clean_tune_connected_account()
        if global_variables.testStatus == "Fail":
            name = self.__getattribute__("_testMethodName").split("_")
            file_name = f'{name[0]}_{name[1]}_logcat.txt'
            file_path = os.path.join(self.logdirectory, file_name)
            collect_logcat_logs_over_wifi(device_ip=COILY_DESK_IP, file_path=file_path)
            tune_app = TuneElectron()
            tune_app.save_logitune_logs_in_testlogs(testlogs_path=self.logdirectory, test_name=self.id())

        Base.tearDown(self)
        if CoilyBase.test_flag != True:
            assert False

