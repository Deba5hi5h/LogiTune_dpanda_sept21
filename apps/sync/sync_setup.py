import time

from apps.sync.sync_app import SyncApp
from base import global_variables
from locators.sync_app.sync_app_setup_locators import SyncAppSetupLocators


class SyncSetup(SyncApp):

    def click_get_started(self):
        """
        Method to click on Get Started button

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.GET_STARTED).click()
        return SyncSetup()

    def click_system_doesnt_see_device(self):
        """
        Method to click on System Doesn't see the device link

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.SYSTEM_DOESNT_SEE_DEVICE).click()
        time.sleep(2)
        return SyncSetup()

    def click_setup_meetup(self):
        """
        Method to click on Setup MeetUp link

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.SETUP_MEETUP).click()
        time.sleep(2)
        return SyncSetup()

    def click_setup_rally_camera(self):
        """
        Method to click on Setup Rally Camera link

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.SETUP_RALLY_CAMERA).click()
        time.sleep(2)
        return SyncSetup()

    def click_close(self):
        """
        Method to click Close link

        :param :
        :return SyncSetup:
        """
        e = self.look_element(SyncAppSetupLocators.CLOSE)
        self.click_by_script(e)
        return SyncSetup()

    def click_done(self):
        """
        Method to click on Done button

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.DONE).click()
        return SyncSetup()

    def click_where_should_i_place_computer(self):
        """
        Method to click on Where Should I place computer

        :param :
        :return SyncSetup:
        """
        time.sleep(1)
        self.look_element(SyncAppSetupLocators.WHERE_PLACE_COMPUTER).click()
        return SyncSetup()

    def click_computer_by_the_tv(self):
        """
        Method to click on Computer by the TV

        :param :
        :return SyncSetup:
        """
        time.sleep(1)
        self.look_element(SyncAppSetupLocators.COMPUTER_BY_THE_TV).click()
        time.sleep(2)
        return SyncSetup()

    def click_computer_by_the_table(self):
        """
        Method to click on Computer by the Table

        :param :
        :return SyncSetup:
        """
        time.sleep(1)
        self.look_element(SyncAppSetupLocators.COMPUTER_BY_THE_TABLE).click()
        time.sleep(2)
        return SyncSetup()

    def click_next(self):
        """
        Method to click on Next button

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.NEXT).click()
        return SyncSetup()

    def click_ok_got_it(self):
        """
        Method to click on OK Got It button

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.OK_GOT_IT).click()
        return SyncSetup()

    def click_share_analytics_date(self):
        """
        Method to click on Share Analytics Data button

        :param :
        :return SyncSetup:
        """
        self.look_element(SyncAppSetupLocators.SHARE_ANALYTICS_DATA).click()
        return SyncSetup()

    def type_in_room_name(self, input_text: str):
        """
        Method to input text in Room Name field

        :param input_text:
        :return SyncSetup:
        """
        e = self.look_element(SyncAppSetupLocators.ROOM_NAME_SETUP)
        global_variables.driver.execute_script("arguments[0].value=''", e)
        e.send_keys(input_text)
        return SyncSetup()

    def type_in_seat_count(self, input_text: str):
        """
        Method to input text in Seat Count field

        :param input_text:
        :return SyncSetup:
        """
        e = self.look_element(SyncAppSetupLocators.SEAT_COUNT_SETUP)
        e.click()
        global_variables.driver.execute_script("arguments[0].value=''", e)
        e.send_keys(input_text)
        return SyncSetup()

    def verify_seat_count_error(self) -> bool:
        """
        Method to verify Seat count error message displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.SEAT_ERROR)

    def verify_system_doesnt_see_device(self) -> bool:
        """
        Method to verify System doesn't see the device link displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.SYSTEM_DOESNT_SEE_DEVICE)

    def verify_lets_setup_device(self, device_name: str) -> bool:
        """
        Method to verify Let's Setup device screen displayed

        :param device_name:
        :return bool:
        """
        if device_name.upper() == "MEETUP":
            return self.verify_element(SyncAppSetupLocators.LETS_SETUP_MEETUP)
        elif device_name.upper() == "RALLY CAMERA":
            return self.verify_element(SyncAppSetupLocators.LETS_SETUP_RALLY_CAMERA)
        elif device_name.upper() == "RALLY":
            return self.verify_element(SyncAppSetupLocators.LETS_SETUP_RALLY)
        else:
            return False

    def verify_connect_this_room_to_sync_portal(self) -> bool:
        """
        Method to verify Connect this room to Sync Portal screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.CONNECT_THIS_ROOM_TO_SYNC_PORTAL, timeunit=5)

    def verify_sign_in_to_sync_portal(self) -> bool:
        """
        Method to verify Sign in to Sync Portal screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.SIGN_IN_TO_SYNC_PORTAL, timeunit=5)

    def verify_skip_setup(self) -> bool:
        """
        Method to verify Skip Setup link displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.SKIP_SETUP, timeunit=2)

    def verify_room_information(self) -> bool:
        """
        Method to verify Room Information Screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.ROOM_INFORMATION, timeunit=5)

    def verify_where_should_i_place_computer(self) -> bool:
        """
        Method to verify Where Should I place computer link displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.WHERE_PLACE_COMPUTER)

    def verify_what_would_you_like_to_setup(self) -> bool:
        """
        Method to verify What would you like to setup screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.WHAT_WOULD_YOU_LIKE_TO_SET_UP)

    def verify_rally_camera_setup_button(self) -> bool:
        """
        Method to verify Rally Camera Setup section displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.RALLY_CAMERA_SETUP_BUTTON)

    def verify_rally_setup_button(self) -> bool:
        """
        Method to verify Rally/Rally Plus Setup section displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.RALLY_SETUP_BUTTON)

    def verify_meetup_setup_button(self) -> bool:
        """
        Method to verify MeetUp Setup section displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.MEETUP_SETUP_BUTTON)

    def verify_device_setup_video(self, device_name: str) -> bool:
        """
        Method to verify Setup MeetUp Video screen displayed

        :param device_name:
        :return bool:
        """
        result = False
        iframe = global_variables.driver.find_element_by_xpath("//iframe")
        iframe.click()
        global_variables.driver.switch_to.frame(iframe)
        if device_name.upper() == "MEETUP":
            result = self.verify_element(SyncAppSetupLocators.SETUP_MEETUP_VIDEO, timeunit=10)
        elif device_name.upper() == "RALLY CAMERA":
            result = self.verify_element(SyncAppSetupLocators.RALLY_CAMERA_SETUP_VIDEO, timeunit=10)
        global_variables.driver.switch_to.default_content()
        return result

    def verify_rally_setup_video(self, accessory: str) -> bool:
        """
        Method to verify Setup MeetUp Video screen displayed

        :param accessory:
        :return bool:
        """
        result = False
        iframe = global_variables.driver.find_element_by_xpath("//iframe")
        iframe.click()
        global_variables.driver.switch_to.frame(iframe)
        if accessory.upper() == "TABLE":
            result = self.verify_element(SyncAppSetupLocators.COMPUTER_BY_THE_TABLE_VIDEO, timeunit=10)
        elif accessory.upper() == "TV":
            result = self.verify_element(SyncAppSetupLocators.COMPUTER_BY_THE_TV_VIDEO, timeunit=10)
        global_variables.driver.switch_to.default_content()
        return result

    def verify_sync_setup_complete(self) -> bool:
        """
        Method to verify Sync Setup complete screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.SYNC_SETUP_COMPLETE, timeunit=10)

    def verify_help_us_improve(self) -> bool:
        """
        Method to verify Help us Improve screen displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppSetupLocators.HELP_US_IMPROVE, timeunit=10)