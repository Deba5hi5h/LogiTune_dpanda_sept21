from apps.tune_mobile.tune_mobile import TuneMobile
from locators.tune_mobile.tune_mobile_notification_locators import TuneMobileNotificationLocators


class TuneMobileNotification(TuneMobile):

    def click_close(self):
        """
        Method to click close

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.CLOSE).click()
        return self

    def click_dismiss_notification(self):
        """
        Method to click dismiss notification button

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.DISMISS_NOTIFICATION).click()
        return self

    def click_clear_all(self):
        """
        Method to click Clear all button

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.CLEAR_ALL).click()
        return self

    def click_confirm_clear_all(self):
        """
        Method to click Clear all button on the confirmation

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.CONFIRM_CLEAR_ALL).click()
        return self

    def click_cancel(self):
        """
        Method to click Cancel button on the confirmation

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.CANCEL).click()
        return self

    def click_show_expired_notifications(self):
        """
        Method to click Show expired notifications

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.SHOW_EXPIRED_NOTIFICATIONS).click()
        return self

    def click_hide_expired_notifications(self):
        """
        Method to click Hide expired notifications

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.HIDE_EXPIRED_NOTIFICATIONS).click()
        return self

    def click_modify_booking(self):
        """
        Method to click Modify Booking button

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.MODIFY_BOOKING).click()
        return self

    def click_review_booking(self):
        """
        Method to click Review Booking button

        :param :
        :return TuneMobileNotification:
        """
        self.find_element(TuneMobileNotificationLocators.REVIEW_BOOKING).click()
        return self

    def verify_clear_all(self) -> bool:
        """
        Method to verify Clear all button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.CLEAR_ALL, timeout=5)

    def verify_show_expired_notifications(self) -> bool:
        """
        Method to verify Show expired notifications displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.SHOW_EXPIRED_NOTIFICATIONS, timeout=2)

    def verify_hide_expired_notifications(self) -> bool:
        """
        Method to verify Hide expired notifications displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.HIDE_EXPIRED_NOTIFICATIONS, timeout=2)

    def verify_no_active_notifications(self) -> bool:
        """
        Method to verify No Active notifications displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.NO_NEW_NOTIFICATIONS)

    def verify_clear_all_text(self) -> bool:
        """
        Method to verify Clear all notifications? displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.CLEAR_ALL_TEXT)

    def verify_clear_all_message(self) -> bool:
        """
        Method to verify Dismissed notifications cannot be accessed later. displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.CLEAR_ALL_MESSAGE)

    def verify_book_nearby_button(self) -> bool:
        """
        Method to verify Book desk nearby button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.BOOK_DESK_NEARBY)

    def verify_book_nearby_description(self) -> bool:
        """
        Method to verify "Would you like to book a desk near teammate" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.BOOK_DESK_NEARBY_DESCRIPTION)

    def verify_modify_booking_button(self) -> bool:
        """
        Method to verify Modify Booking button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.MODIFY_BOOKING)

    def verify_teammate_cancelled_message(self, teammate_name: str) -> bool:
        """
        Method to verify "<teammate> cancelled their booking" displayed

        :param teammate_name:
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.TEAMMATE_CANCELLED_MESSAGE, param=teammate_name)

    def verify_teammate_changed_message(self, teammate_name: str) -> bool:
        """
        Method to verify "<teammate> changed a desk booking" displayed

        :param teammate_name:
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.TEAMMATE_CHANGED_MESSAGE, param=teammate_name)

    def verify_teammate_cancelled_description(self) -> bool:
        """
        Method to verify "Would you like to modify your booking?" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.TEAMMATE_CANCELLED_DESCRIPTION)

    def verify_admin_booked_description(self) -> bool:
        """
        Method to verify "Would you like to book a desk near teammate" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.ADMIN_BOOKED_DESCRIPTION)

    def verify_admin_cancelled_description(self) -> bool:
        """
        Method to verify "Your booking was cancelled by an administrator" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.ADMIN_CANCELLED_DESCRIPTION)

    def verify_admin_updated_description(self) -> bool:
        """
        Method to verify "Your desk booking has been modified by an administrator" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.ADMIN_UPDATED_DESCRIPTION)

    def verify_review_booking_description(self) -> bool:
        """
        Method to verify "Review your updated booking and make any necessary changes" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.REVIEW_BOOKING_DESCRIPTION)

    def verify_review_booking_button(self) -> bool:
        """
        Method to verify Review Booking button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.REVIEW_BOOKING)

    def verify_book_a_new_desk_button(self) -> bool:
        """
        Method to verify Book A New Desk button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.BOOK_A_NEW_DESK)

    def verify_book_new_desk_description(self) -> bool:
        """
        Method to verify "Would you like to book a new desk?" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.BOOK_NEW_DESK_DESCRIPTION)

    def verify_custom_message(self, custom_message: str) -> bool:
        """
        Method to verify custom message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.CUSTOM_MESSAGE, param=custom_message)

    def verify_check_in_notification(self) -> bool:
        """
        Method to verify "You need to check-in at the desk" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.CHECK_IN_NOTIFICATION, timeout=60)

    def verify_check_in_description(self) -> bool:
        """
        Method to verify "To not lose your reservation, confirm it at the desk. Need to review
        or change your booking?" displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileNotificationLocators.CHECK_IN_DESCRIPTION)