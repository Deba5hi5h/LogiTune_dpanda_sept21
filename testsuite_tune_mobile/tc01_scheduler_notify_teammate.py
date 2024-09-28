import unittest
from unittest import SkipTest

from apps.tune_mobile.config.tune_mobile_config import TuneMobileConfig
from apps.tune_mobile.tune_mobile_tests import TuneMobileTests
from base import global_variables
from base.base_mobile import MobileBase
from extentreport.report import Report
from testsuite_tune_mobile import test_data


class SchedulerNotifyTeammate(MobileBase):
    tc_methods = TuneMobileTests()

    @classmethod
    def setUpClass(cls) -> None:
        global_variables.HEADSET = "Notify Teammate"
        super(SchedulerNotifyTeammate, cls).setUpClass()
        if global_variables.reportInstance is None:
            global_variables.reportInstance = global_variables.extent.createTest("Notify Teammate Setup",
                                                                                 "Test Case Details")
        cls.setup_teammate_account()
        cls.tc_methods.raiden_api.update_desk_policy_settings(group_path=f'/{TuneMobileConfig.site()}')
        cls.tc_methods.open_app()
        if not cls.tc_methods.dashboard.verify_home():
            cls.tc_methods.tc_connect_to_calendar(email=TuneMobileConfig.user_email(), verification=False,
                                                  site_name=TuneMobileConfig.site(),
                                                  building_name=TuneMobileConfig.building(),
                                                  teammates=test_data.tc_signin_teammates)
        teammate_name = cls.tc_methods.raiden_api.get_user_name_by_email(TuneMobileConfig.teammate_email())
        cls.tc_methods.tc_setup_add_teammate(teammates=[teammate_name])

    @classmethod
    def setup_teammate_account(cls):
        global_variables.driver = None
        cls.tc_methods.open_app(teammate=True)
        teammate = TuneMobileConfig.teammate_email()
        cls.tc_methods.tc_connect_to_calendar(email=teammate, verification=False,
                                              site_name=TuneMobileConfig.site(),
                                              building_name=TuneMobileConfig.building(), teammates=[],
                                              teammate_phone=True)
        cls.tc_methods.tc_setup_clear_notifications()
        cls.tc_methods.close()

    def test_1001_VC_111082_notify_teammate_with_message_during_booking(self):
        self.tc_methods.tc_notify_teammate_with_message_during_booking(desk_name=TuneMobileConfig.user_desk(),
                                                                       day=0, start='', end='',
                                                                       custom_message="This is custom message")

    def test_1002_VC_118356_notify_teammate_with_message_edit_booking(self):
        self.tc_methods.tc_notify_teammate_with_message_edit_booking(desk_name=TuneMobileConfig.user_desk(),
                                                                     day=0, start='', end='',
                                                                     custom_message="This is custom message")

    def test_1003_VC_111083_notify_teammate_without_message_during_booking(self):
        self.tc_methods.tc_notify_teammate_with_message_during_booking(desk_name=TuneMobileConfig.user_desk(),
                                                                       day=0, start='', end='')

    def test_1004_VC_118355_notify_teammate_without_message_edit_booking(self):
        self.tc_methods.tc_notify_teammate_with_message_edit_booking(desk_name=TuneMobileConfig.user_desk(),
                                                                     day=0, start='', end='')

    def test_1005_VC_118358_notify_teammate_second_time_edit_booking(self):
        self.tc_methods.tc_notify_teammate_second_time_edit_booking(desk_name=TuneMobileConfig.user_desk(),
                                                                    day=0, start='', end='')

    def test_1006_VC_118349_book_near_teammate_from_people_screen_and_notify(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_book_near_teammate_from_people_screen(teammate_email=TuneMobileConfig.teammate_email(),
                                                                 teammate_desk=TuneMobileConfig.user_desk(),
                                                                 desk_name=TuneMobileConfig.nearest_desk(),
                                                                 start=start, end=end, day=1, notify_teammate=True)

    def test_1007_VC_118350_book_near_teammate_from_office_screen_and_notify(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_book_near_teammate_from_people_screen(teammate_email=TuneMobileConfig.teammate_email(),
                                                                 teammate_desk=TuneMobileConfig.user_desk(),
                                                                 desk_name=TuneMobileConfig.nearest_desk(),
                                                                 start=start, end=end, day=0, notify_teammate=True,
                                                                 office=True)

    def test_1008_VC_107014_teammate_cancels_booking_notification(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_teammate_cancels_booking_notification(teammate_email=TuneMobileConfig.teammate_email(),
                                                                 teammate_desk=TuneMobileConfig.user_desk(),
                                                                 desk_name=TuneMobileConfig.nearest_desk(),
                                                                 day=0, start=start, end=end)
        #Also covers VC-90708

    def test_1009_VC_90709_teammate_modifies_booking_notification(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        self.tc_methods.tc_teammate_modifies_booking_notification(teammate_email=TuneMobileConfig.teammate_email(),
                                                                 teammate_desk=TuneMobileConfig.user_desk(),
                                                                  desk_name=TuneMobileConfig.nearest_desk(),
                                                                 day=0, start=start, end=end)

    def test_1010_VC_111085_notify_teammate_emoji(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        message = "\U0001F600 \U0001F601 \U0001F606 \U0001F923 \U0001F609"
        self.tc_methods.tc_notify_teammate_emoji(desk_name=TuneMobileConfig.user_desk(), day=0, start=start, end=end,
                                                 custom_message=message, emoji_count=5)

    def test_1011_VC_111086_notify_teammate_emoji_text(self):
        message = "This is text and emoji characters \U0001F970 \U0001F618"
        self.tc_methods.tc_notify_teammate_emoji_text(desk_name=TuneMobileConfig.user_desk(), day=0, start='', end='',
                                                 custom_message=message, emoji_count=2)

    def test_1012_VC_111088_notify_teammate_max_characters(self):
        start, end = self.tc_methods.get_start_end_time(booking_duration=1)
        message = "This is text with more than 128 characters to validate the maximum number of characters " \
                  "supported in Tune Mobile App while sendi"
        self.tc_methods.tc_notify_teammate_emoji(desk_name=TuneMobileConfig.user_desk(), day=0, start=start, end=end,
                                                 custom_message=message)
        #Also covers VC-111087


if __name__ == "__main__":
    unittest.main()
