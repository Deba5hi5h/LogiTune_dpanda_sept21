import unittest

from apps.tune.tc_scenarios.notifications_scenarios import NotificationsScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class NotificationsPageMicrosoft(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=NotificationsScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.microsoft_credentials_coily)

    def test_451_VC_134040_notifications_page_admin_created_booking_microsoft(self):
        self.scenario.tc_notifications_page_admin_created_booking(**self.microsoft_credentials_coily)

    def test_452_VC_134041_notifications_page_admin_edited_booking_microsoft(self):
        self.scenario.tc_notifications_page_admin_edited_booking(**self.microsoft_credentials_coily)

    def test_453_VC_134042_notifications_page_admin_edited_booking_created_by_user_microsoft(self):
        self.scenario.tc_notifications_page_admin_edited_booking_created_by_user(**self.microsoft_credentials_coily)

    def test_454_VC_134043_notifications_page_admin_cancelled_booking_microsoft(self):
        self.scenario.tc_notifications_page_admin_cancelled_booking(**self.microsoft_credentials_coily)

    def test_455_VC_134044_notifications_page_admin_cancelled_booking_booking_created_by_user_microsoft(self):
        self.scenario.tc_notifications_page_admin_cancelled_booking_created_by_user(**self.microsoft_credentials_coily)

    def test_456_VC_134045_notifications_page_notifications_order_microsoft(self):
        self.scenario.tc_notifications_page_notifications_order(**self.microsoft_credentials_coily)

    def test_457_VC_134046_notifications_page_cancel_booking_created_by_admin_microsoft(self):
        self.scenario.tc_notifications_page_cancel_booking_created_by_admin(**self.microsoft_credentials_coily)

    def test_458_VC_134047_notifications_page_rebook_after_booking_deleted_by_admin_microsoft(self):
        self.scenario.tc_notifications_page_rebook_after_booking_deleted_by_admin(**self.microsoft_credentials_coily)

    def test_459_VC_134048_notifications_page_check_in_required_microsoft(self):
        self.scenario.tc_notifications_page_check_in_required(**self.microsoft_credentials_coily)

    def test_460_VC_134049_notifications_close_buttons_check_microsoft(self):
        self.scenario.tc_notifications_page_close_button_check(**self.microsoft_credentials_coily)


if __name__ == "__main__":
    unittest.main()
