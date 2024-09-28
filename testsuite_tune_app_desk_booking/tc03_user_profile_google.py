import unittest

from apps.tune.tc_scenarios.user_profile_scenarios import UserProfileScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class UserProfileGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=UserProfileScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def test_301_VC_134020_user_profile_page_check_google(self):
        self.scenario.tc_user_profile_page_check(**self.google_credentials_coily)

    def test_302_VC_134021_user_profile_default_building_change_google(self):
        self.scenario.tc_user_profile_page_default_building_change(**self.google_credentials_coily)

    def test_303_VC_134022_user_profile_keep_bookings_private_check_google(self):
        self.scenario.tc_user_profile_page_keep_bookings_private_check()

    def test_304_VC_134023_user_profile_default_building_change_and_book_google(self):
        self.scenario.tc_user_profile_page_default_building_change_and_book(**self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
