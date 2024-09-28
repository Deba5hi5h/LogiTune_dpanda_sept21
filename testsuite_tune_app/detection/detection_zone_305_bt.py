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
from apps.tune.TuneElectron import TuneElectron, disconnect_all
from apps.tune.bluetooth_methods import BluetoothControl
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_305_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZone305Bt(UIBase):
    # used in tearDown to update test status on zephyr
    tune_app = TuneElectron()
    device_name = zone_305_api.name
    conn_type = ConnectionType.bt

    btCtrl = BluetoothControl()
    ryCtrl = GenericRelayControl()

    def setUp(self):
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
               power on bluetooth
        """
        try:
            super(DetectZone305Bt, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            disconnect_all()

            # Communicate with the relay connected with Zone 305
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

        # Reboot headset and keep it on for the following tests
        # For Zone 305 press button over 0.5 sec will enter pairing mode
        cls.ryCtrl.press_btn(ZONE_305_POWER_ON_OFF_PAIR_BUTTON, 0.3)
        time.sleep(5)
        cls.ryCtrl.press_btn(ZONE_305_POWER_ON_OFF_PAIR_BUTTON, 0.3)

        # Close COM port communication with relay
        cls.ryCtrl.disconnect_relay()

        # Kill Settings process
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    log.info(f'Process {proc.name()} is killed.')

        cls.btCtrl.bluetooth_unpair(zone_305_api.headset_bt_address, cls.device_name)

        super(DetectZone305Bt, cls).tearDownClass()

    def test_001_VC_141156_detect_zone_305_bt(self):
        """Verification of detection of Zone 300 via bluetooth
        This test pairs and PC with Zone 300 via bluetooth and check the info on Tune
        It will fail if Tune does not show Zone 300 on the page
        """
        device_name = self.device_name
        device_mac = zone_305_api.headset_bt_address

        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()

            for i in range(1, 6):
                Report.logInfo(f"{device_name} bluetooth detection. Try {i}")
                self.ryCtrl.press_btn(ZONE_305_POWER_ON_OFF_PAIR_BUTTON, 3)
                self.btCtrl.bluetooth_pair(device_mac, device_name)
                self.tune_app.is_device_battery_displayed(device_name)
                time.sleep(3)
                self.btCtrl.bluetooth_unpair(device_mac, device_name)
                time.sleep(3)
                self.tune_app.verify_no_devices_connected()
                time.sleep(3)
        except Exception as e:
            Report.logException(str(e))

        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def test_002_VC_141155_power_on_off_zone_305_bt(self):
        """Verification of detection of Zone 305 via bluetooth after power on/off"""

        device_name = self.device_name
        device_mac = zone_305_api.headset_bt_address

        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()

            self.ryCtrl.press_btn(ZONE_305_POWER_ON_OFF_PAIR_BUTTON, 3)
            self.btCtrl.bluetooth_pair(device_mac, device_name)


            # it should autoconnect for each time after power on
            for i in range(1, 6):
                Report.logInfo(f"{device_name} bluetooth power on/off. Try {i}")
                try:
                    self.tune_app.is_device_battery_displayed(device_name)
                    Report.logPass(f"Successfully connected to {device_name}")
                except Exception as e:
                    Report.logFail(f"{device_name} not displayed in Tune App", True)
                # For Zone 300 press button over 0.5 sec will enter pairing mode
                self.ryCtrl.press_btn(ZONE_305_POWER_ON_OFF_PAIR_BUTTON, 0.3)
                time.sleep(5)

                if self.tune_app.verify_no_devices_connected():
                    Report.logPass("No devices connected yet message displayed")
                else:
                    Report.logFail("There is still remaining some devices on Tune", True)
                # For Zone 305 press button over 0.5 sec will enter pairing mode
                self.ryCtrl.press_btn(ZONE_305_POWER_ON_OFF_PAIR_BUTTON, 0.3)
                time.sleep(5)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZone305Bt)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
