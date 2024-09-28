import unittest

from apps.tune.tc_scenarios.home_dashboard_scenarios import HomeDashboardScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class HomeDashboardMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=HomeDashboardScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def setUp(self) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_251_VC_131644_home_screen_page_check_microsoft(self):
        self.scenario.tc_home_screen_page_check(**self.microsoft_credentials_coily)

    def test_252_VC_131646_calendar_not_expanded_check_microsoft(self):
        self.scenario.tc_calendar_not_expanded_calendar_check()

    def test_253_VC_131648_calendar_expanded_check_microsoft(self):
        self.scenario.tc_calendar_expanded_calendar_check()

    def test_254_VC_131650_future_date_select_microsoft(self):
        self.scenario.tc_calendar_future_date_select(**self.microsoft_credentials_coily)

    def test_255_VC_131652_meeting_details_check_microsoft(self):
        self.scenario.tc_calenar_meeting_details_check(**self.microsoft_credentials_coily)

    def test_256_VC_131654_multiple_events_scrollable_microsoft(self):
        self.scenario.tc_multiple_events_scrollable(**self.microsoft_credentials_coily)

    def test_257_VC_131656_booking_a_desk_microsoft(self):
        self.scenario.tc_book_a_desk_default()

    def test_258_VC_131658_multiple_booking_microsoft(self):
        self.scenario.tc_multiple_booking()

    def test_259_VC_131660_days_in_advance_change_microsoft(self):
        self.scenario.tc_max_days_in_advance()


if __name__ == "__main__":
    unittest.main()
