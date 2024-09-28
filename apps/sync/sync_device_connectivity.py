import time

from apps.sync.sync_config import SyncConfig
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_app.sync_app_device_connectivity_locators import SyncAppDeviceConnectivityLocators


class SyncDeviceConnectivity(UIBase):

    def enable_bluetooth(self):
        """
        Method to enable Bluetooth

        :param :
        :return SyncDeviceConnectivity:
        """
        if self.verify_bluetooth_enabled(timeout=1, enabled=False):
            Report.logInfo("Enabling Bluetooth")
            self.look_element(SyncAppDeviceConnectivityLocators.BLUETOOTH).click()
            time.sleep(1)
            self.verify_bluetooth_enabled()
        return SyncDeviceConnectivity()

    def disable_bluetooth(self):
        """
        Method to disable Bluetooth

        :param :
        :return SyncDeviceConnectivity:
        """
        if self.verify_bluetooth_enabled(timeout=1, enabled=True):
            Report.logInfo("Disabling Bluetooth")
            self.look_element(SyncAppDeviceConnectivityLocators.BLUETOOTH).click()
            time.sleep(1)
            self.verify_bluetooth_enabled(enabled=False)
        return SyncDeviceConnectivity()

    def verify_bluetooth_enabled(self, timeout: int = None, enabled: bool = True) -> bool:
        """
        Method to verify Bluetooth is Enabled

        :param timeout:
        :param enabled:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceConnectivityLocators.BLUETOOTH)
        return SyncConfig.is_selected(e, timeout=timeout, selected=enabled)



