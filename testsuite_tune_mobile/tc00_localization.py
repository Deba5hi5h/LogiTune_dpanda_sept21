import shutil
import unittest

from apps.tune_mobile.phone_settings import PhoneSettings
from base import global_variables
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base.base_mobile import MobileBase


class Localization(MobileBase):
    tc_methods = TuneMobileTests()
    phone_settings = PhoneSettings()
    headset = "Zone Wireless 2"
    bluetooth = True

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = cls.headset
        global_variables.retry_count = 0
        super(Localization, cls).setUpClass()
        shutil.copyfile(f"{MobileBase.rootPath}/apps/tune_mobile/config/{cls.headset}.html",
                        f"{global_variables.reportPath}/{cls.headset}.html")

    def setUp(self) -> None:
        global_variables.testStatus = "Pass"
        testName = self.__getattribute__("_testMethodName")
        global_variables.reportInstance = global_variables.extent.createTest(f"{testName}_{self.headset}",
                                                                             "Test Case Details")
        if not Localization.bluetooth:
            Localization.bluetooth = True
            self.phone_settings.open()
            self.phone_settings.disconnect_all_bluetooth_devices()
            self.phone_settings.connect_bluetooth_device(self.headset)
            self.phone_settings.close()

    def test_0001_VC_84289_navigation_spanish(self):
        self.tc_methods.change_language("Spanish")
        self.tc_methods.tc_localization_navigation(headset=self.headset)

    def test_0002_VC_84289_navigation_french(self):
        self.tc_methods.change_language("French")
        self.tc_methods.tc_localization_navigation(headset=self.headset)

    def test_0003_VC_84289_navigation_portuguse(self):
        self.tc_methods.change_language("Portuguese")
        self.tc_methods.tc_localization_navigation(headset=self.headset)

    def test_0004_VC_84289_navigation_german(self):
        self.tc_methods.change_language("German")
        self.tc_methods.tc_localization_navigation(headset=self.headset)

    def test_0005_VC_84289_navigation_italian(self):
        self.tc_methods.change_language("Italian")
        self.tc_methods.tc_localization_navigation(headset=self.headset)

    def test_0006_VC_84289_navigation_english(self):
        self.tc_methods.change_language("English")
        self.tc_methods.tc_localization_navigation(headset=self.headset)


if __name__ == "__main__":
    unittest.main()
