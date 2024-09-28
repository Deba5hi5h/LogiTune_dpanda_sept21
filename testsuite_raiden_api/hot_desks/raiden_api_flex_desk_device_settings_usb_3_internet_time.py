import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime(UIBase):
    """
        Tests to verify Device Settings- USB 3.0 Priority and Internet time

        Tests:
            1.Disable USB 3.0 Priority
            2.Enable USB 3.0 Priority
            3.Disable internet time and set NTP server to time.android.com
            Negative test:
            4.Disable internet time and set NTP server to time@android.com
            5.Disable internet time and set NTP server to 0.us.pool.ntp.org
            6.Enable auto-configuration of internet time
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()

    device_name = "Coily"
    role = 'OrgAdmin'

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskDeviceSettingsUSB3InternetTime, self).tearDown()

    def test_1101_VC_121749_flex_desks_device_settings_usb_3_priority_enable(self):

        usb_3_priority_setting = 1

        Report.logInfo('STEP 1: Enable USB 3.0 Priority setting')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_usb_3_priority(
            role=self.role, device_name=self.device_name, high_speed_usb=usb_3_priority_setting)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1102_VC_121749_flex_desks_device_settings_usb_3_priority_disable(self):

        usb_3_priority_setting = 0

        Report.logInfo('STEP 1: Disable USB 3.0 Priority setting')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_usb_3_priority(
            role=self.role, device_name=self.device_name, high_speed_usb=usb_3_priority_setting)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1103_VC_121749_flex_desks_device_settings_disable_internet_time_set_ntp_server(self):

        ntp_server = 'time.android.com'

        Report.logInfo(
            f'STEP 1: Disable internet time and set NTP server to {ntp_server}')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_disable_internet_time_set_ntp_server(
            role=self.role, device_name=self.device_name, ntp_server=ntp_server)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1104_VC_121749_flex_desks_device_settings_disable_internet_time_set_ntp_server(self):

        ntp_server = '0.us.pool.ntp.org'

        Report.logInfo(
            f'STEP 1: Disable internet time and set NTP server to {ntp_server}')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_disable_internet_time_set_ntp_server(
            role=self.role, device_name=self.device_name, ntp_server=ntp_server)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1105_VC_121749_flex_desks_device_settings_disable_internet_time_set_ntp_server(self):

        ntp_server = 'time@android.com'

        Report.logInfo(
            f'STEP 1: Disable internet time and set NTP server to {ntp_server}')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_disable_internet_time_set_ntp_server(
            role=self.role, device_name=self.device_name, ntp_server=ntp_server)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

    def test_1106_VC_121749_flex_desks_device_settings_disable_internet_time_set_ntp_server(self):

        ntp_server = ""

        Report.logInfo(
            f'STEP 1: Enable auto - configuration of internet time, set ntp server to {ntp_server}')
        desk_id, site = self.syncportal_hotdesks_methods.tc_flex_desk_device_setting_disable_internet_time_set_ntp_server(
            role=self.role, device_name=self.device_name, ntp_server=ntp_server)

        Report.logInfo('STEP 2: Delete desk')
        self.syncportal_hotdesks_methods.tc_delete_flex_desk(self.role, desk_id)

        Report.logInfo(
            'STEP 3 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)


if __name__ == "__main__":
    unittest.main()
