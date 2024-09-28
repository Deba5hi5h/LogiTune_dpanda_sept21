import unittest

from apps.tune.tc_scenarios.team_creation_scenarios import TeamCreationScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class TeamCreationMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=TeamCreationScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def setUp(self, *args, **kwargs) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_751_VC_141082_create_team_input_team_name_check_microsoft(self):
        self.scenario.tc_create_team_input_team_name_check()

    def test_752_VC_141083_edit_team_input_team_name_check_microsoft(self):
        self.scenario.tc_edit_team_input_team_name_check()

    def test_753_VC_141084_edit_team_team_delete_microsoft(self):
        self.scenario.tc_edit_team_team_delete()

    def test_754_VC_141085_custom_team_teammate_add_microsoft(self):
        self.scenario.tc_custom_team_teammate_add(opposite_creds=self.google_credentials_coily)

    def test_755_VC_141086_custom_team_teammate_remove_microsoft(self):
        self.scenario.tc_custom_team_teammate_remove(opposite_creds=self.google_credentials_coily)

    def test_756_VC_141087_custom_team_create_team_from_manage_teams_page_microsoft(self):
        self.scenario.custom_team_create_team_from_manage_teams_page(opposite_creds=self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
