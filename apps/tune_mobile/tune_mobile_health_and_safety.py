from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_health_and_safety_locators import TuneMobileHealthAndSafetyLocators


class TuneMobileHealthAndSafety(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to click back

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileHealthAndSafetyLocators.BACK).click()
        return TuneMobileHome()

