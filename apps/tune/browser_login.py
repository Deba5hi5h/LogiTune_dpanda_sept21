from typing import Optional
from apps.browser_methods import BrowserClass
from apps.tune.tune_browser import TuneBrowser
from common.framework_params import (GOOGLE_ACCOUNT, GOOGLE_PASSWORD,
                                     OUTLOOK_ACCOUNT, OUTLOOK_PASSWORD)
from extentreport.report import Report


class TuneBrowserLogin:
    def __init__(self):
        self.browser = BrowserClass()

    def prepare_opened_browser(self, guest_mode: bool = False) -> None:
        self.browser.prepare_opened_browser(guest_mode)
        Report.logInfo(f'Browser has been opened successfully'
                       f'{" in Guest Mode" if guest_mode else ""}')

    def sign_in_to_google_work_account(self, credentials: Optional[dict] = None) -> bool:
        try:
            self.browser.connect_to_google_accounts_browser_page()
            tune_browser = TuneBrowser()

            if credentials:
                Report.logInfo(f"Sign in to Google Work account as "
                               f"{credentials['signin_payload']['email']}")
                login_status = tune_browser.sign_in_to_google_work_account(
                    credentials['signin_payload']['email'],
                    credentials['signin_payload']['password'],
                    credentials['signin_payload']['employee_id']
                )
            else:
                Report.logInfo(f"Sign in to Google Calendar account as {GOOGLE_ACCOUNT}")
                login_status = tune_browser.sign_in_to_google_work_account(
                    GOOGLE_ACCOUNT, GOOGLE_PASSWORD)
            return login_status
        except Exception as e:
            Report.logInfo(str(e))
            return False

    def sign_in_to_outlook_work_account(self, credentials: Optional[dict] = None) -> bool:
        try:
            self.browser.connect_to_outlook_accounts_browser_page()
            tune_browser = TuneBrowser()

            if credentials:
                Report.logInfo(f"Sign in to Google Work account as "
                               f"{credentials['signin_payload']['email']}")
                login_status = tune_browser.sign_in_to_outlook_work_account(
                    credentials['signin_payload']['email'],
                    credentials['signin_payload']['password'])
            else:
                Report.logInfo(f"Sign in to Google Calendar account as {OUTLOOK_ACCOUNT}")
                login_status = tune_browser.sign_in_to_outlook_work_account(
                    OUTLOOK_ACCOUNT, OUTLOOK_PASSWORD)

            return login_status
        except Exception as e:
            Report.logInfo(str(e))
            return False

    def close_all_browsers(self):
        self.browser.close_all_browsers()
