import unittest

from apps.tune.tc_scenarios.user_profile_scenarios import UserProfileScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class UserProfileMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=UserProfileScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def test_351_VC_134024_user_profile_page_check_microsoft(self):
        self.scenario.tc_user_profile_page_check(**self.microsoft_credentials_coily)

    def test_352_VC_134025_user_profile_default_building_change_microsoft(self):
        self.scenario.tc_user_profile_page_default_building_change(**self.microsoft_credentials_coily)

    def test_353_VC_134026_user_profile_keep_bookings_private_check_microsoft(self):
        self.scenario.tc_user_profile_page_keep_bookings_private_check(**self.microsoft_credentials_coily)

    def test_354_VC_134027_user_profile_default_building_change_and_book_microsoft(self):
        self.scenario.tc_user_profile_page_default_building_change_and_book(**self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
