import sys
import time
import unittest

from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from common.usb_switch import connect_device
from testsuite_sync_app.tc_methods import SyncTCMethods


class SyncAPISetup(UIBase):
    def test_install_sync_and_connect_devices(self):
        """
        Method to install Sync App and connect Rally Bar, Rally Bar Mini, MeetUp, Tap,
        Brio, Scribe, Rally and Rally Camera before running Sync API tests

        :param none
        :return none
        """
        sync_methods = SyncTCMethods()
        sync_app = SyncAppMethods()
        sync_methods.tc_install_sync_app()
        sync_app.open()
        sync_app.setup_seat_count().close()
        sync_methods.tc_connect_to_sync_portal()

        # install = Install()
        # install.test_001_VC_39949_install_sync_app()
        # syncApp = SyncUI()
        # syncApp.openSyncApp()
        # syncApp.setup_seat_count()
        # syncApp.closeSyncApp()
        # install.test_002_VC_39971_connect_to_sync_portal()
        devices = ["Rally", "Rally Camera", "MeetUp", "Rally Bar", "Rally Bar Mini", "Brio", "Tap", "Scribe"]
        for device in devices:
            connect_device(device)
            time.sleep(10)
        sync_app.open()
        # syncApp.openSyncApp()
        time.sleep(20)
        # syncApp.closeSyncApp()
        sync_app.close()

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(SyncAPISetup)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
