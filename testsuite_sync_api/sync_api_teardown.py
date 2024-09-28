import sys
import time
import unittest

from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from common.usb_switch import disconnect_all
from testsuite_sync_app.tc_methods import SyncTCMethods


class SyncAPITeardown(UIBase):
    def test_uninstall_sync_and_disconnect_devices(self):
        """
        Method to uninstall Sync App and disconnect Rally Bar, Rally Bar Mini, MeetUp, Tap,
        Brio, Scribe, Rally and Rally Camera after running Sync API tests

        :param none
        :return none
        """
        sync_methods = SyncTCMethods()
        sync_app = SyncAppMethods()
        disconnect_all()
        sync_app.close()
        sync_methods.tc_uninstall_sync_app()

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(SyncAPITeardown)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")
