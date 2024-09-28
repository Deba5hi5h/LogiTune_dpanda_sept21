import logging
import os
import unittest
import psutil
import time

from base.base_ui import UIBase
from extentreport.report import Report
from common.framework_params import ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER, ZONE_VIBE_WIRELESS_ON_BUTTON, ZONE_VIBE_WIRELESS_OFF_BUTTON, ZONE_VIBE_WIRELESS_PAIR_BUTTON
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_vibe_wireless_api
from common.relay_board_control import GenericRelayControl
from common.platform_helper import get_custom_platform
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType

from apps.tune.TuneElectron import TuneElectron, disconnect_all
from apps.tune.bluetooth_methods import BluetoothControl

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneVibeWirelessBt(UIBase):
    # used in tearDown to update test status on zephyr
    tune_app = TuneElectron()
    device_name = zone_vibe_wireless_api.name
    conn_type = ConnectionType.bt

    def setUp(self):
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
               power on bluetooth
        """
        try:
            super(DetectZoneVibeWirelessBt, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            disconnect_all()
            self.btCtrl = BluetoothControl()
            self.ryCtrl = GenericRelayControl()

            # Communicate with the relay connected with Zone Vibe 130
            relay_com_port = self.ryCtrl.get_relay_com_port(ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER)
            self.ryCtrl.connect_relay(relay_com_port)

        except Exception as e:
            log.error('Unable to setUp test_XXX_VC_YYYYY_detect_vibe_wireless_bt')
            raise e

    def tearDown(self):
        """
        tearDown: Close Tune if it's still running, closing COM port communication
        """
        if self.tune_app:
            self.tune_app.close_tune_app()

        # Reboot headset and keep it on for the following tests
        self.ryCtrl.press_btn(ZONE_VIBE_WIRELESS_OFF_BUTTON, 3)
        self.ryCtrl.press_btn(ZONE_VIBE_WIRELESS_ON_BUTTON, 1)

        # Close COM port communication with relay
        self.ryCtrl.disconnect_relay()

        # Kill Settings process
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    log.info(f'Process {proc.name()} is killed.')

        self.btCtrl.bluetooth_unpair(zone_vibe_wireless_api.headset_bt_address, zone_vibe_wireless_api.name)

        super(DetectZoneVibeWirelessBt, self).tearDown()

    def test_XXX_VC_123391_detect_zone_vibe_wireless_bt(self):
        """Verification of detection of Zone Vibe Wireless via bluetooth
        This test pairs and PC with Zone Vibe Wireless via bluetooth and check the info on Tune
        It will fail if Tune does not show Zone Vibe Wireless on the page
        """
        device_name = zone_vibe_wireless_api.name
        device_mac = zone_vibe_wireless_api.headset_bt_address

        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()

            for i in range(1, 3):
                Report.logInfo(f"{device_name} bluetooth detection. Try {i}")
                self.ryCtrl.press_btn(ZONE_VIBE_WIRELESS_ON_BUTTON, 1)
                self.ryCtrl.press_btn(ZONE_VIBE_WIRELESS_PAIR_BUTTON, 3)
                self.btCtrl.bluetooth_pair(device_mac, device_name)
                if get_custom_platform() == "macos":
                    self.btCtrl.bluetooth_connect(device_name)
                self.tune_app.is_device_battery_displayed(device_name)
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

    def test_XXX_VC_103783_power_on_off_vibe_wireless_bt(self):
        """Verification of detection of Zone Vibe Wireless via bluetooth after power on/off"""

        device_mac = zone_vibe_wireless_api.headset_bt_address
        device_name = zone_vibe_wireless_api.name
        power_on_btn = ZONE_VIBE_WIRELESS_ON_BUTTON
        power_off_btn = ZONE_VIBE_WIRELESS_OFF_BUTTON
        pair_btn = ZONE_VIBE_WIRELESS_PAIR_BUTTON

        try:
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()

            self.ryCtrl.press_btn(power_on_btn, 2)
            time.sleep(3)
            self.ryCtrl.press_btn(pair_btn, 4)
            time.sleep(3)
            self.btCtrl.bluetooth_pair(device_mac, device_name)
            if get_custom_platform() == "macos":
                self.btCtrl.bluetooth_connect(device_name)

            # it should autoconnect for each time after power on
            for i in range(1, 6):
                Report.logInfo(f"{device_name} bluetooth power on/off. Try {i}")
                try:
                    self.tune_app.is_device_battery_displayed(device_name)
                    Report.logPass(f"Successfully connected to {device_name}")
                except Exception as e:
                    Report.logFail(f"{device_name} not displayed in Tune App", True)


                self.ryCtrl.press_btn(power_off_btn, 2)
                time.sleep(3)

                if self.tune_app.verify_no_devices_connected():
                    Report.logPass("No devices connected yet message displayed")
                else:
                    Report.logFail("There is still remaining some devices on Tune", True)

                self.ryCtrl.press_btn(power_on_btn, 2)
                time.sleep(3)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneVibeWirelessBt)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
