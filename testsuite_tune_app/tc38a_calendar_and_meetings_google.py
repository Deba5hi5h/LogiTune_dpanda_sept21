import unittest

from apps.tune.tc_scenarios.calendar_and_meetings_scenarios import CalendarAndMeetingsScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class CalendarAndMeetingsTestsGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=CalendarAndMeetingsScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_calendar)

    def setUp(self):
        super().setUp()
        self.tune_app.reopen_tune_app()
        self.scenario.tune_pages.home.click_home_tab()
        self.scenario.delete_calendar_events(**self.google_credentials_calendar)

    def tearDown(self) -> None:
        super().tearDown()

    def test_3801_VC_134009_calendar_and_meetings_page_check_google(self):
        self.scenario.tc_calendar_and_meetings_page_check()

    def test_3802_VC_134010_calendar_non_video_meetings_google(self):
        self.scenario.tc_calendar_non_video_meetings(**self.google_credentials_calendar)

    def test_3803_VC_134011_calendar_declined_meetings_google(self):
        self.scenario.tc_calendar_declined_meetings(**self.google_credentials_calendar)

    def test_3804_VC_134012_calendar_all_day_meetings_google(self):
        self.scenario.tc_calendar_all_day_meetings(**self.google_credentials_calendar)


if __name__ == "__main__":
    unittest.main()
