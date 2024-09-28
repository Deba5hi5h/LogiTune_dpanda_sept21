import time

from base.base_ui import UIBase
from extentreport.report import Report
from locators.local_network_access.lna_connectivity_locators import LNAConnectivityLocators


class LNAConnectivity(UIBase):
    """
    LNA Connectivity page methods
    """

    def click_apply(self):
        """
        Method to click on Apply button which appears when settings changed
        :param :
        :return :LNAConnectivity
        """
        time.sleep(1)
        self.look_element(LNAConnectivityLocators.BUTTON_APPLY).click()
        while self.verify_element(LNAConnectivityLocators.BUTTON_APPLY, timeunit=2):
            time.sleep(1)
        return LNAConnectivity()

    def expand_bluetooth_section(self):
        """
        Method to expand Bluetooth section
        :param :
        :return :LNAConnectivity
        """
        e = self.look_element(LNAConnectivityLocators.BLUETOOTH_EXPAND)
        if "open" not in e.get_attribute('className'):
            Report.logInfo("Expanding bluetooth section")
            self.look_element(LNAConnectivityLocators.BLUETOOTH).click()
            time.sleep(1)
        return LNAConnectivity()

    def verify_bluetooth_enabled(self) -> bool:
        """
        Method to verify Bluetooth is enabled
        :param :
        :return :bool
        """
        e = self.look_element(LNAConnectivityLocators.BLUETOOTH_CHECKBOX)
        return e.get_attribute('checked')

    def enable_bluetooth(self):
        """
        Method to enable Bluetooth
        :param none
        :return none
        """
        if not self.verify_bluetooth_enabled():
            Report.logInfo("Enabling bluetooth")
            self.look_element(LNAConnectivityLocators.BLUETOOTH_CHECKBOX).click()
            self.click_apply()

    def disable_bluetooth(self):
        """
        Method to disable Bluetooth
        :param none
        :return none
        """
        if self.verify_bluetooth_enabled():
            Report.logInfo("Disabling bluetooth")
            self.look_element(LNAConnectivityLocators.BLUETOOTH_CHECKBOX).click()
            self.click_apply()
