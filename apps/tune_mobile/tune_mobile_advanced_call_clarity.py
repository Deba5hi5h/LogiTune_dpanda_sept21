from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_advanced_call_clarity_locators import TuneMobileAdvancedCallClarityLocators


class TuneMobileAdvancedCallClarity(TuneMobile):

    def click_close(self) -> TuneMobileHome:
        """
        Method to click Close

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileAdvancedCallClarityLocators.CLOSE).click()
        return TuneMobileHome()

