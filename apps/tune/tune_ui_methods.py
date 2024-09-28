import os
import re
import random
import string
from datetime import datetime, timedelta
from random import choice
from subprocess import Popen, check_output
from typing import Dict, List, Optional
import subprocess
import psutil

from selenium.webdriver.support.events import EventFiringWebDriver

from apps.tune.bluetooth_methods import BluetoothControl
from apps.DriverOpenApp import GetDriverForOpenApp
from apps.browser_methods import BrowserClass
from apps.tune.TuneElectron import TuneElectron
from apps.tune.TunesAppInstall import TunesUIInstall, TunesUIInstallWindows
from apps.tune.TunesAppInstallMacOS import TunesUIInstallMacOS
from apps.tune.device_parameters_utilities import TuneEnv
from apps.tune.calendar_api import CalendarApi, OutlookCalendarDriver
from apps.collabos.coily.tune_coily_config import GOOGLE
from apps.tune.tune_browser import TuneBrowser
from base.base_settings import TUNEAPP_NAME
from base.base_ui import UIBase
from base.listener import CustomListener
from common.json_helper import JsonHelper
from common.platform_helper import get_custom_platform
from common.relay_board_control import GenericRelayControl
from common.recorder import initialize_recorder
from common.usb_switch import *
from locators.app_locators import WinAppLocators
from locators.tunes_ui_locators import TunesAppLocators
from testsuite_firmware_api_tests.api_tests.device_api_names import DeviceName
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zone_wireless_2 import ZONE_WIRELESS_2_PROFILES_UI
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_zonewirelessplus import \
    ZONE_WIRELESS_PLUS_BUTTONS_MAPPING
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.usb_hid_communication_base import UsbHidCommunicationBase
from testsuite_tune_app.update_easteregg.device_parameters import Languages
from base import base_settings
from common.comparators import Comparator
from common.ota_versions import TuneVersionGetter


