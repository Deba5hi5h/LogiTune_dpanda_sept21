import unittest

from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.phone_settings import PhoneSettings
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from testsuite_tune_mobile import test_data


class SchedulerSignIn(MobileBase):
    tc_methods = TuneMobileTests()
    phone_settings = PhoneSettings()

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Connect to Calendar"
        super(SchedulerSignIn, cls).setUpClass()
        # cls.phone_settings.open()
        # cls.phone_settings.disconnect_all_bluetooth_devices()
        # cls.phone_settings.close()

    def test_2001_VC_90687_connect_to_calendar_google(self):
        self.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.google_email(),
                                               site_name=TuneMobileConfig.site(),
                                               building_name=TuneMobileConfig.building(),
                                               teammates=test_data.tc_signin_teammates)

    def test_2002_VC_90714_profile_work_account(self):
        self.tc_methods.tc_profile_work_account()

    def test_2003_VC_98517_connect_to_calendar_microsoft(self):
        self.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.microsoft_email(), google=False,
                                               site_name=TuneMobileConfig.site(),
                                               building_name=TuneMobileConfig.building(),
                                               teammates=test_data.tc_signin_teammates)

    def test_2004_VC_99380_profile_work_account_microsoft(self):
        self.tc_methods.tc_profile_work_account(google=False)

    def test_2005_VC_106160_connect_to_calendar_google_existing_teammates_account(self):
        self.tc_methods.connect_to_calendar_existing_teammates_account(email=TuneMobileConfig.google_email(),
                                                                       site_name=TuneMobileConfig.site(),
                                                                       building_name=TuneMobileConfig.building(),
                                                                       teammates=test_data.tc_signin_teammates)

    def test_2006_VC_106168_connect_to_calendar_microsoft_existing_teammates_account(self):
        self.tc_methods.connect_to_calendar_existing_teammates_account(email=TuneMobileConfig.microsoft_email(),
                                                                       google=False, site_name=TuneMobileConfig.site(),
                                                                       building_name=TuneMobileConfig.building(),
                                                                       teammates=test_data.tc_signin_teammates)

    def test_2007_VC_90694_connect_to_calendar_google_no_access(self):
        self.tc_methods.tc_connect_to_calendar_no_access(email=TuneMobileConfig.google_email())

    def test_2008_VC_98524_connect_to_calendar_microsoft_no_access(self):
        self.tc_methods.tc_connect_to_calendar_no_access(email=TuneMobileConfig.microsoft_email(), google=False)

    def test_2009_VC_106153_connect_to_calendar_google_no_basecamp(self):
        self.tc_methods.tc_user_with_no_basecamp(email=TuneMobileConfig.google_email())

    def test_2010_VC_106164_connect_to_calendar_microsoft_no_basecamp(self):
        self.tc_methods.tc_user_with_no_basecamp(email=TuneMobileConfig.microsoft_email(), google=False)

    def test_2011_VC_90689_connect_to_calendar_google_skip_teammate(self):
        self.tc_methods.tc_connect_to_calendar_skip(email=TuneMobileConfig.google_email(),
                                                    site_name=TuneMobileConfig.site(),
                                                    building_name=TuneMobileConfig.building())

    def test_2012_VC_98519_connect_to_calendar_microsoft_skip_teammate(self):
        self.tc_methods.tc_connect_to_calendar_skip(email=TuneMobileConfig.microsoft_email(),
                                                    site_name=TuneMobileConfig.site(),
                                                    building_name=TuneMobileConfig.building(), google=False)

    def test_2013_VC_109152_connect_to_calendar_google_stress(self):
        for _ in range(10):
            self.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.google_email(), verification=False,
                                                   site_name=TuneMobileConfig.site(),
                                                   building_name=TuneMobileConfig.building(),
                                                   teammates=test_data.tc_signin_teammates)
            self.tc_methods.tc_profile_work_account(verification=False)

    def test_2014_VC_99376_connect_to_calendar_microsoft_stress(self):
        for _ in range(10):
            self.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.microsoft_email(), google=False,
                                                   verification=False, site_name=TuneMobileConfig.site(),
                                                   building_name=TuneMobileConfig.building(),
                                                   teammates=test_data.tc_signin_teammates)
            self.tc_methods.tc_profile_work_account(google=False, verification=False)


if __name__ == "__main__":
    unittest.main()
