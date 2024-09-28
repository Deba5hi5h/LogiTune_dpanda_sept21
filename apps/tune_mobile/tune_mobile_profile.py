from apps.tune_mobile.tune_mobile import TuneMobile
from locators.tune_mobile.tune_mobile_profile_locators import TuneMobileProfileLocators


class TuneMobileProfile(TuneMobile):

    def click_work_account(self):
        """
        Method to click Work account

        :param :
        :return TuneMobileProfile:
        """
        self.find_element(TuneMobileProfileLocators.WORK_ACCOUNT).click()
        return self

    def click_disconnect(self):
        """
        Method to click Disconnect button

        :param :
        :return TuneMobileProfile:
        """
        self.find_element(TuneMobileProfileLocators.DISCONNECT).click()
        return self

    def click_confirm_disconnect(self):
        """
        Method to click Disconnect button on confirmation dialog

        :param :
        :return TuneMobileProfile:
        """
        self.find_element(TuneMobileProfileLocators.CONFIRM_DISCONNECT).click()
        return self

    def click_cancel(self):
        """
        Method to click Cancel button

        :param :
        :return TuneMobileProfile:
        """
        self.find_element(TuneMobileProfileLocators.CANCEL).click()
        return self

    def verify_cancel_button(self) -> bool:
        """
        Method to verify Cancel button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.CANCEL)

    def verify_disconnect_button(self) -> bool:
        """
        Method to verify Disconnect button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.DISCONNECT)

    def verify_confirm_disconnect_button(self) -> bool:
        """
        Method to verify Disconnect button displayed on confirmation

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.CONFIRM_DISCONNECT)

    def verify_google_calendar(self) -> bool:
        """
        Method to verify Google Calendar displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.GOOGLE_CALENDAR)

    def verify_o365_calendar(self) -> bool:
        """
        Method to verify Google Calendar displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.O365_CALENDAR)

    def verify_connected(self) -> bool:
        """
        Method to verify Connected displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.CONNECTED)

    def verify_disconnect_work_account(self) -> bool:
        """
        Method to verify Disconnect work account? message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.DISCONNECT_WORK_ACCOUNT)

    def verify_feature_unavailable(self) -> bool:
        """
        Method to verify Desk booking feature will be unavailable text displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileProfileLocators.FEATURE_UNAVAILABLE)
