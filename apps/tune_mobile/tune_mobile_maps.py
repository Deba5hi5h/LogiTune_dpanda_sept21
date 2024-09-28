import time

from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_image import TuneMobileImage
from extentreport.report import Report
from locators.tune_mobile.tune_mobile_maps_locators import TuneMobileMapsLocators


class TuneMobileMaps(TuneMobile):

    def click_change_building(self):
        """
        Method to click selected building to change

        :param :
        :return TuneMobileMaps:
        """
        self.find_element(TuneMobileMapsLocators.SELECTED_BUILDING).click()
        return self

    def get_selected_building(self) -> str:
        """
        Method to get selected building name

        :param :
        :return building_name:
        """
        el = self.find_element(TuneMobileMapsLocators.SELECTED_BUILDING)
        value = "value" if self.is_ios_device() else "text"
        return el.get_attribute(value)

    def click_change_floor(self):
        """
        Method to click selected floor to change

        :param :
        :return TuneMobileMaps:
        """
        self.find_element(TuneMobileMapsLocators.SELECTED_FLOOR).click()
        return self

    def get_selected_floor(self) -> str:
        """
        Method to get selected floor name

        :param :
        :return floor_name:
        """
        el = self.find_element(TuneMobileMapsLocators.SELECTED_FLOOR)
        value = "value" if self.is_ios_device() else "text"
        return el.get_attribute(value)

    def click_building(self, building_name: str):
        """
        Method to click building name from change building screen

        :param building_name:
        :return TuneMobileMaps:
        """
        self.find_element(TuneMobileMapsLocators.STATIC_TEXT, param=building_name).click()
        return self

    def click_floor(self, floor_name: str):
        """
        Method to click floor name from change floor screen

        :param floor_name:
        :return TuneMobileMaps:
        """
        self.find_element(TuneMobileMapsLocators.STATIC_TEXT, param=floor_name).click()
        return self

    def click_ok(self):
        """
        Method to click OK button

        :param :
        :return TuneMobileMaps:
        """
        self.find_element(TuneMobileMapsLocators.OK).click()
        return self

    def click_room(self, room_name: str):
        """
        Method to click conference room

        :param room_name:
        :return TuneMobileMaps:
        """
        time.sleep(2)
        factor = 5
        el = self.find_element(TuneMobileMapsLocators.MAP_IMAGE, visibility=False)
        img = Report.get_element_screenshot(el, "maps", factor=factor)
        x, y = TuneMobileImage.get_text_coordinates(image_path=img, text=room_name)
        factor = factor*3 if self.is_ios_device() else factor
        x = (x/factor) + el.location['x']
        y = (y/factor) + el.location['y']
        self.tap_by_coordinates(x, y)
        return self

    def get_room_name(self) -> str:
        """
        Method to get room name from the bottom sheet

        :param :
        :return str:
        """
        el = self.find_element(TuneMobileMapsLocators.ROOM_NAME)
        value = "value" if self.is_ios_device() else "text"
        return el.get_attribute(value)

    def get_room_status(self) -> str:
        """
        Method to get room status from the bottom sheet

        :param :
        :return str:
        """
        el = self.find_element(TuneMobileMapsLocators.ROOM_STATUS)
        value = "value" if self.is_ios_device() else "text"
        return el.get_attribute(value)

    def get_room_people_count(self) -> str:
        """
        Method to get room people count from the bottom sheet

        :param :
        :return str:
        """
        el = self.find_element(TuneMobileMapsLocators.PEOPLE_COUNT)
        value = "value" if self.is_ios_device() else "text"
        return el.get_attribute(value)

    def change_building(self, building_name: str):
        """
        Method to change building

        :param building_name:
        :return TuneMobileMaps:
        """
        if self.get_selected_building().lower() != building_name.lower():
            self.click_change_building().click_building(building_name=building_name)
        return self

    def change_floor(self, floor_name: str):
        """
        Method to change floor

        :param floor_name:
        :return TuneMobileMaps:
        """
        floor = self.get_selected_floor().lower()
        if floor_name.lower() not in self.get_selected_floor().lower():
            self.click_change_floor().click_floor(floor_name=floor_name)
            if self.is_android_device():
                self.click_ok()
        return self