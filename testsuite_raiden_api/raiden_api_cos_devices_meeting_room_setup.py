import sys
import unittest
from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from testsuite_sync_app.tc_methods import SyncTCMethods
from datetime import datetime
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from common.platform_helper import get_custom_platform
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from common import config
from common.usb_switch import connect_device
import time


class RaidenAPICOSDevicesSetup(UIBase):

    sync_methods = SyncTCMethods()
    sync_app = SyncAppMethods()
    sync_portal = SyncPortalAppMethods()
    syncportal_methods = SyncPortalTCMethods()
    room_name = None

    def test_001_VC_11009_install_sync_app_and_connect_to_sync_portal(self):
        """
        Method to install Sync App and connect it to Sync Portal.
        Prerequisite: Connect Rally Bar in device mode and Rally Bar Mini in device mode to acroname connected to the
        computer running sync app.

        :param none
        :return none
        """
        raiden_backend_version = self.syncportal_methods.tc_raiden_backend_version()
        settings = config.CommonConfig.get_instance()
        if raiden_backend_version is not None:
            settings.set_value_in_section('RUN_CONFIG', 'SYNC_API_VERSION', raiden_backend_version)

        self.sync_methods.tc_install_sync_app()
        now = datetime.now()
        type(self).room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        provision_code = self.sync_portal.create_empty_room_and_get_provision_code(room_name=self.room_name)
        self.sync_app.open()
        self.sync_app.connect_to_sync_portal_using_provision_code(provision_code=provision_code).close()

        devices = ["Rally Bar", "Rally Bar Mini"]
        for device in devices:
            connect_device(device)
            time.sleep(10)


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICOSDevicesSetup)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
