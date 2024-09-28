from typing import Optional, List

from apps.tune.pages.base_page import TuneBasePage, WebDriver, WebElement
from datetime import datetime, timedelta
from locators.tune.meeting_detail_locators import TuneMeetingDetailsPageLocators


class TuneMeetingDetailPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def click_back_to_dashboard(self) -> None:

        self._click(TuneMeetingDetailsPageLocators.BACK_TO_DASHBOARD)

    def verify_meeting_title(self, meeting_title: str) -> bool:

        return self._compare_text(TuneMeetingDetailsPageLocators.MEETING_TITLE, expected_text=meeting_title)

    def verify_meeting_subtitle(self, meeting_subtitle: str) -> bool:

        return self._compare_text(TuneMeetingDetailsPageLocators.MEETING_SUBTITLE, expected_text=meeting_subtitle)

    def verify_details(self, event_link: str) -> bool:
        details_link: str = self._get_attribute_of_xpath_locator(TuneMeetingDetailsPageLocators.EXTERNAL_LINK,
                                                                 attribute='title')
        return event_link == details_link

    def verify_copy_link(self, hangout_link: str) -> bool:
        hangout_copy: str = self._get_attribute_of_xpath_locator(TuneMeetingDetailsPageLocators.COPY_LINK,
                                                                 attribute='title')
        return hangout_link == hangout_copy

    def verify_attendees_label(self, attendees_number: int) -> bool:
        return self._compare_text(TuneMeetingDetailsPageLocators.ATTENDEES_INFO,
                                  f"ATTENDEES ({attendees_number})")

    def verify_attendees_list(self, attendees_list: List[str]) -> bool:
        return self._verify_all_found_elements_values(TuneMeetingDetailsPageLocators.ATTENDEE_ITEM,
                                                      attendees_list)
