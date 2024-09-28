from base.base_ui import UIBase
from extentreport.report import Report
from locators.local_network_access.lna_sync_locators import LNASyncLocators


class LNASync(UIBase):
    """
    LNA Sync page methods
    """

    def expand_connection(self):
        """
        Method to expand Sync Connection section
        :param :
        :return : LNASync
        """
        e = self.look_element(LNASyncLocators.CONNECTION_EXPAND)
        if "open" not in e.get_attribute('className'):
            Report.logInfo("Expanding Connection section")
            self.look_element(LNASyncLocators.CONNECTION_EXPAND).click()
        return LNASync()

    def click_connect_to_sync(self):
        """
        Method to click on Connect to Sync button
        :param :
        :return : LNASync
        """
        self.look_element(LNASyncLocators.CONNECT_TO_SYNC).click()
        return LNASync()

    def click_continue(self):
        """
        Method to click on Continue button
        :param :
        :return : LNASync
        """
        self.look_element(LNASyncLocators.CONTINUE).click()
        return LNASync()

    def click_skip_this_step(self):
        """
        Method to click on Skip this step button
        :param :
        :return : LNASync
        """
        self.look_element(LNASyncLocators.SKIP_THIS_STEP).click()
        return LNASync()

    def click_submit(self):
        """
        Method to click on Submit button
        :param :
        :return : LNASync
        """
        self.look_element(LNASyncLocators.SUBMIT).click()
        return LNASync()

    def type_in_provision_code(self, provision_code: str):
        """
        Method to input provision_code in Provision Code text box
        :param : provision_code
        :return : LNASync
        """
        self.look_element(LNASyncLocators.SYNC_PROVISION_CODE_INPUT).send_keys(provision_code)
        return LNASync()

    def type_in_seat_count(self, seat_count: str):
        """
        Method to input seat_count in Seat Count text box
        :param : seat_count
        :return : LNASync
        """
        self.look_element(LNASyncLocators.SEAT_COUNT).send_keys(seat_count)
        return LNASync()

    def verify_disconnect_from_sync_button_displayed(self) -> bool:
        """
        Method to verify if Disconnect from Sync button displays
        :param :
        :return : bool
        """
        return self.verify_element(LNASyncLocators.DISCONNECT_FROM_SYNC, timeunit=2, wait_for_visibility=True)

    def verify_connect_to_sync_button_displayed(self) -> bool:
        """
        Method to verify if Connect to Sync button displays
        :param :
        :return : bool
        """
        return self.verify_element(LNASyncLocators.CONNECT_TO_SYNC, timeunit=1)