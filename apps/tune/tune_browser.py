import time
from typing import Optional

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from locators.tune_browser_locators import *


class TuneBrowser(UIBase):

    def click_use_another_account(self) -> None:
        """
        Method to click on Use another account if there are signed in accounts
        :return none
        """
        if self.verify_element(TunesBrowserLocators.USE_ANOTHER_ACCOUNT, timeunit=20):
            self.look_element(TunesBrowserLocators.USE_ANOTHER_ACCOUNT).click()

    def sign_in_to_google_calendar(self, email: str, password: str,
                                   employee_id: Optional[str] = None) -> None:
        """
        Method to sign in to google account using email and password during calendar integration
        :param email - Gmail email address
        :param password - Gmail password for the account
        :param employee_id - Gmail Employee ID for the account
        :return None
        """
        try:
            self.verify_element(TunesBrowserLocators.EMAIL, wait_for_visibility=True)
            time.sleep(2)
            self.look_element(TunesBrowserLocators.EMAIL).clear()
            self.look_element(TunesBrowserLocators.EMAIL).send_keys(email)
            self.look_element(TunesBrowserLocators.NEXT).click()
            self.verify_element(TunesBrowserLocators.PASSWORD, wait_for_visibility=True)
            time.sleep(2)
            self.look_element(TunesBrowserLocators.PASSWORD).clear()
            self.look_element(TunesBrowserLocators.PASSWORD).send_keys(password)
            self.look_element(TunesBrowserLocators.PASSWORD_NEXT).click()
            if (self.verify_element(TunesBrowserLocators.EMPLOYEE_ID, wait_for_visibility=True)
                    and employee_id is not None):
                time.sleep(2)
                self.look_element(TunesBrowserLocators.EMPLOYEE_ID).clear()
                self.look_element(TunesBrowserLocators.EMPLOYEE_ID).send_keys(password)
                self.look_element(TunesBrowserLocators.EMPLOYEE_ID_NEXT).click()
            time.sleep(5)
            if self.verify_element(TunesBrowserLocators.CHECK_BOX, timeunit=5):
                check_boxes = self.look_all_elements(TunesBrowserLocators.CHECK_BOX)
                for check_box in check_boxes:
                    if check_box.get_attribute('disabled') or check_box.get_attribute('checked'):
                        continue
                    check_box.click()
            self.look_element(TunesBrowserLocators.CONTINUE).click()
            self.verify_element(TunesBrowserLocators.YOU_CAN_CLOSE_WINDOW)
            time.sleep(5)

        except Exception as e:
            Report.logException(e)

    def sign_in_to_google_work_account(self, email: str, password: str,
                                       employee_id: Optional[str] = None) -> bool:
        """
        Method to sign in to google account using email and password during calendar integration
        :param email - Gmail email address
        :param password - Gmail password for the account
        :param employee_id - Gmail employee ID for the account
        :return none
        """
        try:

            time.sleep(3)
            self._email_google_work_account(email)
            self._password_google_work_account(password)
            if (self.verify_element(TunesBrowserLocators.EMPLOYEE_ID, timeunit=15)
                    and employee_id is not None):
                self._employee_id_google_work_account(employee_id)
            time.sleep(7)
            if self.verify_element(TunesBrowserLocators.CHECK_BOX, timeunit=5):
                check_boxes = self.look_all_elements(TunesBrowserLocators.CHECK_BOX)
                for check_box in check_boxes:
                    if check_box.get_attribute('disabled'):
                        continue
                    check_box.click()
            self.look_element(TunesBrowserLocators.CONTINUE).click()
            time.sleep(3)
            if self.verify_element(TunesBrowserLocators.CONTINUE, timeunit=5):
                self.look_element(TunesBrowserLocators.CONTINUE).click()

            if self.verify_element(TunesBrowserLocators.ALLOW, timeunit=5):
                self.look_element(TunesBrowserLocators.ALLOW).click()

            return self.verify_redirecting_to_logi_tune_confirmation()

        except Exception as e:
            Report.logInfo(f'sign_in_to_google_work_account: {e}')
            return False

    def _email_google_work_account(self, email: str) -> None:
        try:
            email_element = self.look_clickable_element(TunesBrowserLocators.EMAIL, timeout=15)
            email_element.clear()
            email_element.send_keys(email)
            self.look_element(TunesBrowserLocators.NEXT).click()
        except Exception as e:
            Report.logInfo(f"Retry -> Exception found: {str(e)}.")
            email_element = self.look_clickable_element(TunesBrowserLocators.EMAIL, timeout=15)
            email_element.clear()
            email_element.send_keys(email)
            self.look_clickable_element(TunesBrowserLocators.NEXT).click()

    def _password_google_work_account(self, password: str) -> None:
        try:
            password_element = self.look_clickable_element(TunesBrowserLocators.PASSWORD,
                                                           timeout=15)
            password_element.clear()
            password_element.send_keys(password)
            self.look_clickable_element(TunesBrowserLocators.PASSWORD_NEXT).click()
        except Exception as e:
            Report.logInfo(f"Retry -> Exception found: {str(e)}.")
            password_element = self.look_clickable_element(TunesBrowserLocators.PASSWORD,
                                                           timeout=15)
            password_element.clear()
            password_element.send_keys(password)
            self.look_clickable_element(TunesBrowserLocators.PASSWORD_NEXT).click()

    def _employee_id_google_work_account(self, employee_id: str) -> None:
        try:
            employee_id_element = self.look_clickable_element(TunesBrowserLocators.EMPLOYEE_ID,
                                                              timeout=15)
            employee_id_element.clear()
            employee_id_element.send_keys(employee_id)
            self.look_clickable_element(TunesBrowserLocators.EMPLOYEE_ID_NEXT).click()
        except Exception as e:
            Report.logInfo(f"Retry -> Exception found: {str(e)}.")
            employee_id_element = self.look_clickable_element(TunesBrowserLocators.EMPLOYEE_ID,
                                                              timeout=15)
            employee_id_element.clear()
            employee_id_element.send_keys(employee_id)
            self.look_clickable_element(TunesBrowserLocators.EMPLOYEE_ID_NEXT).click()

    def verify_redirecting_to_logi_tune_confirmation(self):
        return self.verify_element(TunesBrowserLocators.REDIRECTING_TO_LOGI_TUNE)

    def sign_in_to_google_token(self, email: str, password: str,
                                employee_id: Optional[str] = None) -> None:
        """
        Method to sign in to google account using email and password during token
        :param email - Gmail email address
        :param password - Gmail password for the account
        :param employee_id - Gmail Employee ID for the account
        :return none
        """
        self.click_use_another_account()
        time.sleep(2)
        self.verify_element(TunesBrowserLocators.EMAIL, wait_for_visibility=True)
        self.look_element(TunesBrowserLocators.EMAIL).clear()
        self.look_element(TunesBrowserLocators.EMAIL).send_keys(email)
        self.look_element(TunesBrowserLocators.NEXT).click()
        self.verify_element(TunesBrowserLocators.PASSWORD, wait_for_visibility=True)
        time.sleep(2)
        self.look_element(TunesBrowserLocators.PASSWORD).clear()
        self.look_element(TunesBrowserLocators.PASSWORD).send_keys(password)
        self.look_element(TunesBrowserLocators.PASSWORD_NEXT).click()
        if (self.verify_element(TunesBrowserLocators.EMPLOYEE_ID, timeunit=15)
                and employee_id is not None):
            self._employee_id_google_work_account(employee_id)
        self.verify_element(TunesBrowserLocators.CONTINUE, wait_for_visibility=True)
        time.sleep(2)
        self.look_element(TunesBrowserLocators.CONTINUE).click()
        self.verify_element(TunesBrowserLocators.CONTINUE, wait_for_visibility=True)
        time.sleep(2)
        self.look_element(TunesBrowserLocators.CONTINUE).click()
        self.verify_element(TunesBrowserLocators.AUTHENTICATION_COMPLETED)

    def sign_in_to_outlook_calendar(self, email: str, password: str) -> None:
        """
        Method to sign in to Outlook account using email and password during calendar integration
        :param email - Outlook email address
        :param password - Outlook password for the account
        :return none
        """
        if self.verify_element(TunesBrowserLocators.REDIRECTING_TO_LOGI_TUNE):
            return
        self.look_element(TunesBrowserLocators.EMAIL).clear()
        self.look_element(TunesBrowserLocators.EMAIL).send_keys(email)
        self.look_element(TunesBrowserLocators.SUBMIT).click()
        time.sleep(2)
        self.look_element(TunesBrowserLocators.PASSWORD).clear()
        self.look_element(TunesBrowserLocators.PASSWORD).send_keys(password)
        self.look_element(TunesBrowserLocators.SUBMIT).click()
        time.sleep(2)
        self.look_element(TunesBrowserLocators.NO).click()
        if self.verify_element(TunesBrowserLocators.OUTLOOK_ACCEPT):
            self.look_element(TunesBrowserLocators.OUTLOOK_ACCEPT).click()
        self.verify_element(TunesBrowserLocators.YOU_CAN_CLOSE_WINDOW)
        time.sleep(2)

    def sign_in_to_outlook_work_account(self, email: str, password: str) -> bool:
        """
        Method to sign in to Outlook account using email and password during calendar integration
        :param email - Outlook email address
        :param password - Outlook password for the account
        :return none
        """
        try:

            time.sleep(3)
            self._email_outlook_work_account(email)
            self._password_outlook_work_account(password)
            self._accept_permissions_outlook_work_account()

            return self.verify_redirecting_to_logi_tune_confirmation()

        except Exception as e:
            Report.logWarning(str(e))
            return False

    def _email_outlook_work_account(self, email):
        try:
            email_element = self.look_clickable_element(TunesBrowserLocators.EMAIL, timeout=15)
            email_element.click()
            email_element.clear()
            email_element.send_keys(email)
            self.look_clickable_element(TunesBrowserLocators.SUBMIT).click()
        except Exception as e:
            Report.logInfo(f"Retry -> Exception found: {str(e)}.")
            email_element = self.look_clickable_element(TunesBrowserLocators.EMAIL, timeout=15)
            email_element.click()
            email_element.clear()
            email_element.send_keys(email)
            self.look_clickable_element(TunesBrowserLocators.SUBMIT).click()

    def _password_outlook_work_account(self, password):
        try:
            password_element = self.look_clickable_element(TunesBrowserLocators.PASSWORD, timeout=15)
            password_element.click()
            password_element.clear()
            password_element.send_keys(password)
            self.look_clickable_element(TunesBrowserLocators.SUBMIT).click()
        except Exception as e:
            Report.logInfo(f"Retry -> Exception found: {str(e)}.")
            password_element = self.look_clickable_element(TunesBrowserLocators.PASSWORD, timeout=15)
            password_element.click()
            password_element.clear()
            password_element.send_keys(password)
            self.look_clickable_element(TunesBrowserLocators.SUBMIT).click()

    def _accept_permissions_outlook_work_account(self):
        try:
            self.look_clickable_element(TunesBrowserLocators.STAY_SIGNED_IN_FINAL, timeout=15).click()
        except Exception as e:
            Report.logInfo(f"Retry -> Exception found: {str(e)}.")
            self.look_clickable_element(TunesBrowserLocators.STAY_SIGNED_IN_FINAL, timeout=15).click()


    def add_outlook_calendar_event(self, meeting_title: str) -> None:
        """
        Method to add an event in Outlook calendar
        :param meeting_title
        :return none
        """
        self.look_element(TunesBrowserLocators.NOTHING_PLANNED_FOR_THE_DAY)
        self.look_element(TunesBrowserLocators.NEW_EVENT).click()
        self.look_element(TunesBrowserLocators.ADD_A_TITLE).clear()
        self.look_element(TunesBrowserLocators.ADD_A_TITLE).send_keys(meeting_title)
        self.look_element(TunesBrowserLocators.SAVE).click()

    def del_outlook_calendar_event(self) -> None:
        """
        Method to delete an event in Outlook calendar
        :return none
        """
        while self.verify_element(TunesBrowserLocators.TUNE_MEETING):
            self.look_element(TunesBrowserLocators.TUNE_MEETING).click()
            self.look_element(TunesBrowserLocators.DELETE).click()
            self.look_element(TunesBrowserLocators.DELETE_EVENT).click()
            time.sleep(2)
        self.look_element(TunesBrowserLocators.NOTHING_PLANNED_FOR_THE_DAY)

    def verify_support_webpage_title(self) -> bool:
        """
        Method to verify Support webpage title should include Getting Started - Logi Tune
        :return bool
        """
        return self.verify_element(TunesBrowserLocators.GETTING_STARTED_LOGI_TUNE)

    def verify_share_feedback_webpage_title(self) -> bool:
        """
        Method to verify Share feedback webpage title should include Give feedback button
        :return bool
        """
        return self.verify_element(TunesBrowserLocators.GIVE_FEEDBACK)
