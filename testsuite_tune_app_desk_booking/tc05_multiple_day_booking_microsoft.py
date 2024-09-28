import unittest

from apps.tune.tc_scenarios.multiple_day_booking_scenarios import MultipleDayBookingScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class MultipleDayBookingMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=MultipleDayBookingScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def test_551_VC_140079_book_multiple_day_booking(self):
        self.scenario.tc_book_multiple_day_booking()

    def test_552_VC_140080_book_multiple_day_booking_edit_one_booking(self):
        self.scenario.tc_book_multiple_day_booking_edit_one_booking()

    def test_553_VC_140081_book_multiple_day_booking_delete_one_booking(self):
        self.scenario.tc_book_multiple_day_booking_delete_one_booking()

    def test_554_VC_140082_book_multiple_day_booking_max_days_in_advance(self):
        self.scenario.tc_book_multiple_day_booking_max_days_in_advance(**self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
