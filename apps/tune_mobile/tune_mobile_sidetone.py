from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_sidetone_locators import TuneMobileSidetoneLocators


class TuneMobileSidetone(TuneMobile):

    def click_close(self) -> TuneMobileHome:
        """
        Method to click Close

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSidetoneLocators.CLOSE).click()
        return TuneMobileHome()

    def click_done(self) -> TuneMobileHome:
        """
        Method to click Done button

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSidetoneLocators.DONE).click()
        return TuneMobileHome()

    def adjust_sidetone_slider(self, value: int):
        """
        Method to adjust Sidetone slider

        :param :
        :return TuneMobileHome:
        """
        if self.is_ios_device():
            value = 1 if value >=100 else round((value+2)/100, 2)
        else:
            value = round((value) / 10, 0)
        self.find_element(TuneMobileSidetoneLocators.SIDETONE_SLIDER).send_keys(str(value))
        return TuneMobileHome()

    def verify_done_button(self) -> bool:
        """
        Method to Done button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSidetoneLocators.DONE_LABEL)

    def verify_sidetone_info(self) -> bool:
        """
        Method to Sidetone Information displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSidetoneLocators.SIDETONE_INFO, visibility=False)

    def verify_sidetone_slider(self) -> bool:
        """
        Method to Sidetone Slider displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSidetoneLocators.SIDETONE_SLIDER)

    def verify_sidetone_percentage(self, value: int) -> bool:
        """
        Method to Sidetone Percentage value displayed

        :param value:
        :return bool:
        """
        return self.verify_element(TuneMobileSidetoneLocators.SIDETONE_PERCENTAGE, param=str(value))

    def click_ok(self) -> TuneMobileHome:
        """
        Method to click OK button

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSidetoneLocators.OK).click()
        return TuneMobileHome()

    def verify_ok_button(self) -> bool:
        """
        Method to verify OK button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSidetoneLocators.OK, timeout=3)

    def click_allow(self) -> TuneMobileHome:
        """
        Method to click Allow button

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSidetoneLocators.ALLOW).click()
        return TuneMobileHome()

    def verify_allow_button(self) -> bool:
        """
        Method to verify Allow button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSidetoneLocators.ALLOW, timeout=3)