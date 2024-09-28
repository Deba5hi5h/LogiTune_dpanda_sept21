import logging
import os
import unittest
import time
import psutil

from base.base_ui import UIBase
from extentreport.report import Report
from common.framework_params import ZONE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER, ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_api
from common.relay_board_control import GenericRelayControl
from common.platform_helper import get_custom_platform
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

from apps.tune.TuneElectron import TuneElectron, disconnect_all
from apps.tune.bluetooth_methods import BluetoothControl

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWirelessBt(UIBase):
    # used in tearDown to update test status on zephyr
    tune_app = TuneElectron()
    device_name = zone_wireless_api.name
    device_mac = zone_wireless_api.headset_bt_address
    conn_type = ConnectionType.bt

    def setUp(self):
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
               power on bluetooth
        """
        try:
            super(DetectZoneWirelessBt, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            disconnect_all()
            self.btCtrl = BluetoothControl()
            self.ryCtrl = GenericRelayControl()

            # Communicate with the relay connected with Zone Wireless
            relay_com_port = self.ryCtrl.get_relay_com_port(ZONE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER)
            self.ryCtrl.connect_relay(relay_com_port)

        except Exception as e:
            log.error('Unable to setUp test_XXX_VC_YYYYY_detect_zone_wireless_bt')
            raise e

    def tearDown(self):
        """
        tearDown: Close Tune if it's still running, closing COM port communication
        """
        if self.tune_app:
            self.tune_app.close_tune_app()

        # Close COM port communication with relay
        self.ryCtrl.disconnect_relay()

        # Kill Settings process
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    log.info(f'Process {proc.name()} is killed.')

        self.btCtrl.bluetooth_unpair(zone_wireless_api.headset_bt_address, zone_wireless_api.name)

        super(DetectZoneWirelessBt, self).tearDown()

    def test_XXX_VC_123394_detect_zone_wireless_bt(self):
        """Verification of detection of Zone Wireless via bluetooth
        This test pairs and PC with Zone Wireless via bluetooth and check the info on Tune
        It will fail if Tune does not show Zone Wireless on the page
        """
        device_name = zone_wireless_api.name
        device_mac = zone_wireless_api.headset_bt_address

        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()

            for i in range(1, 3):
                Report.logInfo(f"{device_name} bluetooth detection. Try {i}")
                #  Enter pairing mode
                self.ryCtrl.press_btn(ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON, 3)
                self.btCtrl.bluetooth_pair(device_mac, device_name)
                self.tunesApp.is_device_battery_displayed(device_name)
                self.btCtrl.bluetooth_unpair(device_mac, device_name)
                if self.tune_app.verify_no_devices_connected():
                    Report.logPass("Tune shows No devices connected", True)
                else:
                    Report.logFail("There is still remaining some devices on Tune")

        except Exception as e:
            Report.logException(str(e))

        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def test_XXX_VC_122444_power_on_off_zone_wireless_bt(self):
        """Verification of detection of Zone Wireless via bluetooth after power on/off"""

        device_name = self.device_name
        device_mac = zone_wireless_api.headset_bt_address
        power_on_off_pair_btn = ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON

        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()

            self.ryCtrl.press_btn(power_on_off_pair_btn, 1)
            time.sleep(3)
            self.ryCtrl.press_btn(power_on_off_pair_btn, 1)
            time.sleep(3)
            self.btCtrl.bluetooth_pair(device_mac, device_name)
            if get_custom_platform() == "macos":
                self.btCtrl.bluetooth_connect(device_name)

            # it should autoconnect for each time after power on
            for i in range(1, 4):
                Report.logInfo(f"{device_name} bluetooth power on/off. Try {i}")
                try:
                    self.tune_app.is_device_battery_displayed(device_name)
                    Report.logPass(f"Successfully connected to {device_name}")
                except Exception as e:
                    Report.logFail(f"{device_name} not displayed in Tune App", True)

                self.ryCtrl.press_btn(power_on_off_pair_btn, 1)
                time.sleep(3)

                if self.tune_app.verify_no_devices_connected():
                    Report.logPass("No devices connected yet message displayed")
                else:
                    Report.logFail("There is still remaining some devices on Tune", True)

                self.ryCtrl.press_btn(power_on_off_pair_btn, 1)
                time.sleep(3)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWirelessBt)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
