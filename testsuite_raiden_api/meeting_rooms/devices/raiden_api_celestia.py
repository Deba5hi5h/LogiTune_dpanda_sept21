import logging
import unittest
import json
import sys
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report
from apis.raiden_api import raiden_helper, raiden_validation_methods
from apps.sync.sync_app_methods import SyncAppMethods
from common import raiden_config
from common.image_settings import get_image_settings
from base import global_variables

log = logging.getLogger(__name__)


class RaidenAPICelestia(UIBase):
    """
    Test to verify device APIs for Celestia.
    """
    sync_app = SyncAppMethods()
    syncportal_methods = SyncPortalTCMethods()
    sync_driver = None
    device_type = 'Celestia'
    room_name = None

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPICelestia, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPICelestia, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPICelestia, self).setUp()
        RaidenAPICelestia.room_name = self.sync_app.open_and_get_room_name()
        self.sync_app.close()
        self.token = raiden_helper.signin_method(global_variables.config, self.role)
        self.org_id = raiden_helper.get_org_id(self.role, global_variables.config, self.token)
        self.device_id = raiden_helper.get_device_id_from_room_name(global_variables.config, self.room_name,
                                                                    self.org_id, self.token, self.device_type)
        self.device_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/device/" + \
                          self.device_id

        # Default settings: Perspective correction - enabled, Video enhancement- enabled, Full presenter removal
        # disabled and Color Inversion disabled.
        self.default_whiteboard_settings_payload = {"whiteboardSettings": {"imageEnhancement": 1, "ghosting": 1,
                                                    "perspectiveCorrection": 1, "colorInversion": 0}}
        raiden_helper.put_whiteboard_settings_of_celestia(self.device_url, self.token,
                                                          self.default_whiteboard_settings_payload)

    def tearDown(self):
        super(RaidenAPICelestia, self).tearDown()
        # Revert the settings back to default values.
        raiden_helper.put_whiteboard_settings_of_celestia(self.device_url, self.token,
                                                          self.default_whiteboard_settings_payload)

    def test_1201_VC_53849_Get_Device_Celestia(self):
        self.syncportal_methods.tc_get_device(room_name=self.room_name,
                                              role=self.role,
                                              device_name=self.device_type)

    def test_1202_VC_95111_Verify_default_whiteboard_settings_of_Celestia(self):
        """Default Whiteboard Settings of Celestia.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Celestia is connected to the organization: VC-AUTOINFRA.

            Test:
                 1. Query the API:
                 GET ~/org/{org-id}/room/{room-id}/device/{device-id}
                 to get the values associated with whiteboard settings of Celestia.
                 2. Check the default whiteboard settings.

        """
        try:
            self.banner(f'Default Whiteboard Settings of Celestia')

            # Step 1: Get the whiteboard settings of the celestia.
            Report.logInfo('Step 1: Get the whiteboard settings of the celestia.')
            response, whiteboard_settings = raiden_helper.get_whiteboard_settings_of_celestia(self.device_url,
                                                                                              self.token)
            status_response = raiden_validation_methods.validate_get_device(response)

            # Step 2: Expected Default whiteboard settings
            Report.logInfo('Step 2: Expected Default whiteboard settings')
            expected_whiteboard_settings = dict()
            expected_whiteboard_settings['perspectiveCorrection'] = 1
            expected_whiteboard_settings['imageEnhancement'] = 1
            expected_whiteboard_settings['colorInversion'] = 0
            expected_whiteboard_settings['ghosting'] = 1

            json_formatted_expected_whiteboard_settings = json.dumps(expected_whiteboard_settings, indent=2)
            Report.logInfo(f'Expected Default Whiteboard Settings')
            Report.logInfo(f'{json_formatted_expected_whiteboard_settings}')

            # Step 3: Compare the whiteboard settings of celestia and default whiteboard settings.
            Report.logInfo('Step 3: Compare the whiteboard settings of celestia and default whiteboard settings.')
            status_comparison = True
            for key, value in expected_whiteboard_settings.items():
                if int(whiteboard_settings[key]) != int(value):
                    status_comparison = False

            status = status_response & status_comparison

            if status:
                Report.logPass(f'Whiteboard settings of Celestia matches the expected default settings.')
            else:
                Report.logFail('Whiteboard settings of Celestia do not match the expected default settings')

            assert status is True, 'Error in status'

        except AssertionError as e:
            Report.logException(f'{e}')
            raise e

    def test_1203_VC_95112_update_whiteboard_settings_of_Celestia(self):
        """Update whiteboard settings: Celestia.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Celestia is connected to the organization: VC-AUTOINFRA.

            Test:
                 1. Check the current whiteboard settings of celestia.
                 2. Capture the screenshot of the camera stream.
                 3. Update whiteboard settings by turning on both Full Presenter removal and Color Inversion.
                  Query the API: PUT call to Device
                  PUT ~/org/{org-id}/room/{room-id}/device/{device-id} providing the payload of whiteboardSettings and
                  update the whiteboard settings by updating Color Inversion.
                 4. Get the whiteboard settings associated with Celestia.
                 5. Capture screenshot of the camera stream with updated whiteboard settings.
                 6. Verify that the change in whiteboard settings made via sync portal propagates to the device by doing
                 image comparison using the above screenshots. The Screenshots should differ from each other.

        """
        try:
            self.banner('Update whiteboard settings: Celestia')

            # Step 1: Check the current whiteboard settings of celestia.
            Report.logInfo('Step 1: Check the current whiteboard settings of celestia.')
            raiden_helper.get_whiteboard_settings_of_celestia(device_url=self.device_url, token=self.token)

            # Step 2: Capture the screenshot of the camera stream.
            Report.logInfo('Step 2: Capture the screenshot of the camera stream.')
            device_name = "Scribe"
            self.sync_app.open().click_device_camera(device_name=device_name)
            current = self.sync_app.camera.get_screenshot_from_video_stream(name='Current')
            brightness_current = (get_image_settings(current))[0]
            Report.logInfo(f'Brightness of the capture before updating whiteboard settings is {brightness_current}')
            self.sync_app.close()

            # Step 3: Update whiteboard settings by turning on both Full Presenter removal and Color Inversion.
            Report.logInfo('Step 3: Update whiteboard settings by turning on both Full Presenter removal and '
                           'Color Inversion.')
            whiteboard_settings_payload = {"whiteboardSettings": {"imageEnhancement": 1, "ghosting": 0,
                                                                  "perspectiveCorrection": 1, "colorInversion": 1}}
            response = raiden_helper.put_whiteboard_settings_of_celestia(self.device_url, self.token,
                                                                         whiteboard_settings_payload)
            status_response = raiden_validation_methods.validate_empty_response(response)

            # Step 4: Get the whiteboard settings associated with Celestia.
            Report.logInfo('Step 4: Get the whiteboard settings associated with Celestia.')
            raiden_helper.get_whiteboard_settings_of_celestia(self.device_url, self.token)

            # Step 5: Capture the screenshot of the camera stream with updated whiteboard settings.
            Report.logInfo('Step 5: Capture the screenshot of the camera stream with updated whiteboard settings.')
            device_name = "Scribe"
            self.sync_app.open().click_device_camera(device_name=device_name)
            updated = self.sync_app.camera.get_screenshot_from_video_stream(name='Updated')
            brightness_updated = (get_image_settings(updated))[0]
            Report.logInfo(f'Brightness of the capture after updating whiteboard settings is {brightness_updated}')

            # Step 6: Verify that the change in whiteboard settings made via sync portal propagates to the device by
            # doing image comparison using the above screenshots. Brightness in light mode should be greater than
            # dark mode.
            Report.logInfo('Verify that the change in whiteboard settings made via sync portal propagates to the device'
                           'by doing image comparison using the above screenshots. Brightness in light mode should be '
                           'greater than dark mode.')
            status_setting_applied = False
            if brightness_updated < brightness_current:
                status_setting_applied = True
                Report.logPass(f'Color inversion setting applied. Light background turned into dark background '
                               f'as expected')

            else:
                Report.logFail(f'Color inversion setting did not apply.')
            self.sync_app.close()

            status= status_response & status_setting_applied
            assert status is True, 'Error in status'

        except AssertionError as e:
            Report.logException(f'e')
            raise e


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPICelestia)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")
