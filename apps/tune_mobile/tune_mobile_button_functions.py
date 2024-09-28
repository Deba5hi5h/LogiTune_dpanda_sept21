import time

from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_button_functions_locators import TuneMobileButtonFunctionsLocators


class TuneMobileButtonFunctions(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to click Back

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileButtonFunctionsLocators.BACK).click()
        return TuneMobileHome()

    def click_left_ear_bud(self):
        """
        Method to click Left Ear Bud

        :param :
        :return TuneMobileButtonFunctions:
        """
        self.find_element(TuneMobileButtonFunctionsLocators.LEFT_EAR_BUD).click()
        return self

    def click_right_ear_bud(self):
        """
        Method to click Right Ear Bud

        :param :
        :return TuneMobileButtonFunctions:
        """
        self.find_element(TuneMobileButtonFunctionsLocators.RIGHT_EAR_BUD).click()
        return self

    def click_short_press(self):
        """
        Method to click Short Press

        :param :
        :return TuneMobileButtonFunctions:
        """
        time.sleep(1)
        self.find_element(TuneMobileButtonFunctionsLocators.SHORT_PRESS).click()
        return self

    def click_long_press(self):
        """
        Method to click Long Press

        :param :
        :return TuneMobileButtonFunctions:
        """
        time.sleep(1)
        self.find_element(TuneMobileButtonFunctionsLocators.LONG_PRESS).click()
        return self

    def click_double_tap(self):
        """
        Method to click Double Tap

        :param :
        :return TuneMobileButtonFunctions:
        """
        time.sleep(1)
        self.find_element(TuneMobileButtonFunctionsLocators.DOUBLE_TAP).click()
        return self

    def click_close(self):
        """
        Method to click Close

        :param :
        :return TuneMobileButtonFunctions:
        """
        self.find_element(TuneMobileButtonFunctionsLocators.CLOSE).click()
        return self