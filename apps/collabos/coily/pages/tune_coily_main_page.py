import sys
import time
from typing import List, Optional, Tuple

import base.base_settings
from apps.collabos import collabos_config
from apps.collabos.base_collabos_methods import CollabOsBaseMethods
from apps.tune.helpers import get_python_version
from base import global_variables
from extentreport.report import Report
from appium.webdriver.webdriver import MobileWebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.coily_locators import TuneCoilyAuthorizedDeskLocators, TuneCoilyBookedDeskLocators, \
    TuneCoilyLaptopDisconnectedLocators, \
    TuneCoilyMainPageLocators, \
    TuneCoilyMessagesLocators, TuneCoilySessionIsOverLocators, TuneCoilyDeskTimeLimit, TuneCoilySettingsLocators


class TuneCoilyMainPage(CollabOsBaseMethods):

    def get_desk_name(self) -> str:
        """
        Method to return the desk name from Coily idle page.

        :param :
        :return str: desk name
        """
        element = self.find_element_collabos(TuneCoilyMainPageLocators.DESK_NAME)
        value = 'text'
        desk_name = element.get_attribute(value)
        return str(desk_name)

    def get_group_name(self) -> str:
        """
        Method to return the Org name form Coily idle page.

        :param :
        :return str: group name
        """
        element = self.find_element_collabos(TuneCoilyMainPageLocators.GROUP_NAME)
        value = 'text'
        group_name = element.get_attribute(value)
        return str(group_name)

    def get_time_from_idle_page(self) -> str:
        """
        Method to get a current time from Coily idle page.

        :param :
        :return str: current time
        """
        element = self.find_element_collabos(TuneCoilyMainPageLocators.CLOCK)
        value = 'text'
        time = element.get_attribute(value)
        return str(time)

    def verify_time_idle_page(self):
        element = self.verify_element_collabos(TuneCoilyMainPageLocators.CLOCK)
        if not element:
            raise Exception("Idle Page Clock not found")

    def get_time_left_to_beginning_of_reservation(self) -> Optional[str]:
        """
        Method to return the time left to begin the of reservation from center pile

        :param :
        :return str: desk name
        """
        element = self.find_element_collabos(TuneCoilyMainPageLocators.TIME_LEFT_TO_RESERVATION,
                                             skip_exception=True)
        if element:
            value = 'text'
            desk_name = element.get_attribute(value)
            return str(desk_name)
        return None

    def click_center_pile_with_time_left_in_the_reservation(self) -> None:
        """
        Method to click on center pile.

        :return None:
        """
        self.find_element_collabos(TuneCoilyMainPageLocators.TIME_LEFT_TO_RESERVATION).click()

    def get_time_left_to_end_of_reservation(self) -> str:
        """
        Method to return the time left to end of reservation from center pile

        :param :
        :return str: desk name
        """
        element = self.find_element_collabos(TuneCoilyMainPageLocators.TIME_LEFT_TO_RESERVATION)
        value = 'text'
        desk_name = element.get_attribute(value)
        return str(desk_name)

    def verify_time_left_to_end_of_reservation_is_dispalyed(self) -> str:
        """
        Method to return the verify if center pile is displayed

        :param :
        :return str: desk name
        """
        return self.verify_element_collabos(TuneCoilyMainPageLocators.TIME_LEFT_TO_RESERVATION,
                                            timeout=5)

    def get_booking_message(self) -> Tuple[str, str]:
        """
        Method to get a title and message from booking page.

        :param :
        :return str:
        """
        title_element = self.find_element_collabos(TuneCoilyMessagesLocators.MESSAGE_TITLE)
        message_element = self.find_element_collabos(TuneCoilyMessagesLocators.MESSAGE_TEXT)
        value = 'text'

        title_box = title_element.get_attribute(value)
        title = str(title_box).split("·")[0].strip()

        message_box = message_element.get_attribute(value)
        message = str(message_box).split("·")[0].strip()

        return title, message

    def get_desk_hierarchy_authenticated_page(self) -> str:
        """
        Method to get a desk hierarchy from Coily authenticated page.

        :param :
        :return str: desk hierarchy
        """
        element = self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.HIERARHY)
        value = 'text'
        hierarchy = element.get_attribute(value)
        return str(hierarchy)

    def get_agenda_item_by_title(self, event_title: str) -> Optional[WebElement]:
        """
        Args:
            event_title: The title of the agenda item to search for.

        Returns:
            Optional[WebElement]: The web element representing the agenda item with the
                                  specified title, or None if no such agenda item is found.
        """
        all_elements = self._get_all_agenda_items()
        for parent in all_elements:
            child = parent.find_element(By.ID, TuneCoilyAuthorizedDeskLocators.EVENT_TITLE[1])
            if child and str(child.get_attribute('text')) == event_title:
                return parent
        return None

    def click_agenda_item_by_title(self, event_title: str) -> None:
        child_element = False
        all_elements = self._get_all_agenda_items()
        for parent in all_elements:
            child = parent.find_element(By.ID, TuneCoilyAuthorizedDeskLocators.EVENT_TITLE[1])
            if child and str(child.get_attribute('text')) == event_title:
                child_element = True
                child.click()

        if not child_element:
            print(f'Element "{event_title}" not found')

    def click_close_event_details(self):
        self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.EVENT_VIEW_CLOSE_BUTTON).click()

    def scroll_to_agenda_notes(self):
        return self.scroll_to_element_by_resource_id(TuneCoilyAuthorizedDeskLocators.EVENT_NOTES)

    def click_show_all_attendees(self):
        self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.EVENT_SHOW_ALL_ATTENDEES).click()

    def verify_any_agenda_item_displayed(self) -> bool:
        time.sleep(3)
        return self.verify_element_collabos(TuneCoilyAuthorizedDeskLocators.EVENT_ITEM, timeout=5)

    @staticmethod
    def get_agenda_event_time_frames(element: WebElement) -> str:
        """
        Method to get a agenda item event timeframes

        :param :
        :return str: desk hierarchy
        """
        el = element.find_element(By.ID, TuneCoilyAuthorizedDeskLocators.EVENT_TIME[1])
        value = 'text'
        hierarchy = el.get_attribute(value)
        return str(hierarchy)

    @staticmethod
    def get_agenda_event_attendees(element: WebElement) -> str:
        """
        Method to get a agenda item event attendees

        :param :
        :return str: desk hierarchy
        """
        el = element.find_element(By.ID, TuneCoilyAuthorizedDeskLocators.EVENT_ATTENDEES[1])
        value = 'text'
        hierarchy = el.get_attribute(value)
        return str(hierarchy)

    @staticmethod
    def get_agenda_event_join_now_button(element: WebElement) -> bool:
        """
        Method to get a agenda item event attendees

        :param :
        :return str: desk hierarchy
        """
        try:
            el = element.find_element(By.ID, TuneCoilyAuthorizedDeskLocators.EVENT_JOIN_NOW_BUTTON[1])
            if el:
                return True
        except Exception as e:
            return False

    def extend_agenda_view(self) -> None:
        bottom_sheet: MobileWebElement = self.find_element_collabos(
            TuneCoilyAuthorizedDeskLocators.AGENDA_BOTTOM_SHEET)

        # Get the size of the screen
        window_size = global_variables.collabos_driver.get_window_size()

        end_x = window_size['width'] / 2  # Move to the middle of the screen
        end_y = window_size['height'] / 2  # Move to the center of the screen

        # Initialize ActionChains to swipe up
        if get_python_version() < 312:
            from appium.webdriver.common.touch_action import TouchAction

            start_x = bottom_sheet.location['x'] + bottom_sheet.rect.get('width') // 2
            start_y = bottom_sheet.location['y'] + bottom_sheet.rect.get('height') // 2

            # Perform the drag action using TouchAction
            action = TouchAction(global_variables.collabos_driver)
            action.press(x=start_x, y=start_y)
            action.wait(ms=1000)
            action.move_to(x=end_x, y=end_y)
            action.release()
            action.perform()
        else:
            from appium.webdriver.extensions.action_helpers import ActionBuilder, ActionChains, \
                interaction, PointerInput

            touch_input = PointerInput(interaction.POINTER_TOUCH, 'touch')
            action_new = ActionChains(global_variables.collabos_driver)
            action_new.w3c_actions = ActionBuilder(global_variables.collabos_driver,
                                                   mouse=touch_input)

            action_new.w3c_actions.pointer_action.click_and_hold(bottom_sheet)
            action_new.w3c_actions.pointer_action.move_to_location(x=end_x, y=end_y)
            action_new.w3c_actions.pointer_action.release()
            action_new.perform()

            time.sleep(10)

    def click_close_agenda_view(self) -> None:
        self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.AGENDA_VIEW_CLOSE_BUTTON).click()

    def _get_all_agenda_items(self) -> List[WebElement]:
        """
        Method to get a desk hierarchy from Coily authenticated page.

        :param :
        :return str: desk hierarchy

        """
        return self.find_elements_collabos(TuneCoilyAuthorizedDeskLocators.EVENT_ITEM, timeout=30)

    def get_privacy_mode_events(self) -> MobileWebElement:
        """
        Method to check if privacy_agenda element is present on main page

        :param :
        :return str: desk hierarchy

        """
        return self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.PRIVACY_AGENDA)

    @staticmethod
    def check_if_no_meetings_match_in_privacy_mode(meetings_number: int) -> bool:
        verdict = True

        global_variables.collabos_driver.implicitly_wait(0)
        try:
            wait = WebDriverWait(global_variables.collabos_driver, 10)
            privacy_agenda = wait.until(
                EC.visibility_of_element_located(TuneCoilyAuthorizedDeskLocators.PRIVACY_AGENDA))
            (WebDriverWait(privacy_agenda, 10).
             until(EC.text_to_be_present_in_element(TuneCoilyAuthorizedDeskLocators.EVENT_TITLE,
                                                    f"{meetings_number} meeting" + "s" if meetings_number > 1 else ""
                                                    + "today")))

        except Exception as e:
            verdict = False
        finally:
            global_variables.collabos_driver.implicitly_wait(base.base_settings.IMPLICIT_WAIT)
            return verdict

    def get_desk_hierarchy_idle_page(self) -> str:
        """
        Method to get a desk hierarchy from Coily authenticated page.

        :param :
        :return str: desk hierarchy
        """
        element = self.find_element_collabos(TuneCoilyMainPageLocators.HIERARCHY)
        value = 'text'
        hierarchy = element.get_attribute(value)
        return str(hierarchy)

    def click_book_desk_button(self) -> None:
        """
        Clicks on the book desk button.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        self.find_element_collabos(TuneCoilyMainPageLocators.BOOK_DESK).click()

    def click_book_desk_button_confirmation(self) -> None:
        """
        Clicks on the book desk button.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
        self.find_element_collabos(TuneCoilyMainPageLocators.BOOK_DESK_GOT_IT).click()

    def click_settings_button_main_page(self):
        self.find_element_collabos(TuneCoilySettingsLocators.SETTINGS_FROM_MAIN_MENU).click()

    def click_close_admin_settings_page(self):
        self.find_element_collabos(TuneCoilySettingsLocators.CLOSE_BUTTON).click()

    def click_language_settings_button(self):
        self.find_element_collabos(TuneCoilySettingsLocators.SETTINGS_MENU_LANGUAGE).click()

    def click_close_pin_page(self) -> None:
        self.find_element_collabos(TuneCoilyMainPageLocators.PIN_PAGE_CLOSE).click()

    def click_notification_action_during_check_in(self):
        self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.NOTIFICATION_ACTION).click()

    def click_notification_dismiss_during_check_in(self):
        self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.NOTIFICATION_DISMISS).click()

    def get_date_authenticated_page(self) -> str:
        """
        Method to get a date from Coily authenticated page.

        :param :
        :return str: current date
        """
        element = self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.DATE)
        value = 'text'
        date = element.get_attribute(value)
        return str(date)

    def get_time_authenticated_page(self) -> str:
        """
        method to get a time from Coily authenticated page.

        :param :
        :return str: current time
        """
        element = self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.CLOCK)
        value = 'text'
        time = element.get_attribute(value)
        return str(time)

    def get_info_for_who_the_desk_is_booked_for(self) -> str:
        """
        Method to get a info about the person who booked a desk.

        :param :
        :return str: info who booked the desk
        """
        element = self.find_element_collabos(TuneCoilyMessagesLocators.MESSAGE_TEXT)
        value = 'text'
        message = element.get_attribute(value)
        return str(message)

    def get_actually_you_sure_xxx_text(self) -> str:
        """
        Method to get a full "Actually you .." text message.

        :param :
        :return str: notification text
        """
        element = self.find_element_collabos(TuneCoilyMessagesLocators.ACTUALLY_YOU_QUESTION_TEXT)
        value = 'text'
        message = element.get_attribute(value)
        return str(message)

    def get_reservation_notification_message(self, timeout: int = collabos_config.implicit_wait
                                             ) -> str:
        """
        Method to get a text from reservation notification message.

        :param timeout: timeout for appearing the message
        :return str: reservation notification message.
        """
        title_element = self.find_element_collabos(
            TuneCoilyAuthorizedDeskLocators.NOTIFICATION_MESSAGE, timeout=timeout)
        value = 'text'

        title_box = title_element.get_attribute(value)
        title = str(title_box).split("·")[0].strip()

        return title

    def wait_for_notification_message(self, message: str,
                                      timeout: int = collabos_config.implicit_wait) -> str:
        """
        Method to wait for a new notification message.

        :param message: expected text message
        :param timeout: timeout for appearing the message
        :return str: reservation notification text message
        """
        try:
            title_element = self.find_element_collabos_text_to_be_present(
                TuneCoilyAuthorizedDeskLocators.NOTIFICATION_MESSAGE,
                timeout=timeout,
                message=message
            )
            value = 'text'

            title_box = title_element.get_attribute(value)
            title = str(title_box).split("·")[0].strip()

            return title
        except Exception as e:
            raise e

    def wait_for_notification_on_checking_window(self, message: str,
                                                 timeout: int = collabos_config.implicit_wait
                                                 ) -> str:
        """
        Method to wait for a new notification window with specified message and within defined time.

        :param message: expected text message
        :param timeout: timeout for appearing the message
        :return str: notification text message
        """
        title_element = self.find_element_collabos_text_to_be_present(
            TuneCoilyMessagesLocators.QUESTION_TEXT, timeout=timeout, message=message)
        value = 'text'

        title_box = title_element.get_attribute(value)
        title = str(title_box).split("·")[0].strip()

        return title

    def wait_for_message_on_checking_window(self, message: str,
                                            timeout: int = collabos_config.implicit_wait) -> str:
        """
        Method to wait for a new message on checking window.

        :param message: expected text message
        :param timeout: timeout for appearing the message
        :return str: notification text message
        """
        title_element = self.find_element_collabos_text_to_be_present(
            TuneCoilyMessagesLocators.MESSAGE_TITLE, timeout=timeout, message=message)
        value = 'text'

        title_box = title_element.get_attribute(value)
        title = str(title_box).split("·")[0].strip()

        return title

    def verify_release_the_desk_button(self) -> bool:
        """
        Method to verify if 'Release' button is visible.

        :param :
        :return str: True if button is visible, False otherwise
        """
        return self.verify_element_collabos(TuneCoilyLaptopDisconnectedLocators.RELEASE_DESK,
                                            timeout=10)

    def click_release_the_desk_button(self) -> None:
        """
        Method to click on the 'Release' button.

        :param :
        :return None:
        """
        self.find_element_collabos(TuneCoilyLaptopDisconnectedLocators.RELEASE_DESK).click()

    def click_got_it_on_error_screen(self) -> None:
        """
        Method to click on the 'Got it' button.

        :param :
        :return None:
        """
        self.find_element_collabos(TuneCoilyMessagesLocators.GOT_IT).click()

    def verify_check_in_via_mobile_app_button_displayed(self) -> bool:
        """
        Method to verify if 'Check in via mobile app' button is displayed.

        :param :
        :return str: True if button is displayed, False otherwise
        """
        return self.verify_element_collabos(TuneCoilyMessagesLocators.ACTION_BUTTON, timeout=5)

    def click_check_in_via_mobile_app_button_displayed(self) -> None:
        """
        Method to verify if 'Check in via mobile app' button is displayed.

        :param :
        :return str: True if button is displayed, False otherwise
        """
        self.find_element_collabos(TuneCoilyMessagesLocators.ACTION_BUTTON, timeout=5).click()

    def click_back_on_check_in_via_mobile_app_button(self) -> None:
        self.find_element_collabos(TuneCoilyMessagesLocators.BACK, timeout=5).click()

    def verify_notification_action_button_is_diplayed(self, text: str) -> bool:
        """
        Method to verify if button on the notification popup is available.

        :param :
        :return str: True if detected, False otherwise
        """
        if self.verify_element_collabos(TuneCoilyAuthorizedDeskLocators.NOTIFICATION_ACTION, timeout=5):
            Report.logInfo("Notification action button found.")
            element = self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.NOTIFICATION_ACTION)
            value = 'text'
            dashboard = element.get_attribute(value)
            button_text = str(dashboard).split("·")[0].strip()
            assert button_text == text, f"Text on the notification action button '{button_text}', does not match expected on '{text}'."
            return True
        return False

    def click_notification_action(self) -> None:
        """
        Method to click on the button on notification popup.

        :param :
        :return None:
        """
        self.find_element_collabos(TuneCoilyAuthorizedDeskLocators.NOTIFICATION_ACTION).click()

    def click_away_state(self, locator) -> None:
        """
        Method to click on the away state message.

        :param locator: locator with away message
        :return None:
        """
        Report.logInfo(f"Click on the {locator}.")
        self.find_element_collabos(locator).click()

    def get_away_message_strict(self) -> str:
        """
        Method to get the text of away state message.

        :param :
        :return str: Away messgae
        """
        Report.logInfo("Checking away message on coily")
        element = self.find_element_collabos(TuneCoilyLaptopDisconnectedLocators.AWAY_MESSAGE)
        value = 'text'
        away_message = element.get_attribute(value)
        return away_message

    def get_away_message(self) -> str:
        """
        Method to get the text of away state message.

        :param :
        :return str: Away messgae
        """
        element = self.find_element_collabos(TuneCoilyLaptopDisconnectedLocators.AWAY_MESSAGE)
        value = 'text'
        dashboard = element.get_attribute(value)
        desk_name = str(dashboard).split("·")[0].strip()
        return desk_name

    def get_user_name_from_away_page(self) -> str:
        """
        Method to get the user name from the away page.

        :param :
        :return str: Away message
        """
        element = self.find_element_collabos(
            TuneCoilyLaptopDisconnectedLocators.USER_NAME_AWAY_PAGE)
        value = 'text'
        dashboard = element.get_attribute(value)
        desk_name = str(dashboard).split("·")[0].strip()
        return desk_name

    def get_session_is_over_message(self) -> Tuple[str, str]:
        """
        Method to get a title and message texts from Session is over window.

        :param :
        :return str:
        """
        title_element = self.find_element_collabos(TuneCoilySessionIsOverLocators.MESSAGE_TITLE)
        message_element = self.find_element_collabos(TuneCoilySessionIsOverLocators.MESSAGE_TEXT)
        value = 'text'

        title_box = title_element.get_attribute(value)
        title = str(title_box).split("·")[0].strip()

        message_box = message_element.get_attribute(value)
        message = str(message_box).split("·")[0].strip()

        return title, message

    def get_user_name_from_booked_screen(self) -> Optional[str]:
        """
        Method to get a name from session in progress page.

        :param :
        :return str: text with info for whom the desk is booked for.
        """
        element = self.find_element_collabos(TuneCoilyBookedDeskLocators.USER_NAME,
                                             skip_exception=True)
        if element:
            value = 'text'
            dashboard = element.get_attribute(value)
            user_name = str(dashboard).split("·")[0].strip()
            return user_name
        return None

    def verify_session_in_progress_displayed(self) -> bool:
        """
        Method to verify if 'Session in progress' label is displayed.

        :param :
        :return str: True if label is displayed, False otherwise
        """
        return self.verify_element_collabos(TuneCoilyBookedDeskLocators.START_STATUS, timeout=5)

    def get_booked_in_x_minutes_for_text(self) -> Optional[str]:
        """
        Method to verify if 'Session in progress' label is displayed.

        :param :
        :return str: True if label is displayed, False otherwise
        """
        element = self.find_element_collabos(TuneCoilyBookedDeskLocators.START_STATUS,
                                             skip_exception=True)
        if element:
            value = 'text'
            dashboard = element.get_attribute(value)
            text = str(dashboard).split("·")[0].strip()
            return text
        return None

    def verify_countdown_icon_is_displayed(self, timeout: int) -> bool:
        """
        Method to verify if countdown icon is displayed.

        :param :
        :return str: True if label is displayed, False otherwise
        """
        return self.verify_element_collabos(TuneCoilySessionIsOverLocators.COUNTDOWN_ICON,
                                            timeout=timeout)

    def verify_clock_icon_is_displayed(self, timeout: int) -> bool:
        """
        Method to verify if clock icon is displayed.

        :param :
        :return str: True if label is displayed, False otherwise
        """
        return self.verify_element_collabos(TuneCoilySessionIsOverLocators.CLOCK_ICON,
                                            timeout=timeout)

    def click_desk_limit_got_it_button(self) -> None:
        """
        Method to click on Got it button on desk limit page.

        :return None:
        """
        self.find_element_collabos(TuneCoilyDeskTimeLimit.GOT_IT).click()

    def get_desk_time_limit_messages(self) -> Tuple[str, str]:
        """
        Method to get a title and message texts from Desk time is limited page.

        :param :
        :return str:
        """
        title_element = self.find_element_collabos(TuneCoilyDeskTimeLimit.MESSAGE_TITLE)
        message_element = self.find_element_collabos(TuneCoilyDeskTimeLimit.MESSAGE_TEXT)
        value = 'text'

        title_box = title_element.get_attribute(value)
        title = str(title_box).split("·")[0].strip()

        message_box = message_element.get_attribute(value)
        message = str(message_box).split("·")[0].strip()

        return title, message

    def click_check_in(self) -> None:
        """
        Method to click Check in button

        :param :
        :return :
        """
        self.find_element_collabos(TuneCoilyBookedDeskLocators.CHECK_IN_BUTTON).click()

    def click_got_it(self) -> None:
        """
        Method to click Got it button

        :param :
        :return :
        """
        self.find_element_collabos(TuneCoilyBookedDeskLocators.GOT_IT_BUTTON).click()

    def click_back(self) -> None:
        """
        Method to click Back button

        :param :
        :return :
        """
        self.find_element_collabos(TuneCoilyBookedDeskLocators.BACK).click()

    def click_cancel_transfer_desk(self) -> None:
        """
        Method to click Back button

        :param :
        :return :
        """
        self.find_element_collabos(TuneCoilyBookedDeskLocators.CANCEL_TRANSFER).click()
