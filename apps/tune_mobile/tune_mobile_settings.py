from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_settings_locators import TuneMobileSettingsLocators


class TuneMobileSettings(TuneMobile):

    def click_signin(self):
        """
        Method to click Sign in with work account

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.SIGNIN).click()
        return self

    def click_google(self):
        """
        Method to click Google

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.GOOGLE).click()
        return self

    def click_microsoft(self):
        """
        Method to click Google

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.MICROSOFT).click()
        return self

    def click_continue(self, timeout: int = tune_mobile_config.implicit_wait):
        """
        Method to click continue button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.CONTINUE, timeout=timeout).click()
        return self

    def click_signin_close(self):
        """
        Method to click close button on Sign in page

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.SIGNIN_CLOSE).click()
        return self

    def verify_signin_close(self) -> bool:
        """
        Method to verify close button on Sign in page

        :param :
        :return TuneMobileSettings:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN_CLOSE, timeout=10)

    def click_google_email(self, email):
        """
        Method to click Google

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.GOOGLE_EMAIL, param=email).click()
        return self

    def click_microsoft_email(self, email):
        """
        Method to click Google

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.MICROSOFT_EMAIL, param=email).click()
        return self

    def type_microsoft_email(self, email: str):
        """
        Method to enter microsoft email

        :param email:
        :return TuneMobileSettings:
        """
        if self.verify_microsoft_email_textfield():
            if self.is_ios_device():
                self.find_element(TuneMobileSettingsLocators.SIGNIN_MICROSOFT_TEXTFIELD).click()
            self.find_element(TuneMobileSettingsLocators.SIGNIN_MICROSOFT_TEXTFIELD).send_keys(email)
            self.click_next()
        return self

    def verify_microsoft_email_textfield(self) -> bool:
        """
        Verify Microsoft Email Text Field displayed

        :param :
        :return TuneMobileSettings:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN_MICROSOFT_TEXTFIELD, timeout=2)

    def click_accept(self, timeout: int = tune_mobile_config.new_command_timeout):
        """
        Method to click Accept button

        :param timeout:
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.ACCEPT, timeout=timeout).click()

    def click_allow(self):
        """
        Method to click Allow button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.ALLOW).click()
        return self

    def click_grant_permission(self):
        """
        Method to click Grant Permission button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.GRANT_PERMISSION).click()
        return self

    def click_next(self):
        """
        Method to click Next button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.NEXT).click()
        return self

    def click_start_testing(self):
        """
        Method to click Start Testing button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.START_TESTING).click()
        return self

    def click_ok(self):
        """
        Method to click OK button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.OK_BUTTON).click()
        return self

    def verify_ok(self, timeout: int = 2) -> bool:
        """
        Method to verify OK button displayed

        :param :
        :return TuneMobileSettings:
        """
        return self.verify_element(TuneMobileSettingsLocators.OK_BUTTON, timeout=timeout)

    def verify_grant_permission(self) -> bool:
        """
        Method to verify Grant Permission button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.GRANT_PERMISSION, timeout=5)

    def click_confirm(self):
        """
        Method to click Google

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.CONFIRM).click()
        return self

    def click_back(self) -> TuneMobileHome:
        """
        Method to get Equalizer value

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileSettingsLocators.BACK).click()
        return TuneMobileHome()

    def click_done(self):
        """
        Method to click Done button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.DONE).click()
        return self

    def click_building(self):
        """
        Method to click Building

        :param :
        :return TuneMobileBuilding:
        """
        self.find_element(TuneMobileSettingsLocators.BUILDING).click()
        from apps.tune_mobile.tune_mobile_building import TuneMobileBuilding
        return TuneMobileBuilding()

    def click_skip(self):
        """
        Method to click Skip

        :param :
        :return TuneMobileBuilding:
        """
        self.find_element(TuneMobileSettingsLocators.SKIP).click()
        from apps.tune_mobile.tune_mobile_dashboard import TuneMobileDashboard
        return TuneMobileDashboard()

    def click_add_teammates(self):
        """
        Method to click Building

        :param :
        :return TuneMobilePeople:
        """
        self.find_element(TuneMobileSettingsLocators.ADD_TEAMMATES).click()
        from apps.tune_mobile.tune_mobile_people import TuneMobilePeople
        return TuneMobilePeople()

    def click_got_it(self):
        """
        Method to click Got it button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.GOT_IT).click()
        return self

    def click_ask_later(self):
        """
        Method to click Ask Later button

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.ASK_LATER).click()
        return self

    def enable_privacy_policy_checkbox(self):
        """
        Method to enable privacy policy checkox

        :param :
        :return TuneMobileSettings:
        """
        if not self.verify_privacy_policy_checkbox_enabled():
            self.find_element(TuneMobileSettingsLocators.PRIVACY_POLICY_CHECKBOX).click()

    def get_building_name(self) -> str:
        """
        Method to get Building Name

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileSettingsLocators.BUILDING_NAME)
        value = 'value' if self.is_ios_device() else 'text'
        return str(element.get_attribute(value)).strip()

    def verify_signin(self) -> bool:
        """
        Method to verify sign in link displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN, timeout=5)

    def verify_teammates_label(self, teammates_text: str) -> bool:
        """
        Method to verify displayed teammates text

        :param teammates_text:
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.TEAMMATES_LABEL, param=teammates_text, timeout=2)

    def verify_continue(self, timeout: int = 2) -> bool:
        """
        Method to verify Continue button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.CONTINUE, timeout=timeout)

    def verify_signin_to_logitune(self, timeout: int = 5) -> bool:
        """
        Method to verify Sign in to Logi Tune displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN_TO_LOGITUNE, timeout=timeout)

    def verify_confirm(self) -> bool:
        """
        Method to verify Confirm button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.CONFIRM, timeout=2)

    def verify_done(self) -> bool:
        """
        Method to verify Done button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.DONE, timeout=2)

    def verify_sign_in_screen(self) -> bool:
        """
        Method to verify Sign In screen shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN_WORK_ACCOUNT)

    def verify_enroll_device_message(self) -> bool:
        """
        Method to verify Enroll Device message shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.ENROLL_DEVICE_MSG, timeout=1)

    def verify_privacy_policy_message(self) -> bool:
        """
        Method to verify Privacy Policy message shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.PRIVACY_POLICY_MSG, timeout=1)

    def verify_privacy_policy_checkbox(self) -> bool:
        """
        Method to verify Privacy Policy Checkbox shown

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.PRIVACY_POLICY_CHECKBOX, timeout=1)

    def verify_privacy_policy_checkbox_enabled(self) -> bool:
        """
        Method to verify Privacy Policy Checkbox shown

        :param :
        :return bool:
        """
        element = self.find_element(TuneMobileSettingsLocators.PRIVACY_POLICY_CHECKBOX, timeout=1)
        if self.is_ios_device():
            return int(element.get_attribute('value')) == 1
        else:
            return element.get_attribute('checked') == 'true'

    def verify_google_icon(self) -> bool:
        """
        Method to verify Google Icon displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.GOOGLE)

    def verify_microsoft_icon(self) -> bool:
        """
        Method to verify Microsoft Icon displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.MICROSOFT)

    def verify_sign_in_with_google_screen(self) -> bool:
        """
        Method to verify Google Sign in screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN_WITH_GOOGLE)

    def verify_sign_in_with_microsoft_screen(self) -> bool:
        """
        Method to verify Microsoft Sign in screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.SIGNIN_WITH_MICROSOFT)

    def verify_sign_in_with_microsoft_message(self) -> bool:
        """
        Method to verify mesage in Microsoft Sign in screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.MICROSOFT_PICK_ACCOUNT)

    def verify_google_access_message(self) -> bool:
        """
        Method to verify message displayed for google account access

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.GOOGLE_ACCESS_MESSAGE)

    def verify_google_allow_message(self, timeout:int = tune_mobile_config.implicit_wait) -> bool:
        """
        Method to verify message displayed - LogiTune wants to access your Google Account

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.GOOGLE_ALLOW_MESSAGE, timeout=timeout)

    def verify_microsoft_access_message(self) -> bool:
        """
        Method to verify message displayed for google account access

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.MICROSOFT_ACCESS_MESSAGE)

    def verify_booking_welcome_screen(self) -> bool:
        """
        Method to verify Tune Booking welcome screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.WELCOME_SCREEN)

    def verify_booking_welcome_screen_message(self) -> bool:
        """
        Method to verify Tune Booking welcome message

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.WELCOME_MESSAGE)

    def verify_booking_basecamp_screen(self) -> bool:
        """
        Method to verify Tune Booking Basecamp to choose building screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.BASECAMP_SCREEN)

    def verify_booking_basecamp_screen_message(self) -> bool:
        """
        Method to verify Tune Booking Basecamp message

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.BASECAMP_MESSAGE)

    def verify_booking_whos_on_your_team_screen(self) -> bool:
        """
        Method to verify Tune Booking Whos on Your Team to choose teammates screen

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.WHOS_ON_TEAM)

    def verify_booking_whos_on_your_team_message(self) -> bool:
        """
        Method to verify Tune Booking Whos on Your Team message

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.WHOS_ON_TEAM_MESSAGE, timeout=1)

    def verify_no_access_title(self) -> bool:
        """
        Method to verify No Access title

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.NO_ACCESS_TITLE)

    def verify_no_access_message(self) -> bool:
        """
        Method to verify No Access message

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.NO_ACCESS_MESSAGE, timeout=3)

    def verify_no_basecamp_title(self) -> bool:
        """
        Method to verify No Basecamp title

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.NO_BASECAMP_TITLE)

    def verify_no_basecamp_message(self) -> bool:
        """
        Method to verify No Basecamp message

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.NO_BASECAMP_MESSAGE, timeout=3)

    def verify_got_it(self) -> bool:
        """
        Method to verify Got it button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.GOT_IT, timeout=3)

    def verify_allow(self) -> bool:
        """
        Method to verify Allow button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.ALLOW, timeout=5)

    def click_dismiss(self):
        """
        Method to click Dismiss button on Google Signin screen (Only Android)

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileSettingsLocators.DISMISS).click()
        return self

    def verify_dismiss(self) -> bool:
        """
        Method to verify Dismiss button displayed (Only Android)

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileSettingsLocators.DISMISS, timeout=5)