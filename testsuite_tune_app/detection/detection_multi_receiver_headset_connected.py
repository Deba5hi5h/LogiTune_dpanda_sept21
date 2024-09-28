import logging
import os
import unittest
import psutil

from base.base_ui import UIBase
from extentreport.report import Report
from common.platform_helper import get_custom_platform
from apps.tune.TuneElectron import TuneElectron, connect_device, disconnect_all
from apps.tune.tune_ui_methods import TuneUIMethods
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_750_api, zone_wired_earbuds_api

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectMultiReceiverHeadsetConnected(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    def setUp(self):
        """
        setUp: print testcase title to log
        """
        try:
            super(DetectMultiReceiverHeadsetConnected, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            # Kill Settings to avoid Settings launching error
            if get_custom_platform() == "windows":
                for proc in psutil.process_iter():
                    if proc.name() == "SystemSettings.exe":
                        proc.kill()
                        log.info(f'Process {proc.name()} is killed.')

        except Exception as e:
            log.error('Unable to setUp VC56905')
            raise e

    def tearDown(self):
        """
        tearDown: Close Tune if it is still opened
        """
        if self.tunesApp:
            self.tunesApp.close_tune_app()

        disconnect_all()

        super(DetectMultiReceiverHeadsetConnected, self).tearDown()

    def test_XXX_VC_56905_detect_multi_receiver_headset_connected(self):
        """Headset detection test after FW update
        The test purpose is to check if the Tune app is able to detect multiple headsets.
        The headset under test no need to be the same model
        It will fail if any one of the devices cannot be detected or is not on system sound input/output list.
        """
        device_name_1 = zone_750_api.name
        device_name_2 = zone_wired_earbuds_api.name

        try:
            disconnect_all()
            self.tunesApp = TuneElectron()
            self.tuneMethods = TuneUIMethods()

            # Connect first device
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()
            Report.logInfo(f"First device: {device_name_1} detection.")
            connect_device(device_name_1)
            self.tunesApp.is_device_label_displayed(device_name_1)

            # Detect first device in sound settings
            self.tuneMethods.tc_verify_settings_sound_input_output(device_name_1)

            # Connect second device
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()
            Report.logInfo(f"Second device: {device_name_2} detection.")
            connect_device(device_name_2)
            #  device1 and device2 are shown on Tune at the same time
            self.tunesApp.is_device_label_displayed(device_name_1)
            self.tunesApp.click_back_button_to_device_settings()
            self.tunesApp.is_device_label_displayed(device_name_2)

            # Detect second device in sound settings
            self.tuneMethods.tc_verify_settings_sound_input_output(device_name_2)

        except Exception as e:
            Report.logException(str(e))

        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectMultiReceiverHeadsetConnected)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
