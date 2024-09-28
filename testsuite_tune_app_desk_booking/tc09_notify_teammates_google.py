import unittest

from apps.tune.tc_scenarios.notify_teammates_scenarios import NotifyTeammatesScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class NotifyTeammatesGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=NotifyTeammatesScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def setUp(self) -> None:
        super().setUp()
        self.delete_remaining_teams(self.scenario)
        self.clear_teammates(self.scenario)

    def test_951_VC_146838_notify_teammates_when_no_teams_microsoft(self):
        self.scenario.tc_notify_teammates_when_no_teams()

    def test_952_VC_146839_notify_teammates_when_teams_created_microsoft(self):
        self.scenario.tc_notify_teammates_when_teams_created()

    def test_953_VC_146840_notify_teammates_selection_persistency_in_other_bookings_microsoft(self):
        self.scenario.tc_notify_teammates_selection_persistency_in_other_bookings()

    def test_954_VC_146841_notify_teammates_selection_persistency_after_relaunch_microsoft(self):
        self.scenario.tc_notify_teammates_selection_persistency_after_relaunch()

    def test_955_VC_146842_notify_teammates_selection_persistency_after_relog_microsoft(self):
        self.scenario.tc_notify_teammates_selection_persistency_after_relog(self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
