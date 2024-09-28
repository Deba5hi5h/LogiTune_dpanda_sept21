import unittest

from apps.tune.tc_scenarios.notify_teammates_scenarios import NotifyTeammatesScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class NotifyTeammatesMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=NotifyTeammatesScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def setUp(self) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_901_VC_146833_notify_teammates_when_no_teams_google(self):
        self.scenario.tc_notify_teammates_when_no_teams()

    def test_902_VC_146834_notify_teammates_when_teams_created_google(self):
        self.scenario.tc_notify_teammates_when_teams_created()

    def test_903_VC_146835_notify_teammates_selection_persistency_in_other_bookings_google(self):
        self.scenario.tc_notify_teammates_selection_persistency_in_other_bookings()

    def test_904_VC_146836_notify_teammates_selection_persistency_after_relaunch_google(self):
        self.scenario.tc_notify_teammates_selection_persistency_after_relaunch()

    def test_905_VC_146837_notify_teammates_selection_persistency_after_relog_google(self):
        self.scenario.tc_notify_teammates_selection_persistency_after_relog(self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
