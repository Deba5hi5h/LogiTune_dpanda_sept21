import unittest

from apps.tune.tc_scenarios.desk_booking_scenarios import DeskBookingScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class DeskBooking(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args, **kwargs) -> None:
        super().setUpClass(*args, scenario_class=DeskBookingScenarios)

    def test_100_VC_XXXXXX_connect_to_google_work_account(self):
        self.scenario.tc_login_to_work_account(**self.google_credentials_coily)

    def test_101_VC_XXXXXX_verify_book_a_desk_pop_up_controls(self):
        self.scenario.tc_verify_book_a_desk_pop_up_controls()

    def test_102_VC_XXXXXX_verify_book_a_desk_page_default_options(self):
        self.scenario.tc_verify_book_a_desk_page_default_options()

    def test_103_VC_XXXXXX_verify_book_a_desk_page_inner_options(self):
        self.scenario.tc_verify_book_a_desk_page_inner_options()

    def test_1001_VC_XXXXXX_set_random_desk_booking_time_range(self):
        self.scenario.tc_set_random_desk_booking_time_range()

    def test_1002_VC_XXXXXX_book_a_desk(self):
        self.scenario.tc_book_a_desk()

    def test_1003_VC_XXXXXX_end_booking_of_the_desk(self):
        self.scenario.tc_end_occupying_of_the_desk()


if __name__ == "__main__":
    unittest.main()
