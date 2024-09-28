from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_connected_devices_locators import TuneMobileConnectedDevicesLocators


class TuneMobileConnectedDevices(TuneMobile):

    def click_back(self) -> TuneMobileHome:
        """
        Method to get Equalizer value

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileConnectedDevicesLocators.BACK).click()
        return TuneMobileHome()

