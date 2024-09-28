import unittest

from apps.tune.tc_scenarios.people_tab_scenarios import PeopleTabScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class PeoplePageGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=PeopleTabScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def setUp(self) -> None:
        super().setUp()
        self.clear_teammates(self.scenario)
        self.delete_remaining_teams(self.scenario)
    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_app.reopen_tune_app()
        cls.clear_teammates(cls.scenario)
        cls.delete_remaining_teams(cls.scenario)

        super().tearDownClass()

    def test_601_VC_141069_teammate_order_bar_everyone_tab_google(self):
        self.scenario.tc_teammate_order_everyone_tab()

    def test_602_VC_141070_teammate_search_bar_everyone_tab_google(self):
        self.scenario.tc_teammate_search_bar_everyone_tab()

    def test_603_VC_141071_teammate_search_profile_check_google(self):
        self.scenario.tc_teammate_search_profile_check()

    def test_604_VC_141072_teammates_add_from_everyone_tab_google(self):
        self.scenario.tc_teammates_add_from_everyone_tab()

    def test_605_VC_141073_teammates_add_from_all_teammates_page_google(self):
        self.scenario.tc_teammates_add_from_all_teammates_page()

    def test_606_VC_141074_teammates_remove_random_teammates_everyone_tab_google(self):
        self.scenario.tc_teammates_remove_random_teammates_everyone_tab()

    def test_607_VC_141075_teammates_remove_random_teammates_all_teammates_page_google(self):
        self.scenario.tc_teammates_remove_random_teammates_all_teammates_page()

    def test_608_VC_141076_teammate_gets_new_booking_google(self):
        self.scenario.tc_teammate_gets_new_booking(opposite_creds=self.microsoft_credentials_coily)

    def test_609_VC_141077_book_next_to_teammate_google(self):
        self.scenario.tc_book_next_to_teammate(opposite_creds=self.microsoft_credentials_coily)

    def test_610_VC_142128_people_in_office_everyone_tab_google(self):
        self.scenario.tc_people_in_office_everyone_tab(opposite_creds=self.microsoft_credentials_coily)

    def test_611_VC_142129_people_in_office_teammates_tab_google(self):
        self.scenario.tc_people_in_office_teammates_tab(opposite_creds=self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
