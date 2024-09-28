from typing import Optional, List
from apps.tune.pages.base_page import TuneBasePage, WebDriver
from locators.tune.notifications_page_locators import TuneNotificationsPageLocators
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class NotificationCard:
    def __init__(self, card_element: WebElement):
        self.card_element = card_element
        label, time_created, main_text, action = (el.text for el in
                                                  self.card_element.find_elements(By.XPATH, ".//p"))
        self.label = label
        self.time_created = time_created
        self.time_created_seconds = int(self.time_created.split(" ")[0]) if "second" in self.time_created \
            else int(self.time_created[0]) * 60 if "minute" in self.time_created else int(self.time_created[0]) * 3600
        self.main_text = main_text
        self.action = action
        card_buttons = self.card_element.find_elements(By.XPATH, ".//button")
        self.close_button = card_buttons[0]
        if len(card_buttons) == 2:
            self.action_button = card_buttons[1]
        else:
            self.action_button = None

    def verify_label(self, label_text: str, strict: bool = False) -> bool:
        return self.label == label_text if strict else label_text in self.label

    def verify_time_created(self, time_created: str, strict: bool = False) -> bool:
        return self.time_created == time_created if strict else time_created in self.time_created

    def verify_main_text(self, main_text: str, strict: bool = False) -> bool:
        return self.main_text == main_text if strict else main_text in self.main_text

    def verify_action(self, action: str, strict: bool = False) -> bool:
        return self.action == action if strict else action in self.action


class TuneNotificationsPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)

    def _get_notification_list(self) -> List[WebElement]:
        return self._wait_for_multiple_elements_presence(TuneNotificationsPageLocators.NOTIFICATION_CARD,
                                                         comparison=">", no_elements=0)

    def _get_notification_cards(self) -> List[NotificationCard]:
        notifications = []

        found_notifications = self._get_notification_list()
        for notification in found_notifications:
            notifications.append(NotificationCard(notification))

        return notifications

    def get_latest_notification(self) -> NotificationCard:
        return self._get_notification_cards()[0]

    def scroll_to_notification(self, card: NotificationCard) -> None:
        return self._scroll_to_element(card.card_element)

    def get_all_notifications(self) -> List[NotificationCard]:
        return self._get_notification_cards()

    def click_back_to_dashboard_button(self) -> None:
        self._click(TuneNotificationsPageLocators.BACK_TO_DASHBOARD_BUTTON)

    def click_clear_notifications_button(self) -> None:
        self._click(TuneNotificationsPageLocators.CLEAR_ALERTS_BUTTON)

    def click_clear_notifications_button_confirm(self) -> None:
        self._click(TuneNotificationsPageLocators.CLEAR_ALERTS_BUTTON_CONFIRM)
        self._is_visible(TuneNotificationsPageLocators.NO_NOTIFICATIONS_LABEL, timeout=2)

    def click_clear_notifications_button_cancel(self) -> None:
        self._click(TuneNotificationsPageLocators.CLEAR_ALERTS_BUTTON_CANCEL)

    def verify_notifications_empty(self) -> bool:
        return self._is_visible(TuneNotificationsPageLocators.NO_NOTIFICATIONS_LABEL, timeout=2)

    def verify_notifications_page_present(self) -> bool:
        return self._is_visible(TuneNotificationsPageLocators.NOTIFICATIONS_PAGE_HEADER, timeout=2)

    def wait_for_notifications_to_load(self) -> None:
        self._is_visible(TuneNotificationsPageLocators.NOTIFICATIONS_LOADER, timeout=2)
        self._is_not_visible(TuneNotificationsPageLocators.NOTIFICATIONS_LOADER, timeout=5)
