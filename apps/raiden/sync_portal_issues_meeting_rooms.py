from base.base_ui import UIBase
from locators.sync_portal.sync_portal_issues_meeting_rooms_locators import SyncPortalIssuesMeetingRoomsLocators


class SyncPortalIssuesMeetingRooms(UIBase):
    """
    Sync Portal Meeting Rooms Issues Page test methods
    """

    def verify_meeting_rooms_issues_page(self) -> bool:
        """
        Method to verify issues tab displayed in Meeting rooms Issues Page

        :return bool
        """
        return self.verify_element(SyncPortalIssuesMeetingRoomsLocators.MEETING_ROOMS_ISSUES_TAB, timeunit=5)
