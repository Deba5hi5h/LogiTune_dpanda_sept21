import unittest

from apps.raiden.sync_portal_methods import SyncPortalMethods
from apps.raiden.sync_portal_tests import SyncPortalTests
from base import global_variables
from base.base_ui import UIBase


class SyncPortalSanity(UIBase):
    raiden_tests = SyncPortalTests()
    raiden = SyncPortalMethods()
    UIBase.logi_tune_flag = True

    def test_101_VC_21429_landing_page(self):
        self.raiden_tests.tc_landing_page()

    def test_102_VC_21430_signin_to_sync_portal(self):
        self.raiden_tests.tc_login_to_sync_portal()

    def test_103_VC_10997_install_sync_desktop_app(self):
        self.raiden_tests.tc_install_sync_desktop_app()

    def test_104_VC_12884_provision_room_using_credentials(self):
        self.raiden_tests.tc_provision_room_using_credentials()

    def test_105_VC_11005_delete_room_from_sync_portal(self):
        self.raiden_tests.tc_delete_room_from_sync_portal()

    def test_106_VC_11034_logout_from_sync_portal(self):
        self.raiden.login_to_sync_portal(config=global_variables.config, role=global_variables.SYNC_ROLE)
        self.raiden_tests.tc_logout_from_sync_portal()


if __name__ == "__main__":
    unittest.main()