class TuneUIMethods(UIBase):
    tune_app = TuneElectron()
    bt_ctrl = BluetoothControl()
    _win_tune_updater = os.path.join(str(UIBase.rootPath), "firmware_tunes", "restart_tune_updater_service.bat")

    def tc_app_with_no_device(self):
        try:
            disconnect_all()
            self.tune_app.open_tune_app()
            self.tune_app.click_my_devices()
            if self.tune_app.verify_no_devices_connected():
                Report.logPass("No devices connected yet message displayed", True)
            else:
                Report.logFail("No devices connected yet message not displayed")
            time.sleep(1)
            self.tune_app.click_supported_devices()
            if self.tune_app.verify_headsets_header():
                Report.logPass("HEADSETS header displayed")
            else:
                Report.logFail("HEADSETS header not displayed")
            if self.tune_app.verify_webcams_header():
                Report.logPass("WEBCAMS header displayed", True)
            else:
                Report.logFail("WEBCAMS header not displayed")
            if self.tune_app.verify_docks_header():
                Report.logPass("DOCKS header displayed", True)
            else:
                Report.logFail("DOCKS header not displayed")
            if self.tune_app.verify_mice_header():
                Report.logPass("MICE header displayed", True)
            else:
                Report.logFail("MICE header not displayed")
            if self.tune_app.verify_keyboards_header():
                Report.logPass("KEYBOARDS header displayed", True)
            else:
                Report.logFail("KEYBOARDS header not displayed")
            if self.tune_app.verify_streaming_light_header():
                Report.logPass("STREAMING LIGHTS header displayed", True)
            else:
                Report.logFail("STREAMING LIGHTS header not displayed")

            headsets = ['Zone 750', 'Zone 900', 'Zone 950', 'Zone True Wireless', 'Zone Vibe 100', 'Zone Vibe 125',
                        'Zone Vibe 130', 'Zone Vibe Wireless', 'Zone Wired', 'Zone Wired Earbuds',
                        'Zone Wireless', 'Zone Wireless 2', 'Zone Wireless Plus']
            webcams = ['1080P Pro Stream Webcam', '4K Pro Magnetic', 'Brio', 'Brio 1080p Webcam',
                       'Brio 300', 'Brio 301', 'Brio 305', 'Brio 4K Stream',
                       'Brio 500', 'Brio 501', 'Brio 505',
                       'C920 HD Pro Webcam', 'C920c', 'C920e', 'C920s HD Pro Webcam', 'C920x HD Pro Webcam',
                       'C922 Pro Stream Webcam', 'C922x Pro Stream Webcam',
                       'C925e', 'C930 Pro Webcam',
                       'C930c', 'C930e', 'C930n', 'C930s', 'Pro Stream Webcam', 'Pro Webcam', 'StreamCam']
            docks = ['Logi Dock', 'Logi Dock Flex']
            mice = ['ERGO M575', 'ERGO M575 for Business', 'Lift', 'Lift Left', 'Lift for Business',
                    'Lift for Business Left', 'Lift for Mac', 'M240 Silent', 'M240 for Business', 'M705 Marathon',
                    'M720 Triathlon', 'MX Anywhere 2', 'MX Anywhere 2S', 'MX Anywhere 3', 'MX Anywhere 3 for Business',
                    'MX Anywhere 3 for Mac', 'MX Anywhere 3S', 'MX Anywhere 3S for Business', 'MX Anywhere 3S for Mac',
                    'MX Ergo', 'MX Master 2S', 'MX Master 3', 'MX Master 3 for Business', 'MX Master 3 for Mac',
                    'MX Master 3S', 'MX Master 3S for Business', 'MX Master 3S for Mac', 'MX Vertical', 'POP Mouse',
                    'Signature M550', 'Signature M550 L', 'Signature M650', 'Signature M650 L', 'Signature M650 L Left',
                    'Signature M650 L for Business', 'Signature M650 for Business']
            keyboards = ['Craft', 'ERGO K860', 'ERGO K860 for Business', 'K370 for Business', 'K780', 'K850', 'MX Keys',
                         'MX Keys Mini', 'MX Keys Mini for Business', 'MX Keys Mini for Mac', 'MX Keys S',
                         'MX Keys S for Mac', 'MX Keys for Business', 'MX Keys for Mac', 'MX Mechanical',
                         'MX Mechanical Mini', 'MX Mechanical Mini for Mac', 'POP Keys', 'Signature K650',
                         'Signature K650 for Business', 'Wave Keys', 'Wave Keys for Business', 'Wave Keys for Mac']
            lights = ['Litra Beam', 'Litra Glow']

            supported_devices = headsets + webcams + docks + mice + keyboards + lights

            for device in supported_devices:
                if self.tune_app.verify_device_displayed_on_supported_list(device_name=device):
                    Report.logPass(f"{device} - displayed under supported devices")
                else:
                    Report.logFail(f"{device} - not displayed under supported devices")
            self.tune_app.click_ok_button_on_supported_devices()
        except Exception as e:
            Report.logException(str(e))

    def tc_connect_dock(self, device_name):
        try:
            connect_device(device_name=device_name)
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            if self.tune_app.verify_device_connected() and self.tune_app.verify_device_name_displayed(device_name):
                Report.logPass(f"{device_name} - Connected displayed")
            else:
                Report.logFail(f"{device_name} - Connected not displayed")
            if self.tune_app.verify_equalizer_displayed():
                Report.logPass("Equalizer displayed")
            else:
                Report.logFail("Equalizer not displayed")
            if self.tune_app.verify_mic_level_displayed():
                Report.logPass("Mic level displayed")
            else:
                Report.logFail("Mic level not displayed")

            if self.tune_app.verify_device_name_label_displayed():
                Report.logPass("Device Name displayed", True)
            else:
                Report.logFail("Device Name not displayed")
            if self.tune_app.verify_meeting_alerts_displayed():
                Report.logPass("Meeting alert displayed", True)
            else:
                Report.logFail("Meeting alert not displayed")
            if self.tune_app.verify_hi_speed_usb_30_displayed():
                Report.logPass("Hi-Speed USB 3.0 displayed", True)
            else:
                Report.logFail("Hi-Speed USB 3.0 not displayed")

            if self.tune_app.verify_headset_diagnostics_displayed():
                Report.logPass("Sound diagnostics displayed", True)
            else:
                Report.logFail("Sound diagnostics not displayed")

        except Exception as e:
            Report.logException(str(e))
        finally:
            enable_port_if_not_connected(device_name=device_name)

    def tc_connect_headset(self, device_name: str, is_wireless: bool = False) -> None:
        """ Method to connect headset via USB HUB and check if all
        features are displayed

        @param device_name: device name
        @param is_wireless: True is headset is wireless, False for wired headsets
        @return: None
        """
        try:
            connect_device(device_name=device_name)
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            if is_wireless:
                if self.tune_app.verify_device_name_displayed(device_name):
                    Report.logPass(f"{device_name} - displayed in LogiTune")
                else:
                    Report.logFail(f"{device_name} - not displayed in LogiTune")
            else:
                if self.tune_app.verify_headset_connected() and self.tune_app.verify_device_name_displayed(device_name):
                    Report.logPass(f"{device_name} - Connected displayed")
                else:
                    Report.logFail(f"{device_name} - Connected not displayed")

            if is_wireless:
                if device_name in ["Zone Wireless", "Zone Wireless Plus", "Zone 900"]:
                    if self.tune_app.verify_noise_cancellation_displayed():
                        Report.logPass("Noise cancellation displayed")
                    else:
                        Report.logFail("Noise cancellation not displayed")

                    if self.tune_app.verify_connection_priority_label_displayed():
                        Report.logPass("Connection priority displayed", True)
                    else:
                        Report.logFail("Connection priority not displayed")

                if device_name in ["Zone Wireless", "Zone Wireless Plus", "Zone 900", "Zone True Wireless"]:
                    if self.tune_app.verify_button_functions_label_displayed():
                        Report.logPass("Button functions displayed", True)
                    else:
                        Report.logFail("Button functions not displayed")

                    if self.tune_app.verify_connection_priority_label_displayed():
                        Report.logPass("Connection priority displayed", True)
                    else:
                        Report.logFail("Connection priority not displayed")

                if self.tune_app.verify_equalizer_displayed():
                    Report.logPass("Equalizer displayed")
                else:
                    Report.logFail("Equalizer not displayed")

                if self.tune_app.verify_device_name_label_displayed():
                    Report.logPass("Device Name displayed", True)
                else:
                    Report.logFail("Device Name not displayed")

                if self.tune_app.verify_sleep_settings_label_displayed():
                    Report.logPass("Sleep settings displayed", True)
                else:
                    Report.logFail("Sleep settings not displayed")
                if self.tune_app.verify_connected_device_label_displayed():
                    Report.logPass("Connected device displayed", True)
                else:
                    Report.logFail("Connected device not displayed")

                if self.tune_app.verify_headset_language_displayed():
                    Report.logPass("Headset language displayed", True)
                else:
                    Report.logFail("Headset language not displayed")

                if device_name not in ["Zone True Wireless"]:
                    if self.tune_app.verify_headset_language_displayed():
                        Report.logPass("Headset language displayed", True)
                    else:
                        Report.logFail("Headset language not displayed")

            if device_name not in ["Zone True Wireless"]:
                if self.tune_app.verify_sidetone_displayed():
                    Report.logPass("Sidetone displayed")
                else:
                    Report.logFail("Sidetone not displayed")

                if self.tune_app.verify_mic_level_displayed():
                    Report.logPass("Mic level displayed")
                else:
                    Report.logFail("Mic level not displayed")

            if self.tune_app.verify_headset_diagnostics_displayed():
                Report.logPass("Headset diagnostics displayed", True)
            else:
                Report.logFail("Headset diagnostics not displayed")

            # if "Earbuds" and "Zone True Wireless" not in device_name:
            if device_name not in ["Zone Wired Earbuds", "Zone True Wireless", "H570e Mono", "H570e Stereo"]:
                if self.tune_app.verify_rotate_to_mute_label_displayed():
                    Report.logPass("Rotate to mute displayed", True)
                else:
                    Report.logFail("Rotate to mute not displayed")

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                if self.tune_app.verify_personal_eq_displayed():
                    Report.logPass("Personal EQ displayed", True)
                else:
                    Report.logFail("Personal EQ not displayed")
                if self.tune_app.verify_anc_button_options_displayed():
                    Report.logPass("ANC Group Button displayed", True)
                else:
                    Report.logFail("ANC Group Button not displayed")
                if self.tune_app.verify_health_and_safety_displayed():
                    Report.logPass("Health and Safety displayed", True)
                else:
                    Report.logFail("Health and Safety not displayed")
                if self.tune_app.verify_on_head_detection_displayed():
                    Report.logPass("On head detection displayed", True)
                else:
                    Report.logFail("On head detection not displayed")
                if self.tune_app.verify_touch_pad_displayed():
                    Report.logPass("Touch Pad displayed", True)
                else:
                    Report.logFail("Touch Pad not displayed")
                if self.tune_app.verify_anc_button_options_displayed():
                    Report.logPass("ANC Button options displayed", True)
                else:
                    Report.logFail("ANC Button options not displayed")
                if self.tune_app.verify_voice_prompts_3_levels_displayed():
                    Report.logPass("Voice Prompts displayed", True)
                else:
                    Report.logFail("Voice Prompts not displayed")
                if self.tune_app.verify_advanced_call_clarity_displayed():
                    Report.logPass("Advanced Call Clarity displayed", True)
                else:
                    Report.logFail("Advanced Call Clarity not displayed")
            else:
                if self.tune_app.verify_voice_prompts_displayed():
                    Report.logPass("Voice prompts displayed", True)
                else:
                    Report.logFail("Voice prompts not displayed")

            if device_name in ["Zone True Wireless"]:
                if self.tune_app.verify_in_ear_detection_label_displayed():
                    Report.logPass("In-ear detection displayed", True)
                else:
                    Report.logFail("In-ear detection not displayed")
                if self.tune_app.verify_enable_receiver_connection_label_displayed():
                    Report.logPass("Enable receiver connection displayed", True)
                else:
                    Report.logFail("Enable receiver connection not displayed")

            if device_name in ["H570e Mono", "H570e Stereo"]:
                if self.tune_app.verify_anti_startle_label_displayed():
                    Report.logPass("Anti Startle Protection displayed", True)
                else:
                    Report.logFail("Anti Startle Protection not displayed")


        except Exception as e:
            Report.logException(str(e))

        finally:
            enable_port_if_not_connected(device_name=device_name)

    def tc_pan_tilt(self, device_name):  # TODO: DELETE IT AFTER CREATING VALID PAN TILT TEST
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.click_zoom_in()
            Report.logInfo(self.tune_app.capture_video_stream())
            time.sleep(1)
            self.tune_app.click_pan_left()
            Report.logInfo(self.tune_app.capture_video_stream())
            time.sleep(1)
            self.tune_app.click_pan_right()
            Report.logInfo(self.tune_app.capture_video_stream())
            time.sleep(1)
            self.tune_app.click_tilt_up()
            Report.logInfo(self.tune_app.capture_video_stream())
            time.sleep(1)
            self.tune_app.click_tilt_down()
            Report.logInfo(self.tune_app.capture_video_stream())
            self.tune_app.click_zoom_out()
        except Exception as e:
            Report.logException(str(e))

    def tc_about_camera(self, device_name):
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.click_info_button()

            time.sleep(1)
            if self.tune_app.verify_device_name_displayed(device_name=device_name):
                Report.logPass(f"{device_name} - displayed in About")
            else:
                Report.logFail(f"{device_name} - not displayed in About")
            if self.tune_app.verify_more_details_displayed():
                Report.logPass("More details link displayed in About")
            else:
                Report.logFail("More details link not displayed in About")
            if self.tune_app.verify_factory_reset_displayed():
                Report.logPass("Factory reset button displayed in About")
            else:
                Report.logFail("Factory reset button not displayed in About")
        except Exception as e:
            Report.logException(str(e))

    def tc_firmware_update_brio4k(self, device_name):
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.click_info_button()
            if self.tune_app.verify_update_available_button():
                Report.logPass("Update button displayed", True)
                self.tune_app.click_update_button()
                update_version = self.tune_app.get_firmware_update_available_version()
                self.tune_app.click_start_update_button()
                self.tune_app.click_done_button()
                time.sleep(3)
                new_version = self.tune_app.get_firmware_version()
                if new_version == update_version:
                    Report.logPass(f"Firmware updated successfully to {new_version}", True)
                else:
                    Report.logFail(f"Firmware not updated successfully to {new_version}")
            else:
                Report.logFail("Update Available button not displayed")

        except Exception as e:
            Report.logException(str(e))

    def tc_dock_parameters_persistency(self, device_name: str, reconnect_timeout: int, profiles: Dict) -> None:
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            Report.logInfo(f'Set Equalizer profile.')
            current_name = self.tune_app.get_equalizer_profile_name()

            new_equalizer_profile = choice([i for i in profiles.keys() if i not in [current_name]])
            self.tune_app.click_equalizer()
            self.tune_app.set_equalizer_profile(profile_name=new_equalizer_profile)
            time.sleep(1)
            self.tune_app.verify_equalizer_name(new_equalizer_profile)

            Report.logInfo(f'Set Mic level.')
            self.tune_app.click_mic_level()

            value = self.tune_app.get_mic_level_slider_value()
            new_value = choice([i for i in range(0, 100) if i not in [value]])

            time.sleep(5)
            self.tune_app.set_mic_level_slider(new_value)
            time.sleep(5)
            self.tune_app.verify_mic_level_value(str(new_value), device_name)

            Report.logInfo(f'Set Device Name')
            self.tune_app.click_device_name_rename()
            self.tune_app.clear_device_name()
            chars = string.ascii_uppercase + string.digits
            new_name = f"{device_name} {''.join(random.choice(chars) for _ in range(40))}"
            new_name = new_name[:48]
            self.tune_app.set_new_device_name(new_name)
            Report.logInfo(f'New Device Name is: {new_name}')

            Report.logInfo(f'Set meeting alert.')
            meeting_alert_state = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f'Meeting alert state is {meeting_alert_state}')
            if meeting_alert_state:
                Report.logInfo(f'Change meeting alert state to False.')
                self.tune_app.click_meeting_alerts_toggle()
                time.sleep(2)
                meeting_alert_state = self.tune_app.get_meeting_alerts_state()
                Report.logInfo(f'Meeting alert state is: {meeting_alert_state}.')

            Report.logInfo(f'Set Hi Speed USB 3.0 mode')
            hi_speed_usb_mode = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f'Hi Speed USB 3.0 state is {hi_speed_usb_mode}')
            if hi_speed_usb_mode:
                Report.logInfo(f'Change Hi Speed USB 3.0 state to False.')
                self.tune_app.click_hi_speed_usb_3_0_toggle()
                self.tune_app.verify_reconnecting_device_label_displayed()
                self.tune_app.verify_supported_device_label(timeout=30)
                self.tune_app.click_device(device_name=device_name)
                time.sleep(2)
                hi_speed_usb_mode = self.tune_app.get_hi_speed_usb_3_0_state()
                Report.logInfo(f'Hi Speed USB 3.0 state is: {hi_speed_usb_mode}.')

            # RECONNECTION
            time.sleep(4)
            disconnect_device(device_name=device_name)
            time.sleep(reconnect_timeout)
            connect_device(device_name=device_name)
            time.sleep(10)

            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            time.sleep(2)

            self.tune_app.verify_equalizer_name(new_equalizer_profile)

            time.sleep(1)
            device_name_after_reconnect = self.tune_app.get_device_name_from_settings_page()
            if device_name_after_reconnect == new_name:
                Report.logPass(f"New device name displayed correctly on Settings page.", True)
            else:
                Report.logFail(
                    f"New device name not displayed correctly on Settings page: {device_name_after_reconnect}")

            hi_speed_usb_mode_2 = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f"Hi-Speed USB 3.0 state is {hi_speed_usb_mode_2}")
            if hi_speed_usb_mode_2 == hi_speed_usb_mode:
                Report.logPass("Hi Speed USB 3.0 mode is persisted.", True)
            else:
                Report.logFail("Hi Speed USB 3.0 mode is NOT persisted.")

            meeting_alert_2 = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f"Meeting Alert state is {meeting_alert_2}")
            if meeting_alert_2 == meeting_alert_state:
                Report.logPass("Meeting Alert mode is persisted.", True)
            else:
                Report.logFail("Meeting Alert mode is NOT persisted.")
        except Exception as e:
            Report.logException(str(e))

    def tc_meeting_alert(self, device_name: str) -> None:
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            Report.logInfo(f'Set meeting alert.')
            meeting_alert_state = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f'Meeting alert state is {meeting_alert_state}')

            Report.logInfo(f'Change meeting alert state to {not meeting_alert_state}')
            self.tune_app.click_meeting_alerts_toggle()

            time.sleep(1)
            meeting_alert_2 = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f"Meeting Alert state is {meeting_alert_2}")
            if meeting_alert_2 != meeting_alert_state:
                Report.logPass("Meeting Alert mode is changed successfully.", True)
            else:
                Report.logFail("Meeting Alert mode is not changed.")

            Report.logInfo(f'Change meeting alert state to {not meeting_alert_state}')
            self.tune_app.click_meeting_alerts_toggle()

            time.sleep(1)
            meeting_alert_3 = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f"Meeting Alert state is {meeting_alert_3}")
            if meeting_alert_3 != meeting_alert_2:
                Report.logPass("Meeting Alert mode is changed successfully.", True)
            else:
                Report.logFail("Meeting Alert mode is not changed.")

        except Exception as e:
            Report.logException(str(e))

    def tc_hi_speed_usb_3_0_logi_dock(self, device_name):
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            hi_speed_usb_mode = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f"Hi-Speed USB 3.0 state is {hi_speed_usb_mode}")
            self.tune_app.click_hi_speed_usb_3_0_toggle()
            self.tune_app.verify_reconnecting_device_label_displayed()
            self.tune_app.verify_supported_device_label(timeout=30)

            self.tune_app.click_device(device_name=device_name)

            hi_speed_usb_mode_2 = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f"Hi-Speed USB 3.0 state is {hi_speed_usb_mode_2}")
            if hi_speed_usb_mode_2 != hi_speed_usb_mode:
                Report.logPass("Hi Speed USB 3.0 mode is changed successfully.", True)
            else:
                Report.logFail("Hi Speed USB 3.0 mode is not changed.")

            self.tune_app.click_hi_speed_usb_3_0_toggle()
            self.tune_app.verify_reconnecting_device_label_displayed()
            self.tune_app.verify_supported_device_label(timeout=40)

            self.tune_app.click_device(device_name=device_name)

            hi_speed_usb_mode_3 = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f"Hi-Speed USB 3.0 state is {hi_speed_usb_mode_3}")
            if hi_speed_usb_mode_3 != hi_speed_usb_mode_2:
                Report.logPass("Hi Speed USB 3.0 mode is changed successfully.", True)
            else:
                Report.logFail("Hi Speed USB 3.0 mode is not changed.")

        except Exception as e:
            Report.logException(str(e))

    def tc_dock_factory_reset(self, device_name: str, profiles: Dict):
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            Report.logInfo(f'Set Equalizer profile.')
            current_name = self.tune_app.get_equalizer_profile_name()

            new_equalizer_profile = choice([i for i in profiles.keys() if i not in [current_name]])

            self.tune_app.click_equalizer()
            self.tune_app.set_equalizer_profile(profile_name=new_equalizer_profile)
            time.sleep(1)
            self.tune_app.verify_equalizer_name(new_equalizer_profile)

            Report.logInfo(f'Set Device Name')
            self.tune_app.click_device_name_rename()
            self.tune_app.clear_device_name()
            chars = string.ascii_uppercase + string.digits
            new_name = f"{device_name} {''.join(random.choice(chars) for _ in range(40))}"
            self.tune_app.set_new_device_name(new_name)
            Report.logInfo(f'New Device Name is: {new_name}')

            Report.logInfo(f'Set meeting alert.')
            meeting_alert_state = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f'Meeting alert state is {meeting_alert_state}')
            if not meeting_alert_state:
                Report.logInfo(f'Change meeting alert state to True.')
                self.tune_app.click_meeting_alerts_toggle()

            Report.logInfo(f'Set Hi Speed USB 3.0 mode')
            hi_speed_usb_mode = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f'Hi Speed USB 3.0 state is {meeting_alert_state}')
            if hi_speed_usb_mode:
                Report.logInfo(f'Change Hi Speed USB 3.0 state to False.')
                self.tune_app.click_hi_speed_usb_3_0_toggle()
                self.tune_app.verify_reconnecting_device_label_displayed()
                self.tune_app.verify_supported_device_label(timeout=30)
                self.tune_app.click_device(device_name=device_name)

            Report.logInfo(f'Factory reset')
            self.tune_app.click_info_button()

            self.tune_app.click_factory_reset()
            time.sleep(1)
            self.tune_app.click_proceed_to_factory_reset()
            time.sleep(2)

            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            time.sleep(5)

            self.tune_app.verify_equalizer_name("Default")

            device_name_factory_reset = self.tune_app.get_device_name_from_settings_page()
            if device_name_factory_reset == device_name:
                Report.logPass(f"Device name is reset successfully to default.", True)
            else:
                Report.logFail(
                    f"Device name is NOT reset successfully to default. Displayed name is {device_name_factory_reset}")

            hi_speed_usb_mode_2 = self.tune_app.get_hi_speed_usb_3_0_state()
            Report.logInfo(f"Hi-Speed USB 3.0 state is {hi_speed_usb_mode_2}")
            if hi_speed_usb_mode_2 is True:
                Report.logPass("Hi Speed USB 3.0 mode is reset successfully to default.", True)
            else:
                Report.logFail(f"Hi Speed USB 3.0 mode is NOT reset to default. Current value is {hi_speed_usb_mode_2}.")

            meeting_alert_2 = self.tune_app.get_meeting_alerts_state()
            Report.logInfo(f"Meeting Alert state is {meeting_alert_2}")
            if meeting_alert_2 is True:
                Report.logPass("Meeting Alert mode is reset successfully to default.", True)
            else:
                Report.logFail(f"Meeting Alert mode is NOT reset successfully to default. Current value is {meeting_alert_2}.")

        except Exception as e:
            Report.logException(str(e))

    def tc_sidetone(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify sidetone level.

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)

            self.tune_app.click_sidetone()
            time.sleep(2)
            value = self.tune_app.get_sidetone_slider_value()
            new_value = choice([i for i in range(0, 10) if i not in [value/10]])

            self.tune_app.set_sidetone_slider(new_value*10)
            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(5)
            self.tune_app.verify_sidetone_value(str(new_value*10))

            time.sleep(5)
            self._verify_sidetone_level(product_string=device_name,
                                        conn_type=conn_type,
                                        level=new_value)

        except Exception as e:
            Report.logException(str(e))

    def _verify_sidetone_level(self, product_string: str, conn_type: str, level: int) -> None:
        """ Method to verify sidetone level on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param level: sidetone level
        @return: None
        """
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.headset_audio_feature.get_sidetone_level()
        self.features.headset_audio_feature.verify_get_sidetone_level(response,
                                                                      level)
        self.centurion.close_port()

    def tc_mic_level(self, device_name: str) -> None:
        """ Method to change and verify mic level.

        @param device_name: device name
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)

            self.tune_app.verify_mic_level_displayed()

            self.tune_app.click_mic_level()

            value = self.tune_app.get_mic_level_slider_value()
            new_value = choice([i for i in range(0, 100) if i not in [value]])

            time.sleep(5)
            self.tune_app.set_mic_level_slider(new_value)

            time.sleep(5)
            self.tune_app.verify_mic_level_value(str(new_value), device_name)

        except Exception as e:
            Report.logException(str(e))

    def tc_wireless_headset_equalizer(self, device_name: str, conn_type: str, profiles: Dict) -> None:
        """Method to change and verify if Equalizer name is updated on the Sound page

        @param device_name: device name
        @return: None
        """
        self.tune_app.connect_tune_app(device_name=device_name)
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=device_name)

        current_name = self.tune_app.get_equalizer_profile_name()

        new_equalizer_profile = choice([i for i in profiles.keys() if i not in [current_name]])

        self.tune_app.click_equalizer()
        self.tune_app.set_equalizer_profile(profile_name=new_equalizer_profile)
        time.sleep(1)
        self.tune_app.verify_equalizer_name(new_equalizer_profile)

        time.sleep(5)
        if device_name != "Logi Dock":
            self._verify_equalizer_profile_over_api(product_string=device_name,
                                                    conn_type=conn_type,
                                                    profile=profiles[new_equalizer_profile])

    def _verify_equalizer_profile_over_api(self, product_string: str, conn_type: str, profile: int) -> None:
        """ Method to verify Rotate to mute state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
            self.features = Features(self.centurion)
            response = self.features.eqset_feature.get_eq_mode()
            self.features.eqset_feature.verify_eq_profile(response, profile)
        except Exception:
            report.logException("Verification over API failed")
        finally:
            if self.centurion:
                self.centurion.close_port()

    def tc_rotate_to_mute(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Rotate to mute state

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_rotate_to_mute_label_displayed()

            state = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Change Rotate to Mute state to {not state}")
            self.tune_app.click_rotate_to_mute_toggle()
            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(3)
            new_state = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Rotate to mute state changed correctly.", True)
            else:
                Report.logFail(f"Rotate to mute NOT state changed correctly.")
            time.sleep(5)
            self._verify_rotate_to_mute_over_api(product_string=device_name,
                                                 conn_type=conn_type,
                                                 state=new_state)

            # Change state for 2nd time
            Report.logInfo(f"Change Rotate to Mute state to {not new_state}")
            self.tune_app.click_rotate_to_mute_toggle()
            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(3)
            new_state_2 = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Rotate to mute state changed correctly.", True)
            else:
                Report.logFail(f"Rotate to mute NOT state changed correctly.")

            time.sleep(5)
            self._verify_rotate_to_mute_over_api(product_string=device_name,
                                                 conn_type=conn_type,
                                                 state=new_state_2)

        except Exception as e:
            Report.logException(str(e))

    def _verify_rotate_to_mute_over_api(self, product_string: str, conn_type: str, state: bool) -> None:
        """ Method to verify Rotate to mute state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Rotate to mute state
        @return: None
        """
        try:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
            self.features = Features(self.centurion)
            response = self.features.headset_misc_feature.get_mic_boom_status()
            self.features.headset_misc_feature.verify_mic_boom_status(response,
                                                                      state)
        except Exception:
            Report.logException("verification over APi failed")
        finally:
            if self.centurion:
                self.centurion.close_port()

    def tc_touch_pad(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Touch Pad state

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            time.sleep(10)

            self.tune_app.verify_touch_pad_displayed()

            state = self.tune_app.get_touch_pad_state()
            Report.logInfo(f"Touch Pad state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Change Touch Pad state to {not state}")
            self.tune_app.click_touch_pad_toggle()
            time.sleep(5)
            new_state = self.tune_app.get_touch_pad_state()
            Report.logInfo(f"Touch Pad state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Touch Pad state changed correctly.", True)
            else:
                Report.logFail(f"Touch Pad NOT state changed correctly.")
            time.sleep(5)
            self._verify_touch_pad_over_api(product_string=device_name,
                                            conn_type=conn_type,
                                            state=new_state)

            # Change state for 2nd time
            Report.logInfo(f"Change Touch Pad state to {not new_state}")
            self.tune_app.click_touch_pad_toggle()
            time.sleep(5)
            new_state_2 = self.tune_app.get_touch_pad_state()
            Report.logInfo(f"Touch Pad state is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Touch Pad state changed correctly.", True)
            else:
                Report.logFail(f"Touch Pad NOT state changed correctly.")

            time.sleep(5)
            self._verify_touch_pad_over_api(product_string=device_name,
                                            conn_type=conn_type,
                                            state=new_state_2)

        except Exception as e:
            Report.logException(str(e))

    def _verify_touch_pad_over_api(self, product_string: str, conn_type: str, state: bool) -> None:
        """ Method to verify Rotate to mute state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Rotate to mute state
        @return: None
        """
        try:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
            self.features = Features(self.centurion)
            response = self.features.touch_sensor_state.get_touch_sensor_state()
            self.features.touch_sensor_state.verify_get_touch_sensor_state(response, state)
        except Exception:
            Report.logException("Verification over API failed.")
        finally:
            if self.centurion:
                self.centurion.close_port()


    def tc_noise_cancellation(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Noise cancellation state

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_noise_cancellation_displayed()

            state = self.tune_app.get_noise_cancellation_state()
            Report.logInfo(f"Noise cancellation state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Change Noise cancellation state to {not state}")
            self.tune_app.click_noise_cancellation_toggle()
            new_state = self.tune_app.get_noise_cancellation_state()
            Report.logInfo(f"Noise cancellation state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Noise cancellation state changed correctly.", True)
            else:
                Report.logFail(f"Noise cancellation NOT state changed correctly.")
            time.sleep(2)
            self._verify_noise_cancellation_over_api(product_string=device_name,
                                                     conn_type=conn_type,
                                                     state=new_state)

            # Change state for 2nd time
            Report.logInfo(f"Change Noise cancellation state to {not new_state}")
            self.tune_app.click_noise_cancellation_toggle()
            new_state_2 = self.tune_app.get_noise_cancellation_state()
            Report.logInfo(f"Noise cancellation state is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Noise cancellation state changed correctly.")
            else:
                Report.logFail(f"Noise cancellation NOT state changed correctly.")

            time.sleep(2)
            self._verify_noise_cancellation_over_api(product_string=device_name,
                                                     conn_type=conn_type,
                                                     state=new_state_2)

        except Exception as e:
            Report.logException(str(e))

    def tc_anc_buttons(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify ANC buttons states.

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            time.sleep(3)

            anc_buttons = {"anc-off": (0, TunesAppLocators.ANC_DISABLED),
                           "anc-high": (1, TunesAppLocators.ANC_HIGH),
                           "anc-transparency": (2, TunesAppLocators.ANC_AMBIENCE_TRANSPARENCY),
                           "anc-low": (3, TunesAppLocators.ANC_LOW),
                           }

            for key, value in anc_buttons.items():
                Report.logInfo(f"Change ANC state to: {key}.")
                self.tune_app.click_anc_button(value[1])
                time.sleep(1)
                Report.logInfo(f"Verify: {key} is highlighted.")
                is_highlighted = self.tune_app.verify_anc_button_active(value[1])
                if is_highlighted:
                    Report.logPass(f"ANC value is changed and properly highlighted.")
                else:
                    Report.logFail(f"ANC value is NOT changed and properly highlighted.")
                time.sleep(5)
                Report.logInfo(f"Verify: ANC value over API.")

                self._verify_noise_cancellation_over_api(product_string=device_name,
                                                         conn_type=conn_type,
                                                         state=value[0])
                time.sleep(3)
                if conn_type == 'bt':
                    self.tune_app.connect_tune_app(device_name=device_name)
                    self.tune_app.click_my_devices()
                    self.tune_app.click_device(device_name=device_name)


        except Exception as e:
            Report.logException(str(e))

    def _verify_noise_cancellation_over_api(self, product_string: str, conn_type: str, state: int) -> None:
        """ Method to verify Rotate to mute state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Rotate to mute state
        @return: None
        """
        try:
            if conn_type == 'bt':
                com_port = self._get_centrion_com_port(device_name=product_string)
                self.tune_app.close_tune_app()
                time.sleep(10)
                self.centurion = CenturionCommands(device_name=product_string,
                                                   conn_type=conn_type,
                                                   com_port=com_port)
            else:
                self.centurion = CenturionCommands(device_name=product_string,
                                                   conn_type=conn_type)
            self.features = Features(self.centurion)
            response = self.features.headset_audio_feature.get_anc_state()
            self.features.headset_audio_feature.verify_get_anc_state(response,
                                                                     state)
        except Exception:
            Report.logException('Verification over API failed')
        finally:
            if self.centurion:
                self.centurion.close_port()

    def tc_anc_button_options(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify ANC Button Options.

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_anc_button_options_displayed()
            self.tune_app.click_anc_button_options()
            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(15)

            anc_button_options = {"anc-off": (1,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_LABEL,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_CHECKBOX,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_TOGGLE),
                                  "anc-high": (2,
                                               TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_LABEL,
                                               TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_CHECKBOX,
                                               TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_TOGGLE),
                                  "anc-transparency": (4,
                                                       TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_LABEL,
                                                       TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_CHECKBOX,
                                                       TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_TOGGLE),
                                  "anc-low": (8,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_LABEL,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_CHECKBOX,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_TOGGLE),
                                  }

            Report.logInfo(f"Step 1. Enable all options.")
            options = []
            for key, value in anc_button_options.items():
                options.append(key)
                Report.logInfo(f"Verify label is displayed for: {key}.")
                self.tune_app.verify_anc_button_option_label_displayed(value[1])
                if not self.tune_app.get_anc_button_option_state(value[2]):
                    Report.logInfo(f"{key} is Disabled. Click toggle to Enable it.")
                    self.tune_app.click_anc_button_option_toggle(value[3])
                    time.sleep(1)

            time.sleep(7)
            self._verify_anc_customization_over_api(product_string=device_name, conn_type=conn_type, mode=15)

            if conn_type == 'bt':
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_anc_button_options()

            Report.logInfo(f"Step 2. Disable first anc button option.")
            option_to_remove = options.pop(random.randrange(len(options)))
            Report.logInfo(f"Disable: {option_to_remove}")
            self.tune_app.click_anc_button_option_toggle(anc_button_options[option_to_remove][3])
            time.sleep(2)
            if not self.tune_app.get_anc_button_option_state(anc_button_options[option_to_remove][2]):
                Report.logPass(f"ANC button option {option_to_remove} successfully disabled.")
            else:
                Report.logFail(f"ANC button option {option_to_remove} is still enabled.")

            time.sleep(5)
            self._verify_anc_customization_over_api(product_string=device_name,
                                                    conn_type=conn_type,
                                                    mode=15 - anc_button_options[option_to_remove][0])
            if conn_type == 'bt':
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_anc_button_options()

            Report.logInfo(f"Step 3. Disable second option.")
            option_to_remove_2 = options.pop(random.randrange(len(options)))
            Report.logInfo(f"Disable: {option_to_remove_2}")
            self.tune_app.click_anc_button_option_toggle(anc_button_options[option_to_remove_2][3])
            time.sleep(2)
            if not self.tune_app.get_anc_button_option_state(anc_button_options[option_to_remove_2][2]):
                Report.logPass(f"ANC button option {option_to_remove_2} successfully disabled.")
            else:
                Report.logFail(f"ANC button option {option_to_remove_2} is still enabled.")

            time.sleep(5)
            self._verify_anc_customization_over_api(product_string=device_name,
                                                    conn_type=conn_type,
                                                    mode=15 - anc_button_options[option_to_remove][0]- anc_button_options[option_to_remove_2][0])
            if conn_type == 'bt':
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_anc_button_options()

            Report.logInfo(f"Step 4. Disable third option. It should not be possible")
            option_to_remove_3 = options.pop(random.randrange(len(options)))
            Report.logInfo(f"Disable: {option_to_remove_3}")
            self.tune_app.click_anc_button_option_toggle(anc_button_options[option_to_remove_3][3])
            time.sleep(2)
            if self.tune_app.get_anc_button_option_state(anc_button_options[option_to_remove_3][2]):
                Report.logPass(f"{option_to_remove_3} is still enabled. At least two button options need to be enabled.")
            else:
                Report.logFail(f"{option_to_remove_3} is disabled. At least two button options should be enabled.")

            time.sleep(5)
            self._verify_anc_customization_over_api(product_string=device_name,
                                                    conn_type=conn_type,
                                                    mode=15 - anc_button_options[option_to_remove][0] - anc_button_options[option_to_remove_2][0])

        except Exception as e:
            Report.logException(str(e))

    def _verify_anc_customization_over_api(self, product_string: str, conn_type: str, mode: int) -> None:
        """ Method to verify ANC customization state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            if conn_type == 'bt':
                comport = self._get_centrion_com_port(device_name=product_string)
                self.tune_app.close_tune_app()
                time.sleep(10)
                self.centurion = CenturionCommands(device_name=product_string,
                                                   conn_type=conn_type,
                                                   com_port=comport)
            else:
                self.centurion = CenturionCommands(device_name=product_string,
                                                   conn_type=conn_type)

            self.features = Features(self.centurion)
            response = self.features.headset_audio_feature.get_anc_customization_mode()
            self.features.headset_audio_feature.verify_get_anc_customization_mode(response, mode)
        except Exception:
            Report.logException("Verification over API failed")
        finally:
            if self.centurion:
                self.centurion.close_port()

    def tc_voice_prompts(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Voice Prompts state

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_voice_prompts_displayed()

            state = self.tune_app.get_voice_prompts_state()
            Report.logInfo(f"Voice prompts state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Voice prompts state to {not state}")
            self.tune_app.click_voice_prompts_toggle()
            new_state = self.tune_app.get_voice_prompts_state()
            Report.logInfo(f"Voice prompts state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Voice prompts changed correctly.", True)
            else:
                Report.logFail(f"Voice prompts NOT state changed correctly.")
            time.sleep(5)
            self._verify_voice_prompts(product_string=device_name,
                                       conn_type=conn_type,
                                       state=new_state)

            # Change state for 2nd time
            Report.logInfo(f"Voice prompts to {not new_state}")
            self.tune_app.click_voice_prompts_toggle()
            new_state_2 = self.tune_app.get_voice_prompts_state()
            Report.logInfo(f"Voice prompts is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Voice prompts changed correctly.", True)
            else:
                Report.logFail(f"Voice prompts NOT state changed correctly.")

            time.sleep(5)
            self._verify_voice_prompts(product_string=device_name,
                                       conn_type=conn_type,
                                       state=new_state_2)
        except Exception as e:
            Report.logException(str(e))

    def tc_voice_prompts_3_levels(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Voice Prompts names

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            levels = {"Off": 2,
                      "Voice": 1,
                      "Tones": 0}

            self.tune_app.verify_voice_prompts_3_levels_displayed()

            chosen_voice_prompt_levels = []
            time.sleep(2)
            initial_voice_prompt_level = self.tune_app.get_voice_prompts_level_name()
            chosen_voice_prompt_levels.append(initial_voice_prompt_level)
            Report.logInfo(f"Voice prompt level is: {initial_voice_prompt_level}")

            # Change state for 1st time
            self.tune_app.click_voice_prompts_level_name()
            new_voice_prompt_level = choice([i for i in levels.keys() if i not in chosen_voice_prompt_levels])
            chosen_voice_prompt_levels.append(new_voice_prompt_level)
            Report.logInfo(f"Change Voice prompts level to {new_voice_prompt_level}")

            self.tune_app.choose_new_voice_prompt_level(new_voice_prompt_level)
            time.sleep(2)
            updated_level = self.tune_app.get_voice_prompts_level_name()
            if updated_level == new_voice_prompt_level:
                Report.logPass(f"Voice prompts name updated correctly.", True)
            else:
                Report.logFail(f"Voice prompts name NOT updated correctly. Displayed name is: {updated_level}")

            time.sleep(5)
            self._verify_voice_prompts(product_string=device_name,
                                       conn_type=conn_type,
                                       state=levels[new_voice_prompt_level])

            # Reopen tune app after verification for BT SPP
            if conn_type =='bt':
                self.tune_app.connect_tune_app(device_name=device_name)
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)

            # Change state for 2nd time
            self.tune_app.click_voice_prompts_level_name()
            new_voice_prompt_level_2 = choice([i for i in levels.keys() if i not in chosen_voice_prompt_levels])
            Report.logInfo(f"Change Voice prompts level to {new_voice_prompt_level_2}")

            self.tune_app.choose_new_voice_prompt_level(new_voice_prompt_level_2)
            time.sleep(2)
            updated_level = self.tune_app.get_voice_prompts_level_name()
            if updated_level == new_voice_prompt_level_2:
                Report.logPass(f"Voice prompts name updated correctly.", True)
            else:
                Report.logFail(f"Voice prompts name NOT updated correctly. Displayed name is: {updated_level}")

            time.sleep(5)
            self._verify_voice_prompts(product_string=device_name,
                                       conn_type=conn_type,
                                       state=levels[new_voice_prompt_level_2])

            # Reopen tune app after verification for BT SPP
            if conn_type == 'bt':
                self.tune_app.connect_tune_app(device_name=device_name)
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)

            # Change state for 2nd time
            self.tune_app.click_voice_prompts_level_name()
            Report.logInfo(f"Change Voice prompts level to {initial_voice_prompt_level}")

            self.tune_app.choose_new_voice_prompt_level(initial_voice_prompt_level)
            time.sleep(2)
            updated_level = self.tune_app.get_voice_prompts_level_name()
            if updated_level == initial_voice_prompt_level:
                Report.logPass(f"Voice prompts name updated correctly.", True)
            else:
                Report.logFail(f"Voice prompts name NOT updated correctly. Displayed name is: {updated_level}")

            time.sleep(5)
            self._verify_voice_prompts(product_string=device_name,
                                       conn_type=conn_type,
                                       state=levels[initial_voice_prompt_level])

        except Exception as e:
            Report.logException(str(e))

    def tc_advanced_call_clarity(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Voice Prompts state

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)

            levels = {"Off": 0,
                      "Low": 1,
                      "High": 3}

            self.tune_app.verify_advanced_call_clarity_displayed()

            chosen_advanced_call_clarity_levels = []
            time.sleep(2)
            initial_advanced_call_clarity_level = self.tune_app.get_advanced_call_clarity_level_name()
            chosen_advanced_call_clarity_levels.append(initial_advanced_call_clarity_level)
            Report.logInfo(f"Advanced Call Clarity level is: {initial_advanced_call_clarity_level}")

            # Change state for 1st time
            self.tune_app.click_advance_call_clarity_level_name()
            new_advanced_call_clarity_level = choice([i for i in levels.keys() if i not in chosen_advanced_call_clarity_levels])
            chosen_advanced_call_clarity_levels.append(new_advanced_call_clarity_level)
            Report.logInfo(f"Change Advanced Call Clarity level to {new_advanced_call_clarity_level}")

            self.tune_app.choose_new_advanced_call_clarity_level(new_advanced_call_clarity_level)
            time.sleep(2)
            updated_level = self.tune_app.get_advanced_call_clarity_level_name()
            if updated_level == new_advanced_call_clarity_level:
                Report.logPass(f"Advanced Call Clarity level updated correctly.", True)
            else:
                Report.logFail(f"Advanced Call Clarity level NOT updated correctly. Displayed level is: {updated_level}")

            time.sleep(5)
            self._verify_advanced_call_clarity_level(product_string=device_name,
                                                     conn_type=conn_type,
                                                     state=levels[new_advanced_call_clarity_level])

            # Reopen tune app after verfied through bt_spp
            if conn_type == 'bt':
                time.sleep(5)
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)

            # Change state for 2nd time
            self.tune_app.click_advance_call_clarity_level_name()
            new_advanced_call_clarity_level_2 = choice([i for i in levels.keys() if i not in chosen_advanced_call_clarity_levels])
            Report.logInfo(f"Change Advanced Call Clarity level to {new_advanced_call_clarity_level_2}")

            self.tune_app.choose_new_advanced_call_clarity_level(new_advanced_call_clarity_level_2)
            time.sleep(2)
            updated_level = self.tune_app.get_advanced_call_clarity_level_name()
            if updated_level == new_advanced_call_clarity_level_2:
                Report.logPass(f"Advanced Call Clarity level updated correctly.", True)
            else:
                Report.logFail(f"Advanced Call Clarity level NOT updated correctly. Displayed level is: {updated_level}")

            time.sleep(5)
            self._verify_advanced_call_clarity_level(product_string=device_name,
                                                     conn_type=conn_type,
                                                     state=levels[new_advanced_call_clarity_level_2])

            # Reopen tune app after verfied through bt_spp
            if conn_type == 'bt':
                time.sleep(5)
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)

            # Change state for 2nd time
            self.tune_app.click_advance_call_clarity_level_name()
            Report.logInfo(f"Change Advanced Call Clarity level to {initial_advanced_call_clarity_level}")

            self.tune_app.choose_new_advanced_call_clarity_level(initial_advanced_call_clarity_level)
            time.sleep(2)
            updated_level = self.tune_app.get_advanced_call_clarity_level_name()
            if updated_level == initial_advanced_call_clarity_level:
                Report.logPass(f"Advanced Call Clarity level updated correctly.", True)
            else:
                Report.logFail(f"Advanced Call Clarity level NOT updated correctly. Displayed name is: {updated_level}")

            time.sleep(5)
            self._verify_advanced_call_clarity_level(product_string=device_name,
                                                     conn_type=conn_type,
                                                     state=levels[initial_advanced_call_clarity_level])

        except Exception as e:
            Report.logException(str(e))

    def _verify_advanced_call_clarity_level(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Enable Voice Notifications state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Advanced Call Clarity level
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            time.sleep(10)
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.ai_noise_reduction.get_ai_noise_reduction_state()
        self.features.ai_noise_reduction.verify_get_ai_noise_reduction_state(
            response, state)
        self.centurion.close_port()



    def _verify_voice_prompts(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Enable Voice Notifications state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Voice Notifications state
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            time.sleep(10)
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.headset_misc_feature.get_voice_notification_status()
        self.features.headset_misc_feature.verify_get_voice_notification_status(
            response, state)
        self.centurion.close_port()

    def tc_health_and_safety_anti_startle(self, device_name: str, conn_type: str, is_dashboard_feature: bool = False) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            if device_name in ["Zone 950", "Zone Wireless 2"]:
                self.tune_app.verify_health_and_safety_displayed()
                self.tune_app.click_health_and_safety_label()
                time.sleep(10)

            anti_startle_state = self.tune_app.get_anti_startle_protection_state(is_dashboard_feature)
            Report.logInfo(f"Anti startle protection state is: {anti_startle_state}")

            # Change Anti Startle state for 1st time
            Report.logInfo(f"Change Anti startle protection state to {not anti_startle_state}")
            self.tune_app.click_anti_startle_protection_toggle(is_dashboard_feature)
            new_anti_startle_state = self.tune_app.get_anti_startle_protection_state(is_dashboard_feature)
            Report.logInfo(f"Anti startle protection state is: {new_anti_startle_state}")
            if new_anti_startle_state != anti_startle_state:
                Report.logPass(f"Anti startle protection state changed correctly.", True)
            else:
                Report.logFail(f"Anti startle protection state NOT changed correctly.")

            time.sleep(5)
            self._verify_anti_startle_protection(product_string=device_name,
                                                 conn_type=conn_type,
                                                 state=not anti_startle_state)

            # Reopen tune app after verifying through bt_spp
            if conn_type == 'bt':
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_health_and_safety_label()

            # Change Anti Startle state for 1st time
            Report.logInfo(f"Change Anti startle protection state to {anti_startle_state}")
            self.tune_app.click_anti_startle_protection_toggle(is_dashboard_feature)
            new_anti_startle_state_2 = self.tune_app.get_anti_startle_protection_state(is_dashboard_feature)
            Report.logInfo(f"Anti startle protection state is: {new_anti_startle_state_2}")
            if new_anti_startle_state_2 == anti_startle_state:
                Report.logPass(f"Anti startle protection state changed correctly.", True)
            else:
                Report.logFail(f"Anti startle protection state NOT changed correctly.")

            time.sleep(5)
            self._verify_anti_startle_protection(product_string=device_name,
                                                 conn_type=conn_type,
                                                 state=anti_startle_state)


        except Exception as e:
            Report.logException(str(e))

    def _verify_anti_startle_protection(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Anti Startle Protection state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Anti Startle Protection state
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            time.sleep(10)
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.anti_startle.get_anti_startle()
        self.features.anti_startle.verify_get_anti_startle(
            response, state)
        self.centurion.close_port()

    def tc_health_and_safety_noise_exposure(self, device_name: str, conn_type: str) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.verify_health_and_safety_displayed()
            self.tune_app.click_health_and_safety_label()
            time.sleep(10)

            noise_exposure_control_state = self.tune_app.get_noise_exposure_control_state()
            Report.logInfo(f"Noise Exposure Control state is: {noise_exposure_control_state}")

            # Change Noise Exposure Control state for 1st time
            Report.logInfo(f"Change Noise Exposure Control state to {not noise_exposure_control_state}")
            self.tune_app.click_noise_exposure_control_toggle()
            new_noise_exposure_control_state = self.tune_app.get_noise_exposure_control_state()
            Report.logInfo(f"Noise Exposure Control state is: {new_noise_exposure_control_state}")
            if new_noise_exposure_control_state != noise_exposure_control_state:
                Report.logPass(f"Noise Exposure Control state changed correctly.", True)
            else:
                Report.logFail(f"Noise Exposure Control state NOT changed correctly.")

            time.sleep(5)
            self._verify_noise_exposure_control(product_string=device_name,
                                                conn_type=conn_type,
                                                state=not noise_exposure_control_state)

            # Reopen tune app after verifying through bt_spp
            if conn_type == 'bt':
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_health_and_safety_label()

            # Change Noise Exposure Control state for 1st time
            Report.logInfo(f"Change Noise Exposure Control state to {noise_exposure_control_state}")
            self.tune_app.click_noise_exposure_control_toggle()
            new_noise_exposure_control_state_2 = self.tune_app.get_noise_exposure_control_state()
            Report.logInfo(f"Noise Exposure Control state is: {new_noise_exposure_control_state_2}")
            if new_noise_exposure_control_state_2 == noise_exposure_control_state:
                Report.logPass(f"Noise Exposure Control state changed correctly.", True)
            else:
                Report.logFail(f"Noise Exposure Control state NOT changed correctly.")

            time.sleep(5)
            self._verify_noise_exposure_control(product_string=device_name,
                                                conn_type=conn_type,
                                                state=noise_exposure_control_state)
        except Exception as e:
            Report.logException(str(e))

    def _verify_noise_exposure_control(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Anti Startle Protection state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Anti Startle Protection state
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            time.sleep(10)
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.noise_exposure.get_noise_exposure_state()
        self.features.noise_exposure.verify_get_noise_exposure_state(
            response, state)
        self.centurion.close_port()

    def tc_on_head_detection_auto_mute(self, device_name: str, conn_type: str) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.verify_on_head_detection_displayed()
            self.tune_app.click_on_head_detection()
            time.sleep(12)

            self.tune_app.verify_auto_mute_displayed()
            auto_mute_state = self.tune_app.get_auto_mute_state()
            Report.logInfo(f"Auto Mute state is: {auto_mute_state}")

            # Change Auto Mute state for 1st time
            Report.logInfo(f"Change Auto Mute state to {not auto_mute_state}")
            self.tune_app.click_auto_mute_toggle()
            time.sleep(1)
            new_auto_mute_state = self.tune_app.get_auto_mute_state()
            Report.logInfo(f"Auto Mute state is: {new_auto_mute_state}")
            if new_auto_mute_state != auto_mute_state:
                Report.logPass(f"Auto Mute state changed correctly.", True)
            else:
                Report.logFail(f"Auto Mute state NOT changed correctly.")

            time.sleep(7)
            self._verify_auto_mute(product_string=device_name,
                                   conn_type=conn_type,
                                   state=not auto_mute_state)

            # Reopen tune app after verifying through bt_spp
            if conn_type == 'bt':
                time.sleep(5)
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_on_head_detection()

            # Change Auto Mute state for 1st time
            Report.logInfo(f"Change Auto Mute state to {auto_mute_state}")
            self.tune_app.click_auto_mute_toggle()
            time.sleep(1)
            new_auto_mute_state_2 = self.tune_app.get_auto_mute_state()
            Report.logInfo(f"Auto Mute state is: {new_auto_mute_state_2}")
            if new_auto_mute_state_2 == auto_mute_state:
                Report.logPass(f"Auto Mute state changed correctly.", True)
            else:
                Report.logFail(f"Auto Mute state NOT changed correctly.")

            time.sleep(7)
            self._verify_auto_mute(product_string=device_name,
                                   conn_type=conn_type,
                                   state=auto_mute_state)
        except Exception as e:
            Report.logException(str(e))

    def _verify_auto_mute(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Anti Startle Protection state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Auto Mute state
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            time.sleep(10)
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.auto_mute_on_call.get_auto_mute_on_call()
        self.features.auto_mute_on_call.verify_get_auto_mute_on_call(
            response, state)
        self.centurion.close_port()

    def tc_on_head_detection_auto_answer(self, device_name: str, conn_type: str) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.verify_on_head_detection_displayed()
            self.tune_app.click_on_head_detection()
            time.sleep(12)

            self.tune_app.verify_auto_answer_displayed()
            auto_answer_state = self.tune_app.get_auto_answer_state()
            Report.logInfo(f"Auto Answer state is: {auto_answer_state}")

            # Change Auto Answer state for 1st time
            Report.logInfo(f"Change Answer Mute state to {not auto_answer_state}")
            self.tune_app.click_auto_answer_toggle()
            time.sleep(1)
            new_auto_answer_state = self.tune_app.get_auto_answer_state()
            Report.logInfo(f"Auto Answer state is: {new_auto_answer_state}")
            if new_auto_answer_state != auto_answer_state:
                Report.logPass(f"Auto Answer state changed correctly.", True)
            else:
                Report.logFail(f"Auto Answer state NOT changed correctly.")

            time.sleep(7)
            self._verify_auto_answer(product_string=device_name,
                                     conn_type=conn_type,
                                     state=not auto_answer_state)

            # Reopen tune app after verifying through bt_spp
            if conn_type == 'bt':
                time.sleep(5)
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_on_head_detection()

            # Change Auto Answer state for 1st time
            Report.logInfo(f"Change Answer Mute state to {auto_answer_state}")
            self.tune_app.click_auto_answer_toggle()
            time.sleep(1)
            new_auto_answer_state_2 = self.tune_app.get_auto_answer_state()
            Report.logInfo(f"Auto Answer state is: {new_auto_answer_state_2}")
            if new_auto_answer_state_2 == auto_answer_state:
                Report.logPass(f"Auto Answer state changed correctly.", True)
            else:
                Report.logFail(f"Auto Answer state NOT changed correctly.")

            time.sleep(7)
            self._verify_auto_answer(product_string=device_name,
                                     conn_type=conn_type,
                                     state=auto_answer_state)
        except Exception as e:
            Report.logException(str(e))

    def _verify_auto_answer(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Anti Startle Protection state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Auto Answer state
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.auto_call_answer.get_auto_answer_on_call()
        self.features.auto_call_answer.verify_get_auto_answer_on_call(
            response, state)
        self.centurion.close_port()

    def tc_on_head_detection_auto_pause(self, device_name: str, conn_type: str) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.verify_on_head_detection_displayed()
            self.tune_app.click_on_head_detection()
            time.sleep(12)

            self.tune_app.verify_auto_pause_displayed()
            auto_pause_state = self.tune_app.get_auto_pause_state()
            Report.logInfo(f"Auto Pause state is: {auto_pause_state}")

            # Change Auto Pause state for 1st time
            Report.logInfo(f"Change Auto Pause state to {not auto_pause_state}")
            self.tune_app.click_auto_pause_toggle()
            time.sleep(1)
            new_auto_pause_state = self.tune_app.get_auto_pause_state()
            Report.logInfo(f"Auto Pause state is: {new_auto_pause_state}")
            if new_auto_pause_state != auto_pause_state:
                Report.logPass(f"Auto Pause state changed correctly.", True)
            else:
                Report.logFail(f"Auto Pause state NOT changed correctly.")

            time.sleep(5)
            self._verify_auto_pause(product_string=device_name,
                                    conn_type=conn_type,
                                    state=not auto_pause_state)
            # Reopen tune app after verifying through bt_spp
            if conn_type == 'bt':
                time.sleep(5)
                self.tune_app.connect_tune_app()
                self.tune_app.click_my_devices()
                self.tune_app.click_device(device_name=device_name)
                self.tune_app.click_on_head_detection()

            # Change Auto Pause state for 1st time
            Report.logInfo(f"Change Auto Pause state to {auto_pause_state}")
            self.tune_app.click_auto_pause_toggle()
            time.sleep(1)
            new_auto_pause_state_2 = self.tune_app.get_auto_pause_state()
            Report.logInfo(f"Auto Pause state is: {new_auto_pause_state_2}")
            if new_auto_pause_state_2 == auto_pause_state:
                Report.logPass(f"Auto Pause state changed correctly.", True)
            else:
                Report.logFail(f"Auto Pause state NOT changed correctly.")

            time.sleep(5)
            self._verify_auto_pause(product_string=device_name,
                                    conn_type=conn_type,
                                    state=auto_pause_state)
        except Exception as e:
            Report.logException(str(e))

    def _verify_auto_pause(self, product_string: str, conn_type: str, state: int) -> None:
        """Method to verify Anti Startle Protection state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Auto Pause state
        @return: None
        """
        if conn_type == 'bt':
            comport = self._get_centrion_com_port(device_name=product_string)
            self.tune_app.close_tune_app()
            time.sleep(10)
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=comport)
        else:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
        self.features = Features(self.centurion)

        response = self.features.tw_in_ear_detection_feature.get_ear_detection_state()
        self.features.tw_in_ear_detection_feature.verify_get_ear_detection_state(
            response, state)
        self.centurion.close_port()

    def tc_device_name(self, device_name: str, conn_type: str, name_max_len: int) -> None:
        """ Method to change Device Name and verify it

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_device_name_label_displayed()

            Report.logInfo("1. Change device name with 'Surprise Me' and verify it.")
            initial_device_name = self.tune_app.get_device_name_from_settings_page()

            # Change Device Name with Surprise Me
            self.tune_app.click_device_name_rename()
            self.tune_app.click_device_name_surprise_me()

            time.sleep(1)
            new_name_surprise = self.tune_app.get_value_from_device_name_input()
            self.tune_app.click_device_name_update()

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)
            else:
                time.sleep(5)
            if self.tune_app.get_device_name_from_settings_page() == new_name_surprise:
                Report.logPass(f"New device name displayed correctly on Settings page.", True)
            else:
                Report.logFail(f"New device name not displayed correctly on Settings page.")

            time.sleep(5)
            if device_name != 'Litra Beam':
                self._verify_device_name(product_string=device_name,
                                         conn_type=conn_type,
                                         device_name=new_name_surprise, name_max_len=name_max_len)

            Report.logInfo("2. Verify empty device name.")
            self.tune_app.click_device_name_rename()
            self.tune_app.clear_device_name()

            if self.tune_app.get_device_name_error() == "The field cannot be left empty.":
                Report.logPass(f"Correct error name displayed.", True)
            else:
                Report.logFail(f"Incorrect error name displayed.")

            if not self.tune_app.get_update_button_state_on_device_name_popup():
                Report.logPass(f"Correct state of Update button.", True)
            else:
                Report.logFail(f"Incorrect state of Update button.")

            Report.logInfo("3. Verify max device name")
            chars = string.ascii_uppercase + string.digits
            new_name = f"{device_name} {''.join(random.choice(chars) for _ in range(40))}"
            self.tune_app.set_new_device_name(new_name)

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)
            else:
                time.sleep(5)
            if self.tune_app.get_device_name_from_settings_page() == new_name[:name_max_len]:
                Report.logPass(f"New device name displayed correctly on Settings page.", True)
            else:
                Report.logFail(f"New device name not displayed correctly on Settings page.")

            if device_name != 'Litra Beam':
                time.sleep(5)
                self._verify_device_name(product_string=device_name,
                                         conn_type=conn_type,
                                         device_name=new_name[:name_max_len],
                                         name_max_len=name_max_len)

        except Exception as e:
            Report.logException(str(e))

    def _verify_device_name(self, product_string: str, conn_type: str, device_name: str, name_max_len: int) -> None:
        """Method to verify Enable Voice Notifications state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param device_name: device name to verify
        @return: None
        """
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.device_name_feature.get_device_name()
        self.features.device_name_feature.verify_name(response, device_name, name_max_len)
        self.centurion.close_port()

    def tc_sleep_settings(self, device_name: str, conn_type: str) -> None:
        """ Method to change Sleep timeout and verify it

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_sleep_settings_label_displayed()

            current_sleep_timeout = self.tune_app.get_current_sleep_settings_timeout()

            self.tune_app.click_current_sleep_settings_timeout()

            new_value = choice([i for i in [0, 5, 10, 15, 30, 60, 120, 240] if i not in [current_sleep_timeout]])

            self.tune_app.choose_new_sleep_timeout(new_value)
            if device_name in ["Zone Wireless 2", "Zone 950"]:
                time.sleep(10)

            value = self.tune_app.get_current_sleep_settings_timeout()

            if value == new_value:
                Report.logPass(f"New sleep timeout displayed correctly on Settings page.", True)
            else:
                Report.logFail(f"New sleep timeout not displayed correctly on Settings page: {value} != {new_value}")

            time.sleep(5)
            self._verify_sleep_timer(product_string=device_name,
                                     conn_type=conn_type,
                                     sleep_timer=new_value)

        except Exception as e:
            Report.logException(str(e))

        finally:
            self.set_never_sleep_timer(device_name, conn_type)

    def _verify_sleep_timer(self, product_string: str, conn_type: str, sleep_timer: int) -> None:
        """Method to verify Sleep timeout state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param sleep_timer: sleep timeout
        @return: None
        """

        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.auto_sleep_feature.get_sleep_timer()
        self.features.auto_sleep_feature.verify_sleep_timer(response, sleep_timer)
        self.centurion.close_port()

    def set_never_sleep_timer(self, product_string: str, conn_type: str) -> None:
        """ Method to set Sleep Timeout equal to Never (0).

        @return: None
        """
        try:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
            self.features = Features(self.centurion)
            self.features.auto_sleep_feature.set_never_sleep_timer()
        except Exception as e:
            Report.logException("Setting sleep timer to never failed")
        finally:
            self.centurion.close_port()

    def set_device_name_over_api(self, product_string: str, conn_type: str) -> None:
        """ Method to set Device name over Centurion++ API.

        @return: None
        """
        try:
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type)
            self.features = Features(self.centurion)
            self.features.device_name_feature.set_device_name(name=product_string)
        except Exception:
            Report.logException("Verification over API failed")
        finally:
            if self.centurion:
                self.centurion.close_port()

    def tc_button_functions(self, device_name: str, conn_type: str, button_actions: Dict) -> None:
        """ Method to change Button functions and verify it

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_button_functions_label_displayed()

            self.tune_app.click_button_functions_label()

            Report.logInfo("1. Change each button function and verify it.")
            initial_single_press_function = self.tune_app.get_current_button_single_press_function()
            initial_double_press_function = self.tune_app.get_current_button_double_press_function()
            initial_long_press_function = self.tune_app.get_current_button_long_press_function()

            time.sleep(1)
            self.tune_app.click_single_press_label()
            new_single_press_function = choice(
                [i for i in button_actions["single_press"]["functions"] if i not in [initial_single_press_function]])
            self.tune_app.choose_new_button_function(new_single_press_function)

            time.sleep(1)
            self.tune_app.click_double_press_label()
            new_double_press_function = choice(
                [i for i in button_actions["double_press"]["functions"] if i not in [initial_double_press_function]])
            self.tune_app.choose_new_button_function(new_double_press_function)

            time.sleep(1)
            self.tune_app.click_long_press_label()
            new_long_press_function = choice(
                [i for i in button_actions["long_press"]["functions"] if i not in [initial_long_press_function]])
            self.tune_app.choose_new_button_function(new_long_press_function)

            time.sleep(1)
            updated_single_press_function = self.tune_app.get_current_button_single_press_function()
            updated_double_press_function = self.tune_app.get_current_button_double_press_function()
            updated_long_press_function = self.tune_app.get_current_button_long_press_function()

            if updated_single_press_function == new_single_press_function:
                Report.logPass(f"Single Press function updated")
            else:
                Report.logFail(f"Single Press function not updated: {updated_single_press_function} != {new_single_press_function}")
            if updated_double_press_function == new_double_press_function:
                Report.logPass(f"Double Press function updated")
            else:
                Report.logFail(f"Double Press function not updated: {updated_double_press_function} != {new_double_press_function}")
            if updated_long_press_function == new_long_press_function:
                Report.logPass(f"Long Press function updated", True)
            else:
                Report.logFail(f"Long Press function not updated: {updated_long_press_function} != {new_long_press_function}")

            time.sleep(1)
            functions_indexes = [ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[updated_long_press_function],
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[updated_single_press_function],
                                 0,
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[updated_double_press_function]]
            self._verify_button_functions_via_api(product_string=device_name,
                                                  conn_type=conn_type,
                                                  function_indexes=functions_indexes)

            time.sleep(1)
            Report.logInfo("2. Press Restore defaults and verify it.")
            self.tune_app.click_restore_defaults_button()
            time.sleep(1)

            restored_single_press_function = self.tune_app.get_current_button_single_press_function()
            restored_double_press_function = self.tune_app.get_current_button_double_press_function()
            restored_long_press_function = self.tune_app.get_current_button_long_press_function()

            if restored_single_press_function == button_actions["single_press"]["default"]:
                Report.logPass(f"Single Press function restored to correct default value.")
            else:
                Report.logFail(f"Single Press function not restored to correct default value: {restored_single_press_function} != {button_actions['single_press']['default']}")
            if restored_double_press_function == button_actions["double_press"]["default"]:
                Report.logPass(f"Double Press function restored to correct default value.")
            else:
                Report.logFail(f"Double Press function not restored to correct default value: {restored_double_press_function} != {button_actions['double_press']['default']}")
            if restored_long_press_function == button_actions["long_press"]["default"]:
                Report.logPass(f"Long Press function restored to correct default value.", True)
            else:
                Report.logFail(f"Long Press function not restored to correct default value: {restored_long_press_function} != {button_actions['double_press']['default']}")

            time.sleep(1)
            functions_indexes = [ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[button_actions["long_press"]["default"]],
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[button_actions["single_press"]["default"]],
                                 0,
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[button_actions["double_press"]["default"]]]
            self._verify_button_functions_via_api(product_string=device_name,
                                                  conn_type=conn_type,
                                                  function_indexes=functions_indexes)

        except Exception as e:
            Report.logException(str(e))

    def _verify_button_functions_via_api(self, product_string: str, conn_type: str, function_indexes: List[int]) -> None:
        """ Method to verify over API the button functions.

        @param conn_type: type of connection, i.e. BT, DONGLE
        @param function_indexes: function indexes due to centurion++ protocol
        @return: None
        """
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.headset_misc_feature.get_button_general_settings()
        self.features.headset_misc_feature.verify_get_button_general_settings(response=response,
                                                                              button_index=0,
                                                                              long_press=function_indexes[0],
                                                                              short_press=function_indexes[1],
                                                                              tripple_press=function_indexes[2],
                                                                              double_press=function_indexes[3])
        self.centurion.close_port()

    def tc_connection_priority(self, device_name: str) -> None:
        try:

            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_connection_priority_label_displayed()
            current_value = self.tune_app.get_current_connection_priority()
            self.tune_app.click_current_connection_priority()
            self.tune_app.choose_new_connection_priority(current_value=current_value)
            new_value = self.tune_app.get_current_connection_priority()
            if new_value != current_value:
                Report.logPass("Connection priority value updated successfully", True)
            else:
                Report.logFail(f"Connection priority value NOT updated successfully")

            self.tune_app.click_current_connection_priority()
            self.tune_app.choose_new_connection_priority(current_value=new_value)
            new_value_2 = self.tune_app.get_current_connection_priority()
            if new_value_2 != new_value:
                Report.logPass("Connection priority value updated successfully", True)
            else:
                Report.logFail(f"Connection priority value NOT updated successfully")

        except Exception as e:
            Report.logException(str(e))

    def tc_connected_devices(self, device_name: str, conn_type: str, receiver_name: str) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.click_connected_devices()

            current_name = self.tune_app.get_currently_connected_device()

            if receiver_name in current_name:
                Report.logPass(f"Correctly displayed connected device name", True)
            else:
                Report.logFail(f"Incorrectly displayed connected device name")

            self.tune_app.click_on_close_connected_device_page()

            # TODO API returns Zone Wireless Plus Dongle instead of Zone Wireless Plus Receiver, to investigate
            # self._verify_connected_device_name(product_string=device_name,
            #                                    conn_type=conn_type,
            #                                    receiver_name=receiver_name)

        except Exception as e:
            Report.logException(str(e))

    def _verify_connected_device_name(self, product_string: str, conn_type: str, receiver_name: str) -> None:
        """Method to verify Connected device name on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """

        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type)
        self.features = Features(self.centurion)
        response_info = self.features.headset_bt_conn_info_feature.get_connected_device_info(1)
        bt_address = self.features.headset_bt_conn_info_feature.get_bt_address_from_get_connected_device_info_response(response_info)

        response_name = self.features.headset_bt_conn_info_feature.get_device_connected_name(bt_address=bt_address)
        self.features.headset_bt_conn_info_feature.verify_get_device_connected_name(response_name, response_name)

        self.centurion.close_port()

    def tc_about_headset(self, device_name: str) -> None:
        """ Method to check elements on the Bout the headset page

        @param device_name:
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.open_about_the_device()
            time.sleep(1)
            if self.tune_app.verify_device_name_displayed(device_name=device_name):
                Report.logPass(f"{device_name} - displayed in About")
            else:
                Report.logFail(f"{device_name} - not displayed in About")
            if self.tune_app.verify_more_details_displayed():
                Report.logPass("More details link displayed in About")
            else:
                Report.logFail("More details link not displayed in About")
            if self.tune_app.verify_factory_reset_displayed() and (device_name is not DeviceName.zone_true_wireless):
                Report.logPass("Factory reset button displayed in About", True)
            elif device_name is DeviceName.zone_true_wireless:
                if not self.tune_app.verify_factory_reset_displayed():
                    Report.logPass("Zone True Wireless does not have factory reset button")
                else:
                    Report.logFail("Zone True Wireless has factory reset button")
            else:
                Report.logFail("Factory reset button not displayed in About")
        except Exception as e:
            Report.logException(str(e))

    def tc_headset_diagnostics(self, device_name: str) -> None:
        # TODO: currently this is without real input and output, just UI validation
        """ Method to validate headset diagnostics

        @param device_name:
        @return: None
        """
        try:

            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            if self.tune_app.verify_headset_diagnostics_displayed():
                Report.logPass("Headset diagnostics displayed", True)
            else:
                Report.logFail("Headset diagnostics not displayed")

            self.tune_app.click_headset_diagnostics()
            if self.verify_element(TunesAppLocators.HEADSET_DIAGNOSTICS_START_TESTING_BTN, timeunit=10):
                Report.logInfo("Start Test button displayed")
                self.look_element(TunesAppLocators.HEADSET_DIAGNOSTICS_START_TESTING_BTN).click()
            time.sleep(3)
            self.tune_app.verify_ringtone_diagnostics_displayed()
            self.tune_app.click_if_ringtone_hearable()
            time.sleep(3)
            self.tune_app.click_headset_diagnostics_record_button()
            time.sleep(10)
            self.tune_app.click_if_record_hearable()
            self.tune_app.verify_headset_diagnostics_result()
            self.tune_app.click_headset_diagnostics_close_button()

        except Exception as e:
            Report.logException(str(e))

    def tc_factory_reset_wired_headset(self, device_name: str) -> None:
        """ Method to check params state after factory reset

        @param device_name: device name
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            # Sidetone
            self.tune_app.click_sidetone()
            value = self.tune_app.get_sidetone_slider_value()
            new_value = choice([i for i in range(0, 10) if i not in [value / 10]])

            self.tune_app.set_sidetone_slider(new_value * 10)

            # Rotate to Mute
            if device_name not in [DeviceName.zone_wired_earbuds,
                                   DeviceName.bomberman_mono,
                                   DeviceName.bomberman_stereo]:
                self.tune_app.click_rotate_to_mute_toggle()

            # Enable voice prompts
            self.tune_app.click_voice_prompts_toggle()


            #Anti-Startle
            if device_name in [DeviceName.bomberman_mono, DeviceName.bomberman_stereo]:
                self.tune_app.click_anti_startle_protection_toggle(is_dashboard_feature=True)

            # Factory reset
            self.tune_app.click_info_button()
            self.tune_app.click_factory_reset()
            self.tune_app.click_proceed_to_factory_reset()
            if self.tune_app.verify_reconnect_device():
                Report.logPass("Reconnect Device to complete the process message displayed", True)
            else:
                Report.logFail("Reconnect Device to complete the process message not displayed")
            disconnect_device(device_name=device_name)
            time.sleep(1)
            connect_device(device_name=device_name)
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            # Check sidetone
            if device_name == DeviceName.zone_wired_earbuds:
                default_sidetone = '50'
            else:
                default_sidetone = '70'

            if self.tune_app.verify_sidetone_value(default_sidetone):
                Report.logPass("Sidetone reset to default value 50%", True)
            else:
                Report.logFail("Sidetone value did not reset")

            # Check Rotate to Mute
            if device_name not in [DeviceName.zone_wired_earbuds,
                                   DeviceName.bomberman_mono,
                                   DeviceName.bomberman_stereo]:
                if self.tune_app.get_rotate_to_mute_state():
                    Report.logPass("Rotate to mute value reset to default value True", True)
                else:
                    Report.logFail("Rotate to mute value did not reset")

            #Check Enable Voice prompts
            if self.tune_app.get_voice_prompts_state():
                Report.logPass("Enable Voice Prompts value reset to default value True", True)
            else:
                Report.logFail("Enable Voice Prompts value did not reset")

            if device_name in [DeviceName.bomberman_mono, DeviceName.bomberman_stereo]:
                if not self.tune_app.get_anti_startle_protection_state(is_dashboard_feature=True):
                    Report.logPass("Anti-Startle protection value reset to default value False", True)
                else:
                    Report.logFail("Anti-Startle protection value did not reset")
        except Exception as e:
            Report.logException(str(e))

    def tc_factory_reset_wireless_headset(self, device_name: str) -> None:
        """ Method to check params state after factory reset of the wireless headset.
        The feature applies only to Cybermorph headsets.

        @param device_name: device name
        @return: None
        """
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            anc_buttons = {"anc-off": (0, TunesAppLocators.ANC_DISABLED),
                           "anc-high": (1, TunesAppLocators.ANC_HIGH),
                           "anc-transparency": (2, TunesAppLocators.ANC_AMBIENCE_TRANSPARENCY),
                           "anc-low": (3, TunesAppLocators.ANC_LOW),
                           }

            anc_button_value = random.choice(list(anc_buttons.keys()))
            Report.logInfo(f"Change ANC state to: {anc_button_value}.")
            self.tune_app.click_anc_button(anc_buttons[anc_button_value][1])

            # Sidetone
            self.tune_app.click_sidetone()
            value = self.tune_app.get_sidetone_slider_value()
            new_value = choice([i for i in range(0, 10) if i not in [value / 10]])

            self.tune_app.set_sidetone_slider(new_value * 10)

            # Advance Call Clarity
            advance_call_clarity_levels = {"Off": 0, "Low": 1, "High": 2}
            self.tune_app.click_advance_call_clarity_level_name()
            new_advanced_call_clarity_level = choice([i for i in advance_call_clarity_levels.keys() if i not in ["Off"]])
            Report.logInfo(f"Change Advanced Call Clarity level to {new_advanced_call_clarity_level}")
            self.tune_app.choose_new_advanced_call_clarity_level(new_advanced_call_clarity_level)

            # Equalizer
            eq_profiles = ZONE_WIRELESS_2_PROFILES_UI
            new_equalizer_profile = choice([i for i in eq_profiles.keys()])
            self.tune_app.click_equalizer()
            self.tune_app.set_equalizer_profile(profile_name=new_equalizer_profile)

            # Health and Safety: Anti Startle
            self.tune_app.click_health_and_safety_label()
            time.sleep(10)

            anti_startle_state = self.tune_app.get_anti_startle_protection_state()
            Report.logInfo(f"Anti startle protection state is: {anti_startle_state}")
            if not anti_startle_state:
                Report.logInfo(f"Change Anti startle protection state to {not anti_startle_state}")
                self.tune_app.click_anti_startle_protection_toggle()

            # Health and Safety: Noise Exposure Control
            noise_exposure_control_state = self.tune_app.get_noise_exposure_control_state()
            Report.logInfo(f"Noise Exposure Control state is: {noise_exposure_control_state}")
            if not noise_exposure_control_state:
                self.tune_app.click_noise_exposure_control_toggle()

            if self.tune_app.verify_back_button_cybermorph():
                self.tune_app.click_back_button_cybermorph()

            # Device Name
            Report.logInfo("2. Verify empty device name.")
            self.tune_app.click_device_name_rename()
            self.tune_app.clear_device_name()

            chars = string.ascii_uppercase + string.digits
            new_name = f"{device_name} {''.join(random.choice(chars) for _ in range(40))}"
            new_name = new_name[:31]
            self.tune_app.set_new_device_name(new_name)

            # Sleep timer
            current_sleep_timeout = self.tune_app.get_current_sleep_settings_timeout()
            self.tune_app.click_current_sleep_settings_timeout()
            new_value = choice([i for i in [0, 5, 10, 15, 30, 60, 120, 240] if i not in [current_sleep_timeout]])
            self.tune_app.choose_new_sleep_timeout(new_value)

            # Rotate to Mute
            rotate_to_mute = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {rotate_to_mute}")
            if not rotate_to_mute:
                Report.logInfo(f"Change Rotate to mute state to: {not rotate_to_mute}")
                self.tune_app.click_rotate_to_mute_toggle()

            # ANC button options
            self.tune_app.click_anc_button_options()

            anc_button_options = {"anc-off": (1,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_LABEL,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_CHECKBOX,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_TOGGLE,
                                              False),
                                  "anc-high": (2,
                                               TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_LABEL,
                                               TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_CHECKBOX,
                                               TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_TOGGLE,
                                               True),
                                  "anc-transparency": (4,
                                                       TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_LABEL,
                                                       TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_CHECKBOX,
                                                       TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_TOGGLE,
                                                       True),
                                  "anc-low": (8,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_LABEL,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_CHECKBOX,
                                              TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_TOGGLE,
                                              False),
                                  }

            Report.logInfo(f"Enable all options.")
            options = []
            for key, value in anc_button_options.items():
                options.append(key)
                Report.logInfo(f"Verify label is displayed for: {key}.")
                self.tune_app.verify_anc_button_option_label_displayed(value[1])
                if not self.tune_app.get_anc_button_option_state(value[2]):
                    Report.logInfo(f"{key} is Disabled. Click toggle to Enable it.")
                    self.tune_app.click_anc_button_option_toggle(value[3])
                    time.sleep(1)

            if self.tune_app.verify_back_button_cybermorph():
                self.tune_app.click_back_button_cybermorph()

            # On head detection: Auto Mute
            self.tune_app.click_on_head_detection()
            time.sleep(10)

            auto_mute_state = self.tune_app.get_auto_mute_state()
            Report.logInfo(f"Auto Mute state is: {auto_mute_state}")
            if auto_mute_state:
                Report.logInfo(f"Change Auto Mute state is: {not auto_mute_state}")
                self.tune_app.click_auto_mute_toggle()

            # On head detection: Auto Answer
            auto_answer_state = self.tune_app.get_auto_answer_state()
            Report.logInfo(f"Auto Answer state is: {auto_answer_state}")
            if not auto_mute_state:
                Report.logInfo(f"Change Answer Mute state to {not auto_answer_state}")
                self.tune_app.click_auto_answer_toggle()

            # On head detection: Auto Pause
            auto_pause_state = self.tune_app.get_auto_pause_state()
            Report.logInfo(f"Auto Pause state is: {auto_pause_state}")
            if not auto_mute_state:
                Report.logInfo(f"Change Auto Pause state to {not auto_pause_state}")
                self.tune_app.click_auto_pause_toggle()

            if self.tune_app.verify_back_button_cybermorph():
                self.tune_app.click_back_button_cybermorph()

            # Voice prompts
            voice_prompts_levels = {"Off": 2, "Voice": 1, "Tones": 0}

            initial_voice_prompt_level = self.tune_app.get_voice_prompts_level_name()
            Report.logInfo(f"Voice prompt level is: {initial_voice_prompt_level}")

            self.tune_app.click_voice_prompts_level_name()
            new_voice_prompt_level = choice([i for i in voice_prompts_levels.keys() if i not in initial_voice_prompt_level])
            Report.logInfo(f"Change Voice prompts level to {new_voice_prompt_level}")
            self.tune_app.choose_new_voice_prompt_level(new_voice_prompt_level)
            time.sleep(2)

            # Factory reset
            self.tune_app.open_about_the_device()
            self.tune_app.click_factory_reset()
            self.tune_app.click_proceed_to_factory_reset()

            time.sleep(10)

            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            time.sleep(10)

            # Check ANC
            default_anc = 'anc-high'
            is_anc_highlighted = self.tune_app.verify_anc_button_active(anc_buttons[default_anc][1])
            if is_anc_highlighted:
                Report.logPass(f"ANC reset to default value: {default_anc}", True)
            else:
                Report.logFail("ANC NOT reset to default value.")

            # Check sidetone
            default_sidetone = '50'
            if self.tune_app.verify_sidetone_value(default_sidetone):
                Report.logPass("Sidetone reset to default value 50%", True)
            else:
                Report.logFail("Sidetone value did not reset")

            # Check Advanced Call Clarity
            default_advanced_call_clarity = "Off"
            updated_advanced_call_clarity_level = self.tune_app.get_advanced_call_clarity_level_name()
            if updated_advanced_call_clarity_level == default_advanced_call_clarity:
                Report.logPass(f"Advanced Call Clarity level reset to default value: {default_advanced_call_clarity}", True)
            else:
                Report.logFail(
                    f"Advanced Call Clarity level NOT reset to default value. Displayed level is: {updated_advanced_call_clarity_level}")

            # Check Equalizer
            default_eq_profile = "Default"
            current_eq_name = self.tune_app.get_equalizer_profile_name()
            if default_eq_profile == current_eq_name:
                Report.logPass(f"Equalizer profile reset to default value: {default_eq_profile}", True)
            else:
                Report.logFail(
                    f"Equalizer profile NOT reset to default value. Displayed level is: {current_eq_name}")

            # Check Health and Safety
            self.tune_app.click_health_and_safety_label()
            time.sleep(10)

            default_anti_startle = False
            anti_startle_state = self.tune_app.get_anti_startle_protection_state()
            Report.logInfo(f"Anti startle protection state is: {anti_startle_state}")
            if anti_startle_state == default_anti_startle:
                Report.logPass(f"Anti Startle reset to default value: {default_anti_startle}", True)
            else:
                Report.logFail(
                    f"Anti Startle NOT reset to default value. Displayed level is: {anti_startle_state}")

            default_noise_exposure_control = False
            noise_exposure_control_state = self.tune_app.get_noise_exposure_control_state()
            Report.logInfo(f"Anti startle protection state is: {noise_exposure_control_state}")
            if noise_exposure_control_state == default_noise_exposure_control:
                Report.logPass(f"Noise Exposure Control reset to default value: {default_noise_exposure_control}", True)
            else:
                Report.logFail(
                    f"Noise Exposure Control NOT reset to default value. Displayed level is: {noise_exposure_control_state}")

            if self.tune_app.verify_back_button_cybermorph():
                self.tune_app.click_back_button_cybermorph()

            # Check device Name
            default_device_name = device_name
            current_device_name = self.tune_app.get_device_name_from_settings_page()
            if current_device_name == default_device_name:
                Report.logPass(f"Device Name reset to default value: {default_device_name}", True)
            else:
                Report.logFail(
                    f"Device name NOT reset to default value. Displayed level is: {current_device_name}")

            # Check Sleep timer
            default_sleep_timer = 60
            current_sleep_timer = self.tune_app.get_current_sleep_settings_timeout()
            if current_sleep_timer == default_sleep_timer:
                Report.logPass(f"Sleep timeout reset to default value: {default_sleep_timer}", True)
            else:
                Report.logFail(
                    f"Sleep timeout  NOT reset to default value. Displayed level is: {current_sleep_timer}")

            # Check Rotate to Mute
            default_rotate_to_mute = True
            current_rotate_to_mute = self.tune_app.get_rotate_to_mute_state()
            if current_rotate_to_mute == default_rotate_to_mute:
                Report.logPass(f"Rotate to mute value reset to default value: {default_rotate_to_mute}", True)
            else:
                Report.logFail(f"Rotate to mute value NOT reset to default value. Displayed level is: {current_rotate_to_mute}")

            # Check ANC button options
            Report.logInfo(f"Verify ANC button options.")
            self.tune_app.click_anc_button_options()

            for key, value in anc_button_options.items():
                Report.logInfo(f"Verify ANC button option state for: {key}.")
                default_anc_off_state = value[4]
                anc_button_state = self.tune_app.get_anc_button_option_state(value[2])
                if anc_button_state == default_anc_off_state:
                    Report.logPass(f"{key} value reset to default: {default_anc_off_state}", True)
                else:
                    Report.logFail(f"{key} value NOT reset to default value. Displayed level is: {anc_button_state}")

            if self.tune_app.verify_back_button_cybermorph():
                self.tune_app.click_back_button_cybermorph()

            # Check on head detection
            self.tune_app.click_on_head_detection()
            time.sleep(10)

            default_auto_mute_state = False
            auto_mute_state = self.tune_app.get_auto_mute_state()
            if auto_mute_state == default_auto_mute_state:
                Report.logPass(f"Auto Mute value reset to default: {default_auto_mute_state}", True)
            else:
                Report.logFail(f"Auto Mute value NOT reset to default value. Displayed level is: {auto_mute_state}")

            default_auto_answer_state = True
            auto_answer_state = self.tune_app.get_auto_answer_state()
            if auto_answer_state == default_auto_answer_state:
                Report.logPass(f"Auto Answer value reset to default: {default_auto_answer_state}", True)
            else:
                Report.logFail(f"Auto Answer value NOT reset to default value. Displayed level is: {auto_answer_state}")

            default_auto_pause_state = True
            auto_pause_state = self.tune_app.get_auto_pause_state()
            if auto_pause_state == default_auto_pause_state:
                Report.logPass(f"Auto Pause value reset to default: {default_auto_pause_state}", True)
            else:
                Report.logFail(f"Auto Pause value NOT reset to default value. Displayed level is: {auto_pause_state}")

            if self.tune_app.verify_back_button_cybermorph():
                self.tune_app.click_back_button_cybermorph()

            #Check Voice prompts
            default_voice_prompt_level = "Voice"
            voice_prompt_level = self.tune_app.get_voice_prompts_level_name()
            if voice_prompt_level == default_voice_prompt_level:
                Report.logPass(f"Voice Prompt value reset to default: {default_voice_prompt_level}", True)
            else:
                Report.logFail(f"Voice Prompt value NOT reset to default value. Displayed level is: {voice_prompt_level}")

        except Exception as e:
            Report.logException(str(e))

    def _check_filter(self):
        self.tune_app.click_adjustments_tab()
        white_balance = self.tune_app.verify_adjustments_auto_white_balance_enable()
        brightness = int(self.tune_app.get_adjustments_brightness_slider_value())
        contrast = int(self.tune_app.get_adjustments_contrast_slider_value())
        saturation = int(self.tune_app.get_adjustments_saturation_slider_value())
        sharpness = int(self.tune_app.get_adjustments_sharpness_slider_value())
        Report.logInfo(f"{brightness}, {contrast}, {saturation}, {sharpness}")
        filter = None
        if white_balance and brightness==180 and contrast==150 and saturation==128 and sharpness==128:
            filter = "Bright"
        elif not white_balance and  brightness==128 and contrast==128 and saturation==102 and sharpness==76:
            filter = "Blossom"
        elif not white_balance and brightness==140 and contrast==128 and saturation==51 and sharpness==128:
            filter = "Forest"
        elif white_balance and brightness==128 and contrast==76 and saturation==178 and sharpness==255:
            filter = "Film"
        elif not white_balance and brightness==128 and contrast==153 and saturation==140 and sharpness==153:
            filter = "Glaze"
        elif white_balance and brightness==128 and contrast==128 and saturation==0 and sharpness==128:
            filter = "Mono B"
        self.tune_app.click_color_filters_tab()
        return filter

    def tc_connect_to_calendar(self, guest_mode: bool = False):
        """
        Method to connect to google calendar
        :param None
        :return None
        """
        try:
            browser = BrowserClass()
            browser.prepare_opened_browser(guest_mode=guest_mode)
            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_sign_in()
            self.tune_app.click_google()
            self._sign_in_to_google_calendar()
        except Exception as e:
            Report.logException(str(e))

    def connect_to_work_or_agenda_account(self, account_type, test_type='coily',
                                          account_credentials=None):
        try:
            Report.logInfo("Connect to LogiTune Work/Calendar account.")
            if account_type == GOOGLE:
                status = self.tc_connect_to_google_work_account(account_credentials)
            else:
                status = self.tc_connect_to_outlook_work_account(account_credentials)

            if not status:
                Report.logInfo("Connecting to LogiTune Work/Calendar account failed. Try one more time.")
                self.tune_app.open_tune_app()
                if account_type == GOOGLE:
                    status = self.tc_connect_to_google_work_account(account_credentials)
                else:
                    status = self.tc_connect_to_outlook_work_account(account_credentials)

            assert status is True, "Log in to LogiTune Work/Calendar account failed"

            if test_type == 'coily':
                self.tune_app.click_logitech_desk_booking()
            self.verify_sign_in_button_is_displayed()
        except Exception as e:
            Report.logException(str(e))

    def tc_connect_to_google_work_account(self, credentials: Dict) -> bool:
        """
        Method to connect to google account
        :param credentials: Dictionary which consist of name, surname, email and password stored in config file on s3
        :return none
        """
        try:
            browser = BrowserClass()
            browser.prepare_opened_browser(guest_mode=True)
            time.sleep(7)
            self.tune_app.click_home()
            self.tune_app.click_sign_in()
            self.tune_app.click_privacy_box_in_work_account()
            self.tune_app.click_google_work_account()
            return self._sign_in_to_google_work_account(credentials)
        except Exception as e:
            Report.logInfo(str(e))
            return False
        finally:
            browser = BrowserClass()
            browser.close_all_browsers()
            time.sleep(3)

    def tc_connect_to_outlook_work_account(self, credentials) -> bool:
        """
        Method to connect to outlook account
        :param None
        :return None
        """
        try:
            browser = BrowserClass()
            browser.prepare_opened_browser(guest_mode=True)
            time.sleep(7)
            self.tune_app.click_home()
            self.tune_app.click_sign_in()
            self.tune_app.click_privacy_box_in_work_account()
            self.tune_app.click_outlook_work_account()
            return self._sign_in_to_outlook_work_account(credentials)
        except Exception as e:
            Report.logInfo(str(e))
            return False
        finally:
            browser = BrowserClass()
            browser.close_all_browsers()
            time.sleep(3)

    def _sign_in_to_google_calendar(self, credentials: Dict = None):
        """
        Private Method to sign in to google account. Email and Password are stored in ENV variable
        :param credentials: Dictionary which consist of name, surname, email and password stored in config file on s3
        :return none
        """
        try:
            driver = global_variables.driver
            browser = BrowserClass()
            global_variables.driver = browser.connect_to_google_accounts_browser_page()
            tune_browser = TuneBrowser()
            if credentials:
                tune_browser.sign_in_to_google_calendar(
                    credentials['signin_payload']['email'],
                    credentials['signin_payload']['password'],
                    credentials['signin_payload']['employee_id'],
                )
            else:
                tune_browser.sign_in_to_google_calendar(GOOGLE_ACCOUNT, GOOGLE_PASSWORD)
            browser.close_all_browsers()
            global_variables.driver = driver
        except Exception as e:
            Report.logException(str(e))

    def _sign_in_to_google_work_account(self, credentials: Dict) -> bool:
        """
        Private Method to sign in to google account. Email and Password are stored in ENV variable
        :param credentials: Dictionary which consist of name, surname, email and password stored in config file on s3
        :return none
        """
        driver = global_variables.driver
        try:
            browser = BrowserClass()
            global_variables.driver = browser.connect_to_google_accounts_browser_page()
            tune_browser = TuneBrowser()

            Report.logInfo(f"Sign in to Google account as  {credentials['signin_payload']['email']}")
            login_status = tune_browser.sign_in_to_google_work_account(credentials['signin_payload']['email'],
                                                                       credentials['signin_payload']['password'])

            return login_status
        except Exception as e:
            Report.logInfo(str(e))
            return False
        finally:
            global_variables.driver = driver

    def tc_verify_events(self):
        """
        Method to create event and verify the event displays in Logi Tune.
        Delete the event and check event removed from LogiTune
        """
        try:
            calendar_api = CalendarApi()
            start_time = str(datetime.now() + timedelta(hours=0.5))
            meeting_title = "Tune Meeting " + str(round(int(datetime.timestamp(datetime.now())), 0))
            event = calendar_api.create_event(start_time, summary=meeting_title, duration=0.5, time_zone="GMT-8",
                                              description="Testing", location="Newark")
            time.sleep(5)
            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            if self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=20):
                Report.logPass(f"Event {meeting_title} displayed in Logi Tune", True)
            else:
                Report.logFail(f"Event {meeting_title} not displayed in Logi Tune")
            calendar_api.delete_event(event_id=event['id'])
            time.sleep(10)
            if not self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=2):
                Report.logPass(f"Event {meeting_title} deleted in Logi Tune", True)
            else:
                Report.logFail(f"Event {meeting_title} not deleted in Logi Tune")

        except Exception as e:
            Report.logException(str(e))

    def tc_disconnect_calendar(self):
        """
        Method to disconnect to google calendar
        Script to move Disconnect button to the center position for click()
        :param None
        :return None
        """
        try:
            self.tune_app.click_tune_menu()
            self.tune_app.click_app_settings()
            self.tune_app.click_calendar_connection()
            self.tune_app.click_disconnect_button()
            self.tune_app.verify_calendar_not_connected()
            self.tune_app.click_back_button_to_my_devices()
            self.tune_app.click_close_settings_screen()

        except Exception as e:
            Report.logException(str(e))

    def tc_disconnect_calendar_account(self):
        """
        Method to disconnect from calendar
        Script to move Disconnect button to the center position for click()
        :param None
        :return None
        """
        try:
            self.tune_app.click_tune_menu()
            self.tune_app.click_app_settings()
            self.tune_app.click_calendar_connection()
            self.tune_app.click_disconnect_button()
            self.tune_app.verify_calendar_not_connected()
            self.tune_app.click_back_button_to_device_settings()
            self.tune_app.click_close_settings_screen()

        except Exception as e:
            Report.logException(str(e))

    def tc_disconnect_connected_account(self):
        """
        Method to disconnect to google calendar
        Script to move Disconnect button to the center position for click()
        :param None
        :return None
        """
        try:
            self.tune_app.click_tune_menu()
            self.tune_app.click_app_settings()
            self.tune_app.click_settings_connected_account()
            self.tune_app.click_disconnect_button()

            self.tune_app.click_home()
            time.sleep(3)
            assert self.tune_app.verify_sign_int_button_is_displayed() is True, Report.logFail("Work account NOT disconnected successfully!")

        except Exception as e:
            Report.logException(str(e))

    def verify_sign_in_button_is_displayed(self) -> bool:
        try:
            self.tune_app.click_home()
            return self.tune_app.verify_sign_int_button_is_displayed()

        except Exception as e:
            Report.logException(str(e))

    def tc_connect_to_outlook_calendar(self, guest_mode: bool = False) -> None:
        """
        Method to connect to Outlook calendar
        :param None
        :return None
        """
        try:
            browser = BrowserClass()
            browser.prepare_opened_browser(guest_mode=guest_mode)
            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            self.tune_app.click_connect_now()
            self.tune_app.click_outlook()
            self._sign_in_to_outlook_calendar()
        except Exception as e:
            Report.logException(str(e))

    def _sign_in_to_outlook_calendar(self, credentials=None) -> None:
        """
        Private Method to sign in to Outlook account. Email and Password are stored in ENV variable
        :param credentials
        :return none
        """
        try:
            driver = global_variables.driver
            browser = BrowserClass()
            global_variables.driver = browser.connect_to_outlook_accounts_browser_page()
            tune_browser = TuneBrowser()
            if credentials:
                tune_browser._sign_in_to_outlook_work_account(credentials['signin_payload']['email'],
                                                              credentials['signin_payload']['password'])
            else:
                tune_browser.sign_in_to_outlook_calendar(OUTLOOK_ACCOUNT, OUTLOOK_PASSWORD)
            global_variables.driver = driver
        except Exception as e:
            Report.logException(str(e))

    def _sign_in_to_outlook_work_account(self, credentials) -> bool:
        """
        Private Method to sign in to Outlook account. Email and Password are stored in ENV variable
        :param credentials
        :return none
        """
        driver = global_variables.driver
        try:
            browser = BrowserClass()
            global_variables.driver = browser.connect_to_outlook_accounts_browser_page()
            tune_browser = TuneBrowser()

            Report.logInfo(f"Sign in to Outlook account as  {credentials['signin_payload']['email']}")
            login_status = tune_browser.sign_in_to_outlook_work_account(credentials['signin_payload']['email'],
                                                                         credentials['signin_payload']['password'])
            return login_status
        except Exception as e:
            Report.logWarning(str(e))
            return False
        finally:
            global_variables.driver = driver

    def tc_verify_outlook_calendar_event(self) -> None:
        """
        Method to create Outlook calendar event and verify the event displays in Logi Tune.
        Delete the event and check event removed from LogiTune
        :param None
        :return None
        """
        try:
            outlook_calendar_api = OutlookCalendarDriver()
            meeting_title = "Tune Meeting " + str(round(int(datetime.timestamp(datetime.now())), 0))
            event = outlook_calendar_api.create_outlook_event(meeting_title=meeting_title)
            time.sleep(5)
            self.tune_app.connect_tune_app()
            self.tune_app.click_home()
            if self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=20):
                Report.logPass(f"Event {meeting_title} displayed in Logi Tune", True)
            else:
                Report.logFail(f"Event {meeting_title} not displayed in Logi Tune")
            outlook_calendar_api.delete_outlook_event(meeting_title)
            time.sleep(10)
            if not self.tune_app.verify_meeting_title(meeting_title=meeting_title, timeout=2):
                Report.logPass(f"Event {meeting_title} deleted in Logi Tune", True)
            else:
                Report.logFail(f"Event {meeting_title} not deleted in Logi Tune")

        except Exception as e:
            Report.logException(str(e))

    def tc_verify_outlook_disconnect_reconnect_event_status(self) -> None:
        """
        Method to verify if event status remains the same after disconnect and reconnect Outlook account
        :param None
        :return None
        """
        try:
            self.tc_disconnect_calendar()
            # Click two times to go back to main manu
            self.tune_app.click_back_button_to_my_devices()
            self.tune_app.click_back_button_to_my_devices()
            self.tc_connect_to_outlook_calendar()
            self.tune_app.verify_no_meeting_soon()
            browser = BrowserClass()
            browser.close_all_browsers()

        except Exception as e:
            Report.logException(str(e))

    def tc_verify_support_webpage(self) -> None:
        """
        Method to verify Support webpage shows up after clicking Support on Tune
        :param None
        :return None
        """
        try:
            browser = BrowserClass()
            browser.prepare_opened_browser()
            self.tune_app.connect_tune_app()
            self.tune_app.click_tune_menu()
            self.tune_app.click_support()
            self._verify_support_page()

        except Exception as e:
            Report.logException(str(e))

    def _verify_support_page(self) -> None:
        """
        Private Method to verify Support webpage
        :param None
        :return None
        """
        driver = global_variables.driver
        browser = BrowserClass()
        global_variables.driver = browser.connect_to_support_browser_page()
        tune_browser = TuneBrowser()
        if tune_browser.verify_support_webpage_title():
            Report.logPass("Getting Started - Logi Tune shown on support webpage", True)
        else:
            Report.logFail("Getting Started - Logi Tune doesn't show on support webpage")
        browser.close_all_browsers()
        global_variables.driver = driver

    def tc_verify_share_feedback_webpage(self) -> None:
        """
        Method to verify Share feedback shows up after clicking Support on Tune
        :param None
        :return None
        """
        try:
            browser = BrowserClass()
            browser.prepare_opened_browser()
            self.tune_app.connect_tune_app()
            self.tune_app.click_tune_menu()
            self.tune_app.click_share_feedback()
            self._verify_share_feedback_page()

        except Exception as e:
            Report.logException(str(e))

    def _verify_share_feedback_page(self) -> None:
        """
        Private Method to verify Share feedback webpage
        :param None
        :return None
        """
        driver = global_variables.driver
        browser = BrowserClass()
        global_variables.driver = browser.connect_to_share_feedback_browser_page()
        tune_browser = TuneBrowser()
        if tune_browser.verify_share_feedback_webpage_title():
            Report.logPass("Give feedback button is on Share feedback webpage", True)
        else:
            Report.logFail("Give feedback button doesn't show on Share feedback webpage")
        browser.close_all_browsers()
        global_variables.driver = driver

    def tc_verify_settings_sound_input_output(self, device_name: str) -> None:
        """
        Method to verify if the device is on the list of sound input/output in systems
        :param device_name: name of device
        :return none
        """
        if get_custom_platform() == "windows":
            try:
                # Launch Windows Settings - Sound
                Report.logInfo("Launch Settings Sound")
                Popen(["start", "ms-settings:sound"], shell=True).wait()
                time.sleep(2)

                # Attach driver to Settings - Sound
                driver = global_variables.driver
                app = GetDriverForOpenApp()
                Report.logInfo("Get driver of Settings")
                driverRaw = app.getDriver("Settings")
                self.driver = EventFiringWebDriver(driverRaw, CustomListener())
                global_variables.driver = self.driver

                batcmd = "systeminfo"
                result = check_output(batcmd, shell=True)
                result = result.decode("utf-8")

                if device_name == "Zone 750":
                    if "Microsoft Windows 10" in result:
                        # Verify if device is on output list
                        self.look_element(WinAppLocators.SOUND_OUTPUT).click()
                        if self.verify_element(WinAppLocators.WIN_OUTPUT_ZONE_750):
                            Report.logPass("Zone 750 is on the output device list", True)
                        else:
                            Report.logFail("Zone 750 is not on the output device list")

                        # Verify if device is on input list
                        self.look_element(WinAppLocators.SOUND_INPUT).click()  # It nees to click two times to cancel the previous selection
                        self.look_element(WinAppLocators.SOUND_INPUT).click()
                        if self.verify_element(WinAppLocators.WIN_INPUT_ZONE_750):
                            Report.logPass("Zone 750 is on the input device list", True)
                        else:
                            Report.logFail("Zone 750 is not on the input device list")

                    else:  # Windows 11
                        # Verify if device is on output list
                        if self.verify_element(WinAppLocators.WIN_11_OUTPUT_ZONE_750):
                            Report.logPass("Zone 750 is on the output device list", True)
                        else:
                            Report.logFail("Zone 750 is not on the output device list")
                        # Verify if device is on input list
                        if self.verify_element(WinAppLocators.WIN_11_INPUT_ZONE_750):
                            Report.logPass("Zone 750 is on the input device list", True)
                        else:
                            Report.logFail("Zone 750 is not on the input device list")

                else:  # Zone Wired Earbuds
                    if "Microsoft Windows 10" in result:
                        # Verify if device is on output list
                        self.look_element(WinAppLocators.SOUND_OUTPUT).click()
                        if self.verify_element(WinAppLocators.WIN_OUTPUT_ZONE_WIRED_EARBUDS):
                            Report.logPass("Zone Wired Earbuds is on the output device list", True)
                        else:
                            Report.logFail("Zone Wired Earbuds is not on the output device list")

                        # Verify if device is on input list
                        self.look_element(WinAppLocators.SOUND_INPUT).click()  # It nees to click two times to cancel the previous selection
                        self.look_element(WinAppLocators.SOUND_INPUT).click()
                        if self.verify_element(WinAppLocators.WIN_INPUT_ZONE_WIRED_EARBUDS):
                            Report.logPass("Zone Wired Earbuds is on the input device list", True)
                        else:
                            Report.logFail("Zone Wired Earbuds is not on the input device list")

                    else:  # Windows 11
                        # Verify if device is on output list
                        if self.verify_element(WinAppLocators.WIN_11_OUTPUT_ZONE_WIRED_EARBUDS):
                            Report.logPass("Zone Wired Earbuds is on the output device list", True)
                        else:
                            Report.logFail("Zone Wired Earbuds is not on the output device list")

                        # Verify if device is on input list
                        if self.verify_element(WinAppLocators.WIN_11_INPUT_ZONE_WIRED_EARBUDS):
                            Report.logPass("Zone Wired Earbuds is on the input device list", True)
                        else:
                            Report.logFail("Zone Wired Earbuds is not on the input device list")

                global_variables.driver.close()
                global_variables.driver = driver

            except Exception as e:
                Report.logException(str(e))

        else:  # MacOS
            try:
                import json
                #  Read audio list information and output as json
                output_bytes = check_output(["system_profiler", "SPAudioDataType", "-json"])
                output_text = output_bytes.decode("utf-8")
                f = json.loads(output_text)

                counts = []
                for i in range(len(f["SPAudioDataType"][0]["_items"])):
                    if device_name in f["SPAudioDataType"][0]["_items"][i]["_name"]:
                        Report.logInfo(f"{device_name} is on audio list")
                        if "coreaudio_input_source" in f["SPAudioDataType"][0]["_items"][i]:
                            Report.logPass(f"{device_name} is on audio input list")
                            counts.append(1)
                        elif "coreaudio_output_source" in f["SPAudioDataType"][0]["_items"][i]:
                            Report.logPass(f"{device_name} is on audio output list")
                            counts.append(1)
                        else:
                            Report.logFail(f"{device_name} is not on input or output list")

                #  counts are supposed to be 2: input and output. Otherwise, it is failed.
                if len(counts) != 2:
                    Report.logFail(f"{device_name} is not on audio list")

            except Exception as e:
                Report.logException(str(e))

    def tc_language_update(self, device_name: str, test_name: str = 'language_update'):
        def start_recording(recording_name: str):
            if TUNE_RECORDER:
                window_coordinates = self.tune_app.get_window_position_and_size()
                recorder_instance = initialize_recorder(self.logdirectory, recording_name,
                                                        **window_coordinates)
                recorder_instance.start_recording()
                time.sleep(5)
                return recorder_instance

        def stop_recording(recorder_instance, save_record: bool = False):
            if TUNE_RECORDER and recorder_instance is not None:
                recorder_instance.stop_recording_and_save()
                if not save_record:
                    recorder_instance.delete()

        recorder = None
        languages = [
            Languages.french,
            Languages.german,
            Languages.portuguese,
            Languages.italian,
            Languages.spanish,
        ]
        if "Zone Vibe" in device_name:
            languages.append(Languages.english)
        try:
            self.tune_app.open_tune_app(clean_logs=True)
            recorder = start_recording(test_name)
            self.tune_app.open_device_in_my_devices_tab(device_name)
            time.sleep(2)
            self.tune_app.verify_headset_language_displayed()
            current_language_name = self.tune_app.get_current_language_name()
            self.tune_app.open_languages_tab()
            new_language = random.choice([x for x in languages
                                          if x.language_name != current_language_name])
            Report.logInfo(f"New language name: {new_language.language_name}")
            try:
                self.tune_app.start_language_update(new_language.button_locator)
            except ValueError:
                Report.logInfo(f"{new_language.language_name} already downloaded")
                new_language = random.choice(
                    [x for x in languages if (x.language_name != current_language_name
                                              and x.language_name != new_language)])
                Report.logInfo(f"New language name: {new_language.language_name}")
                self.tune_app.start_language_update(new_language.button_locator)
            except Exception as e:
                raise e
            self.tune_app.open_device_in_my_devices_tab(device_name=device_name,
                                                        skip_exception=True)
            time.sleep(2)
            self.tune_app.verify_headset_language_displayed()
            self.tune_app.open_languages_tab()
            self.tune_app.verify_language_update_success(new_language.radio_locator)
            stop_recording(recorder)
        except Exception as ex:
            Report.logException(str(ex))
            stop_recording(recorder, save_record=True)
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def tc_cybermorph_language_selection(self, device_name: str) -> None:
        languages = [
            Languages.german,
            Languages.portuguese,
            Languages.spanish,
            Languages.english,
        ]
        try:
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.open_device_in_my_devices_tab(device_name)
            for language in languages:
                self.tune_app.open_languages_tab()
                Report.logInfo(f"Changing language to: {language.language_name}")
                self.tune_app.look_element(language.radio_locator).click()
                self.tune_app.look_element(TunesAppLocators.BACK_CYBERMORPH).click()
                time.sleep(1)
                language_name_after_change = self.tune_app.get_current_language_name()
                assert language_name_after_change == language.language_name, Report.logException(
                    f'Language change was not successful. Expected: {language.language_name}, '
                    f'Observer: {language_name_after_change}'
                )
                Report.logInfo(f'Valid language is visible: {language.language_name}')
            Report.logPass(f'All languages from the list was selected properly!')
        except Exception as e:
            raise e
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def tc_install_logitune(self, version, disconnect_devices=True, app_update: Optional[str] = None):
        """
        Method to install LogiTune App based on the installer version parameter
        :param version
        :return none
        """
        try:
            if disconnect_devices:
                disconnect_all()
            Report.logInfo(f"Installing LogiTune version: {version}")
            if get_custom_platform() == "windows":
                app = TunesUIInstallWindows()
                if app.check_for_app_installed_win(TUNEAPP_NAME):
                    app.uninstall_app()
                time.sleep(10)
                app.install_app(version, app_update=app_update)
                services = app.verify_logi_tune_services_install()
                if services:
                    Report.logPass("Successfully installed Logi Tune")
                else:
                    Report.logFail("Logi Tune not installed Successfully")
            else:
                app = TunesUIInstallMacOS()
                if app.check_tune_installed_macos():
                    app.uninstallApp()
                time.sleep(5)
                app.installApp(version, app_update=app_update)
        except Exception as e:
            Report.logException(str(e))

    def tc_update_logitune(self, change_settings_json=True):
        """
        Method to update LogiTune App. Currently this is limited to Windows only
        Pre-requisite - Install LogiTune and Set global_variables.TUNE_UPDATE_CHANNEL to
        staging channel where update is available. For Example dev
        :param None
        :return none
        """
        from apps.tune.helpers import get_logitune_version_macos
        from apps.tune.TuneAppSettings import TuneUpdaterDaemon, TuneAgentDaemon
        tune_daemon = None
        try:
            platform = get_custom_platform()
            if change_settings_json:
                if platform == "windows":
                    settings_path = base_settings.TUNE_SETTINGS_PATH_WIN
                else:
                    tune_daemon = TuneUpdaterDaemon() if get_logitune_version_macos().startswith(
                        '3.6') else TuneAgentDaemon()
                    settings_path = base_settings.TUNE_SETTINGS_PATH_MAC
                    tune_daemon.unload()
                JsonHelper.add_key_value_to_json(settings_path, ["UpdateChannel",
                                                                 "UpdateManifestUrl"],
                                                 [global_variables.TUNE_UPDATE_CHANNEL,
                                                  global_variables.TUNE_UPDATE_MANIFEST_URL_OLD])
                if "windows" in platform:
                    time.sleep(5)
                    subprocess.run(self._win_tune_updater, shell=True)
                else:
                    tune_daemon.load()
            self.tune_app.open_tune_app(update=True)
            self.tune_app.click_update_logitune_now()
            self.start_performance_test()
            if get_custom_platform() == "windows":
                installer_wait_flag = True
                installer_wait_count = 600
                while installer_wait_flag and installer_wait_count > 0:
                    for proc in psutil.process_iter():
                        if 'LogiTuneInstall' in proc.name():
                            installer_wait_flag = False
                            time.sleep(5)
                            break
                    installer_wait_count -= 1
                installer_wait_flag = True
                installer_wait_count = 300
                while installer_wait_flag and installer_wait_count > 0:
                    for proc in psutil.process_iter():
                        if 'LogiTuneAgent' in proc.name():
                            installer_wait_flag = False
                            time.sleep(5)
                            break
                    installer_wait_count -= 1
            self.end_performance_test("LogiTune App Update")
        except Exception as e:
            Report.logException(str(e))

    def tc_bt_pair_headset(self, device_name: str, device_mac: str) -> None:
        """ Method to connect headset via bluetooth and check if the device
        is displayed on Logi Tune

        @param device_name: device name
        @param device_mac: bt mac address of headset
        @return: None
        """
        try:
            if device_name == 'Zone Wireless 2':

                pid = 0x0AFA
                usage_page = 65280

                hid_command = UsbHidCommunicationBase(device_name=device_name)
                Report.logInfo(f"Start {device_name} bluetooth connection.")
                hid_command.power_on(pid=pid, usage_page=usage_page)
                time.sleep(5)
                hid_command.pairing(pid=pid, usage_page=usage_page)

                self.bt_ctrl.bluetooth_pair(device_mac, device_name)
                if get_custom_platform() == "macos":
                    self.bt_ctrl.bluetooth_connect(device_mac)

                self.tune_app.open_tune_app()
                self.tune_app.open_my_devices_tab()
                time.sleep(3)

                if self.tune_app.verify_device_name_displayed(device_name):
                    Report.logPass(f"{device_name} is displayed on Logi Tune.")
                else:
                    Report.logFail(f"{device_name} is not displayed on Logi Tune.")

            else:
                ry_ctrl = GenericRelayControl()
                relay_serial_num = ""
                power_on_btn = ""
                pair_btn = ""
                # Communicate with the relay connected with Enduro Series
                if "125" in device_name:
                    relay_serial_num = ENDURO_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ENDURO_POWER_ON_BUTTON
                    pair_btn = ENDURO_POWER_PAIR_BUTTON
                elif "130" in device_name:
                    relay_serial_num = ZV130_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZV130_POWER_ON_BUTTON
                    pair_btn = ZV130_POWER_PAIR_BUTTON
                elif device_name == "Zone Vibe Wireless":
                    relay_serial_num = ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZONE_VIBE_WIRELESS_ON_BUTTON
                    pair_btn = ZONE_VIBE_WIRELESS_PAIR_BUTTON
                elif device_name == "Zone Wireless":
                    relay_serial_num = ZONE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER
                    pair_btn = ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON
                elif device_name == "Zone 900":
                    relay_serial_num = ZONE900_RELAY_BOARD_SERIAL_NUMBER
                    pair_btn = ZONE900_POWER_ON_OFF_PAIR_BUTTON
                elif device_name == "Zone 300":
                    relay_serial_num = ZONE_300_RELAY_BOARD_SERIAL_NUMBER
                    pair_btn = ZONE_300_POWER_ON_OFF_PAIR_BUTTON
                elif device_name == "Zone 305":
                    relay_serial_num = ZONE_305_RELAY_BOARD_SERIAL_NUMBER
                    pair_btn = ZONE_305_POWER_ON_OFF_PAIR_BUTTON

                relay_com_port = ry_ctrl.get_relay_com_port(relay_serial_num)
                ry_ctrl.connect_relay(relay_com_port)

                self.tune_app.open_tune_app()
                self.tune_app.open_my_devices_tab()

                Report.logInfo(f"Start {device_name} bluetooth connection.")
                for i in range(3):
                    Report.logInfo(f"Try NO.{i+1} time press button")
                    if "Vibe" in device_name:
                        ry_ctrl.press_btn(power_on_btn, 1)
                    ry_ctrl.press_btn(pair_btn, 3)
                    pair_success, bt_search_result = self.bt_ctrl.bluetooth_pair(device_mac, device_name)
                    Report.logInfo(f"pair success is: {pair_success} and bt search result is: {bt_search_result}")
                    if pair_success and bt_search_result:
                        Report.logInfo("Successfully pair with headset. Break the loop of pressing buttons.")
                        break
                    elif ("Zone 300" in device_name) or ("Zone 305" in device_name):
                        #  Turn off Zone 300 and Zone 305 for the next try
                        ry_ctrl.press_btn(pair_btn, 0.5)
                if get_custom_platform() == "macos":
                    self.bt_ctrl.bluetooth_connect(device_mac)
                if self.tune_app.verify_device_name_displayed(device_name):
                    Report.logPass(f"{device_name} is displayed on Logi Tune.")
                else:
                    Report.logFail(f"{device_name} is not displayed on Logi Tune.")

        except Exception as e:
            Report.logException(str(e))

    def tc_bt_unpair_headset(self, device_mac: str, device_name: str) -> None:
        """ Method to connect headset via bluetooth and check if the device
        is displayed on Logi Tune

        @param device_mac: bt mac address of headset
        @param device_name: name of headset
        @return: None
        """
        try:
            self.bt_ctrl.bluetooth_unpair(device_mac, device_name)

        except Exception as e:
            Report.logException(str(e))

    def tc_bt_connect_headset(self, device_name: str, is_wireless: bool = False) -> None:
        """ Method to connect headset via BT and check if all
        features are displayed

        @param device_name: device name
        @param is_wireless: True is headset is wireless, False for wired headsets
        @return: None
        """
        try:
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            if is_wireless:
                if self.tune_app.verify_device_name_displayed(device_name):
                    Report.logPass(f"{device_name} - displayed in LogiTune")
                else:
                    Report.logFail(f"{device_name} - not displayed in LogiTune")
            else:
                if self.tune_app.verify_headset_connected() and self.tune_app.verify_device_name_displayed(device_name):
                    Report.logPass(f"{device_name} - Connected displayed")
                else:
                    Report.logFail(f"{device_name} - Connected not displayed")

            if is_wireless:
                if device_name in ["Zone Wireless", "Zone Wireless Plus", "Zone 900"]:
                    if self.tune_app.verify_noise_cancellation_displayed():
                        Report.logPass("Noise cancellation displayed")
                    else:
                        Report.logFail("Noise cancellation not displayed")

                    if self.tune_app.verify_button_functions_label_displayed():
                        Report.logPass("Button functions displayed", True)
                    else:
                        Report.logFail("Button functions not displayed")

                    if self.tune_app.verify_connection_priority_label_displayed():
                        Report.logPass("Connection priority displayed", True)
                    else:
                        Report.logFail("Connection priority not displayed")

                if self.tune_app.verify_equalizer_displayed():
                    Report.logPass("Equalizer displayed")
                else:
                    Report.logFail("Equalizer not displayed")

                if self.tune_app.verify_device_name_label_displayed():
                    Report.logPass("Device Name displayed", True)
                else:
                    Report.logFail("Device Name not displayed")

                if self.tune_app.verify_sleep_settings_label_displayed():
                    Report.logPass("Sleep settings displayed", True)
                else:
                    Report.logFail("Sleep settings not displayed")
                if self.tune_app.verify_connected_device_label_displayed():
                    Report.logPass("Connected device displayed", True)
                else:
                    Report.logFail("Connected device not displayed")

                if device_name not in ["Zone Wireless 2", "Zone 950"]:
                    if self.tune_app.verify_headset_language_displayed():
                        Report.logPass("Headset language displayed", True)
                    else:
                        Report.logFail("Headset language not displayed")

            if self.tune_app.verify_sidetone_displayed():
                Report.logPass("Sidetone displayed")
            else:
                Report.logFail("Sidetone not displayed")

            if self.tune_app.verify_mic_level_displayed():
                Report.logPass("Mic level displayed")
            else:
                Report.logFail("Mic level not displayed")

            if self.tune_app.verify_headset_diagnostics_displayed():
                Report.logPass("Headset diagnostics displayed", True)
            else:
                Report.logFail("Headset diagnostics not displayed")

            if "Earbuds" not in device_name:
                if self.tune_app.verify_rotate_to_mute_label_displayed():
                    Report.logPass("Rotate to mute displayed", True)
                else:
                    Report.logFail("Rotate to mute not displayed")

            if device_name in ["Zone Wireless 2", "Zone 950"]:
                if self.tune_app.verify_anc_button_options_displayed():
                    Report.logPass("ANC Group Button displayed", True)
                else:
                    Report.logFail("ANC Group Button not displayed")
                if self.tune_app.verify_health_and_safety_displayed():
                    Report.logPass("Health and Safety displayed", True)
                else:
                    Report.logFail("Health and Safety not displayed")
                if self.tune_app.verify_on_head_detection_displayed():
                    Report.logPass("On head detection displayed", True)
                else:
                    Report.logFail("On head detection not displayed")
                if self.tune_app.verify_anc_button_options_displayed():
                    Report.logPass("ANC Button options displayed", True)
                else:
                    Report.logFail("ANC Button options not displayed")
                if self.tune_app.verify_voice_prompts_3_levels_displayed():
                    Report.logPass("Voice Prompts displayed", True)
                else:
                    Report.logFail("Voice Prompts not displayed")
                if self.tune_app.verify_advanced_call_clarity_displayed():
                    Report.logPass("Advanced Call Clarity displayed", True)
                else:
                    Report.logFail("Advanced Call Clarity not displayed")
            else:
                if self.tune_app.verify_voice_prompts_displayed():
                    Report.logPass("Voice prompts displayed", True)
                else:
                    Report.logFail("Voice prompts not displayed")

        except Exception as e:
            Report.logException(str(e))

    def _get_centrion_com_port(self, device_name: str) -> str:
        """ Method to change and verify sidetone level with headset in BT mode and SPP connection

        @param device_name: device name
        @return: port: bluetooth serial port for CentrionCommands to open
        """
        if get_custom_platform() == "windows":
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            for port, desc, hwid in sorted(ports):
                Report.logInfo(f"{port}: {desc} [{hwid}]")
                # For BTHENUM, please refer to https://stackoverflow.com/questions/2085179/how-can-i-find-out-a-com-port-number-of-a-bluetooth-device-in-c
                # And http://www.alanjmcf.me.uk/comms/bluetooth/32feet.NET%20--%20User%20Guide.html
                if ("BTHENUM" in hwid) and ("VID" in hwid):
                    Report.logInfo(f"COM port used here is: {port}")
                    return port
        else:  # MacOS
            # The naming rule of com ports in macOS is /dev/tty.DeviceName
            shcmd = "ls -l /dev/tty.*"
            output_bytes = check_output([shcmd], shell=True)
            output_text = output_bytes.decode("utf-8")
            Report.logInfo(f"All ports in system are:\n {output_text}")
            device_name_pattern = "/dev/tty." + device_name.replace(" ", "")
            port = re.search(pattern=device_name_pattern, string=output_text)
            Report.logInfo(f"COM port used here is: {port.group(0)}")
            return str(port.group(0))

    def tc_bt_spp_sidetone(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify sidetone level with headset in BT mode and SPP connection

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.click_sidetone()
            value = self.tune_app.get_sidetone_slider_value()
            new_value = choice([i for i in range(0, 10) if i not in [value/10]])

            self.tune_app.set_sidetone_slider(new_value*10)
            self.tune_app.verify_sidetone_value(str(new_value*10))
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_sidetone_level(product_string=device_name,
                                                   conn_type=conn_type,
                                                   level=new_value)
            else:
                self._bt_verify_sidetone(device_name=device_name,
                                         level=new_value*10)

        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_sidetone_level(self, product_string: str, conn_type: str, level: int) -> None:
        """ Method to verify sidetone level on device over centurion++ in BT mode and SPP connection

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param level: sidetone level
        @return: None
        """
        try:
            com_port = self._get_centrion_com_port(device_name=product_string)
            # com_port = com_port.upper()
            # Close Tune to release SPP of headset
            self.tune_app.close_tune_app()
            time.sleep(10)

            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=com_port)
            self.features = Features(self.centurion)
            response = self.features.headset_audio_feature.get_sidetone_level()
            self.features.headset_audio_feature.verify_get_sidetone_level(response,
                                                                          level)
            self.centurion.close_port()

        except Exception as e:
            Report.logException(str(e))

    def tc_bt_spp_wireless_headset_equalizer(self, device_name: str, conn_type: str, profiles: Dict) -> None:
        """Method to change and verify if Equalizer name is updated on the Sound page in BT mode and SPP connection

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param profiles: Equalizer profile
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            current_name = self.tune_app.get_equalizer_profile_name()

            new_equalizer_profile = choice([i for i in profiles.keys() if i not in [current_name]])

            self.tune_app.click_equalizer()
            self.tune_app.set_equalizer_profile(profile_name=new_equalizer_profile)
            time.sleep(5)
            self.tune_app.verify_equalizer_name(new_equalizer_profile)
            time.sleep(5)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_equalizer_profile_over_api(product_string=device_name,
                                                               conn_type=conn_type,
                                                               profile=profiles[new_equalizer_profile])
            elif conn_type == 'bt_ui':
                self._bt_verify_equalizer_profile_over_tune_ui(product_string=device_name,
                                                               profile=new_equalizer_profile)

        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_equalizer_profile_over_api(self, product_string: str, conn_type: str, profile: int) -> None:
        """ Method to verify Equalizer state on device over centurion++ in BT mode and SPP connection

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param profile: Equalizer profile
        @return: None
        """
        try:
            com_port = self._get_centrion_com_port(product_string)
            # com_port = com_port.upper()
            # Close Tune to release SPP of headset
            self.tune_app.close_tune_app()
            self.centurion = CenturionCommands(device_name=product_string,
                                               conn_type=conn_type,
                                               com_port=com_port)
            self.features = Features(self.centurion)
            response = self.features.eqset_feature.get_eq_mode()
            self.features.eqset_feature.verify_eq_profile(response, profile)
            self.centurion.close_port()

        except Exception as e:
            Report.logException(str(e))

    def tc_bt_spp_rotate_to_mute(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Rotate to mute state in BT mode and SPP connection

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_rotate_to_mute_label_displayed()

            state = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Change Rotate to Mute state to {not state}")
            self.tune_app.click_rotate_to_mute_toggle()
            new_state = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Rotate to mute state changed correctly.", True)
            else:
                Report.logFail(f"Rotate to mute NOT state changed correctly.")
            time.sleep(5)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_rotate_to_mute_over_api(product_string=device_name,
                                                            conn_type=conn_type,
                                                            state=new_state)
            else:
                self._bt_verify_rotate_to_mute_over_tune_ui(product_string=device_name,
                                                            state=new_state)

            # Change state for 2nd time
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            Report.logInfo(f"Change Rotate to Mute state to {not new_state}")
            self.tune_app.click_rotate_to_mute_toggle()
            new_state_2 = self.tune_app.get_rotate_to_mute_state()
            Report.logInfo(f"Rotate to mute state is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Rotate to mute state changed correctly.", True)
            else:
                Report.logFail(f"Rotate to mute NOT state changed correctly.")

            time.sleep(2)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_rotate_to_mute_over_api(product_string=device_name,
                                                            conn_type=conn_type,
                                                            state=new_state_2)
            else:
                self._bt_verify_rotate_to_mute_over_tune_ui(product_string=device_name,
                                                            state=new_state_2)

        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_rotate_to_mute_over_api(self, product_string: str, conn_type: str, state: bool) -> None:
        """ Method to verify Rotate to mute state on device over centurion++ in BT mode and SPP connection

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Rotate to mute state
        @return: None
        """
        com_port = self._get_centrion_com_port(product_string)
        # com_port = com_port.upper()
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        response = self.features.headset_misc_feature.get_mic_boom_status()
        self.features.headset_misc_feature.verify_mic_boom_status(response,
                                                                  state)
        self.centurion.close_port()

    def tc_bt_spp_voice_prompts(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Voice Prompts state in BT mode and SPP connection

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_voice_prompts_displayed()

            state = self.tune_app.get_voice_prompts_state()
            Report.logInfo(f"Voice prompts state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Voice prompts state to {not state}")
            self.tune_app.click_voice_prompts_toggle()
            new_state = self.tune_app.get_voice_prompts_state()
            Report.logInfo(f"Voice prompts state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Voice prompts changed correctly.", True)
            else:
                Report.logFail(f"Voice prompts NOT state changed correctly.")
            time.sleep(5)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_voice_prompts(product_string=device_name,
                                                  conn_type=conn_type,
                                                  state=new_state)
            else:
                self._bt_verify_voice_prompt(product_string=device_name,
                                             state=new_state)

            # Change state for 2nd time
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            Report.logInfo(f"Voice prompts to {not new_state}")
            self.tune_app.click_voice_prompts_toggle()
            new_state_2 = self.tune_app.get_voice_prompts_state()
            Report.logInfo(f"Voice prompts is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Voice prompts changed correctly.", True)
            else:
                Report.logFail(f"Voice prompts NOT state changed correctly.")

            time.sleep(2)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_voice_prompts(product_string=device_name,
                                                  conn_type=conn_type,
                                                  state=new_state_2)
            else:
                self._bt_verify_voice_prompt(product_string=device_name,
                                             state=new_state_2)
        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_voice_prompts(self, product_string: str, conn_type: str, state: bool) -> None:
        """Method to verify Enable Voice Notifications state on device over centurion++ in BT mode and SPP connection

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Enable Voice Notifications state
        @return: None
        """
        com_port = self._get_centrion_com_port(product_string)
        # com_port = com_port.upper()
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        response = self.features.headset_misc_feature.get_voice_notification_status()
        self.features.headset_misc_feature.verify_get_voice_notification_status(
            response, state)
        self.centurion.close_port()

    def tc_bt_spp_device_name(self, device_name: str, conn_type: str, name_max_len: int) -> None:
        """ Method to change Device Name and verify it in BT mode and SPP connection

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_device_name_label_displayed()

            Report.logInfo("1. Change device name with 'Surprise Me' and verify it.")
            initial_device_name = self.tune_app.get_device_name_from_settings_page()

            # Change Device Name with Surprise Me
            self.tune_app.click_device_name_rename()
            self.tune_app.click_device_name_surprise_me()
            new_name_surprise = self.tune_app.get_value_from_device_name_input()
            self.tune_app.click_device_name_update()

            time.sleep(1)
            if self.tune_app.get_device_name_from_settings_page() == new_name_surprise:
                Report.logPass(f"New device name displayed correctly on Settings page.", True)
            else:
                Report.logFail(f"New device name not displayed correctly on Settings page.")

            time.sleep(5)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_device_name(product_string=device_name,
                                                conn_type=conn_type,
                                                device_name=new_name_surprise, name_max_len=name_max_len)
            else:
                self._bt_verify_device_name(product_string=device_name,
                                            device_name=new_name_surprise,
                                            name_max_len=name_max_len)

            Report.logInfo("2. Verify empty device name.")
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=new_name_surprise)
            self.tune_app.click_device_name_rename()
            self.tune_app.clear_device_name()

            if self.tune_app.get_device_name_error() == "Name cannot be empty":
                Report.logPass(f"Correct error name displayed.", True)
            else:
                Report.logFail(f"Incorrect error name displayed.")

            if not self.tune_app.get_update_button_state_on_device_name_popup():
                Report.logPass(f"Correct state of Update button.", True)
            else:
                Report.logFail(f"Incorrect state of Update button.")

            Report.logInfo("3. Verify max device name")
            chars = string.ascii_uppercase + string.digits
            new_name = f"{device_name} {''.join(random.choice(chars) for _ in range(40))}"
            self.tune_app.set_new_device_name(new_name)

            time.sleep(1)
            if self.tune_app.get_device_name_from_settings_page() == new_name[:name_max_len]:
                Report.logPass(f"New device name displayed correctly on Settings page.", True)
            else:
                Report.logFail(f"New device name not displayed correctly on Settings page.")

            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_device_name(product_string=device_name,
                                                conn_type=conn_type,
                                                device_name=new_name[:name_max_len],
                                                name_max_len=name_max_len)
            else:
                self._bt_verify_device_name(product_string=device_name,
                                            device_name=new_name[:name_max_len],
                                            name_max_len=name_max_len)
            # Set default device name


        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_device_name(self, product_string: str, conn_type: str, device_name: str, name_max_len: int) -> None:
        """Method to verify Enable Voice Notifications state on device over centurion++ in BT mode and SPP connection

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param device_name: device name to verify
        @return: None
        """
        com_port = self._get_centrion_com_port(product_string)
        # com_port = com_port.upper()
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        response = self.features.device_name_feature.get_device_name()
        self.features.device_name_feature.verify_name(response, device_name, name_max_len)
        self.centurion.close_port()

    def tc_bt_spp_sleep_settings(self, device_name: str, conn_type: str) -> None:
        """ Method to change Sleep timeout and verify it in BT mode and SPP connection

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_sleep_settings_label_displayed()

            current_sleep_timeout = self.tune_app.get_current_sleep_settings_timeout()

            self.tune_app.click_current_sleep_settings_timeout()

            new_value = choice([i for i in [0, 5, 10, 15, 30, 60, 120, 240] if i not in [current_sleep_timeout]])

            self.tune_app.choose_new_sleep_timeout(new_value)

            value = self.tune_app.get_current_sleep_settings_timeout()

            if value == new_value:
                Report.logPass(f"New sleep timeout displayed correctly on Settings page.", True)
            else:
                Report.logFail(f"New sleep timeout displayed correctly on Settings page: {value} != {new_value}")

            time.sleep(7)
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_sleep_timer(product_string=device_name,
                                                conn_type=conn_type,
                                                sleep_timer=new_value)
            else:
                self._bt_verify_sleep_timer(product_string=device_name,
                                            sleep_timer=new_value)

        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_sleep_timer(self, product_string: str, conn_type: str, sleep_timer: int) -> None:
        """Method to verify Sleep timeout state on device over centurion++ in BT mode and SPP connection

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param sleep_timer: sleep timeout
        @return: None
        """
        com_port = self._get_centrion_com_port(product_string)
        # com_port = com_port.upper()
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        response = self.features.auto_sleep_feature.get_sleep_timer()
        self.features.auto_sleep_feature.verify_sleep_timer(response, sleep_timer)
        self.centurion.close_port()

    def bt_spp_set_never_sleep_timer(self, product_string: str, conn_type: str) -> None:
        """ Method to set Sleep Timeout equal to Never (0) in BT mode and SPP connection.

        @return: None
        """
        com_port = self._get_centrion_com_port(device_name=product_string)
        com_port = com_port.upper()
        self.tune_app.close_tune_app()
        time.sleep(5)
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        self.features.auto_sleep_feature.set_never_sleep_timer()
        self.centurion.close_port()

    def tc_set_default_device_name(self, device_name: str) -> None:
        """ Method to set Device Name to the default one
        Purpose: Set device name to the default to avoid impacting the following tests
        Suggest putting this method in tearDown
        @param device_name: device name
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.click_device_name_rename()
            self.tune_app.clear_device_name()
            self.tune_app.set_new_device_name(device_name)

        except Exception as e:
            Report.logException(f'Exception occurred: {e}')
            raise e

    def tc_get_tune_production_ver(self) -> str:
        """
        Method to the production version of LogiTune
        :return production_ver: Production version of Tune
        """
        try:
            if get_custom_platform() == "windows":
                app = TunesUIInstall()
                production_version = app.get_production_version_tune()
                Report.logInfo(f"Tune production version is: {production_version}")

            else:  # MacOS
                app = TunesUIInstallMacOS()
                production_version = app.get_production_version_tune()
                Report.logInfo(f"Tune production version is: {production_version}")

            return production_version

        except Exception as e:
            Report.logException(str(e))

    def tc_update_tune_app(self, base_branch: str, target_branch: str) -> None:
        """
        Method to update Tune app via built in update functionality
        Args:
            base_branch: str - branch name code ('prod', 'qa2') from which update should be done
            target_branch: str - branch name code ('prod', 'qa2') to which update should be done

        Returns:
            None
        """
        from common.ota_versions import TuneVersionGetter

        tune_apps_versions = TuneVersionGetter().get_tune_version_all_branches().get('Logi Tune')
        base_version = tune_apps_versions.get(base_branch).get('version')
        target_version = tune_apps_versions.get(target_branch).get('version')

        self.tc_install_logitune(version=base_version, app_update=target_branch)
        self.tc_update_logitune(change_settings_json=False)
        self.tc_verify_tune_updated(target_version, MAC_SLAVE_PASS, skip_windows=True)


    def tc_verify_tune_updated(self, installer_ver: str, mac_slave_password="password",
                               skip_windows=False) -> None:
        """
        Method to verify if Tune version is equal to Installer
        Pre-requisite - configure Installer to the latest version
        :param installer_ver: Installer version in properties.LOCAL
        :param mac_slave_password: System password of MAC slave PC
        :param skip_windows: flag to skip Windows update app status checking
        :return none:
        """
        try:
            if get_custom_platform() == "windows":
                if not skip_windows:
                    app = TunesUIInstall()
                    if app.check_update_app_status():
                        Report.logPass("Successfully update Logi Tune")
                    else:
                        Report.logFail("Logi Tune not updated successfully")
            else:
                app = TunesUIInstallMacOS()
                root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                DIR_PATH = os.path.join(root_dir, "WinApp")

                Report.logInfo("Run auto fill-in password Apple script")
                try:
                    Popen(["osascript", "fill_in_installer_pass.scpt", mac_slave_password],
                          cwd=DIR_PATH).wait(60)
                except subprocess.TimeoutExpired:
                    pass
                # Check if Tune is installed successfully after app updating
                i = 20
                while i > 0:
                    time.sleep(0.5)
                    if app.check_tune_installed_macos():
                        Report.logInfo(f"Tune is installed successfully.")
                        self.tune_app.open_tune_app()
                        break
                    else:
                        Report.logInfo("Tune is not yet installed during app updating.")
                        i -= 1

            # Verify current Tune version with INSTALLER
            self.tune_app.open_tune_app(clean_logs=True)
            self.tune_app.click_tune_menu()
            self.tune_app.click_about_menu()
            tune_ver = self.tune_app.get_tune_app_ver()
            Report.logInfo(f"Tune version after update is: {tune_ver}", screenshot=True)
            if installer_ver in tune_ver:
                Report.logPass(
                    f"App update successful! Current Tune version {tune_ver} is equal to Installer {installer_ver}.")
            else:
                Report.logFail(
                    f"App update failed! Current Tune version {tune_ver} is not equal to Installer {installer_ver}.")

        except Exception as e:
            Report.logException(str(e))

    def tc_detect_power_on_off_dongle(self, device_name: str) -> None:
        """
        Method to detect devices when turn on the power after dongle connected
        :param device_name: name of device
        :return none
        """

        serial_num = ""
        power_on_btn = ""
        power_off_btn = ""

        try:
            if device_name == "Zone Wireless 2":

                hid_ctrl = UsbHidCommunicationBase(device_name=device_name)
                pid = 0x0AFA
                usage_page = 65280

                disconnect_all()

                self.tune_app.open_tune_app()
                self.tune_app.click_my_devices()
                connect_device(device_name=device_name)
                hid_ctrl.power_on(pid, usage_page)
                time.sleep(5)
                if self.tune_app.verify_device_name_displayed(device_name=device_name):
                    Report.logInfo(f"{device_name} - Connected")
                elif self.tune_app.verify_receiver_displayed():
                    Report.logInfo(f"{device_name} - Not connected with receiver")
                hid_ctrl.power_off(pid, usage_page)
                if self.tune_app.verify_device_name_displayed(device_name=device_name):
                    Report.logInfo(f"{device_name} - Power off FAILED")
                elif self.tune_app.verify_receiver_displayed():
                    Report.logInfo(f"{device_name} - power off")
                time.sleep(3)
                hid_ctrl.power_on(pid, usage_page)
                time.sleep(5)
                if self.tune_app.verify_device_name_displayed(device_name=device_name):
                    Report.logPass(f"{device_name} - Connected after power cycle")
                elif self.tune_app.verify_receiver_displayed():
                    Report.logFail(f"{device_name} - NOT connected after power cycle")

            else:
                if "125" in device_name:
                    serial_num = ENDURO_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ENDURO_POWER_ON_BUTTON
                    power_off_btn = ENDURO_POWER_OFF_BUTTON
                elif "130" in device_name:
                    serial_num = ZV130_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZV130_POWER_ON_BUTTON
                    power_off_btn = ZV130_POWER_OFF_BUTTON
                elif device_name == "Zone Vibe Wireless":
                    serial_num = ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZONE_VIBE_WIRELESS_ON_BUTTON
                    power_off_btn = ZONE_VIBE_WIRELESS_OFF_BUTTON
                elif device_name == "Zone Wireless":
                    serial_num = ZONE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON
                    power_off_btn = ZONE_WIRELESS_POWER_ON_OFF_PAIR_BUTTON
                elif device_name == "Zone 900":
                    serial_num = ZONE900_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZONE900_POWER_ON_OFF_PAIR_BUTTON
                    power_off_btn = ZONE900_POWER_ON_OFF_PAIR_BUTTON
                elif device_name == "Zone 305":
                    serial_num = ZONE_305_RELAY_BOARD_SERIAL_NUMBER
                    power_on_btn = ZONE_305_POWER_ON_OFF_PAIR_BUTTON
                    power_off_btn = ZONE_305_POWER_ON_OFF_PAIR_BUTTON

                disconnect_all()
                self.tune_app.open_tune_app()
                self.tune_app.click_my_devices()
                relay_control = GenericRelayControl()
                comport_num = relay_control.get_relay_com_port(serial_num)
                relay_control.connect_relay(comport_num)
                connect_device(device_name)

                # Try if is connected
                time.sleep(10)

                if self.tune_app.verify_device_name_displayed(device_name) and self.tune_app.verify_device_connected():
                    Report.logInfo(f"{device_name} - is connected")
                elif self.tune_app.verify_receiver_displayed():
                    Report.logInfo(f"{device_name} - not connected with dongle, press power on button")
                    relay_control.press_btn(power_on_btn, 1)
                    time.sleep(3)
                # disconnect_device(device_name)
                # time.sleep(3)
                # Turn headset power off
                relay_control.press_btn(power_off_btn, 1)
                # time.sleep(5)
                # connect_device(device_name)
                time.sleep(3)
                # Check if power is off
                if self.tune_app.verify_receiver_displayed():
                    Report.logPass(f"{device_name} - Power turned off")
                else:
                    Report.logFail(f"{device_name} - Power turn off failed")
                # Turn power on
                relay_control.press_btn(power_on_btn, 1)
                time.sleep(3)
                # Check if connected
                if self.tune_app.verify_device_name_displayed(device_name) and self.tune_app.verify_device_connected():
                    Report.logPass(f"{device_name} - connected after power back on")
                elif self.tune_app.verify_device_name_displayed(
                        device_name) and self.tune_app.verify_statusbar_battery():
                    Report.logPass(f"{device_name} - connected after power back on with charging status")
                else:
                    Report.logFail(f"{device_name} - NOT connected after power cycle")

        except Exception as e:
            Report.logException(str(e))

    def tc_bt_spp_noise_cancellation(self, device_name: str, conn_type: str) -> None:
        """ Method to change and verify Noise cancellation state

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_noise_cancellation_displayed()

            state = self.tune_app.get_noise_cancellation_state()
            Report.logInfo(f"Noise cancellation state is: {state}")

            # Change state for 1st time
            Report.logInfo(f"Change Noise cancellation state to {not state}")
            self.tune_app.click_noise_cancellation_toggle()
            new_state = self.tune_app.get_noise_cancellation_state()
            Report.logInfo(f"Noise cancellation state is: {new_state}")
            if new_state != state:
                Report.logPass(f"Noise cancellation state changed correctly.", True)
            else:
                Report.logFail(f"Noise cancellation NOT state changed correctly.")

            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_noise_cancellation_over_api(product_string=device_name,
                                                                conn_type=conn_type,
                                                                state=new_state)
            else:
                self._bt_verify_noise_cancellation_over_tune_ui(product_string=device_name,
                                                                state=new_state)

            # Change state for 2nd time
            Report.logInfo(f"Change Noise cancellation state to {not new_state}")
            time.sleep(5)
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.click_noise_cancellation_toggle()
            new_state_2 = self.tune_app.get_noise_cancellation_state()
            Report.logInfo(f"Noise cancellation state is: {new_state_2}")
            if new_state_2 == state:
                Report.logPass(f"Noise cancellation state changed correctly.")
            else:
                Report.logFail(f"Noise cancellation NOT state changed correctly.")

            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_noise_cancellation_over_api(product_string=device_name,
                                                                conn_type=conn_type,
                                                                state=new_state_2)
            else:
                self._bt_verify_noise_cancellation_over_tune_ui(product_string=device_name,
                                                                state=new_state_2)
        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_noise_cancellation_over_api(self, product_string: str, conn_type: str, state: bool) -> None:
        """ Method to verify Rotate to mute state on device over centurion++

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param state: Rotate to mute state
        @return: None
        """
        com_port = self._get_centrion_com_port(device_name=product_string)

        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        response = self.features.headset_audio_feature.get_anc_state()
        self.features.headset_audio_feature.verify_get_anc_state(response,
                                                                 state)
        self.centurion.close_port()

    def tc_bt_spp_button_functions(self, device_name: str, conn_type: str, button_actions: Dict) -> None:
        """ Method to change Button functions and verify it

        @param device_name: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.verify_button_functions_label_displayed()

            self.tune_app.click_button_functions_label()

            Report.logInfo("1. Change each button function and verify it.")
            initial_single_press_function = self.tune_app.get_current_button_single_press_function()
            initial_double_press_function = self.tune_app.get_current_button_double_press_function()
            initial_long_press_function = self.tune_app.get_current_button_long_press_function()

            time.sleep(1)
            self.tune_app.click_single_press_label()
            new_single_press_function = choice(
                [i for i in button_actions["single_press"]["functions"] if i not in [initial_single_press_function]])
            self.tune_app.choose_new_button_function(new_single_press_function)

            time.sleep(1)
            self.tune_app.click_double_press_label()
            new_double_press_function = choice(
                [i for i in button_actions["double_press"]["functions"] if i not in [initial_double_press_function]])
            self.tune_app.choose_new_button_function(new_double_press_function)

            time.sleep(1)
            self.tune_app.click_long_press_label()
            new_long_press_function = choice(
                [i for i in button_actions["long_press"]["functions"] if i not in [initial_long_press_function]])
            self.tune_app.choose_new_button_function(new_long_press_function)

            time.sleep(1)
            updated_single_press_function = self.tune_app.get_current_button_single_press_function()
            updated_double_press_function = self.tune_app.get_current_button_double_press_function()
            updated_long_press_function = self.tune_app.get_current_button_long_press_function()

            if updated_single_press_function == new_single_press_function:
                Report.logPass(f"Single Press function updated")
            else:
                Report.logFail(f"Single Press function not updated: {updated_single_press_function} != {new_single_press_function}")
            if updated_double_press_function == new_double_press_function:
                Report.logPass(f"Double Press function updated")
            else:
                Report.logFail(f"Double Press function not updated: {updated_double_press_function} != {new_double_press_function}")
            if updated_long_press_function == new_long_press_function:
                Report.logPass(f"Long Press function updated", True)
            else:
                Report.logFail(f"Long Press function not updated: {updated_long_press_function} != {new_long_press_function}")

            time.sleep(1)
            functions_indexes = [ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[updated_long_press_function],
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[updated_single_press_function],
                                 0,
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[updated_double_press_function]]
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_button_functions_via_api(product_string=device_name,
                                                             conn_type=conn_type,
                                                             function_indexes=functions_indexes)
            else:
                self._bt_verify_button_functions_via_tune_ui(product_string=device_name,
                                                             single_press_function=new_single_press_function,
                                                             double_press_function=new_double_press_function,
                                                             long_press_function=new_long_press_function)

            time.sleep(1)
            Report.logInfo("2. Press Restore defaults and verify it.")
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)

            self.tune_app.click_button_functions_label()
            self.tune_app.click_restore_defaults_button()
            time.sleep(1)

            restored_single_press_function = self.tune_app.get_current_button_single_press_function()
            restored_double_press_function = self.tune_app.get_current_button_double_press_function()
            restored_long_press_function = self.tune_app.get_current_button_long_press_function()

            if restored_single_press_function == button_actions["single_press"]["default"]:
                Report.logPass(f"Single Press function restored to correct default value.")
            else:
                Report.logFail(f"Single Press function not restored to correct default value: {restored_single_press_function} != {button_actions['single_press']['default']}")
            if restored_double_press_function == button_actions["double_press"]["default"]:
                Report.logPass(f"Double Press function restored to correct default value.")
            else:
                Report.logFail(f"Double Press function not restored to correct default value: {restored_double_press_function} != {button_actions['double_press']['default']}")
            if restored_long_press_function == button_actions["long_press"]["default"]:
                Report.logPass(f"Long Press function restored to correct default value.", True)
            else:
                Report.logFail(f"Long Press function not restored to correct default value: {restored_long_press_function} != {button_actions['double_press']['default']}")

            time.sleep(1)
            functions_indexes = [ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[button_actions["long_press"]["default"]],
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[button_actions["single_press"]["default"]],
                                 0,
                                 ZONE_WIRELESS_PLUS_BUTTONS_MAPPING[button_actions["double_press"]["default"]]]
            self.tune_app.close_tune_app()
            time.sleep(5)
            if conn_type == 'bt':
                self._bt_spp_verify_button_functions_via_api(product_string=device_name,
                                                             conn_type=conn_type,
                                                             function_indexes=functions_indexes)
            else:
                self._bt_verify_button_functions_via_tune_ui(product_string=device_name,
                                                             single_press_function=button_actions["single_press"]["default"],
                                                             double_press_function=button_actions["double_press"]["default"],
                                                             long_press_function=button_actions["long_press"]["default"])

        except Exception as e:
            Report.logException(str(e))

    def _bt_spp_verify_button_functions_via_api(self, product_string: str, conn_type: str, function_indexes: List[int]) -> None:
        """ Method to verify over API the button functions.

        @param product_string: device name
        @param conn_type: type of connection, i.e. BT, DONGLE
        @param function_indexes: function indexes due to centurion++ protocol
        @return: None
        """

        com_port = self._get_centrion_com_port(device_name=product_string)
        self.centurion = CenturionCommands(device_name=product_string,
                                           conn_type=conn_type,
                                           com_port=com_port)
        self.features = Features(self.centurion)
        response = self.features.headset_misc_feature.get_button_general_settings()
        self.features.headset_misc_feature.verify_get_button_general_settings(response=response,
                                                                              button_index=0,
                                                                              long_press=function_indexes[0],
                                                                              short_press=function_indexes[1],
                                                                              tripple_press=function_indexes[2],
                                                                              double_press=function_indexes[3])
        self.centurion.close_port()

    def _bt_verify_sidetone(self, device_name: str, level: int) -> None:
        """ Method to change and verify sidetone level for BT connection without COM port
        @param device_name: device name
        @param level: new sidetone value
        @return: None
        """
        try:
            self.tune_app.close_tune_app()
            time.sleep(5)
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.click_sidetone()
            current_value = self.tune_app.get_sidetone_slider_value()
            self.tune_app.set_sidetone_slider(current_value)

            if current_value == level:
                Report.logPass("Sidetone value changed correctly.", True)
            else:
                Report.logFail("Sidetone value NOT changed correctly.")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_equalizer_profile_over_tune_ui(self, product_string: str, profile: str) -> None:
        """ Method to verify Equalizer state on device over Logitune UI for BT connection without COM port

        @param product_string: device name
        @param profile: new equalizer name
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=product_string)
            current_name = self.tune_app.get_equalizer_profile_name()
            if current_name == profile:
                Report.logPass("Equalizer changed correctly.", True)
            else:
                Report.logFail("Equalizer NOT changed correctly.")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_rotate_to_mute_over_tune_ui(self, product_string: str, state: bool) -> None:
        """ Method to change and verify Rotate to mute state for BT connection without COM port

        @param product_string: device name
        @param state: new rotate to mute state
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=product_string)
            self.tune_app.verify_rotate_to_mute_label_displayed()
            current_state = self.tune_app.get_rotate_to_mute_state()

            if current_state == state:
                Report.logPass("Rotate to mute state changed correctly.", True)
            else:
                Report.logFail("Rotate to mute state NOT changed correctly")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_voice_prompt(self, product_string: str, state: bool) -> None:
        """ Method to change and verify Voice Prompts state for BT connection without COM port

        @param product_string: device name
        @param state: new state
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=product_string)
            self.tune_app.verify_voice_prompts_displayed()
            current_state = self.tune_app.get_voice_prompts_state()
            if current_state == state:
                Report.logPass("Voice prompts state changed correctly.", True)
            else:
                Report.logFail("Voice prompts state NOT changed correctly.")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_sleep_timer(self, product_string: str, sleep_timer: int) -> None:
        """ Method to change Sleep timeout and verify it for BT connection without COM port

        @param product_string: device name
        @param sleep_timer: new sleep timeout value
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=product_string)
            self.tune_app.verify_sleep_settings_label_displayed()
            current_sleep_timeout = self.tune_app.get_current_sleep_settings_timeout()
            if current_sleep_timeout == sleep_timer:
                Report.logPass("Sleep timeout changed correctly.", True)
            else:
                Report.logFail("Sleep timeout NOT changed correctly.")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_button_functions_via_tune_ui(self, product_string: str, single_press_function: str, double_press_function: str, long_press_function: str) -> None:
        """ Method to change Button functions and verify it for BT connection without COM port

        @param product_string: device name
        @param single_press_function: new single press function
        @param double_press_function: new double press function
        @param long_press_function: new long press function
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=product_string)
            self.tune_app.verify_button_functions_label_displayed()
            self.tune_app.click_button_functions_label()
            current_single_press_function = self.tune_app.get_current_button_single_press_function()
            current_double_press_function = self.tune_app.get_current_button_double_press_function()
            current_long_press_function = self.tune_app.get_current_button_long_press_function()

            if current_single_press_function == single_press_function:
                Report.logPass(f"Single Press function updated", True)
            else:
                Report.logFail(f"Single Press function not updated: {current_single_press_function} != {single_press_function}")
            if current_double_press_function == double_press_function:
                Report.logPass(f"Double Press function updated")
            else:
                Report.logFail(f"Double Press function not updated: {current_double_press_function} != {double_press_function}")
            if current_long_press_function == long_press_function:
                Report.logPass(f"Long Press function updated", True)
            else:
                Report.logFail(f"Long Press function not updated: {current_long_press_function} != {long_press_function}")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_noise_cancellation(self, product_string: str, state: bool) -> None:
        """ Method to change and verify Noise cancellation state for BT connection without COM port

        @param product_string: device name
        @param state: new state
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=product_string)
            self.tune_app.verify_noise_cancellation_displayed()
            current_state = self.tune_app.get_noise_cancellation_state()
            if current_state == state:
                Report.logPass("Noise cancellation state changed correctly.", True)
            else:
                Report.logFail("Noise cancellation state NOT changed correctly.")

        except Exception as e:
            Report.logException(str(e))

    def _bt_verify_device_name(self, product_string: str, device_name: str, name_max_len: int) -> None:
        """ Method to change Device Name and verify it for BT connection without COM port

        @param product_string: default device name
        @param device_name: new name
        @param name_max_len: name max length
        @return: None
        """
        try:
            self.tune_app.connect_tune_app()
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            current_name = self.tune_app.get_device_name_from_settings_page()
            if current_name == device_name:
                Report.logPass("Device name changed correctly.", True)
            else:
                Report.logFail("Device name NOT changed correctly.")

        except Exception as e:
            Report.logException(str(e))

    def set_never_sleep_timer_ui(self, product_string: str) -> None:
        """ Method to set Sleep Timeout equal to Never (0) through tune UI

        @return: None
        """
        self.tune_app.connect_tune_app()
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=product_string)
        self.tune_app.click_current_sleep_settings_timeout()
        self.tune_app.choose_new_sleep_timeout(0)

    def tc_logi_dock_pair_headset(self) -> None:
        """Method to pair headset with logi dock through tune app

        @return: None
        """
        self.tune_app.connect_tune_app()
        self.tune_app.click_my_devices()

        # Check if there's headset conncected
        if self.tune_app.verify_dock_headset_paired():
            self.tc_logi_dock_unpair_headset()

        self.tune_app.click_logi_dock_pair_headset()
        self.tune_app.click_logi_dock_pair_continue_button()
        self.tune_app.verify_element(TunesAppLocators.LOGI_DOCK_DONE_BTN, wait_for_visibility=True)
        self.tune_app.click_logi_dock_pair_done_button()

    def tc_logi_dock_unpair_headset(self) -> None:
        """Method to unpair headset with logi dock through tune app

        :return None
        """
        self.tune_app.connect_tune_app()
        self.tune_app.click_my_devices()
        self.tune_app.click_logi_dock_unpair_headset()
        self.tune_app.click_logi_dock_unpair_button()

    def tc_headset_enter_pairing_mode(self, device_name: str) -> None:
        """
        Method to set headset to pairing mode

        @param device_name: device name
        :return None
        """
        power_on_btn = ""
        power_off_btn = ""
        pair_btn = ""
        serial_num = ""
        if device_name == "Zone Wireless 2":
            pid = 0x0AFA
            usage_page = 65280

            hid_command = UsbHidCommunicationBase(device_name=device_name)
            Report.logInfo(f"Start {device_name} bluetooth connection.")
            hid_command.power_on(pid=pid, usage_page=usage_page)
            time.sleep(5)
            hid_command.pairing(pid=pid, usage_page=usage_page)
        else:
            if device_name == "Zone Vibe 125":
                serial_num = ENDURO_RELAY_BOARD_SERIAL_NUMBER
                power_on_btn = ENDURO_POWER_ON_BUTTON
                power_off_btn = ENDURO_POWER_OFF_BUTTON
                pair_btn = ENDURO_POWER_PAIR_BUTTON
            elif device_name == "Zone Vibe 130":
                serial_num = ZV130_RELAY_BOARD_SERIAL_NUMBER
                power_on_btn = ZV130_POWER_ON_BUTTON
                power_off_btn = ZV130_POWER_OFF_BUTTON
                pair_btn = ZV130_POWER_PAIR_BUTTON
            elif device_name == "Zone Vibe Wireless":
                serial_num = ZONE_VIBE_WIRELESS_RELAY_BOARD_SERIAL_NUMBER
                power_on_btn = ZONE_VIBE_WIRELESS_ON_BUTTON
                power_off_btn = ZONE_VIBE_WIRELESS_OFF_BUTTON
                pair_btn = ZONE_VIBE_WIRELESS_PAIR_BUTTON

            relay_control = GenericRelayControl()
            comport = relay_control.get_relay_com_port(serial_num)
            relay_control.connect_relay(comport)
            relay_control.press_btn(power_off_btn, 3)
            relay_control.press_btn(power_on_btn, 1)
            relay_control.press_btn(pair_btn, 3)

    def tc_detect_logi_dock_pairing_headsets(self, dock_name: str, device_name: str) -> None:
        """
        Method to detect headset pair with logi dock

        @param dock_name: logi dock name
        @param device_name: headset device name
        :return None
        """
        try:
            disconnect_all()
            connect_device(dock_name)
            self.tc_headset_enter_pairing_mode(device_name=device_name)
            self.tc_logi_dock_pair_headset()
            if self.tune_app.verify_device_name_displayed(device_name) and self.tune_app.verify_dock_headset_paired():
                Report.logPass(f'Device {device_name} paired and shown in tune')
            elif self.tune_app.verify_dock_headset_paired():
                Report.logFail(f'Device {device_name} paired but not shown in tune')
            else:
                Report.logFail(f'Device {device_name} pairing FAILED')

        except Exception as e:
            Report.logException(str(e))

    def tc_pair_headset_with_dongle(self, device_name: str, receiver_name: str) -> None:
        """Method to pair headset with dongle

        @param device_name: device name
        @param receiver_name: receiver name
        """
        disconnect_all()
        connect_device(device_name=device_name)
        self.tune_app.connect_tune_app()
        self.tune_app.click_my_devices()
        self.tune_app.click_receiver_to_pair(receiver_name=receiver_name)
        self.tune_app.click_dongle_pair_headset()
        time.sleep(5)
        self.tc_headset_enter_pairing_mode(device_name=device_name)
        self.tune_app.click_dongle_pair_continue()
        self.tune_app.verify_element(TunesAppLocators.DONGLE_PAIR_DONE_BUTTON, wait_for_visibility=True)
        self.tune_app.click_dongle_pair_done()

    def tc_in_ear_detection(self, device_name: str, conn_type: str) -> None:
        try:
            self.tune_app.connect_tune_app(device_name=device_name)
            self.tune_app.click_my_devices()
            self.tune_app.click_device(device_name=device_name)
            self.tune_app.verify_in_ear_detection_label_displayed()
            # 1. Verify in ear detection current state
            in_ear_state = self.tune_app.get_in_ear_detection_state()
            Report.logInfo(f"In-ear detection is: {in_ear_state}")
            self._verify_auto_pause(product_string=device_name,
                                    conn_type=conn_type,
                                    state=in_ear_state)

            # 2. Click in ear detection toggle and verify again
            self.tune_app.click_in_ear_detection_toggle()
            in_ear_state_new = self.tune_app.get_in_ear_detection_state()
            Report.logInfo(f"In-ear detection state after clicking toggle is: {in_ear_state_new}")
            self._verify_auto_pause(product_string=device_name,
                                    conn_type=conn_type,
                                    state=in_ear_state_new)

        except Exception as e:
            Report.logException(str(e))

    def tc_install_logi_sync_personal_collab_service(self) -> None:
        """
        Installs Logi Sync Personal Collab service and verifies the connection status in Logi Tune.

        Returns:
            None

        Example Usage:
            tc_install_logi_sync_personal_collab_service()
        """
        try:
            from apps.tune.logi_sync_personal_collab.install_logi_sync_personal_collab import \
                InstallLogiSyncPersonalCollab

            self.tune_app.open_tune_app(clean_logs=True)

            installer = InstallLogiSyncPersonalCollab()
            result = installer.install_logi_sync_personal_collab()
            if result:
                Report.logPass("LogiSyncPersonalCollab service successfully installed.")
            else:
                assert False, Report.logFail("LogiSyncPersonalCollab service NOT installed!")

            Report.logInfo("Verify Sync Portal connection in Logi Tune.")
            self.tune_app.click_tune_menu()
            self.tune_app.click_about_menu()
            result = self.tune_app.verify_tune_sync_connected()
            if result:
                Report.logPass("Logi Tune shows correct Helvellyn connection status.", screenshot=True)
            else:
                Report.logFail("Logi Tune DOES NOT shows correct Helvellyn connection status.")

        except Exception as e:
            Report.logException(str(e))

    def tc_uninstall_logi_sync_personal_collab_service(self) -> None:
        """
        Uninstall Logi Sync Personal Collab Service

        This method uninstalls the Logi Sync Personal Collab service by performing the following steps:
        1. Opens the Logi Tune app.
        2. Calls the `uninstall_logi_sync_personal_collab` method from the `InstallLogiSyncPersonalCollab` class to uninstall the service.
        3. Logs a pass message if the uninstallation is successful, or logs an exception if it fails.
        4. Clicks the Tune menu and then clicks the About menu.
        5. Verifies that the Tune app does not display the sync connection status.
        6. Logs a pass message if the verification is successful, or logs an exception if it fails.

        Parameters:
        - self : This instance of the class.

        Returns:
        None
        """
        try:
            from apps.tune.logi_sync_personal_collab.install_logi_sync_personal_collab import \
                InstallLogiSyncPersonalCollab

            self.tune_app.open_tune_app()

            installer = InstallLogiSyncPersonalCollab()
            result = installer.uninstall_logi_sync_personal_collab()
            if result:
                Report.logPass("LogiSyncPersonalCollab service successfully uninstalled.")
            else:
                Report.logException("LogiSyncPersonalCollab uninstallation failed")

            self.tune_app.click_tune_menu()
            self.tune_app.click_about_menu()
            result = self.tune_app.verify_tune_does_not_display_sync_connection_status()
            if result:
                Report.logPass("Logi Tune shows correct Helvellyn connection status: service disconnected",
                               screenshot=True)
            else:
                Report.logException("Logi Tune DOES NOT shows correct Helvellyn connection status.")
        except Exception as e:
            Report.logException(str(e))
