import unittest

from apps.tune.tc_scenarios.maps_scenarios import TuneMapScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class MapsGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=TuneMapScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)
        cls.scenario.sync_api_methods.enable_map_for_desks_floor(cls.scenario.org_id,
                                                                 cls.scenario.desk_id,
                                                                 True)

    def setUp(self, *args, **kwargs) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_801_VC_142782_default_booking_with_map_google(self):
        self.scenario.tc_book_a_desk_with_map_default()

    def test_802_VC_142783_multiple_desks_booking_with_map_google(self):
        self.scenario.tc_multiple_desks_booking_with_map()

    def test_803_VC_142784_multiple_day_booking_with_map_google(self):
        self.scenario.tc_book_multiple_day_booking_with_map()

    def test_804_VC_142785_transfer_desk_with_map_google(self):
        self.scenario.tc_transfer_desk_with_map()

    def test_805_VC_142786_book_next_to_person_on_map_google(self):
        self.scenario.tc_book_next_to_person_on_map(opposite_creds=self.microsoft_credentials_coily)

    def test_806_VC_142787_book_next_to_teammate_on_map_google(self):
        self.scenario.tc_book_next_to_teammate_on_map(opposite_creds=self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
