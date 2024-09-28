import unittest

from apps.raiden.sync_portal_tests import SyncPortalTests
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report


class SyncPortalNavigation(UIBase):
    raiden_tests = SyncPortalTests()
    UIBase.logi_tune_flag = True

    def test_001_VC_21430_login_to_sync_portal(self):
        self.raiden_tests.tc_login_to_sync_portal()

    def test_002_VC_141939_sync_portal_navigation(self):
        self.raiden_tests.tc_sync_portal_navigation()

    def test_003_VC_11034_logout_from_sync_portal(self):
        self.raiden_tests.tc_logout_from_sync_portal()


if __name__ == "__main__":
    unittest.main()
