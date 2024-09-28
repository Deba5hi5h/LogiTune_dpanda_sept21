import unittest

from apps.tune.tc_scenarios.people_tab_scenarios import PeopleTabScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class PeoplePageMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=PeopleTabScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def setUp(self) -> None:
        super().setUp()
        self.clear_teammates(self.scenario)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tune_app.reopen_tune_app()
        cls.clear_teammates(cls.scenario)
        super().tearDownClass()

    def test_651_VC_141059_teammate_order_bar_everyone_tab_microsoft(self):
        self.scenario.tc_teammate_order_everyone_tab()

    def test_652_VC_141060_teammate_search_bar_everyone_tab_microsoft(self):
        self.scenario.tc_teammate_search_bar_everyone_tab()

    def test_653_VC_141061_teammate_search_profile_check_microsoft(self):
        self.scenario.tc_teammate_search_profile_check()

    def test_654_VC_141063_teammates_add_from_everyone_tab_microsoft(self):
        self.scenario.tc_teammates_add_from_everyone_tab()

    def test_655_VC_141064_teammates_add_from_all_teammates_page_microsoft(self):
        self.scenario.tc_teammates_add_from_all_teammates_page()

    def test_656_VC_141065_teammates_remove_random_teammates_everyone_tab_microsoft(self):
        self.scenario.tc_teammates_remove_random_teammates_everyone_tab()

    def test_657_VC_141066_teammates_remove_random_teammates_all_teammates_page_microsoft(self):
        self.scenario.tc_teammates_remove_random_teammates_all_teammates_page()

    def test_658_VC_141067_teammate_gets_new_booking_microsoft(self):
        self.scenario.tc_teammate_gets_new_booking(opposite_creds=self.google_credentials_coily)

    def test_659_VC_141068_book_next_to_teammate_microsoft(self):
        self.scenario.tc_book_next_to_teammate(opposite_creds=self.google_credentials_coily)

    def test_660_VC_142126_people_in_office_everyone_tab_microsoft(self):
        self.scenario.tc_people_in_office_everyone_tab(opposite_creds=self.google_credentials_coily)

    def test_661_VC_142127_people_in_office_teammates_tab_microsoft(self):
        self.scenario.tc_people_in_office_teammates_tab(opposite_creds=self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
