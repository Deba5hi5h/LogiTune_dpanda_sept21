import unittest

from apps.tune.tc_scenarios.team_creation_scenarios import TeamCreationScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class TeamCreationGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=TeamCreationScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def setUp(self, *args, **kwargs) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_701_VC_141088_create_team_input_team_name_check_google(self):
        self.scenario.tc_create_team_input_team_name_check()

    def test_702_VC_141089_edit_team_input_team_name_check_google(self):
        self.scenario.tc_edit_team_input_team_name_check()

    def test_703_VC_141090_edit_team_team_delete_google(self):
        self.scenario.tc_edit_team_team_delete()

    def test_704_VC_141091_custom_team_teammate_add_google(self):
        self.scenario.tc_custom_team_teammate_add(opposite_creds=self.microsoft_credentials_coily)

    def test_705_VC_141092_custom_team_teammate_remove_google(self):
        self.scenario.tc_custom_team_teammate_remove(opposite_creds=self.microsoft_credentials_coily)

    def test_706_VC_141093_custom_team_create_team_from_manage_teams_page_google(self):
        self.scenario.custom_team_create_team_from_manage_teams_page(opposite_creds=self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
