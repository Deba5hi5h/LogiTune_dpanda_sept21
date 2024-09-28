import logging
import os
import unittest
import time
import psutil

from base.base_ui import UIBase
from extentreport.report import Report
from common.framework_params import ZONE_305_RELAY_BOARD_SERIAL_NUMBER, ZONE_305_POWER_ON_OFF_PAIR_BUTTON
from common.relay_board_control import GenericRelayControl
from common.platform_helper import get_custom_platform
from apps.tune.TuneElectron import TuneElectron, disconnect_all, connect_device, disconnect_device
from apps.tune.tune_ui_methods import TuneUIMethods
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_305_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZone305Dongle(UIBase):
    # used in tearDown to update test status on zephyr
    tune_app = TuneElectron()
    tune_method = TuneUIMethods()
    device_name = zone_305_api.name
    conn_type = ConnectionType.dongle

    ryCtrl = GenericRelayControl()

    def setUp(self):
        """
        setUp: disconnect all devices on USB hub
        """
        try:
            super(DetectZone305Dongle, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            disconnect_all()

            # Communicate with the relay connected with Zone 300
            relay_com_port = self.ryCtrl.get_relay_com_port(ZONE_305_RELAY_BOARD_SERIAL_NUMBER)
            self.ryCtrl.connect_relay(relay_com_port)

        except Exception as e:
            log.error('Unable to setUp {}'.format(self._testMethodName))
            raise e

    @classmethod
    def tearDownClass(cls):
        """
        tearDown: Close Tune if it's still running, closing COM port communication
        """
        if cls.tune_app:
            cls.tune_app.close_tune_app()

        # Close COM port communication with relay
        cls.ryCtrl.disconnect_relay()

        # Kill Settings process
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    log.info(f'Process {proc.name()} is killed.')

        super(DetectZone305Dongle, cls).tearDownClass()

    def test_001_VC_141329_detect_zone_305_dongle(self):
        """Verification of detection of Zone 300 via bluetooth
        This test pairs and PC with Zone 300 via bluetooth and check the info on Tune
        It will fail if Tune does not show Zone 300 on the page
        """
        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()
            for i in range(1, 3):
                Report.logInfo(f"{self.device_name} detection. Try {i}")
                connect_device(self.device_name)
                self.tune_app.is_device_battery_displayed(self.device_name)
                disconnect_device(self.device_name)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def test_002_VC_141330_power_on_off_zone_305_dongle(self):
        """Verification of detection of Zone 305 via dongle after power on/off"""

        device_name = self.device_name
        try:
            self.tune_method.tc_detect_power_on_off_dongle(device_name)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZone305Dongle)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
