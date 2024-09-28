import time

from apps.tune_mobile.tune_mobile_coily import TuneMobileCoily
from locators.coily_locators import TuneCoilyMainPageLocators, TuneCoilyBookedDeskLocators


class TuneMobileCoilyHome(TuneMobileCoily):

    def click_check_in(self):
        """
        Method to click Check in button

        :param :
        :return TuneMobileCoilyHome:
        """
        self.find_element_coily(TuneCoilyBookedDeskLocators.CHECK_IN_BUTTON).click()
        return TuneMobileCoilyHome()


