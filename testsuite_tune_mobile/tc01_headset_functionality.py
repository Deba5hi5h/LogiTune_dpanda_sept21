import unittest
from unittest import SkipTest
from apps.tune_mobile.phone_settings import PhoneSettings
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from extentreport.report import Report


class HeadsetFunctionality(MobileBase):
    headset = "Zone Wireless Plus"
    tc_methods = TuneMobileTests()
    phone_settings = PhoneSettings()
    bluetooth = False

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = cls.headset
        global_variables.retry_count = 1
        super(HeadsetFunctionality, cls).setUpClass()

    def setUp(self) -> None:
        global_variables.testStatus = "Pass"
        testName = self.__getattribute__("_testMethodName")
        global_variables.reportInstance = global_variables.extent.createTest(f"{testName}_{self.headset}",
                                                                             "Test Case Details")
        if not HeadsetFunctionality.bluetooth:
            HeadsetFunctionality.bluetooth = True
            self.tc_methods.open_app()
            if self.tc_methods.dashboard.verify_home():  # Disconnect if already connected to Calendar
                self.tc_methods.tc_profile_work_account(verification=False)
            self.phone_settings.open()
            self.phone_settings.disconnect_all_bluetooth_devices()
            self.phone_settings.connect_bluetooth_device(self.headset)
            self.phone_settings.close()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.phone_settings.open()
        cls.phone_settings.disconnect_all_bluetooth_devices()
        cls.phone_settings.close()
        super(HeadsetFunctionality, cls).tearDownClass()

    def test_1001_VC_84270_equalizer_presets(self):
        self.tc_methods.tc_equalizer_presets(headset=self.headset)

    def test_1002_VC_84274_customize_equalizer_presets(self):
        self.tc_methods.tc_customize_equalizer_presets(headset=self.headset)

    def test_1003_VC_103283_customize_equalizer_presets_without_save(self):
        global_variables.retry_test = False
        self.tc_methods.tc_customize_equalizer_presets_without_save(headset=self.headset)

    def test_1004_VC_84280_custom_equalizer_preset_limit(self):
        self.tc_methods.tc_custom_equalizer_preset_limit(headset=self.headset)

    def test_1005_VC_84281_edit_custom_equalizer(self):
        self.tc_methods.tc_edit_custom_equalizer(headset=self.headset)

    def test_1006_VC_84289_device_name(self):
        self.tc_methods.tc_device_name(headset=self.headset)

    def test_1007_VC_83605_sidetone(self):
        if self.headset == "Zone True Wireless":
            Report.logSkip(f"Test Case not supported for {self.headset}")
            raise SkipTest(f"Test Case not supported for {self.headset}")
        self.tc_methods.tc_sidetone(headset=self.headset)

    def test_1008_VC_84404_sleep_settings(self):
        self.tc_methods.tc_sleep_settings(headset=self.headset)

if __name__ == "__main__":
    unittest.main()
