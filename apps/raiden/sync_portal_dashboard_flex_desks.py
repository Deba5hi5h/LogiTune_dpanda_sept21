from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_portal.sync_portal_dashboard_flex_desks_locators import SyncPortalDashboardFlexDesksLocators


class SyncPortalDashboardFlexDesks(UIBase):
    """
    Sync Portal Flex Desks Dashboard Page test methods
    """

    def verify_flex_desks_dashboard_page(self) -> bool:
        """
        Method to verify Meeting rooms heading displayed in Dashboard Page

        :return bool
        """
        return self.verify_element(SyncPortalDashboardFlexDesksLocators.FLEX_DESKS_HEADING, timeunit=5)
