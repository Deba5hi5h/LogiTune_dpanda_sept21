from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_personal_eq_locators import TuneMobilePersonalEqLocators


class TuneMobilePersonalEq(TuneMobile):

    def click_back(self):
        """
        Method to click Back

        :param :
        :return TuneMobilePersonalEq:
        """
        self.find_element(TuneMobilePersonalEqLocators.BACK).click()
        return self

    def click_start(self):
        """
        Method to click Start

        :param :
        :return TuneMobilePersonalEq:
        """
        self.find_element(TuneMobilePersonalEqLocators.START).click()
        return self

    def click_next_step(self):
        """
        Method to click Next Step

        :param :
        :return TuneMobilePersonalEq:
        """
        self.find_element(TuneMobilePersonalEqLocators.NEXT_STEP).click()
        return self

