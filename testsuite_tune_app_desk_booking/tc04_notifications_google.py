import unittest

from apps.tune.tc_scenarios.notifications_scenarios import NotificationsScenarios
from apps.tune.base.desk_booking_base import DeskBookingBaseTestCase


class NotificationsPageGoogle(DeskBookingBaseTestCase):

    @classmethod
    def setUpClass(cls, *args) -> None:
        super().setUpClass(*args, scenario_class=NotificationsScenarios)
        cls.scenario.connect_to_work_account_if_not_logged(**cls.google_credentials_coily)

    def test_401_VC_134030_notifications_page_admin_created_booking_google(self):
        self.scenario.tc_notifications_page_admin_created_booking(**self.google_credentials_coily)

    def test_402_VC_134031_notifications_page_admin_edited_booking_google(self):
        self.scenario.tc_notifications_page_admin_edited_booking(**self.google_credentials_coily)

    def test_403_VC_134032_notifications_page_admin_edited_booking_created_by_user_google(self):
        self.scenario.tc_notifications_page_admin_edited_booking_created_by_user(**self.google_credentials_coily)

    def test_404_VC_134033_notifications_page_admin_cancelled_booking_google(self):
        self.scenario.tc_notifications_page_admin_cancelled_booking(**self.google_credentials_coily)

    def test_405_VC_134034_notifications_page_admin_cancelled_booking_booking_created_by_user_google(self):
        self.scenario.tc_notifications_page_admin_cancelled_booking_created_by_user(**self.google_credentials_coily)

    def test_406_VC_134035_notifications_page_notifications_order_google(self):
        self.scenario.tc_notifications_page_notifications_order(**self.google_credentials_coily)

    def test_407_VC_134036_notifications_page_cancel_booking_created_by_admin_google(self):
        self.scenario.tc_notifications_page_cancel_booking_created_by_admin(**self.google_credentials_coily)

    def test_408_VC_134037_notifications_page_rebook_after_booking_deleted_by_admin_google(self):
        self.scenario.tc_notifications_page_rebook_after_booking_deleted_by_admin(**self.google_credentials_coily)

    def test_409_VC_134038_notifications_page_check_in_required_google(self):
        self.scenario.tc_notifications_page_check_in_required(**self.google_credentials_coily)

    def test_410_VC_134039_notifications_close_buttons_check_google(self):
        self.scenario.tc_notifications_page_close_button_check(**self.google_credentials_coily)


if __name__ == "__main__":
    unittest.main()
