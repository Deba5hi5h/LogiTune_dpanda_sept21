from base.base_ui import UIBase
from locators.sync_portal.sync_portal_issues_flex_desks_locators import SyncPortalIssuesFlexDesksLocators


class SyncPortalIssuesFlexDesks(UIBase):
    """
    Sync Portal Flex Desks Issues Page test methods
    """

    def verify_flex_desks_issues_page(self) -> bool:
        """
        Method to verify Issues displayed in Flex Desks issues Page

        :return bool
        """
        return self.verify_element(SyncPortalIssuesFlexDesksLocators.FLEX_DESKS_ISSUES_TAB, timeunit=5)
