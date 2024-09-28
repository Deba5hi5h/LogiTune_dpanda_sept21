import logging
import unittest
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from base.base_ui import UIBase
from common import config
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPISession(UIBase):
    """
    Test to verify device APIs for Brio.
    """
    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPISession, cls).setUpClass()

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPISession, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPISession, self).setUp()

    def tearDown(self):
        super(RaidenAPISession, self).tearDown()

    def test_101_VC_12849_get_raiden_backend_version(self):
        try:
            raiden_backend_version = self.syncportal_methods.tc_raiden_backend_version()
            settings = config.CommonConfig.get_instance()
            if raiden_backend_version is not None:
                settings.set_value_in_section('RUN_CONFIG', 'SYNC_API_VERSION', raiden_backend_version)
        except Exception as e:
            Report.logException(f'{e}')

    def test_102_VC_16601_sign_in_owner(self):
        role_raiden = 'OrgAdmin'
        self.syncportal_methods.tc_sign_in(role=role_raiden)

    def test_103_VC_37356_sign_in_admin(self):
        role_raiden = 'OrgViewer'
        self.syncportal_methods.tc_sign_in(role=role_raiden)

    def test_104_VC_18491_sign_in_read_only(self):
        role_raiden = 'Readonly'
        self.syncportal_methods.tc_sign_in(role=role_raiden)

    def test_105_VC_100308_sign_in_third_party(self):
        role_raiden = 'ThirdParty'
        self.syncportal_methods.tc_sign_in(role=role_raiden)

    def test_106_VC_115004_sign_in_installer(self):
        role_raiden = "Installer"
        self.syncportal_methods.tc_sign_in(role=role_raiden)

    def test_107_VC_115005_sign_in_device_admin(self):
        role_raiden = "DeviceAdmin"
        self.syncportal_methods.tc_sign_in(role=role_raiden)

    def test_108_VC_115006_sign_in_device_manager(self):
        role_raiden = "DeviceManager"
        self.syncportal_methods.tc_sign_in(role=role_raiden)


if __name__ == "__main__":
    unittest.main()
