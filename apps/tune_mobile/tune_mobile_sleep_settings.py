import time

from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from base.base_ui import UIBase
from locators.tune_mobile.tune_mobile_sleep_settings_locators import TuneMobileSleepSettingsLocators


class TuneMobileSleepSettings(TuneMobile):

    def click_close(self) -> TuneMobileHome:
        """
        Method to click Close button

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSleepSettingsLocators.CLOSE).click()
        return TuneMobileHome()

    def click_save(self) -> TuneMobileHome:
        """
        Method to click on Save button

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSleepSettingsLocators.SAVE).click()
        return TuneMobileHome()

    def click_never_radio(self):
        """
        Method to click on Never Radio option

        :param :
        :return TuneMobileSleepSettings:
        """
        self.find_element(TuneMobileSleepSettingsLocators.SLEEP_NEVER_RADIO).click()
        return TuneMobileSleepSettings()

    def click_minutes_radio(self, minutes: int):
        """
        Method to click on Minutes Radio option

        :param minutes:
        :return TuneMobileSleepSettings:
        """
        self.find_element(TuneMobileSleepSettingsLocators.SLEEP_MINUTES_RADIO, param=str(minutes), visibility=False).click()
        # self.tap_element(TuneMobileSleepSettingsLocators.SLEEP_MINUTES_RADIO, param=str(minutes), visibility=False)
        return TuneMobileSleepSettings()

    def click_hours_radio(self, hours: int):
        """
        Method to click on Hours Radio option

        :param hours:
        :return TuneMobileSleepSettings:
        """
        self.find_element(TuneMobileSleepSettingsLocators.SLEEP_HOUR_RADIO, param=str(hours), visibility = False).click()
        return TuneMobileSleepSettings()

    def verify_never_radio(self) -> bool:
        """
        Method to verify Never Radio option displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSleepSettingsLocators.SLEEP_NEVER)

    def verify_minutes_radio(self, minutes: int) -> bool:
        """
        Method to verify Minutes Radio option displayed

        :param minutes:
        :return bool:
        """
        return self.verify_element(TuneMobileSleepSettingsLocators.SLEEP_MINUTES, param=str(minutes), visibility=False)

    def verify_hours_radio(self, hours: int) -> bool:
        """
        Method to verify Hours Radio option displayed

        :param hours:
        :return bool:
        """
        if hours == 1:
            return self.verify_element(TuneMobileSleepSettingsLocators.SLEEP_HOUR)
        else:
            return self.verify_element(TuneMobileSleepSettingsLocators.SLEEP_HOURS, param=str(hours), visibility=False)

    def verify_save_button(self) -> bool:
        """
        Method to verify Save button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSleepSettingsLocators.SAVE)

    def verify_close_button(self) -> bool:
        """
        Method to verify Close button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSleepSettingsLocators.CLOSE)