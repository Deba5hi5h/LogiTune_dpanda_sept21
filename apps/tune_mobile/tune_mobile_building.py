from apps.tune_mobile.tune_mobile import TuneMobile
from locators.tune_mobile.tune_mobile_building_locators import TuneMobileBuildingLocators


class TuneMobileBuilding(TuneMobile):

    def click_site(self, site_name: str):
        """
        Method to expand Site

        :param :
        :return TuneMobileBuilding:
        """
        self.find_element(TuneMobileBuildingLocators.SITE, param=site_name).click()
        return self

    def click_building(self, building_name: str):
        """
        Method to select building

        :param building_name:
        :return TuneMobileBuilding:
        """
        self.find_element(TuneMobileBuildingLocators.BUILDING, param=building_name).click()
        return self

    def click_back(self):
        """
        Method to click Back arrow

        :param :
        :return :
        """
        self.find_element(TuneMobileBuildingLocators.BACK).click()

    def verify_change_building(self) -> bool:
        """
        Method to verify Change Building screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBuildingLocators.CHANGE_BUILDING)

    def verify_search(self) -> bool:
        """
        Method to verify search box displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileBuildingLocators.SEARCH)

    def change_building(self, site_name: str, building_name: str):
        """
        Method to change building under site

        :param site_name:
        :param building_name:
        :return TuneMobileBuilding:
        """
        if self.is_android_device():
            site_name = site_name.upper()
        if self.verify_element(TuneMobileBuildingLocators.BUILDING, param=building_name, timeout=3):
            self.click_building(building_name=building_name)
        else:
            self.click_site(site_name=site_name).click_building(building_name=building_name)
        return self
