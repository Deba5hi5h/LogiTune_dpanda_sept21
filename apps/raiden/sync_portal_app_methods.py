import time

from apps.raiden.sync_portal_inventory import SyncPortalInventory
from apps.raiden.sync_portal_methods import SyncPortalMethods
from base import global_variables, base_settings
from base.base_ui import UIBase
from config.aws_helper import AWSHelper
from extentreport.report import Report


class SyncPortalAppMethods(SyncPortalMethods):
    """
    Sync Portal methods used my Sync App test cases
    """

    def verify_device_added_in_sync_portal(self, device_name: str, room_name: str, close_browser: bool = True):
        """
        Method to verify device appears in Room in Sync Portal

        :param device_name: e.g. Rally Bar Mini, Sync Portal Room Name
        :param room_name:
        :param close_browser:
        return none
        """
        driver = global_variables.driver
        try:
            inventory = SyncPortalMethods() \
                .login_to_sync_portal(global_variables.config, global_variables.SYNC_ROLE)
            device_list = inventory.get_list_of_devices_in_room(room_name=room_name)
            refresh_count = 5
            while refresh_count > 0:
                if device_name in device_list:
                    break
                else:
                    time.sleep(5)
                    self.browser.refresh()
                    refresh_count -= 1
                    device_list = inventory.get_list_of_devices_in_room(room_name=room_name)
            if device_name in device_list:
                Report.logPass(f"{device_name} is added in Sync Portal Inventory", True)
            else:
                Report.logWarning(f"{device_name} is not added in Sync Portal Inventory", True)
            if inventory.click_on_inventory_room(room_name=room_name) \
                    .verify_device_exists_in_room(device_name=device_name):
                Report.logPass(f"{device_name} is added in Sync Portal Room", True)
            else:
                Report.logFail(f"{device_name} is not added in Sync Portal Room")
        except Exception as e:
            Report.logException(str(e))
        if close_browser:
            self.browser.close_browser()
            global_variables.driver = driver

    def verify_devices_added_in_sync_portal(self, devices: list, room_name: str):
        """
        Method to verify all device appear in Room in Sync Portal

        :param devices:
        :param room_name:
        :return none
        """
        driver = global_variables.driver
        try:
            time.sleep(base_settings.PORTAL_TIMEOUT)
            inventory = SyncPortalMethods() \
                .login_to_sync_portal(global_variables.config, global_variables.SYNC_ROLE)
            device_list = inventory.get_list_of_devices_in_room(room_name=room_name)
            flag = True
            for d1 in devices:
                if d1 in device_list:
                    pass
                else:
                    flag = False
            if flag:
                Report.logPass("All devices exist in Sync Portal Inventory", True)
            else:
                Report.logWarning("Not all devices exist in Sync Portal Inventory", True)
            room = inventory.click_on_inventory_room(room_name=room_name)
            flag = True
            for d1 in devices:
                if not room.verify_device_exists_in_room(d1):
                    flag = False
            if flag:
                Report.logPass("All devices exist in Sync Portal Room", True)
            else:
                Report.logFail("Not all devices added in Sync Portal")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_device_deleted_in_sync_portal(self, device_name, room_name):
        """
        Method to verify device is removed from Sync Portal

        :param device_name: e.g. Rally Bar Mini, Sync Portal Room Name
        :param room_name:
        :return none
        """
        driver = global_variables.driver
        try:
            inventory = SyncPortalMethods() \
                .login_to_sync_portal(global_variables.config, global_variables.SYNC_ROLE)
            device_list = inventory.get_list_of_devices_in_room(room_name=room_name)
            refresh_count = 5
            while refresh_count > 0:
                if device_name in device_list:
                    time.sleep(5)
                    self.browser.refresh()
                    refresh_count -= 1
                    device_list = inventory.get_list_of_devices_in_room(room_name=room_name)
                else:
                    break
            if device_name in device_list:
                Report.logWarning(f"{device_name} is not removed from Sync Portal Inventory", True)
            else:
                Report.logPass(f"{device_name} is removed from Sync Portal Inventory", True)
            if inventory.click_on_inventory_room(room_name=room_name) \
                    .verify_device_exists_in_room(device_name=device_name):
                Report.logFail(f"{device_name} is not removed from Sync Portal Room")
            else:
                Report.logPass(f"{device_name} is removed from Sync Portal Room", True)
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_columns_in_rooms_tab(self, room_name: str, device_list, status, health, use_state):
        """
        Method to verify columns and status in Inventory Page

        :param use_state:
        :param health:
        :param status:
        :param device_list:
        :param room_name:str:
        :return none:
        """
        try:
            inventory = SyncPortalInventory()
            inventory.search(search_text=room_name)
            self._verify_columns()
            if inventory.verify_group_header_displayed():
                Report.logPass("Group Header displayed")
            else:
                Report.logFail("Group Header not displayed")
            if inventory.verify_device_header_displayed():
                Report.logPass("Devices Header displayed")
            else:
                Report.logFail("Devices Header not displayed")
            devices = inventory.get_list_of_devices_in_room(room_name=room_name)
            for device in device_list:
                if device in devices:
                    Report.logPass(f"{device} device displayed under Devices")
                else:
                    Report.logWarning(device + " device not displayed under Devices")
            if inventory.verify_sync_version_header_displayed():
                Report.logPass("Sync Version Header displayed")
            else:
                Report.logFail("Sync Version Header not displayed")
            room_status = inventory.get_room_status(room_name=room_name)
            if room_status == status:
                Report.logPass(f"{status} displayed under Status")
            else:
                Report.logWarning(f"{room_status} instead of {status} displayed under Status")
            room_health = inventory.get_room_health(room_name=room_name)
            if room_health == health:
                Report.logPass(f"{health} displayed under Health")
            else:
                Report.logWarning(f"{room_health} instead of {health} displayed under Health")

            room_use_state = inventory.get_room_use_state(room_name=room_name)
            if room_use_state == use_state:
                Report.logPass(f"{use_state} displayed under Use State")
            else:
                Report.logFail(f"{room_use_state} instead of {use_state} displayed under Use State")
            if inventory.verify_seat_count_header_displayed():
                Report.logPass("Seat Count Header displayed", True)
            else:
                Report.logFail("Seat Count Header not displayed")
        except Exception as e:
            Report.logException(str(e))
            raise e

    def verify_columns_in_devices_tab(self, room_name: str,
                                      device_name, device_health, device_status, device_use_state):
        """
        Method to verify columns and status in Inventory devices tab

        :param device_use_state:
        :param device_status:
        :param device_health:
        :param device_name:
        :param room_name:str:
        :return
        """
        try:
            inventory = SyncPortalInventory()
            inventory.click_on_devices_tab()
            inventory.search(search_text=room_name)
            self._verify_columns()
            health = inventory.get_device_health(device_name=device_name)
            if str(health).upper() == str(device_health).upper():
                Report.logPass(f"{device_health} displayed under Health for {device_name}")
            else:
                Report.logWarning(f"{device_health} not displayed under Health for {device_name}")
            status = inventory.get_device_status(device_name=device_name)
            if str(status).upper() == str(device_status).upper():
                Report.logPass(f"{device_status} displayed under Status for {device_name}")
            else:
                Report.logFail(f"{device_status} not displayed under Status for {device_name}")
            use_state = inventory.get_device_use_state(device_name=device_name)
            if str(use_state).upper() == str(device_use_state).upper():
                Report.logPass(f"{device_use_state} displayed under Use State for {device_name}", True)
            else:
                Report.logFail(f"{device_use_state} not displayed under Use State for {device_name}")
        except Exception as e:
            Report.logException(str(e))
            raise e

    def _verify_columns(self):
        inventory = SyncPortalInventory()
        if inventory.verify_room_header_displayed():
            Report.logPass("Room Header displayed")
        else:
            Report.logFail("Room Header not displayed")
        if inventory.verify_status_header_displayed():
            Report.logPass("Status Header displayed")
        else:
            Report.logFail("Status Header not displayed")
        if inventory.verify_health_header_displayed():
            Report.logPass("Health Header displayed")
        else:
            Report.logFail("Health Header not displayed")
        if inventory.verify_use_state_header_displayed():
            Report.logPass("Use State Header displayed")
        else:
            Report.logFail("Use State Header not displayed")

    def verify_anti_flicker_in_sync_portal(self, device_name, room_name, antiflicker):
        """
        Method to verify Anti-flicker NTSC/PAL in Sync Portal

        :param antiflicker: NTSC or PAL
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return none
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            if str(antiflicker).upper() == "NTSC":
                if room.verify_anti_flicker_ntsc_selected():
                    Report.logPass("Sync Portal: Anti-Flicker NTSC 60Hz is enabled", True)
                else:
                    Report.logFail("Sync Portal:Anti-flicker NTSC 60Hz is disabled")
            else:
                if room.verify_anti_flicker_pal_selected():
                    Report.logPass("Sync Portal: Anti-Flicker PAL 50Hz is enabled", True)
                else:
                    Report.logFail("Sync Portal: Anti-flicker PAL 50Hz is disabled")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_anti_flicker_in_sync_portal(self, device_name, room_name, antiflicker):
        """
        Method to set Anti-flicker NTSC/PAL in Sync Portal

        :param antiflicker: NTSC or PAL
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return none
        """

        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            if str(antiflicker).upper() == "NTSC":
                room.click_anti_flicker_ntsc()
            else:
                room.click_anti_flicker_pal()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_bluetooth_in_sync_portal(self, device_name, room_name, bluetooth):
        """
        Method to verify bluetooth is ON/OFF in Sync Portal

        :param bluetooth: ON or OFF
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_connectivity(device_name=device_name)
            if str(bluetooth).upper() == "ON" and room.verify_bluetooth_enabled():
                Report.logPass("Sync Portal: Bluetooth is enabled", True)
            elif str(bluetooth).upper() == "OFF" and not room.verify_bluetooth_enabled():
                Report.logPass("Sync Portal: Bluetooth is disabled", True)
            else:
                Report.logFail("Sync Portal: Bluetooth status is incorrect", True)
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_bluetooth_in_sync_portal(self, device_name, room_name, bluetooth):
        """
        Method to toggle bluetooth in Sync Portal

        :param bluetooth: ON or OFF
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_connectivity(device_name=device_name)
            if str(bluetooth).upper() == "ON":
                room.enable_bluetooth()
            else:
                room.disable_bluetooth()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_speaker_boost_in_sync_portal(self, device_name, room_name, speaker_boost):
        """
        Method to verify Speaker Boost is ON/OFF in Sync Portal

        :param speaker_boost: ON or OFF
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(speaker_boost).upper() == "ON" and room.verify_speaker_boost_enabled():
                Report.logPass("Sync Portal: Speaker Boost is enabled", True)
            elif str(speaker_boost).upper() == "OFF" and not room.verify_speaker_boost_enabled():
                Report.logPass("Sync Portal: Speaker Boost is disabled", True)
            else:
                Report.logFail("Sync Portal: Speaker Boost status is incorrect")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_speaker_boost_in_sync_portal(self, device_name, room_name, speaker_boost):
        """
        Method to enable or disable Speaker Boost in Sync Portal

        :param speaker_boost: ON or OFF
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(speaker_boost).upper() == "ON":
                room.enable_speaker_boost()
            else:
                room.disable_speaker_boost()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_ai_noise_suppression_in_sync_portal(self, device_name, room_name, noise_suppression):
        """
        Method to check Audio AI Noise Suppression ON/OFF in Sync Portal

        :param noise_suppression: ON or OFF
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(noise_suppression).upper() == "ON" and room.verify_ai_noise_suppression_enabled():
                Report.logPass("Sync Portal: AI Noise Suppression is enabled", True)
            elif str(noise_suppression).upper() == "OFF" and not room.verify_ai_noise_suppression_enabled():
                Report.logPass("Sync Portal: AI Noise Suppression is disabled", True)
            else:
                Report.logFail("Sync Portal: AI Noise Suppression status is incorrect")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_ai_noise_suppression_in_sync_portal(self, device_name, room_name, noise_suppression):
        """
        Method to toggle AI Noise Supression in Sync Portal

        :param noise_suppression: ON or OFF
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(noise_suppression).upper() == "ON":
                room.enable_ai_noise_suppression()
            else:
                room.disable_ai_noise_suppression()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_reverb_control_in_sync_portal(self, device_name, room_name, reverb_control):
        """
        Method to check Audio Reverb Control Disabled/Normal/Agressive in Sync Portal

        :param reverb_control: Disabled, Normal, or Agressive
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(reverb_control).upper() == "DISABLED" and \
                    room.verify_reverb_control_disable_selected(refresh_count=5):
                Report.logPass("Sync Portal: Reverb Control Disable is selected", True)
            elif str(reverb_control).upper() == "NORMAL" and \
                    room.verify_reverb_control_normal_selected(refresh_count=5):
                Report.logPass("Sync Portal: Reverb Control Normal is selected", True)
            elif str(reverb_control).upper() == "AGGRESSIVE" and \
                    room.verify_reverb_control_aggressive_selected(refresh_count=5):
                Report.logPass("Sync Portal: Reverb Control Aggressive is selected", True)
            else:
                Report.logFail("Sync Portal: Incorrect Reverb Control option is selected")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_reverb_control_in_sync_portal(self, device_name, room_name, reverb_control):
        """
        Method to set Audio Reverb Control to Disabled/Normal/Agressive in Sync Portal

        :param reverb_control: Disabled, Normal, or Agressive
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(reverb_control).upper() == "DISABLED":
                room.set_reverb_control_disable()
            elif str(reverb_control).upper() == "NORMAL":
                room.set_reverb_control_normal()
            elif str(reverb_control).upper() == "AGGRESSIVE":
                room.set_reverb_control_aggressive()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_microphone_eq_in_sync_portal(self, device_name, room_name, microphone_eq):
        """
        Method to check Audio Microphone EQ Bass Boost/Normal/Voice Boost in Sync Portal

        :param microphone_eq: Bass Boost, Normal or Voice Boost
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(microphone_eq).upper() == "BASS BOOST" and \
                    room.verify_microphone_bass_boost_selected(refresh_count=5):
                Report.logPass("Sync Portal: Microphone EQ Bass Boost is selected", True)
            elif str(microphone_eq).upper() == "NORMAL" and room.verify_microphone_normal_selected(refresh_count=5):
                Report.logPass("Sync Portal: Microphone EQ Normal is selected", True)
            elif str(microphone_eq).upper() == "VOICE BOOST" \
                    and room.verify_microphone_voice_boost_selected(refresh_count=5):
                Report.logPass("Sync Portal: Microphone EQ Voice Boost is selected", True)
            else:
                Report.logFail("Sync Portal: Incorrect Microphone EQ option selected")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_microphone_eq_in_sync_portal(self, device_name, room_name, microphone_eq):
        """
        Method to set Audio Microphone EQ to Bass Boost/Normal/Voice Boost in Sync Portal

        :param microphone_eq: Bass Boost, Normal or Voice Boost
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(microphone_eq).upper() == "BASS BOOST":
                room.set_microphone_bass_boost()
            elif str(microphone_eq).upper() == "NORMAL":
                room.set_microphone_normal()
            elif str(microphone_eq).upper() == "VOICE BOOST":
                room.set_microphone_voice_boost()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_speaker_eq_in_sync_portal(self, device_name, room_name, speaker_eq):
        """
        Method to check Audio Speaker EQ Bass Boost/Normal/Voice Boost in Sync Portal

        :param microphone_eq: Bass Boost, Normal or Voice Boost
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(speaker_eq).upper() == "BASS BOOST" and \
                    room.verify_speaker_bass_boost_selected(refresh_count=5):
                Report.logPass("Sync Portal: Speaker EQ Bass Boost is selected", True)
            elif str(speaker_eq).upper() == "NORMAL" and room.verify_speaker_normal_selected(refresh_count=5):
                Report.logPass("Sync Portal: Speaker EQ Normal is selected", True)
            elif str(speaker_eq).upper() == "VOICE BOOST" \
                    and room.verify_speaker_voice_boost_selected(refresh_count=5):
                Report.logPass("Sync Portal: Speaker EQ Voice Boost is selected", True)
            else:
                Report.logFail("Sync Portal: Incorrect Speaker EQ option selected")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_speaker_eq_in_sync_portal(self, device_name, room_name, speaker_eq):
        """
        Method to set Audio Speaker EQ to Bass Boost/Normal/Voice Boost in Sync Portal

        :param microphone_eq: Bass Boost, Normal or Voice Boost
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_audio(device_name=device_name)
            if str(speaker_eq).upper() == "BASS BOOST":
                room.set_speaker_bass_boost()
            elif str(speaker_eq).upper() == "NORMAL":
                room.set_speaker_normal()
            elif str(speaker_eq).upper() == "VOICE BOOST":
                room.set_speaker_voice_boost()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def forget_device_in_sync_portal(self, device_name, room_name):
        """
        Method to forget device from Sync Portal

        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device(device_name=device_name) \
                .click_lets_fix_it() \
                .click_forget() \
                .click_forget_now()
            if room.verify_device_forget_message():
                Report.logPass("Device Forget message displayed", True)
            else:
                Report.logFail("Device Forget message not displayed")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_rightsight2_in_sync_portal(self, device_name: str, room_name: str,
                                          group_view: bool, speaker_view: bool, picture_in_picture: bool = None):
        """
        Method to verify Speaker View or Group View is selected and
        picture in picture is enabled or disabled in Sync Portal

        :param picture_in_picture:
        :param speaker_view:
        :param group_view:
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            if group_view:
                if room.verify_group_view_selected(refresh_count=5):
                    Report.logPass("Sync Portal: Group View is selected")
                else:
                    Report.logFail("Sync Portal: Group View is not selected")
            if speaker_view:
                if room.verify_speaker_view_selected(refresh_count=5):
                    Report.logPass("Sync Portal: Speaker View is selected")
                else:
                    Report.logFail("Sync Portal: Speaker View is selected")
            if picture_in_picture is not None and picture_in_picture:
                if room.verify_picture_in_picture(refresh_count=5):
                    Report.logPass("Sync Portal: Picture In Picture is enabled")
                else:
                    Report.logFail("Sync Portal: Picture In Picture is disabled")
            elif picture_in_picture is not None and not picture_in_picture:
                if room.verify_picture_in_picture(refresh_count=5, enabled=False):
                    Report.logPass("Sync Portal: Picture In Picture is disabled")
                else:
                    Report.logFail("Sync Portal: Picture In Picture is enabled")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_rightsight2_in_sync_portal(self, device_name: str, room_name: str, group_view: bool,
                                       speaker_view: bool, picture_in_picture: bool = None):
        """
        Method to set Speaker View or Group View and picture in picture enabled/disabled in Sync Portal

        :param picture_in_picture:
        :param speaker_view:
        :param group_view:
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            if group_view:
                room.set_group_view()
            if speaker_view:
                room.set_speaker_view()
                if picture_in_picture:
                    room.enable_picture_in_picture()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_rightsight_in_sync_portal(self, device_name: str, room_name: str, rightsight: bool) -> None:
        """
        Method to verify RightSight Enable/Disable in Sync Portal

        :param rightsight: True/False
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            if rightsight:
                if room.verify_rightsight2():
                    Report.logPass("Sync Portal: Right Sight 2 is enabled")
                else:
                    Report.logFail("Sync Portal: Right Sight 2 is disabled")
            else:
                if room.verify_rightsight2(enabled=False):
                    Report.logPass("Sync Portal: Right Sight 2 is disabled")
                else:
                    Report.logFail("Sync Portal: Right Sight 2 is enabled")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_speaker_detection_framing_speed_in_sync_portal(self, device_name: str, room_name: str,
                                                              framing_speed: str, speaker_detection: str = None,
                                                              view: str = None):
        """
        Method to verify Speaker Detection/Framing Speed option selected/unslected in Sync Portal

        :param view: Speaker or Group
        :param speaker_detection: Slow, Default or Fast
        :param framing_speed: Slow, Default or Fast
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            if str(view).upper() == "SPEAKER":
                room.set_speaker_view()
                room.verify_framing_speed_fast_selected()
                room.set_group_view()
                time.sleep(5)
            elif str(view).upper() == "GROUP":
                room.set_group_view()
                room.verify_framing_speed_fast_selected()
                room.set_speaker_view()
                time.sleep(5)
            if speaker_detection is not None:
                if str(speaker_detection).upper() == "SLOW":
                    room.verify_speaker_detection_slow_selected()
                elif str(speaker_detection).upper() == "DEFAULT":
                    room.verify_speaker_detection_default_selected()
                elif str(speaker_detection).upper() == "FAST":
                    room.verify_speaker_detection_fast_selected()
            if str(framing_speed).upper() == "SLOW":
                room.verify_framing_speed_slow_selected()
            elif str(framing_speed).upper() == "DEFAULT":
                room.verify_framing_speed_default_selected()
            elif str(framing_speed).upper() == "FAST":
                room.verify_framing_speed_fast_selected()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_speaker_detection_framing_speed_in_sync_portal(self, device_name: str, room_name: str,
                                                           framing_speed: str, speaker_detection: str = None,
                                                           view: str = None):
        """
        Method to set Speaker Detection/Framing Speed option in Sync Portal

        :param view: Speaker or Group
        :param speaker_detection: Slow, Default or Fast
        :param framing_speed: Slow, Default or Fast
        :param room_name:
        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device_camera(device_name=device_name)
            time.sleep(5)
            if str(view).upper() == "SPEAKER":
                room.set_speaker_view()
                room.set_framing_speed_default()
                room.set_group_view()
                time.sleep(10)
            elif str(view).upper() == "GROUP":
                room.set_group_view()
                room.set_framing_speed_default()
                room.set_speaker_view()
                time.sleep(10)
            if speaker_detection is not None:
                if str(speaker_detection).upper() == "SLOW":
                    room.set_speaker_detection_slow()
                elif str(speaker_detection).upper() == "DEFAULT":
                    room.set_speaker_detection_default()
                elif str(speaker_detection).upper() == "FAST":
                    room.set_speaker_detection_fast()
            if str(framing_speed).upper() == "SLOW":
                room.set_framing_speed_slow()
            elif str(framing_speed).upper() == "DEFAULT":
                room.set_framing_speed_default()
            elif str(framing_speed).upper() == "FAST":
                room.set_framing_speed_fast()
        except Exception as e:
            Report.logException(str(e))
        time.sleep(2)
        self.browser.close_browser()
        global_variables.driver = driver

    def create_empty_room_and_get_provision_code(self, room_name) -> str:
        """
        Method to create an empty room on the sync portal and get the provision code

        :param room_name(str)
        :return provision_code(str)
        """
        inventory = self.login_to_sync_portal_and_create_empty_room(config=global_variables.config,
                                                                    role=global_variables.SYNC_ROLE,
                                                                    room_name=room_name, seat_count=5)
        refresh_count = 12
        while refresh_count > 0:
            ui_status = self.verify_room_displayed_in_inventory_search(room_name=room_name)
            if ui_status:
                break
            else:
                time.sleep(5)
                self.browser.refresh()
                refresh_count -= 1
        provision_code = inventory.click_on_inventory_room(room_name=room_name).get_room_provision_code()
        self.browser.close_browser()
        return provision_code

    def get_provision_code_from_existing_room(self, room_name) -> str:
        """
        Method to get the provision code from an existing room

        :param :room_name: str
        :return :provision_code: str
        """
        provision_code = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                                 role=global_variables.SYNC_ROLE, room_name=room_name) \
            .click_provision() \
            .get_room_provision_code()
        self.browser.close_browser()
        return provision_code

    def get_room_information(self, room_name: str) -> dict:
        """
        Method to get Computer information displayed in Sync Portal

        :param :room_name: str
        :return:
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_computer().click_room_info()
            room_info = {"sync_app_version": room.get_menu_item_value(item_name="Sync App version"),
                         "computer_type": room.get_menu_item_value(item_name="Computer type"),
                         "operating_system": room.get_menu_item_value(item_name="Operating System"),
                         "os_version": room.get_menu_item_value(item_name="OS Version"),
                         "processor": room.get_menu_item_value(item_name="Processor"),
                         "memory": room.get_menu_item_value(item_name="Memory")}
            Report.logPass("Capturing Computer Information from Sync Portal", True)
            UIBase.report_flag = False
            room.click_page()
            self.browser.close_browser()
            global_variables.driver = driver
            return room_info
        except Exception as e:
            Report.logException(str(e))
            self.browser.close_browser()
            global_variables.driver = driver
            raise e

    def get_device_information(self, room_name: str, device_name: str, update_flag: bool = False) -> dict:
        """
        Method to get Device information displayed from Sync Portal

        :param :room_name: str
        :param :device_name: str
        :return: dict
        """
        driver = global_variables.driver
        try:
            room = self.login_to_sync_portal_and_open_room(config=global_variables.config,
                                                           role=global_variables.SYNC_ROLE, room_name=room_name) \
                .select_device(device_name=device_name)
            if update_flag:
                if room.verify_firmware_update_available():
                    Report.logPass("Firmware Update Available displayed", True)
                else:
                    Report.logFail("Firmware Update Available displayed")
            room.click_room_info()
            device_info = {}
            device_info["PID"] = room.get_menu_item_value(item_name="PID")
            device_info["BLE_Firmware"] = room.get_menu_item_value(item_name="BLE Firmware")
            device_info["EEPROM_Firmware"] = room.get_menu_item_value(item_name="EEPROM Firmware")
            device_info["Video_Firmware"] = room.get_menu_item_value(item_name="Video Firmware")
            if device_name.upper() == "MEETUP":
                device_info["Audio_Firmware"] = room.get_menu_item_value(item_name="Audio Firmware")
                device_info["Codec_Firmware"] = room.get_menu_item_value(item_name="Codec Firmware")
            Report.logPass(f"Capturing {device_name} Information from Sync Portal", True)
            UIBase.report_flag = False
            room.click_page()
            self.browser.close_browser()
            global_variables.driver = driver
            return device_info
        except Exception as e:
            Report.logException(str(e))
            self.browser.close_browser()
            global_variables.driver = driver
            raise e

    def change_org_and_change_user_role(self, org_name: str, org_role: str, user: str, role: str):
        """
        Method to login to Sync Portal, Change Org and change user role

        :param :org_name
        :param :org_role
        :param :user
        :param :role
        :return:
        """
        driver = global_variables.driver
        try:
            self.login_to_sync_portal(config=global_variables.config, role=org_role)
            self.change_org(org_name=org_name)
            self.change_user_role(user=user, role=role)
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver
