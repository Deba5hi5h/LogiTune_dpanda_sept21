import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPIFlexDeskBookingSettings(UIBase):
    """
            Test case to modify flex desk booking settings
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPIFlexDeskBookingSettings, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIFlexDeskBookingSettings, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIFlexDeskBookingSettings, self).setUp()

    def tearDown(self):
        super(RaidenAPIFlexDeskBookingSettings, self).tearDown()

    def test_1201_VC_119982_flex_desk_booking_settings(self):
        """
             Test case to modify flex desk booking settings

                                 Steps:
                                    1. Sign in to Sync Portal using valid owner credentials.

                                Test:
                                    1.Desk Booking Settings- Enable show meeting agenda & disable hide meeting details
                                    2.Desk Booking Settings- Enable show meeting agenda & enable hide meeting details
                                    3.Desk Booking Settings- Disable show meeting agenda
                                    4.Desk Booking Settings - Set default brightness to 100.
                                    5.Desk Booking Settings - Set default brightness to 250.
                                    6.Desk Booking Settings- Set default language to English
                                    7.Desk Booking Settings- Set default time format to 24 hour clock
                                    8.Desk Booking Settings- Set default time format to 12 hour clock
        """

        rolelist_raiden = ['OrgAdmin', 'ThirdParty','OrgViewer']

        for role_raiden in rolelist_raiden:
            Report.logInfo(
                'STEP 1: Desk Booking Settings - Enable show meeting agenda & disable hide meeting details.')
            site, area = self.syncportal_hotdesks_methods.tc_desk_booking_setting_enable_show_meeting_disable_hide_meeting(
                role=role_raiden)

            Report.logInfo(
                'STEP 2: Desk Booking Settings- Enable show meeting agenda & enable hide meeting details')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_enable_show_meeting_agenda_enable_hide_meeting(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 3: Desk Booking Settings - Disable show meeting agenda.')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_disable_show_meeting_agenda(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 4: Desk Booking Settings - Set default brightness to 100.')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_screen_brightness_100(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 5: Desk Booking Settings - Set default brightness to 250.')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_screen_brightness_250(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 6: Desk Booking Settings - Set default language to English.')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_default_langauge_english(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 7: Desk Booking Settings - Set default time format to 24 hour clock.')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_default_time_format_24_hour(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 8: Desk Booking Settings - Set default time format to 12 hour clock.')
            self.syncportal_hotdesks_methods.tc_desk_booking_setting_default_time_format_12_hour(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP 9: Delete the site.')
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, site)


if __name__ == "__main__":
    unittest.main()
