from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_headset_language_locators import TuneMobileHeadsetLanguageLocators


class TuneMobileHeadsetLanguage(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to get Equalizer value

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileHeadsetLanguageLocators.BACK).click()
        return TuneMobileHome()

    def click_cancel(self):
        """
        Method to get Equalizer value

        :param :
        :return TuneMobileHome:
        """
        if self.verify_element(TuneMobileHeadsetLanguageLocators.CANCEL, timeout=1):
            elements = self.find_elements(TuneMobileHeadsetLanguageLocators.CANCEL, timeout=1)
            if len(elements) == 2:
                elements[1].click()
        return TuneMobileHeadsetLanguage()

