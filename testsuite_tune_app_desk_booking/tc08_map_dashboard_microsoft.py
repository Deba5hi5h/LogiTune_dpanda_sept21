import unittest

from apps.tune.tc_scenarios.maps_scenarios import TuneMapScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class MapsMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=TuneMapScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)
        cls.scenario.sync_api_methods.enable_map_for_desks_floor(cls.scenario.org_id,
                                                                 cls.scenario.desk_id,
                                                                 True)

    def setUp(self, *args, **kwargs) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_851_VC_142776_default_booking_with_map_microsoft(self):
        self.scenario.tc_book_a_desk_with_map_default()

    def test_852_VC_142777_multiple_desks_booking_with_map_microsoft(self):
        self.scenario.tc_multiple_desks_booking_with_map()

    def test_853_VC_142778_multiple_day_booking_with_map_microsoft(self):
        self.scenario.tc_book_multiple_day_booking_with_map()

    def test_854_VC_142779_transfer_desk_with_map_microsoft(self):
        self.scenario.tc_transfer_desk_with_map()

    def test_855_VC_142780_book_next_to_person_on_map_microsoft(self):
        self.scenario.tc_book_next_to_person_on_map(opposite_creds=self.google_credentials_coily)

    def test_856_VC_142781_book_next_to_teammate_on_map_microsoft(self):
        self.scenario.tc_book_next_to_teammate_on_map(opposite_creds=self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
