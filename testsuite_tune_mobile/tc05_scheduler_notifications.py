import unittest

from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from testsuite_tune_mobile import test_data

class SchedulerNotifications(MobileBase):
    tc_methods = TuneMobileTests()

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Notifications"
        super(SchedulerNotifications, cls).setUpClass()
        if global_variables.reportInstance is None:
            global_variables.reportInstance = global_variables.extent.createTest("Notifications Setup", "Test Case Details")
        cls.tc_methods.close()
        cls.tc_methods.open_app()
        if not cls.tc_methods.dashboard.verify_home():
            cls.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.user_email(), verification=False,
                                                  site_name=TuneMobileConfig.site(), 
                                                  building_name=TuneMobileConfig.building(),
                                                  teammates=test_data.tc_signin_teammates)
        cls.tc_methods.dashboard.click_home()


    def setUp(self) -> None:
        super(SchedulerNotifications, self).setUp()
        self.tc_methods.tc_setup_clear_notifications()

    def test_5001_VC_120177_no_active_notifications(self):
        self.tc_methods.tc_notify_no_active_notifications()

    def test_5002_VC_118477_admin_creates_booking(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_admin_creates_booking(email=TuneMobileConfig.user_email(),
                                                 desk_name=TuneMobileConfig.user_desk(),
                                                 start=start, end=end, day=0)

    def test_5003_VC_118479_admin_deletes_booking(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_admin_cancels_booking(email=TuneMobileConfig.user_email(),
                                                 desk_name=TuneMobileConfig.user_desk(),
                                                 start=start, end=end, day=0)

    def test_5004_VC_118478_admin_updates_booking(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        updated_start, updated_end = self.tc_methods.get_start_end_time(booking_duration=2)
        self.tc_methods.tc_admin_updates_booking(email=TuneMobileConfig.user_email(),
                                                 desk_name=TuneMobileConfig.user_desk(),
                                                 start=start, end=end, updated_start=updated_start,
                                                 updated_end=updated_end, day=0, updated_day=0)
        #Also covers VC-107013

    def test_5005_VC_107010_check_in_required(self):
        self.tc_methods.tc_check_in_required(desk_name=TuneMobileConfig.user_desk(), start='', end='', day=0)


if __name__ == "__main__":
    unittest.main()
