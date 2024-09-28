
import unittest
from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from testsuite_tune_mobile import test_data


class InstallApp(MobileBase):
    tc_methods = TuneMobileTests()
    prod_version = '3.13.0-30059'
    current_version = '3.13.0-30060'
    continue_execution = False

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Install"
        super(InstallApp, cls).setUpClass()

    def test_0001_VC_104636_update_app(self):
        if self.is_ios_device():
            self.tc_methods.phone_settings.open()
            self.tc_methods.phone_settings.dismiss_software_update()
            self.tc_methods.phone_settings.close()
        self.tc_methods.uninstall_app()
        self.tc_methods.install_app(version=InstallApp.prod_version)
        self.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.google_email(),
                                               site_name=TuneMobileConfig.site(),
                                               building_name=TuneMobileConfig.building(),
                                               teammates=test_data.tc_signin_teammates,
                                               verification=False, google=True)
        self.tc_methods.phone_settings.disable_tune_notifications()
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        desk_name = TuneMobileConfig.user_desk()
        reservation = self.tc_methods.book_desk_through_sync_portal(email=TuneMobileConfig.user_email(),
                                                                    desk_name=desk_name, start=start, end=end)
        self.tc_methods.update_app(version=InstallApp.current_version)
        self.tc_methods.open_app()
        self.tc_methods.verify_booking_card(desk_name=desk_name, start=start, end=end)
        self.tc_methods.delete_booking_through_sync_portal(desk_name=desk_name, reservation_id=reservation)
        InstallApp.continue_execution = True

if __name__ == "__main__":
    unittest.main()
