import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report


log = logging.getLogger(__name__)

class RaidenAPIFlexDeskRebootDeprovisionDevice(UIBase):
    """
                Tests to verify device reboot and device deprovision

        Tests:
            1. Logi Dock Flex - Reboot - Reboot Now
            2. Logi Dock Flex - Deprovision this device
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()

    device_name = "Coily"
    role = "OrgAdmin"

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskRebootDeprovisionDevice, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskRebootDeprovisionDevice, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskRebootDeprovisionDevice, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskRebootDeprovisionDevice, self).tearDown()

    def test_1301_VC_122975_flex_desks_reboot_device_deprovision_device(self):

        Report.logInfo('STEP 1: Logi Dock Flex - Reboot Device')
        result_list = self.syncportal_hotdesks_methods.tc_flex_desk_reboot_device(
            role=self.role, device_name=self.device_name)

        desk_id = result_list[0]
        site = result_list[1]
        device_id = result_list[2]
        token = result_list[3]
        org_id = result_list[4]
        desk_name = result_list[5]

        Report.logInfo('STEP 2: Logi Dock Flex - Deprovision the device')
        self.syncportal_hotdesks_methods.tc_flex_desk_deprovision_device(
            device_id=device_id, desk_id=desk_id, token=token, org_id=org_id, desk_name=desk_name)

        Report.logInfo('STEP 3: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 4 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)



