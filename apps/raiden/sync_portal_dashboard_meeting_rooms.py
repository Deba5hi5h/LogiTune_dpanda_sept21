import time

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from apps.raiden.sync_portal_room import SyncPortalRoom
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_portal.sync_portal_dashboard_meeting_rooms_locators import SyncPortalDashboardMeetingRoomsLocators


class SyncPortalDashboardMeetingRooms(UIBase):
    """
    Sync Portal Meeting Rooms Dashboard Page test methods
    """
    def verify_meeting_dashboard_page(self) -> bool:
        """
        Method to verify Meeting rooms heading displayed in Dashboard Page

        :return bool
        """
        return self.verify_element(SyncPortalDashboardMeetingRoomsLocators.MEETING_ROOMS_HEADING, timeunit=5)