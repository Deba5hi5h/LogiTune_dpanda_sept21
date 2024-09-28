import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIUpdateFlexDesksPolicy(UIBase):
    """
            Test to update flex desks policy.
    """

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()

    @classmethod
    def setUp(cls):
        try:
            super(RaidenAPIUpdateFlexDesksPolicy, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIUpdateFlexDesksPolicy, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIUpdateFlexDesksPolicy, self).setUp()

    def tearDown(self):
        super(RaidenAPIUpdateFlexDesksPolicy, self).tearDown()

    def test_1002_VC_119815_Update_FlexDesks_Policy(self):
        """Tests to modify desk policy.
                                    Setup:
                                          1. Sign in to Sync Portal using valid owner credentials.

                                    Test:
                                        1. Desk Policy - Disable reserve remotely
                                        2. Desk Policy- Disable reserve remotely, enable walk-in session
                                        3. Desk Policy- Enable reserve remotely
                                        4. Desk Policy- Set max days to advance to 7 days
                                        5. Desk Policy- Set max days to advance to 14 days
                                        6. Desk Policy- Enable reservation time limit with time limit 8 hours
                                        7. Desk Policy - Disable reserved spot visible to others
                                        8. Desk Policy- Enable reserved spot visible to others
                                        9. Desk Policy- Disable walk-in
                                        10.Desk Policy - Enable walk-in with default walk-in session duration set to 1 hour
                                        11.Desk Policy - Disable session time limit
                                        12.Desk Policy - Enable Show QR code
                                        13.Desk Policy - Disable Show QR code
                                        14.Desk Policy - Enable Reservable and enable Check-in required with vacancy release set to 30 minutes
                                        15.Desk Policy - Enable Reservable and disable Check-in required
                                        16.Desk Policy - Enable walk-in with default walk-in session duration set to 1 hour and Notify user before desk released to 5 minutes
                                        17.Desk Policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes
                                        18.Desk Policy - Enable Auto-extend session
                                        19. Desk Policy - Enable Show QR code, Enable Reservable & set Check-in required to 20 minutes
                                        20. Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required
                                        21. Desk Policy - Enable walk-in session, disable auto-extend session and set Blocking user from re-using to 30 mins.
                                        22. Desk Policy - Disable walk-in session, Disable Check-in required, enable auto-extend session.
                                        23. Desk Policy - Enable Reservable, set max days in advance to 7 days and session time limit set to 12 hours and Show QR code enabled, Check-in required enabled
                                        24.Desk Policy - Enable Reservable, set max days in advance to 14 days, disable session time limt, disable Show QR code

                """

        rolelist_raiden = ['OrgAdmin', 'OrgViewer', 'ThirdParty']
       
        for role_raiden in rolelist_raiden:
            Report.logInfo('STEP 1: Desk Policy - Disable reserve remotely')
            site, building, floor, area = self.syncportal_hotdesks_methods.tc_disable_desk_policy_reserve_remotely(
role=role_raiden)

            Report.logInfo('STEP 2: Desk Policy - Disable reserve remotely, enable walk-in session')
            self.syncportal_hotdesks_methods.tc_modify_desk_policy_disable_reserve_remotely_enable_walkin_session(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 3: Desk Policy - Enable reserve remotely')
            self.syncportal_hotdesks_methods.tc_enable_desk_policy_reserve_remotely(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 4: Desk Policy - Set max days to advance to 7 days')
            self.syncportal_hotdesks_methods.tc_desk_policy_set_max_7_days(role=role_raiden, area_name=area)

            Report.logInfo('STEP 5: Desk Policy - Set max days to advance to 14 days')
            self.syncportal_hotdesks_methods.tc_desk_policy_set_max_14_days(role=role_raiden, area_name=area)

            Report.logInfo('STEP 6: Desk Policy - Enable reservation time limit to 8 hours')
            self.syncportal_hotdesks_methods.tc_desk_policy_set_reservation_time_limit_8_hours(role=role_raiden,area_name=area)

            Report.logInfo('STEP 7: Desk Policy - Disable reserved spot visible to others')
            self.syncportal_hotdesks_methods.tc_modify_desk_policy_disable_reserved_spot_visible_to_others(role=role_raiden, area_name=area)

            Report.logInfo('STEP 8: Desk Policy - Enable reserved spot visible to others')
            self.syncportal_hotdesks_methods.tc_desk_policy_enable_reserved_spot_visible_to_others(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 9: Desk Policy- Disable walk-in')
            self.syncportal_hotdesks_methods.tc_desk_policy_disable_walkin_session(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 10: Desk Policy - Enable walk-in with default walk-in session duration set to 1 hour')
            self.syncportal_hotdesks_methods.tc_desk_policy_enable_walkin_session(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 11: Desk Policy - Disable session time limit')
            self.syncportal_hotdesks_methods.tc_desk_policy_disable_session_time_limit(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 12: Desk Policy - Enable Show QR code')
            self.syncportal_hotdesks_methods.tc_desk_policy_enable_show_QR_code(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 13: Desk Policy - Disable Show QR code')
            self.syncportal_hotdesks_methods.tc_desk_policy_disable_show_QR_code(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 14: Desk Policy - Enable Reservable and enable Check - in required with vacancy release set to 30 minutes')
            self.syncportal_hotdesks_methods.tc_desk_policy_enable_reserve_remotely_checkin_vacancy_release_30_minutes(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 15: Desk Policy - Enable Reservable and disable Check-in required')
            self.syncportal_hotdesks_methods.tc_enable_desk_policy_reserve_remotely(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 16: Desk Policy - Enable walk-in with default walk-in session duration set to 1 hour and Notify user before desk released to 5 minutes')
            self.syncportal_hotdesks_methods.tc_enable_walkin_default_session_duration_notify_desk_released(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 17: Desk Policy - Disable Auto-extend session and set  blocking user from re-using set to 10 minutes')
            self.syncportal_hotdesks_methods.tc_desk_policy_disable_auto_extend_session_set_hardstop_10minutes(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 18: Desk Policy - Enable Auto-extend session')
            self.syncportal_hotdesks_methods.tc_desk_policy_enable_auto_extend_session(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 19: Desk Policy - Enable Show QR code, Enable Reservable & set Check-in required to 20 minutes')
            self.syncportal_hotdesks_methods.tc_enable_reservable_show_qr_code_check_in_20minutes(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 20: Desk Policy - Disable QR code reservation, Enable Reservable & disable Check-in required')
            self.syncportal_hotdesks_methods.tc_enable_reservable_disable_qr_code_and_checkin_required(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 21: Desk Policy - Enable walk-in session, disable auto-extend session and set Blocking user from re-using to 30 mins.')
            self.syncportal_hotdesks_methods.tc_enable_walkin_session_disable_auto_extend_block_reserve_reuse(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 22: Desk Policy - Disable walk-in session, Disable Check-in required, enable auto-extend session.')
            self.syncportal_hotdesks_methods.tc_disable_walkin_session_and_checkin_enable_autoextend(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 23: Desk Policy - Enable Reservable, set max days in advance to 7 days and session time limit set to 12 hours and Show QR code enabled, Check-in required enabled')
            self.syncportal_hotdesks_methods.tc_enable_reservable_set_maxdays_and_session_time_enable_qrcode_checkin(
                role=role_raiden, area_name=area)

            Report.logInfo('STEP 24: Desk Policy - Enable Reservable, set max days in advance to 14 days, disable session time limt, disable Show QR code')
            self.syncportal_hotdesks_methods.tc_enable_reservable_set_maxdays_disable_session_time_show_qrcode(
                role=role_raiden, area_name=area)

            Report.logInfo(
                'STEP : Delete the site.')
            self.syncportal_hotdesks_methods.tc_delete_site(role_raiden, site)


if __name__ == "__main__":
    unittest.main()
