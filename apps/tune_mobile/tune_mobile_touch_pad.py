from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_touchpad_locators import TuneMobileTouchPadLocators


class TuneMobileTouchPad(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to click back

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileTouchPadLocators.BACK).click()
        return TuneMobileHome()

