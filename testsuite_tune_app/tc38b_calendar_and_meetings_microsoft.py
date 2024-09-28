import unittest

from apps.tune.tc_scenarios.calendar_and_meetings_scenarios import CalendarAndMeetingsScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class CalendarAndMeetingsTestsMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=CalendarAndMeetingsScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_calendar)

    def setUp(self):
        super().setUp()
        self.tune_app.reopen_tune_app()
        self.scenario.tune_pages.home.click_home_tab()
        self.scenario.delete_calendar_events(**self.microsoft_credentials_calendar)

    def tearDown(self) -> None:
        super().tearDown()

    def test_3805_VC_134013_calendar_and_meetings_page_check_microsoft(self):
        self.scenario.tc_calendar_and_meetings_page_check()

    def test_3806_VC_134014_calendar_non_video_meetings_microsoft(self):
        self.scenario.tc_calendar_non_video_meetings(**self.microsoft_credentials_calendar)

    def test_3807_VC_134015_calendar_declined_meetings_microsoft(self):
        self.scenario.tc_calendar_declined_meetings(**self.microsoft_credentials_calendar)

    def test_3808_VC_134016_calendar_all_day_meetings_microsoft(self):
        self.scenario.tc_calendar_all_day_meetings(**self.microsoft_credentials_calendar)


if __name__ == "__main__":
    unittest.main()
