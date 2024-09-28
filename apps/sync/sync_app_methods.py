import time
from apps.browser_methods import BrowserClass
from apps.sync import sync_config
from apps.sync.sync_app import SyncApp
from apps.sync.sync_device import SyncDevice
from apps.sync.sync_device_audio import SyncDeviceAudio
from apps.sync.sync_device_camera import SyncDeviceCamera
from apps.sync.sync_device_connectivity import SyncDeviceConnectivity
from apps.sync.sync_home import SyncHome
from apps.sync.sync_room import SyncRoom
from apps.sync.sync_setup import SyncSetup
from apps.sync.sync_config import *
from base import global_variables
from common.platform_helper import get_custom_platform
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report


class SyncAppMethods(SyncApp):
    home = SyncHome()
    device = SyncDevice()
    camera = SyncDeviceCamera()
    audio = SyncDeviceAudio()
    connectivity = SyncDeviceConnectivity()
    browser = BrowserClass()
    setup = SyncSetup()
    room = SyncRoom()

    def open(self, fre=False) -> SyncHome:
        """
        Method to open Sync App and return Sync Home Screen

        :param fre:
        :return SyncHome:
        """
        self.open_sync_app(fre=fre)
        if get_custom_platform() != "windows":
            time.sleep(15)
        return self.home

    def close(self):
        """
        Method to close Sync App

        :param :
        :return :
        """
        self.close_sync_app()

    def open_and_get_room_name(self) -> str:
        """
        Method to open Sync App and get room name displayed

        :param :
        :return str:
        """
        return self.open().get_room_name()

    def rename_room(self, room_name: str):
        """
        Method to Rename Room

        :param room_name:
        :return SyncAppMethods:
        """
        self.home.click_menu().click_rename_room().type_in_room_edit_box(room_name)
        return SyncAppMethods()

    def verify_room(self, room_name: str) -> bool:
        """
        Method to verify the supplied room name is same as the room name set in Sync App

        :param room_name: Room name to be verified
        :return bool:
        """
        time.sleep(2)
        return room_name.lower() == self.home.get_room_name().lower()

    def setup_seat_count(self):
        """
        Method to set Seat Count to 5 in Sync App

        :param none
        :return none
        """
        self.home.click_room().type_in_seat_count("5")
        return SyncAppMethods()

    def connect_to_sync_portal(self, config: str, role: str, org_name: str):
        """
        Method to connect Room to Sync Portal

        :param org_name:
        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :return :
        """
        email = config.ROLES[role]['signin_payload']['email']
        pwd = config.ROLES[role]['signin_payload']['password']
        if self.home.click_room().click_connect_to_sync_portal().click_email_and_password() \
                .type_in_user_name(email).type_in_password(pwd).click_connect_room() \
                .select_org_name(org_name).click_join().verify_room_connected():
            Report.logPass("Room connected to Sync Portal successfully", True)
        else:
            Report.logFail("Room connection to Sync Portal Failed")
        return SyncAppMethods()

    def connect_to_sync_portal_using_provision_code(self, provision_code: str):
        """
        Method to connect Room to Sync Portal

        :param provision_code:
        :return :
        """
        if self.home.click_room().click_connect_to_sync_portal().click_room_provision_code() \
                .type_in_provision_code(provision_code).click_connect_room().verify_room_connected():
            Report.logPass("Room connected to Sync Portal successfully", True)
        else:
            Report.logFail("Room connection to Sync Portal Failed")
        return SyncAppMethods()

    def verify_provision_code_multiple_hosts_error(self, provision_code: str):
        """
        Method to verify room already has host PC/appliance device error during provision

        :param provision_code:
        :return :
        """
        if self.home.click_room().click_connect_to_sync_portal().click_room_provision_code() \
                .type_in_provision_code(provision_code).click_connect_room().verify_multiple_hosts_code_error():
            Report.logPass("Error message displayed - This room already has host PC/appliance device", True)
        else:
            Report.logFail("This room already has host PC/appliance device Error message not displayed")
        return SyncAppMethods()

    def verify_incorrect_provision_code_error(self, provision_code: str):
        """
        Method to verify invalid provision code error during room provision

        :param provision_code:
        :return :
        """
        if self.home.click_room().click_connect_to_sync_portal().click_room_provision_code() \
                .type_in_provision_code(provision_code).click_connect_room().verify_incorrect_code_error():
            Report.logPass("Error message displayed - This provisioning code is invalid", True)
        else:
            Report.logFail("This provisioning code is invalid Error message not displayed")
        return SyncAppMethods()

    def disconnect_room_from_sync_portal(self, config: str, role: str):
        """
        Method to connect Room to Sync Portal

        :param role: Sync Portal user role
        :param config: Config object downloaded from AWS
        :return :
        """
        email = config.ROLES[role]['signin_payload']['email']
        pwd = config.ROLES[role]['signin_payload']['password']
        if self.home.click_room().click_disconnect_room() \
                .type_in_user_name(email).type_in_password(pwd).click_disconnect_room().verify_room_disconnected():
            Report.logPass("Room disconnected from Sync Portal successfully", True)
        else:
            Report.logFail("Room disconnect from Sync Portal Failed")
        return SyncAppMethods()

    def setup_connect_to_sync_portal(self):
        """
        Method to connect to Sync Portal during the setup

        :param :
        :return :
        """
        if self.setup.verify_connect_this_room_to_sync_portal() or self.setup.verify_sign_in_to_sync_portal():
            Report.logPass("Sign in to Sync Portal screen displayed", True)
        else:
            Report.logFail("Sign in to Sync Portal screen not displayed")
        if self.setup.verify_skip_setup():
            Report.logPass("Skip Setup link displayed")
        else:
            Report.logFail("Skip Setup link not displayed")

        email = global_variables.config.ROLES[global_variables.SYNC_ROLE]['signin_payload']['email']
        pwd = global_variables.config.ROLES[global_variables.SYNC_ROLE]['signin_payload']['password']
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        if not self.room.click_email_and_password().verify_connect_button_enabled():
            Report.logPass("Connect Room button is disabled")
        else:
            Report.logFail("Connect Room button is enabled")
        self.room.type_in_user_name(email).type_in_password(pwd).click_connect_room() \
            .select_org_name(org_name).click_join()
        return SyncAppMethods()

    def setup_room_name_seat_count(self, room_name: str):
        """
        Method to enter room name and seat count during the setup

        :param room_name:
        :return :
        """

        if self.setup.verify_room_information():
            Report.logPass("Room Information screen displayed", True)
        else:
            Report.logFail("Room Information screen not displayed")
        if self.setup.type_in_room_name(room_name).type_in_seat_count("1000").click_next().verify_seat_count_error():
            Report.logPass("Error message displayed for seat count more than 3 digits", True)
        else:
            Report.logFail("Error message not displayed for seat count more than 3 digits")
        self.setup.type_in_seat_count("10").click_next()

    def add_device(self, device_name: str):
        """
        Method to add device in Sync App by clicking on + and connecting device

        :param device_name:
        :return :
        """
        self.home.click_add_device()
        connect_device(device_name)
        self.verify_device_connected_message(device_name=device_name)
        self.verify_device_displayed_in_sync_app(device_name=device_name)

    def forget_problem_device(self, device_name: str):
        """
        Method to remove device in error from Sync App

        :param device_name:
        :return SyncAppMethods:
        """
        disconnect_device(device_name)
        self.home.click_device(device_name)
        self.verify_problem_with_device_message_appears(device_name=device_name)
        self.device.click_lets_fix_it().click_forget().click_forget_now()
        self.verify_device_disconnected_message(device_name=device_name)
        self.verify_device_removed_from_sync_app(device_name=device_name)
        return SyncAppMethods()

    def forget_device(self, device_name: str):
        """
        Method to forget device from Sync App

        :param device_name:
        :return SyncAppMethods:
        """

        self.home.click_device(device_name).click_kebab().click_forget_device()
        disconnect_device(device_name)
        self.verify_device_disconnected_message(device_name=device_name)
        self.verify_device_removed_from_sync_app(device_name=device_name)
        return SyncAppMethods()

    def add_device_pnp(self, device_name: str):
        """
        Method to add device in Sync App by connecting device (plug n play)

        :param device_name:
        :return SyncAppMethods:
        """
        connect_device(device_name)
        time.sleep(5)
        if device_name.upper() in ("RALLY", "RALLY CAMERA", "MEETUP"):
            self.verify_device_setup(device_name=device_name)
        self.verify_device_connected_message(device_name=device_name)
        self.verify_device_displayed_in_sync_app(device_name=device_name)
        return SyncAppMethods()

    def verify_device_connected_message(self, device_name: str):
        """
        Method to verify device connected message displayed in Sync App

        :param device_name:
        :return :
        """
        if self.device.verify_device_connect_message(device_name=device_name):
            Report.logPass(f"{device_name} device connected message displayed", True)
        else:
            Report.logFail(f"{device_name} device connected message not displayed ")

    def verify_device_disconnected_message(self, device_name: str):
        """
        Method to verify device disconnected message displayed in Sync App

        :param device_name:
        :return :
        """
        if self.device.verify_device_disconnect_message(device_name=device_name):
            Report.logPass(f"{device_name} device disconnected message displayed", True)
        else:
            Report.logFail(f"{device_name} device disconnected message not displayed ")

    def verify_problem_with_device_message_appears(self, device_name: str):
        """
        Method to verify problem with device error message displayed in Sync App

        :param device_name:
        :return :
        """
        if self.device.verify_device_error_message(device_name=device_name):
            Report.logPass(f"Problem with {device_name} message displayed", True)
        else:
            Report.logFail(f"Problem with {device_name} message not displayed ")

    def verify_problem_with_device_message_removed(self, device_name: str):
        """
        Method to verify problem with device error message removed from Sync App

        :param device_name:
        :return :
        """
        self.device.verify_device_connect_message(device_name=device_name)
        if not self.device.verify_device_error_message(device_name=device_name, timeout=2):
            Report.logPass(f"Problem with {device_name} message removed", True)
        else:
            Report.logFail(f"Problem with {device_name} message still displayed ")

    def verify_device_displayed_in_sync_app(self, device_name: str):
        """
        Method to verify device displayed in Sync App

        :param device_name:
        :return :
        """
        if self.home.verify_device_displayed(device_name=device_name):
            Report.logPass(f"{device_name} displayed in Sync App")
        else:
            Report.logFail(f"{device_name} not displayed in Sync App")

    def verify_device_removed_from_sync_app(self, device_name: str):
        """
        Method to verify device displayed in Sync App

        :param device_name:
        :return :
        """
        if not self.home.verify_device_displayed(device_name=device_name):
            Report.logPass(f"{device_name} removed from Sync App")
        else:
            Report.logFail(f"{device_name} not removed from Sync App")

    def verify_kebab_options(self, device_name: str):
        """
        Method to verify the supplied room name is same as the room name set in Sync App

        :param device_name:
        :return bool:
        """
        kebab = self.home.click_device(device_name=device_name).click_kebab()
        self.report_displayed_or_not("Check for Device Update", kebab.verify_check_for_device_update())
        self.report_displayed_or_not("Forget Device", kebab.verify_forget_device())
        self.report_displayed_or_not("Quick Start Guide", kebab.verify_quick_start_guide())
        self.report_displayed_or_not("Setup Video", kebab.verify_setup_video())
        self.report_displayed_or_not("Product Support", kebab.verify_product_support())
        self.report_displayed_or_not("Order Spare Parts", kebab.verify_order_spare_parts())
        self.press_esc_key()

    def verify_kebab_option_device_update(self, device_name: str):
        """
        Method to verify device up to date message displayed on checking update

        :param device_name:
        :return bool:
        """
        self.home.click_device(device_name=device_name).click_kebab().click_check_for_device_update()
        self.report_displayed_or_not("Device Up to Date message", self.device.verify_device_up_to_date(device_name))

    def verify_what_would_you_like_to_setup(self):
        """
        Method to verify what would you like to setup screen during initial setup

        :param :
        :return :
        """
        try:
            self.report_displayed_or_not("What would you like to setup",
                                         self.setup.verify_what_would_you_like_to_setup())
            self.report_displayed_or_not("Setup for Rally Camera", self.setup.verify_rally_camera_setup_button())
            self.report_displayed_or_not("Setup for Rally/Rally Plus", self.setup.verify_rally_setup_button())
            self.report_displayed_or_not("Setup for MeetUp", self.setup.verify_meetup_setup_button())
        except Exception as e:
            Report.logException(str(e))

    def compare_url_with_opened_browser(self, url: str):
        """
        Method to compare capture the URL from opened browser and comapre
        Pre-requisite - call prepare_opened_browser() from BrowserClass
        :param url:
        :return :
        """
        driver = global_variables.driver
        global_variables.driver = self.browser.connect_to_current_browser_page()
        global_variables.driver.maximize_window()
        browser_url = global_variables.driver.current_url
        if url in browser_url:
            Report.logPass(f"Browser Opened with correct URL: {url}", True)
        else:
            Report.logFail(f"Browser opened with incorrect URL: {browser_url}")
        global_variables.driver.close()
        global_variables.driver = driver

    def verify_device_setup(self, device_name: str):
        """
        Method to verify device screen for MeetUp during setup

        :param device_name:
        :return :
        """
        try:
            self.browser.prepare_opened_browser()
            if self.setup.verify_lets_setup_device(device_name=device_name):
                Report.logPass(f"Lets Setup {device_name} Screen displayed", True)
            else:
                Report.logFail(f"Lets Setup {device_name} Screen not displayed")
            if self.setup.verify_system_doesnt_see_device():
                Report.logPass("Link displayed - The system doesn't see my device")
            else:
                Report.logFail("Link not displayed - The system doesn't see my device")
            self.setup.click_system_doesnt_see_device()
            if device_name.upper() == "MEETUP":
                self.compare_url_with_opened_browser(MEETUP_DOESNT_SEE_DEVICE_URL)
            elif device_name.upper() == "RALLY CAMERA":
                self.compare_url_with_opened_browser(RALLY_CAMERA_SYSTEM_DOESNT_SEE_DEVICE_URL)
            elif device_name.upper() == "RALLY":
                self.compare_url_with_opened_browser(RALLY_SYSTEM_DOESNT_SEE_DEVICE_URL)
            if device_name.upper() == "RALLY":
                if self.setup.verify_where_should_i_place_computer():
                    Report.logPass("Link displayed - Where should I place the computer?")
                else:
                    Report.logFail("Link not displayed - Where should I place the computer?")
                self.browser.prepare_opened_browser()
                self.setup.click_where_should_i_place_computer()
                self.compare_url_with_opened_browser(RALLY_WHERE_SHOULD_I_PLACE_COMPUTER_URL)
                self.setup.click_computer_by_the_tv()
                if self.setup.verify_rally_setup_video(accessory="TV"):
                    Report.logPass("Video displayed for Rally Setup with computer at the display", True)
                else:
                    Report.logFail("Video not displayed for Rally Setup with computer at the display")
                self.setup.click_close().click_computer_by_the_table()
                if self.setup.verify_rally_setup_video(accessory="TABLE"):
                    Report.logPass("Video displayed for Rally Setup with computer at the table", True)
                else:
                    Report.logFail("Video not displayed for Rally Setup with computer at the table")
            else:
                if device_name.upper() == "MEETUP":
                    self.setup.click_setup_meetup()
                elif device_name.upper() == "RALLY CAMERA":
                    self.setup.click_setup_rally_camera()
                if self.setup.verify_device_setup_video(device_name=device_name):
                    Report.logPass(f"Video displayed for How To Setup the Logitech {device_name} ConferenceCam", True)
                else:
                    Report.logFail(f"Video not displayed for How To Setup the Logitech {device_name} ConferenceCam")
            self.setup.click_close().click_done()
        except Exception as e:
            Report.logException(str(e))

    def verify_sync_setup_complete_and_share_analytics(self):
        """
        Method to verify Sync setup complete and Share Analytics data screens

        :param :
        :return :
        """
        if self.setup.verify_sync_setup_complete():
            Report.logPass("Sync Setup complete screen displayed", True)
        else:
            Report.logFail("Sync Setup complete screen not displayed")
        self.setup.click_ok_got_it()
        if self.setup.verify_help_us_improve():
            Report.logPass("Help us improve your experience screen displayed", True)
        else:
            Report.logFail("Help us improve your experience screen not displayed")
        self.setup.click_share_analytics_date()

    def get_room_information(self) -> dict:
        """
        Method to get Computer Type, OS, OS Version, Memory displayed in Room Information from Sync App

        :param :
        :return dict:
        """
        room_info = self.home.click_room().click_info()
        time.sleep(2)
        room_info = {"computer_type": room_info.get_computer_type(),
                     "operating_system": room_info.get_operating_system(),
                     "os_version": room_info.get_os_version(),
                     "processor": room_info.get_processor(),
                     "memory": room_info.get_memory()}
        Report.logPass("Capturing Room Information from Sync App", True)
        self.press_esc_key()
        return room_info

    def verify_links_in_camera_section(self, device_name: str):
        """
        Method to click on links displayed under camera section and verify correct link opened in browser

        :param device_name:
        :return :
        """
        self.verify_links_in_audio_section(device_name=device_name)
        self.camera.click_learn_more()
        self.compare_url_with_opened_browser(url=RIGHT_SIGHT_URL)

    def verify_links_in_audio_section(self, device_name: str):
        """
        Method to click on links displayed under camera section and verify correct link opened in browser

        :param device_name:
        :return :
        """
        refer_to_faq = None
        if device_name.lower() == "rally bar":
            refer_to_faq = RALLYBAR_REFER_TO_FAQ
        elif device_name.lower() == "rally bar mini":
            refer_to_faq = RALLYBARMINI_REFER_TO_FAQ
        elif device_name.lower() == "meetup":
            refer_to_faq = MEETUP_REFER_TO_FAQ
        elif device_name.lower() == "rally":
            refer_to_faq = RALLY_REFER_TO_FAQ
        elif device_name.lower() == "rally camera":
            refer_to_faq = RALLYCAMERA_REFER_TO_FAQ
        self.browser.prepare_opened_browser()
        self.camera.click_refer_to_faq()
        self.compare_url_with_opened_browser(url=refer_to_faq)

    def verify_mic_speaker_buttons(self, device_name: str):
        """
        Method to click on Test Mic and Speaker buttons and verify

        :param device_name:
        :return SyncAppMethods:
        """
        self.audio.click_test_mic()
        self.report_displayed_or_not("Clicking Test Mic, STOP Recording button", self.audio.verify_stop_recording())
        self.report_displayed_or_not("After testing complete, Test Mic button", self.audio.verify_test_mic())
        self.audio.click_test_speaker()
        self.report_displayed_or_not("Clicking on Test Speaker, Stop Playing button", self.audio.verify_stop_playing())
        self.audio.click_stop_playing()
        self.report_displayed_or_not("Clicking on Stop Playing, Test Speaker button", self.audio.verify_test_speaker())
        return SyncAppMethods()

    def verify_device_connect_disconnect(self, device_name: str):
        """
        Method to check device shows error after disconnecting and error disappears after connecting back

        :param device_name: e.g. Rally Bar Mini
        :return SyncAppMethods:
        """
        self.home.click_device(device_name=device_name)
        disconnect_device(device_name)
        self.verify_problem_with_device_message_appears(device_name=device_name)
        connect_device(device_name)
        self.verify_problem_with_device_message_removed(device_name=device_name)
        return SyncAppMethods()

    def verify_rightsight(self, enabled: bool):
        """
        Method to verify RightSight is Enabled or disabled

        :param enabled:
        :return bool:
        """
        verification = self.camera.verify_right_sight_enabled(enabled=enabled)
        self.report_enabled_or_disabled("RightSight", verification, enabled)
        return SyncAppMethods()

    def verify_on_call_start(self, selected: bool):
        """
        Method to verify On Call Start Radio is selected or not

        :param selected:
        :return bool:
        """
        verification = self.camera.verify_on_call_start_selected(selected=selected)
        self.report_enabled_or_disabled("RightSight On Call Start", verification, selected)
        return SyncAppMethods()

    def verify_dynamic(self, selected: bool):
        """
        Method to verify Dynamic Radio is selected or not

        :param selected:
        :return bool:
        """
        verification = self.camera.verify_dynamic_selected(selected=selected)
        self.report_enabled_or_disabled("RightSight Dynamic", verification, selected)
        return SyncAppMethods()

    def verify_speaker_view(self, enabled: bool):
        """
        Method to verify Speaker View is Enabled or disabled

        :param enabled:
        :return bool:
        """
        verification = self.camera.verify_speaker_view_selected(selected=enabled)
        self.report_enabled_or_disabled("Speaker View", verification, enabled)
        return SyncAppMethods()

    def verify_group_view(self, enabled: bool):
        """
        Method to verify Group View is Enabled or disabled

        :param enabled:
        :return bool:
        """
        verification = self.camera.verify_group_view_selected(selected=enabled)
        self.report_enabled_or_disabled("Group View", verification, enabled)
        return SyncAppMethods()

    def verify_picture_in_picture(self, enabled: bool):
        """
        Method to verify Group View is Enabled or disabled

        :param enabled:
        :return bool:
        """
        verification = self.camera.verify_picture_in_picture_enabled(enabled=enabled)
        self.report_enabled_or_disabled("Picture in Picture", verification, enabled)
        return SyncAppMethods()

    def verify_speaker_detection_slower(self, selected: bool):
        """
        Method to verify Speaker Detection Slower is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_speaker_detection_slower_selected(selected=selected)
        self.report_enabled_or_disabled("Speaker Detection Slower", verification, selected)
        return SyncAppMethods()

    def verify_speaker_detection_default(self, selected: bool):
        """
        Method to verify Speaker Detection Default is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_speaker_detection_default_selected(selected=selected)
        self.report_enabled_or_disabled("Speaker Detection Default", verification, selected)
        return SyncAppMethods()

    def verify_speaker_detection_faster(self, selected: bool):
        """
        Method to verify Speaker Detection Faster is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_speaker_detection_faster_selected(selected=selected)
        self.report_enabled_or_disabled("Speaker Detection Faster", verification, selected)
        return SyncAppMethods()

    def verify_framing_speed_slower(self, selected: bool):
        """
        Method to verify Framing Speed Slower is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_framing_speed_slower_selected(selected=selected)
        self.report_enabled_or_disabled("Framing Speed Slower", verification, selected)
        return SyncAppMethods()

    def verify_framing_speed_default(self, selected: bool):
        """
        Method to verify Framing Speed Default is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_framing_speed_default_selected(selected=selected)
        self.report_enabled_or_disabled("Framing Speed Default", verification, selected)
        return SyncAppMethods()

    def verify_framing_speed_faster(self, selected: bool):
        """
        Method to verify Framing Speed Faster is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_framing_speed_faster_selected(selected=selected)
        self.report_enabled_or_disabled("Framing Speed Faster", verification, selected)
        return SyncAppMethods()

    def verify_anti_flicker_pal(self, selected: bool):
        """
        Method to verify Anti-Flicker PAL is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_pal_selected(selected=selected)
        self.report_enabled_or_disabled("Anti-Flicker PAL", verification, selected)
        return SyncAppMethods()

    def verify_anti_flicker_ntsc(self, selected: bool):
        """
        Method to verify Anti-Flicker NTSC is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.camera.verify_ntsc_selected(selected=selected)
        self.report_enabled_or_disabled("Anti-Flicker NTSC", verification, selected)
        return SyncAppMethods()

    def verify_speaker_boost(self, enabled: bool):
        """
        Method to verify Speaker Boost is enabled or disabled

        :param enabled:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_speaker_boost_enabled(enabled=enabled)
        self.report_enabled_or_disabled("Speaker Boost", verification, enabled)
        return SyncAppMethods()

    def verify_ai_noise_suppression(self, enabled: bool):
        """
        Method to verify AI Noise Suppression is enabled or disabled

        :param enabled:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_ai_noise_suppression_enabled(enabled=enabled)
        self.report_enabled_or_disabled("AI Noise Suppression", verification, enabled)
        return SyncAppMethods()

    def verify_reverb_control_disabled(self, selected: bool):
        """
        Method to verify Reverb Control Disabled is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_reverb_control_disabled_selected(selected=selected)
        self.report_enabled_or_disabled("Reverb Control Disabled", verification, selected)
        return SyncAppMethods()

    def verify_reverb_control_normal(self, selected: bool):
        """
        Method to verify Reverb Control Normal is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_reverb_control_normal_selected(selected=selected)
        self.report_enabled_or_disabled("Reverb Control Normal", verification, selected)
        return SyncAppMethods()

    def verify_reverb_control_aggressive(self, selected: bool):
        """
        Method to verify Reverb Control Aggressive is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_reverb_control_aggressive_selected(selected=selected)
        self.report_enabled_or_disabled("Reverb Control Aggressive", verification, selected)
        return SyncAppMethods()

    def verify_microphone_eq_bass_boost(self, selected: bool):
        """
        Method to verify Microphone Eq Bass Boost is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_microphone_eq_bass_boost_selected(selected=selected)
        self.report_enabled_or_disabled("Microphone Eq Bass Boost", verification, selected)
        return SyncAppMethods()

    def verify_microphone_eq_normal(self, selected: bool):
        """
        Method to verify Microphone Eq Normal is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_microphone_eq_normal_selected(selected=selected)
        self.report_enabled_or_disabled("Microphone Eq Normal", verification, selected)
        return SyncAppMethods()

    def verify_microphone_eq_voice_boost(self, selected: bool):
        """
        Method to verify Microphone Eq Voice Boost is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_microphone_eq_voice_boost_selected(selected=selected)
        self.report_enabled_or_disabled("Microphone Eq Voice Boost", verification, selected)
        return SyncAppMethods()

    def verify_speaker_eq_bass_boost(self, selected: bool):
        """
        Method to verify Speaker Eq Bass Boost is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_speaker_eq_bass_boost_selected(selected=selected)
        self.report_enabled_or_disabled("Speaker Eq Bass Boost", verification, selected)
        return SyncAppMethods()

    def verify_speaker_eq_normal(self, selected: bool):
        """
        Method to verify Speaker Eq Normal is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_speaker_eq_normal_selected(selected=selected)
        self.report_enabled_or_disabled("Speaker Eq Normal", verification, selected)
        return SyncAppMethods()

    def verify_speaker_eq_voice_boost(self, selected: bool):
        """
        Method to verify Speaker Eq Voice Boost is selected

        :param selected:
        :return SyncAppMethods:
        """
        verification = self.audio.verify_speaker_eq_voice_boost_selected(selected=selected)
        self.report_enabled_or_disabled("Speaker Eq Voice Boost", verification, selected)
        return SyncAppMethods()

    def verify_bluetooth(self, enabled: bool):
        """
        Method to verify Bluetooth is Enabled or disabled

        :param enabled:
        :return bool:
        """
        verification = self.connectivity.verify_bluetooth_enabled(enabled=enabled)
        self.report_enabled_or_disabled("Bluetooth", verification, enabled)
        return SyncAppMethods()

    def verify_default_manual_color_settings(self, device_name: str):
        """
        Method to verify default manual color settings

        :param device_name : name of the device under test
        :return None
        """
        Report.logInfo("Verifying default manual color settings")
        time.sleep(5)
        brightness = contrast = saturation = sharpness = 50
        if device_name in ("Rally Bar", "Rally Bar Mini"):
            sharpness = 33
        elif device_name == "Rally Bar Huddle":
            brightness = 49
            contrast = saturation = sharpness = 44
        if self.camera.get_color_value("Brightness") == brightness \
                and self.camera.get_color_value("Contrast") == contrast \
                and self.camera.get_color_value("SATURATION") == saturation \
                and self.camera.get_color_value("SHARPNESS") == sharpness:
            Report.logPass("Manual color settings values are set to default", True)
        else:
            Report.logFail("Manual color settings values are not set to default")
        return SyncAppMethods()

    def verify_default_camera_adjustments(self, device_name: str):
        """
        Method to verify default Camera Adjustments settings

        :param device_name : name of the device under test
        :return SyncAppMethods:
        """
        if device_name in ("Rally Bar", "Rally", "Rally Camera"):
            if self.camera.verify_auto_focus_enabled() \
                    and self.camera.verify_auto_exposure_enabled() \
                    and self.camera.verify_auto_white_balanace_enabled():
                Report.logPass("Camera Adjustments values are set to default", True)
                return SyncAppMethods()
        else:
            if self.camera.verify_auto_exposure_enabled() and self.camera.verify_auto_white_balanace_enabled():
                Report.logPass("Camera Adjustments values are set to default", True)
                return SyncAppMethods()
        Report.logFail("Camera Adjustments values are not set to default", True)
        return SyncAppMethods()

    @staticmethod
    def compare_color_settings(color_setting, original_value, updated_value, operator):
        """
        Method to compare the color settings and to update the report

        :color_setting: Brightness or Contrast or Saturation or Sharpness
        :return none
        """
        if operator == 'greater':
            if original_value > updated_value:
                Report.logPass(f"Video Stream {color_setting} changed as per correct settings.")
            else:
                Report.logFail(f"Updated {color_setting} : {updated_value} "
                               f" is greater than or equal to original value : {original_value}.")
        elif operator == 'lesser':
            if original_value < updated_value:
                Report.logPass(f"Video Stream {color_setting} changed as per correct settings.")
            else:
                Report.logFail(f"Updated {color_setting} : {updated_value} "
                               f" is less than or equal to original value : {original_value}.")
        else:
            Report.logInfo("Operator not supported")
        return SyncAppMethods()

    def verify_manual_color_setting(self, color_setting: str, percentage: int):
        """
        Method to get manual color setting value

        :param percentage:
        :param color_setting: Manual color setting value eg: brightness, contrast, saturation, sharpness
        :return SyncAppMethods:
        """
        color_value = self.camera.get_color_value(color_setting)
        if color_value == percentage:
            Report.logPass(f"{color_setting} value persists")
        else:
            Report.logFail(f"{color_setting} value does not persist. {color_value} instead of {percentage}")
        return SyncAppMethods()

    @staticmethod
    def report_enabled_or_disabled(attribute: str, verification: bool, status: bool):
        value = "Enabled" if status else "Disabled"
        if verification:
            Report.logPass(f"Sync App: {attribute} is {value}", True)
        else:
            Report.logFail(f"Sync App: {attribute} is not {value}")

    @staticmethod
    def report_displayed_or_not(attribute: str, verification: bool, displayed: bool = True):
        value = " " if displayed else " not "
        fail = " not " if displayed else " "
        if verification:
            Report.logPass(f"Sync App: {attribute}{value}displayed", True)
        else:
            Report.logFail(f"Sync App: {attribute}{fail}displayed")
