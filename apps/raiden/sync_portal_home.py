import time

from apps.raiden.sync_portal_system import SyncPortalSystem
from base.base_ui import UIBase
from locators.sync_portal.sync_portal_home_locators import SyncPortalHomeLocators


class SyncPortalHome(UIBase):

    def click_org_selector_icon(self):
        """
        Method to click on Org Selector Icon

        :param :
        :return : SyncPortalHome
        """
        self.look_element(SyncPortalHomeLocators.ORG_SELECTOR_ICON).click()
        time.sleep(1)
        return SyncPortalHome()

    def click_org_view_all(self):
        """
        Method to click on View All Orgs option

        :param :
        :return :SyncPortalHome
        """
        e = self.look_element(SyncPortalHomeLocators.ORG_VIEW_ALL)
        self.click_by_script(e)
        time.sleep(1)
        return SyncPortalHome()

    def click_on_org_name(self, org_name: str):
        """
        Method to click on Org Selector Icon

        :param :org_name :str
        :return :SyncPortalHome
        """
        self.look_element(SyncPortalHomeLocators.ORG_NAME, param=org_name).click()
        time.sleep(1)
        return SyncPortalHome()

    def click_system(self):
        """
        Method to click on Org Selector Icon

        :param :
        :return :SyncPortalSystem
        """
        self.look_element(SyncPortalHomeLocators.SYSTEM).click()
        return SyncPortalSystem()

    def click_logout_icon(self):
        """
        Method to click on Logout Icon

        :param :
        :return :SyncPortalHome
        """
        self.look_element(SyncPortalHomeLocators.LOGOUT_ICON).click()
        return SyncPortalHome()

    def click_logout(self):
        """
        Method to click on Logout Text

        :param :
        :return :SyncPortalLogin
        """
        time.sleep(1)
        self.look_element(SyncPortalHomeLocators.LOGOUT).click()
        from apps.raiden.sync_portal_login import SyncPortalLogin
        return SyncPortalLogin()

    def verify_logout(self) -> bool:
        """
        Method to verify Logout text

        :param :
        :return :bool
        """
        return self.verify_element(SyncPortalHomeLocators.LOGOUT, timeunit=2)

    def click_meeting_rooms_dashboard(self):
        """
        Method to click on Dashboard under Meeting Rooms

        :param :
        :return :
        """
        self.look_element(SyncPortalHomeLocators.MEETING_ROOMS_DASHBOARD).click()
        from apps.raiden.sync_portal_dashboard_meeting_rooms import SyncPortalDashboardMeetingRooms
        return SyncPortalDashboardMeetingRooms()

    def click_flex_desks_dashboard(self):
        """
        Method to click on Dashboard under Flex Desks

        :param :
        :return :
        """
        self.look_element(SyncPortalHomeLocators.FLEX_DESKS_DASHBOARD).click()
        from apps.raiden.sync_portal_dashboard_flex_desks import SyncPortalDashboardFlexDesks
        return SyncPortalDashboardFlexDesks()

    def click_meeting_rooms_issues(self):
        """
        Method to click on Issues under Meeting Rooms

        :param :
        :return :
        """
        self.look_element(SyncPortalHomeLocators.MEETING_ROOMS_ISSUES).click()
        from apps.raiden.sync_portal_issues_meeting_rooms import SyncPortalIssuesMeetingRooms
        return SyncPortalIssuesMeetingRooms()

    def click_flex_desks_issues(self):
        """
        Method to click on Issues under Flex Desks

        :param :
        :return :
        """
        self.look_element(SyncPortalHomeLocators.FLEX_DESKS_ISSUES).click()
        from apps.raiden.sync_portal_issues_flex_desks import SyncPortalIssuesFlexDesks
        return SyncPortalIssuesFlexDesks()
