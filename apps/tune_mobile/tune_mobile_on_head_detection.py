from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_on_head_detection_locators import TuneMobileOnHeadDetectionLocators


class TuneMobileOnHeadDetection(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to click back

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileOnHeadDetectionLocators.BACK).click()
        return TuneMobileHome()

