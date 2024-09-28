import unittest

from apps.tune.tc_scenarios.home_dashboard_scenarios import HomeDashboardScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class HomeDashboardGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=HomeDashboardScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def setUp(self) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_201_VC_131643_home_screen_page_check_google(self):
        self.scenario.tc_home_screen_page_check(**self.google_credentials_coily)

    def test_202_VC_131645_calendar_not_expanded_check_google(self):
        self.scenario.tc_calendar_not_expanded_calendar_check()

    def test_203_VC_131647_calendar_expanded_check_google(self):
        self.scenario.tc_calendar_expanded_calendar_check()

    def test_204_VC_131649_future_date_select_google(self):
        self.scenario.tc_calendar_future_date_select(**self.google_credentials_coily)

    def test_205_VC_131651_meeting_details_check_google(self):
        self.scenario.tc_calenar_meeting_details_check(**self.google_credentials_coily)

    def test_206_VC_131653_multiple_events_scrollable_google(self):
        self.scenario.tc_multiple_events_scrollable(**self.google_credentials_coily)

    def test_207_VC_131655_booking_a_desk_google(self):
        self.scenario.tc_book_a_desk_default()

    def test_208_VC_131657_multiple_booking_google(self):
        self.scenario.tc_multiple_booking()

    def test_209_VC_131659_days_in_advance_change_google(self):
        self.scenario.tc_max_days_in_advance()


if __name__ == "__main__":
    unittest.main()
