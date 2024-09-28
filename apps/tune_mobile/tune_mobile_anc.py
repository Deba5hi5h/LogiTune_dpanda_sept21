from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_anc_locators import TuneMobileANCLocators


class TuneMobileANC(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to click Close

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileANCLocators.BACK).click()
        return TuneMobileHome()

    def click_short_press(self):
        """
        Method to click Close

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileANCLocators.SHORT_PRESS).click()
        return TuneMobileANC()

