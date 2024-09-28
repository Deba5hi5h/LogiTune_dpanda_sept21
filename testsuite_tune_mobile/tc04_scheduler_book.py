import unittest

from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from testsuite_tune_mobile import test_data

class SchedulerBook(MobileBase):
    tc_methods = TuneMobileTests()

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Dashboard Book"
        super(SchedulerBook, cls).setUpClass()
        if global_variables.reportInstance is None:
            global_variables.reportInstance = global_variables.extent.createTest("Booking Setup", "Test Case Details")
        cls.tc_methods.open_app()
        if not cls.tc_methods.dashboard.verify_home():
            cls.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.user_email(), verification=False,
                                                  site_name=TuneMobileConfig.site(), 
                                                  building_name=TuneMobileConfig.building(),
                                                  teammates=test_data.tc_signin_teammates)

    def test_4001_VC_90730_book_screen_controls(self):
        self.tc_methods.tc_book_screen_controls()

    def test_4002_VC_90733_book_desk_current_date_default_building(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=3)
        self.tc_methods.tc_book_by_location(desk_name=TuneMobileConfig.user_desk(), day=0, start=start, end=end)
        #Also covers VC-90697

    def test_4003_VC_107009_cancel_booking_future_date(self):
        self.tc_methods.tc_cancel_booking(desk_name=TuneMobileConfig.user_desk(), day=1, start='', end='')

    def test_4004_VC_107007_cancel_booking_session_already_started(self):
        self.tc_methods.tc_cancel_booking(desk_name=TuneMobileConfig.user_desk(), day=0, start='', end='')

    def test_4005_VC_90734_book_desk_current_date_different_building(self):
        self.tc_methods.tc_book_by_location(desk_name="auto-tune-qa-desk1", day=0, start='', end='')

    def test_4006_VC_90735_book_desk_future_date_default_building(self):
        self.tc_methods.tc_book_by_location(desk_name=TuneMobileConfig.user_desk(), day=1, start="10:00 AM", end="1:00 PM")

    def test_4007_VC_90737_book_desk_by_preference_and_check_in(self):
        teammate_name = self.tc_methods.raiden_api.get_user_name_by_email(TuneMobileConfig.teammate_email())
        self.tc_methods.tc_check_in_booking(desk_name=TuneMobileConfig.coily_desk(), day=0, start='', end='', teammates=[teammate_name])

    def test_4008_VC_90738_book_near_teammate(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_book_near_teammate(teammate_email=TuneMobileConfig.teammate_email(), 
                                              teammate_desk=TuneMobileConfig.user_desk(),
                                              desk_name=TuneMobileConfig.nearest_desk(), start=start, end=end, day=0, 
                                              notify_teammate=True)

    def test_4009_VC_120173_book_near_teammate_closest_desk_not_available(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        reservation = self.tc_methods.book_desk_through_sync_portal(email=TuneMobileConfig.other_email(),
                                                                    desk_name=TuneMobileConfig.nearest_desk(),
                                                                    start=start, end=end, day=0)
        self.tc_methods.tc_book_near_teammate(teammate_email=TuneMobileConfig.teammate_email(), 
                                              teammate_desk=TuneMobileConfig.user_desk(),
                                              desk_name=TuneMobileConfig.second_nearest_desk(), start=start, end=end, day=0,
                                              notify_teammate=False)
        self.tc_methods.delete_booking_through_sync_portal(desk_name=TuneMobileConfig.nearest_desk(), reservation_id=reservation)

    def test_4010_VC_90749_cancel_and_rebook_same_desk(self):
        self.tc_methods.tc_cancel_and_rebook(desk_name=TuneMobileConfig.nearest_desk(), day=0, start='', end='')

    def test_4011_VC_97234_modify_booking_to_future_date(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_modify_booking_to_future_date(email=TuneMobileConfig.user_email(), 
                                                         desk_name=TuneMobileConfig.nearest_desk(),
                                                         day=2, start=start, end=end)

    def test_4012_VC_104628_notify_no_teammates_added(self):
        self.tc_methods.tc_notify_no_teammates_added(desk_name=TuneMobileConfig.second_nearest_desk(),
                                                     day=1, start='', end='')

    def test_4013_VC_120164_entire_booking_card_clickable(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_entire_booking_card_clickable(email=TuneMobileConfig.user_email(),
                                                         desk_name=TuneMobileConfig.user_desk(),
                                                         day=0, start=start, end=end)


if __name__ == "__main__":
    unittest.main()
