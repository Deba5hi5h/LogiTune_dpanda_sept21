import logging
import os
import unittest
import psutil
import time

from base.base_ui import UIBase
from extentreport.report import Report
from apps.tune.tune_ui_methods import TuneUIMethods
from testsuite_firmware_api_tests.api_tests.api_parameters import zone_wireless_2_api
from common.platform_helper import get_custom_platform

from apps.tune.TuneElectron import TuneElectron, disconnect_all
from apps.tune.bluetooth_methods import BluetoothControl
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.usb_hid_communication_base import UsbHidCommunicationBase

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectZoneWireless2Bt(UIBase):

    def setUp(self):
        """
        setUp: disconnect all devices on USB hub to avoid headset connect to dongle
               power on bluetooth
        """
        try:
            super(DetectZoneWireless2Bt, self).setUp()
            log.info('Starting {}'.format(self._testMethodName))

            disconnect_all()
            self.tunesApp = TuneElectron()
            self.tunesUI = TuneUIMethods()
            self.btCtrl = BluetoothControl()

        except Exception as e:
            log.error('Unable to setUp test_XXX_VC_YYYYY_detect_zone_wireless_bt')
            raise e

    def tearDown(self):
        """
        tearDown: Close Tune if it's still running, closing COM port communication
        """
        if self.tunesApp:
            self.tunesApp.close_tune_app()

        # Kill Settings process
        if get_custom_platform() == "windows":
            for proc in psutil.process_iter():
                if proc.name() == "SystemSettings.exe":
                    proc.kill()
                    log.info(f'Process {proc.name()} is killed.')

        self.btCtrl.bluetooth_unpair(zone_wireless_2_api.headset_bt_address)

        super(DetectZoneWireless2Bt, self).tearDown()

    def test_XXX_VC_123393_detect_zone_wireless_2_bt(self):
        """Verification of detection of Zone Wireless 2 via bluetooth
        This test pairs and PC with Zone Wireless 2 via bluetooth and check the info on Tune
        It will fail if Tune does not show Zone Wireless 2 on the page
        """
        device_name = zone_wireless_2_api.name
        device_mac = zone_wireless_2_api.headset_bt_address

        try:
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()

            for i in range(1, 3):
                Report.logInfo(f"{device_name} bluetooth detection. Try {i}")

                pair_success = False
                for j in range(1, 5):
                    try:
                        if self.tunesUI.tc_bt_pair_headset(device_name, device_mac):
                            pair_success = True
                            break

                    except:
                        Report.logInfo(f"Exception happened during bluetooth detection {i}, pair retry {j}")

                if not pair_success:
                    raise Exception("Fail to Pair with the expected device")

                self.tunesApp.is_device_battery_displayed(device_name)
                self.btCtrl.bluetooth_unpair(device_mac)
                if self.tunesApp.verify_no_devices_connected():
                    Report.logPass("Tune shows No devices connected", True)
                else:
                    Report.logFail("There is still remaining some devices on Tune")

        except Exception as e:
            Report.logException(str(e))

        finally:
            if self.tunesApp:
                self.tunesApp.close_tune_app()

    def test_XXX_VC_122445_power_on_off_zone_wireless_2_bt(self):
        """Verification of detection of Zone Wireless 2 via bluetooth after power on/off"""

        pid = 0x0AFA
        usage_page = 65280
        device_name = zone_wireless_2_api.name
        hid_command = UsbHidCommunicationBase(device_name=device_name)
        device_mac = zone_wireless_2_api.headset_bt_address

        try:
            self.tunesApp.open_tune_app()
            self.tunesApp.open_my_devices_tab()

            hid_command.power_off(pid=pid, usage_page=usage_page)
            time.sleep(3)
            hid_command.power_on(pid=pid, usage_page=usage_page)
            time.sleep(3)
            if self.tunesUI.tc_bt_pair_headset(device_name, device_mac):
                Report.logInfo(f"{device_name} paired successfully.")

            # it should autoconnect for each time after power on
            for i in range(1, 4):
                Report.logInfo(f"{device_name} bluetooth power on/off. Try {i}")
                try:
                    self.tunesApp.is_device_battery_displayed(device_name)
                    Report.logPass(f"Successfully connected to {device_name}")
                except Exception as e:
                    Report.logFail(f"{device_name} not displayed in Tune App", True)

                hid_command.power_off(pid=pid, usage_page=usage_page)
                time.sleep(3)

                if self.tunesApp.verify_no_devices_connected():
                    Report.logPass("No devices connected yet message displayed")
                else:
                    Report.logFail("There is still remaining some devices on Tune", True)

                hid_command.power_on(pid=pid, usage_page=usage_page)
                time.sleep(3)

        except Exception as e:
            Report.logException(str(e))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectZoneWireless2Bt)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)
