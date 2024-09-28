from typing import Optional, List, Tuple
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.map_page_locators import TuneMapPageLocators



class TuneMapsPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_floor_choose_button(self) -> None:
        self._click(TuneMapPageLocators.FLOOR_BUTTON)

    def click_floor_by_name(self, floor_name: str) -> None:
        self._click_by_element_text(TuneMapPageLocators.FLOOR_LIST_BUTTON, floor_name, expected_text_strict_check=False)

    def click_area_by_name(self, area_name: str) -> None:
        self._click_by_element_text(TuneMapPageLocators.AREA_BUTTON, area_name, expected_text_strict_check=False)

    def click_book_button(self) -> None:
        self._click(TuneMapPageLocators.BOOK_A_DESK_BUTTON)

    def verify_map_visible(self) -> bool:
        return self._is_visible(TuneMapPageLocators.MAP_CANVAS)

    def verify_current_desk_name(self, expected_desk_name: str) -> bool:
        return self._compare_text(TuneMapPageLocators.SELECTED_DESK_POPUP_NAME, expected_text=expected_desk_name)

    def click_on_desk_canvas_by_name(self, area_name: str, desk_name: str) -> bool:
        self.click_area_by_name(area_name)
        self.wait_seconds_to_pass(2)
        canvas = self._get_all_available_elements(TuneMapPageLocators.MAP_CANVAS)[0].wrapped_element
        available_desks_coords = self._find_green_circles_on_element(canvas)
        for cords in available_desks_coords:
            self.click_area_by_name(area_name)
            self.wait_seconds_to_pass(3)
            self._click_on_element_with_offset(canvas, cords)
            if self.verify_current_desk_name(desk_name):
                return True
        return False



