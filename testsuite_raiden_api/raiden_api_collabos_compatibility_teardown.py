import sys
import unittest

from apps.sync.sync_app_methods import SyncAppMethods
from base.base_ui import UIBase
from testsuite_sync_app.tc_methods import SyncTCMethods
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apis.raiden_api import raiden_helper
from base import global_variables
from common.usb_switch import connect_device
from common.usb_switch import disconnect_all
import time


class RaidenAPICollabOSCompatibilityTearDown(UIBase):

    sync_methods = SyncTCMethods()
    sync_app = SyncAppMethods()
    sync_portal = SyncPortalAppMethods()
    room_name = None
    role = 'OrgAdmin'

    def test_6001_VC_11135_delete_room_from_sync_portal_and_uninstall_sync_app(self):
        """
        Method to delete room from sync portal, connect device(s) back to the computer via acroname and uninstall sync app.

        :param none
        :return none
        """
        self.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.token = raiden_helper.signin_method(global_variables.config, self.role)
        self.org_id = raiden_helper.get_org_id(self.role, global_variables.config, self.token)
        disconnect_all()
        raiden_helper.delete_room(self.room_name, self.org_id, self.token)
        # Restore by enabling Acroname Port 0 and Port 1.
        # Acroname Port 0 is named as switch_port_rally_bar and Acroname Port 1 is named as switch_port_rally_camera in
        # properties.LOCAL.
        devices = ["Rally Bar", "Rally Camera"]
        for device in devices:
            connect_device(device)
            time.sleep(10)
        self.sync_methods.tc_uninstall_sync_app()


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICollabOSCompatibilityTearDown)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected")