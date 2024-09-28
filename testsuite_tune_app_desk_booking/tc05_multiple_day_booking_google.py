import unittest

from apps.tune.tc_scenarios.multiple_day_booking_scenarios import MultipleDayBookingScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class MultipleDayBookingGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=MultipleDayBookingScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def test_501_VC_140083_book_multiple_day_booking(self):
        self.scenario.tc_book_multiple_day_booking()

    def test_502_VC_140084_book_multiple_day_booking_edit_one_booking(self):
        self.scenario.tc_book_multiple_day_booking_edit_one_booking()

    def test_503_VC_140085_book_multiple_day_booking_delete_one_booking(self):
        self.scenario.tc_book_multiple_day_booking_delete_one_booking()

    def test_504_VC_140086_book_multiple_day_booking_max_days_in_advance(self):
        self.scenario.tc_book_multiple_day_booking_max_days_in_advance(**self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
