from typing import Optional

from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.calendar_and_meetings_locators import TuneCalendarAndMeetingsLocators


class TuneCalendarAndMeetingsPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def verify_label_name(self, label_name: str) -> bool:
        return self._compare_text(locator=TuneCalendarAndMeetingsLocators.TITLE_LABEL, expected_text=label_name)

    def verify_show_non_video_meetings_button(self) -> bool:
        return self._is_visible(locator=TuneCalendarAndMeetingsLocators.SHOW_NON_VIDEO_MEETINGS_LABEL)

    def verify_show_all_day_meetings_button(self) -> bool:
        return self._is_visible(locator=TuneCalendarAndMeetingsLocators.SHOW_ALL_DAY_MEETINGS_LABEL)

    def verify_declined_meetings_button(self) -> bool:
        return self._is_visible(locator=TuneCalendarAndMeetingsLocators.SHOW_DECLINED_MEETINGS_LABEL)

    def click_back(self) -> None:
        self._click(locator=TuneCalendarAndMeetingsLocators.BACK_BUTTON)

    def click_show_non_video_meetings_button(self) -> None:
        self._click(locator=TuneCalendarAndMeetingsLocators.SHOW_NON_VIDEO_MEETINGS_TOGGLE)

    def click_show_all_day_meetings_button(self) -> None:
        self._click(locator=TuneCalendarAndMeetingsLocators.SHOW_ALL_DAY_MEETINGS_TOGGLE)

    def click_declined_meetings_button(self) -> None:
        self._click(locator=TuneCalendarAndMeetingsLocators.SHOW_DECLINED_MEETINGS_TOGGLE)

    def check_value_show_non_video_meetings_button(self) -> bool:
        return self._get_attribute_of_xpath_locator(
            locator=TuneCalendarAndMeetingsLocators.SHOW_NON_VIDEO_MEETINGS_CHECKBOX,
            attribute='checked'
        ) == 'true'

    def check_value_show_all_day_meetings_button(self) -> bool:
        return self._get_attribute_of_xpath_locator(
            locator=TuneCalendarAndMeetingsLocators.SHOW_ALL_DAY_MEETINGS_CHECKBOX,
            attribute='checked'
        ) == 'true'

    def check_value_declined_meetings_button(self) -> bool:
        return self._get_attribute_of_xpath_locator(
            locator=TuneCalendarAndMeetingsLocators.SHOW_DECLINED_MEETINGS_CHECKBOX,
            attribute='checked'
        ) == 'true'


