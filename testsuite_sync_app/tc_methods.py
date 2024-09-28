from datetime import datetime

from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_sync_app_methods import LNASyncAppMethods
from apps.meeting.google_meet import GoogleMeet
from apps.raiden.sync_portal_app_methods import SyncPortalAppMethods
from apps.raiden.sync_portal_inventory import SyncPortalInventory
from apps.sync.AppInstall import AppInstall
from apps.sync.sync_app_methods import SyncAppMethods
from apps.sync import sync_config
from base.base_ui import UIBase
from common.image_settings import get_image_settings
from common.platform_helper import get_custom_platform
from common.usb_switch import *


class SyncTCMethods(UIBase):
    sync_app = SyncAppMethods()
    sync_portal = SyncPortalAppMethods()
    lna = LNASyncAppMethods()
    portal_timeout = 15
    lna_user = "admin"
    lna_pass = "Logi@3456"
    lna_ip = None
    meet = GoogleMeet()
    meet_driver = None
    sync_driver = None

    def tc_install_sync_app(self, version: str = None):
        """
        Method to install Sync App

        :param version:
        :return :
        """
        if version is None:
            version = INSTALLER
        try:
            disconnect_all()
            app = AppInstall()
            if get_custom_platform() == "windows":
                app.uninstallApp()
                app.installApp(version=version)
                services = app.verify_sync_services_install()
                registry = app.verify_registry_install()
                if services and registry:
                    Report.logPass("Successfully installed Sync App")
                else:
                    Report.logFail("Sync App not installed Successfully")
            else:
                app.uninstall_sync_mac()
                app.install_sync_mac(version=version)
        except Exception as e:
            Report.logException(str(e))

    def tc_uninstall_sync_app(self):
        """
        Method to Uninstall Sync App

        :param :
        :return :
        """
        try:
            app = AppInstall()
            if get_custom_platform() == "windows":
                app.uninstallApp()
                services = True  # app.verify_sync_services_uninstall()
                registry = app.verify_registry_uninstall()
                if services and registry:
                    Report.logPass("Successfully uninstalled Sync App")
                else:
                    Report.logFail("Sync App uninstall is not successful")
            else:
                app.uninstall_sync_mac()
        except Exception as e:
            Report.logException(str(e))

    def tc_add_device(self, device_name):
        """
        Method to Add device in Sync App by clicking on + and connecting device.
        Check device shows in Sync Portal after adding

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.add_device(device_name=device_name)
            self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=room_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_video_tab(self, device_name):
        """
        Method to click on links displayed under camera section and verify correct link opened in browser

        :param device_name:
        :return :
        """
        try:
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_links_in_camera_section(device_name=device_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_scribe_video_tab(self, device_name):
        """
        Method to click on links displayed under camera section and verify correct link opened in browser

        :param device_name:
        :return :
        """
        try:
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.camera.click_edit_boundaries()
            verification = self.sync_app.camera.verify_auto_calibrate_enabled()
            self.sync_app.report_enabled_or_disabled("Auto Calibrate button", verification, status=True)
            verification = self.sync_app.camera.verify_cancel_enabled()
            self.sync_app.report_enabled_or_disabled("Cancel button", verification, status=True)
            verification = self.sync_app.camera.verify_confirm_enabled()
            self.sync_app.report_enabled_or_disabled("Confirm button", verification, status=True)

            self.sync_app.camera.click_auto_calibrate()
            verification = not self.sync_app.camera.verify_auto_calibrate_enabled()
            self.sync_app.report_enabled_or_disabled("Auto Calibrate button", verification, status=False)
            verification = not self.sync_app.camera.verify_cancel_enabled()
            self.sync_app.report_enabled_or_disabled("Cancel button", verification, status=False)
            verification = not self.sync_app.camera.verify_confirm_enabled()
            self.sync_app.report_enabled_or_disabled("Confirm button", verification, status=False)

            # Wait till Auto Calibrate completes timeout 10 seconds
            i = 0
            while i < 10:
                if self.sync_app.camera.verify_auto_calibrate_enabled():
                    break
                time.sleep(1)
                i = i + 1
            # Verify buttons are enabled after Auto Calibrate
            verification = self.sync_app.camera.verify_auto_calibrate_enabled()
            self.sync_app.report_enabled_or_disabled("After auto calibration, Auto Calibrate button",
                                                     verification, status=True)
            verification = self.sync_app.camera.verify_cancel_enabled()
            self.sync_app.report_enabled_or_disabled("After auto calibration, Cancel button",
                                                     verification, status=True)
            verification = self.sync_app.camera.verify_confirm_enabled()
            self.sync_app.report_enabled_or_disabled("After auto calibration, Confirm button",
                                                     verification, status=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_tab(self, device_name):
        """
        Method to click on links displayed under camera section and verify correct link opened in browser

        :param device_name:
        :return :
        """
        try:
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_mic_speaker_buttons(device_name=device_name) \
                .verify_links_in_audio_section(device_name=device_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_add_device_pnp(self, device_name):
        """
        Method to Add device in Sync App by connecting device (Plug and Play)
        Check device shows in Sync Portal after adding

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open().get_room_name()
            self.sync_app.add_device_pnp(device_name=device_name)
            self.sync_portal.verify_device_added_in_sync_portal(device_name=device_name, room_name=room_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_check_raiden_portal(self, device_name):
        """
        Method to check Sync Portal for Status, Health, Use State for device added in Sync App

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.close()
            self.sync_portal.login_to_sync_portal(global_variables.config, global_variables.SYNC_ROLE)
            self.sync_portal.verify_columns_in_rooms_tab(room_name=room_name, device_list=[device_name],
                                                         status="Up to Date", health="No Issues",
                                                         use_state="Available")
            self.sync_portal.verify_columns_in_devices_tab(room_name=room_name, device_name=device_name,
                                                           device_status="Up to Date", device_health="No Issues",
                                                           device_use_state="Available")
        except Exception as e:
            Report.logException(str(e))

    def tc_device_detection(self, device_name: str):
        """
        Method to check device shows error after disconnecting and error disappears after connecting back

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open()
            self.sync_app.verify_device_connect_disconnect(device_name=device_name).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_rightsight_in_sync(self, device_name: str):
        """
        Method to check Right Sight is enabled by default. User can enable or disable Right Sight and changes
        persist after disconnect and connect the device

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_camera(device_name=device_name).enable_right_sight()
            if device_name in ("Rally Bar", "Rally Bar Mini"):
                self.sync_app.camera.click_group_view()
            self.sync_app.camera.click_on_call_start()
            self.sync_app.verify_on_call_start(selected=True)
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name)
            if device_name == "Rally Camera":
                time.sleep(15)
            self.sync_app.verify_on_call_start(selected=True)
            self.sync_app.camera.click_dynamic()
            self.sync_app.verify_dynamic(selected=True)
            self.sync_app.camera.disable_right_sight()
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name)
            if device_name == "Rally Camera":
                time.sleep(15)
            self.sync_app.verify_rightsight(enabled=False)
            self.sync_app.camera.enable_right_sight()
            self.sync_app.verify_rightsight(enabled=True).verify_dynamic(selected=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_anti_flicker_in_sync(self, device_name):
        """
        Method to check Anti-flicker is set to NTSC by default. User can change to PAL and NTSC
        Changes persist after disconnect and connect the device

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_camera(device_name=device_name).click_pal()
            self.sync_app.verify_anti_flicker_pal(selected=True)
            # Disconnect & reconnect to check persistence
            if get_custom_platform() == "windows":
                self.sync_app.verify_device_connect_disconnect(device_name=device_name)
                self.sync_app.home.click_device_camera(device_name=device_name)
                self.sync_app.verify_anti_flicker_pal(selected=True)
            # Check Anti-flicker in Sync Portal
            self.sync_portal.verify_anti_flicker_in_sync_portal(device_name, room_name, "PAL")
            self.sync_app.camera.click_ntsc()
            self.sync_app.verify_anti_flicker_ntsc(selected=True)
            # Set Anti-flicker in Sync Portal PAL
            time.sleep(10)
            self.sync_portal.set_anti_flicker_in_sync_portal(device_name, room_name, "PAL")
            self.sync_app.verify_anti_flicker_pal(selected=True)
            # Set Anti-flicker in Sync Portal NTSC
            time.sleep(10)
            self.sync_portal.set_anti_flicker_in_sync_portal(device_name, room_name, "NTSC")
            self.sync_app.verify_anti_flicker_ntsc(selected=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_bluetooth_in_sync(self, device_name):
        """
        Method to check Bluetooth is enabled by default. User can toggle bluetooth to ON/OFF
        Changes persist after disconnect and connect the device, Changes reflected in Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_connectivity(device_name=device_name).disable_bluetooth()
            self.sync_app.verify_bluetooth(enabled=False)
            self.sync_portal.verify_bluetooth_in_sync_portal(device_name=device_name, room_name=room_name,
                                                             bluetooth="OFF")
            self.sync_app.connectivity.enable_bluetooth()
            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_connectivity(device_name=device_name)
            self.sync_app.verify_bluetooth(enabled=True).close()
            # Toggle bluetooth in Sync Portal
            self.sync_portal.verify_bluetooth_in_sync_portal(device_name=device_name, room_name=room_name,
                                                             bluetooth="ON")
            self.sync_portal.set_bluetooth_in_sync_portal(device_name=device_name, room_name=room_name,
                                                          bluetooth="OFF")
            self.sync_app.open().click_device_connectivity(device_name=device_name)
            self.sync_app.verify_bluetooth(enabled=False).close()
            self.sync_portal.set_bluetooth_in_sync_portal(device_name=device_name, room_name=room_name,
                                                          bluetooth="ON")
            self.sync_app.open().click_device_connectivity(device_name=device_name)
            self.sync_app.verify_bluetooth(enabled=True).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_bluetooth_device_in_sync(self, device_name):
        """
        Method to check User can toggle bluetooth to ON/OFF
        Changes reflected in Local Network Access and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_connectivity(device_name=device_name).disable_bluetooth()
            self.sync_app.verify_bluetooth(enabled=False)
            # Check bluetooth in device
            self.lna.verify_bluetooth_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                password=self.lna_pass, bluetooth="OFF")
            self.sync_app.connectivity.enable_bluetooth()
            self.sync_app.verify_bluetooth(enabled=True).close()
            # Check bluetooth in device
            self.lna.verify_bluetooth_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                password=self.lna_pass, bluetooth="ON")

            # self.syncApp.openSyncApp()
            # # room_name = self.syncApp.getRoomName()
            # self.syncApp.select_connectivity_tab(device_name=device_name)
            # self.syncApp.disable_bluetooth()
            # self.syncApp.verify_bluetooth_disable()
            # # Check bluetooth in device
            # self.lna.verify_bluetooth_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
            #                                     password=self.lna_pass, bluetooth="OFF")
            # self.syncApp.enable_bluetooth()
            # self.syncApp.verify_bluetooth_enable()
            # self.syncApp.closeSyncApp()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_speaker_boost(self, device_name):
        """
        Method to check Audio Speaker Boost is disabled by default. User can toggle Speaker Boost to ON/OFF
        Changes persist after disconnect and connect the device, Changes reflected in Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_audio(device_name=device_name).enable_speaker_boost()
            self.sync_app.verify_speaker_boost(enabled=True)
            # Check speaker boost in Sync Portal
            self.sync_portal.verify_speaker_boost_in_sync_portal(device_name=device_name,
                                                                 room_name=room_name, speaker_boost="ON")
            self.sync_app.audio.disable_speaker_boost()
            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_boost(enabled=False).close()
            # Toggle Speaker Boost in Sync Portal
            self.sync_portal.set_speaker_boost_in_sync_portal(device_name=device_name,
                                                              room_name=room_name, speaker_boost="ON")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_boost(enabled=True).close()
            self.sync_portal.set_speaker_boost_in_sync_portal(device_name=device_name,
                                                              room_name=room_name, speaker_boost="OFF")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_boost(enabled=False).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_speaker_boost_device(self, device_name):
        """
        Method to check User can toggle Audio Speaker Boost to ON/OFF
        Changes reflected in Local Network Access and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return none
        """
        try:
            self.sync_app.open().click_device_audio(device_name=device_name).enable_speaker_boost()
            self.sync_app.verify_speaker_boost(enabled=True)
            # Check speaker boost in Device
            self.lna.verify_speaker_boost_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                    password=self.lna_pass, speaker_boost="ON")
            self.sync_app.audio.disable_speaker_boost()
            self.sync_app.verify_speaker_boost(enabled=False)
            # Toggle Speaker Boost in Device
            self.lna.toggle_speaker_boost_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                    password=self.lna_pass, speaker_boost="ON")
            self.sync_app.verify_speaker_boost(enabled=True)
            self.lna.toggle_speaker_boost_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                    password=self.lna_pass, speaker_boost="OFF")
            self.sync_app.verify_speaker_boost(enabled=False).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_ai_noise_suppression(self, device_name):
        """
        Method to check Audio AI Noise Suppression is enabled by default. User can toggle AI Noise Suppression to ON/OFF
        Changes persist after disconnect and connect the device, Changes reflected in Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_audio(device_name=device_name).disable_ai_noise_suppression()
            self.sync_app.verify_ai_noise_suppression(enabled=False)
            # Check AI Noise Suppresion in Sync Portal
            self.sync_portal.verify_ai_noise_suppression_in_sync_portal(device_name=device_name,
                                                                        room_name=room_name, noise_suppression="OFF")
            self.sync_app.audio.enable_ai_noise_suppression()
            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_audio(device_name=device_name)
            self.sync_app.verify_ai_noise_suppression(enabled=True).close()
            # Toggle AI Noise Suppresion in Sync Portal
            self.sync_portal.set_ai_noise_suppression_in_sync_portal(device_name=device_name,
                                                                     room_name=room_name, noise_suppression="OFF")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_ai_noise_suppression(enabled=False).close()
            self.sync_portal.set_ai_noise_suppression_in_sync_portal(device_name=device_name,
                                                                     room_name=room_name, noise_suppression="ON")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_ai_noise_suppression(enabled=True).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_ai_noise_suppression_device(self, device_name):
        """
        Method to check User can toggle Audio AI Noise Supression to ON/OFF
        Changes reflected in Local Network Access and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_audio(device_name=device_name).disable_ai_noise_suppression()
            self.sync_app.verify_ai_noise_suppression(enabled=False)
            # Check AI Noise Suppresion in device
            self.lna.verify_ai_noise_suppression_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                           password=self.lna_pass, noise_suppression="OFF")
            self.sync_app.audio.enable_ai_noise_suppression()
            self.sync_app.verify_ai_noise_suppression(enabled=True)
            # Toggle AI Noise Suppresion in device
            self.lna.toggle_ai_noise_suppression_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                           password=self.lna_pass, noise_suppression="OFF")
            self.sync_app.verify_ai_noise_suppression(enabled=False)
            self.lna.toggle_ai_noise_suppression_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                           password=self.lna_pass, noise_suppression="ON")
            self.sync_app.verify_ai_noise_suppression(enabled=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_reverb_control(self, device_name):
        """
        Method to check Audio Reverb Control is set to Normal by default. User can change Reverb Control to Normal,
        Disabled or Agressive. Changes persist after disconnect and connect the device, Changes reflected in Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_audio(device_name=device_name).click_reverb_control_disabled()
            self.sync_app.verify_reverb_control_disabled(selected=True)
            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_audio(device_name=device_name)
            self.sync_app.verify_reverb_control_disabled(selected=True)
            # Check Reverb Control in Sync Portal
            self.sync_portal.verify_reverb_control_in_sync_portal(device_name=device_name, room_name=room_name,
                                                                  reverb_control="Disabled")
            self.sync_app.audio.click_reverb_control_aggressive()
            self.sync_app.verify_reverb_control_aggressive(selected=True)
            # Check Reverb Control in Sync Portal
            self.sync_portal.verify_reverb_control_in_sync_portal(device_name=device_name, room_name=room_name,
                                                                  reverb_control="Aggressive")
            self.sync_app.audio.click_reverb_control_normal()
            self.sync_app.verify_reverb_control_normal(selected=True).close()
            # Set Reverb Control in Sync Portal
            self.sync_portal.set_reverb_control_in_sync_portal(device_name=device_name, room_name=room_name,
                                                               reverb_control="Disabled")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_reverb_control_disabled(selected=True).close()
            self.sync_portal.set_reverb_control_in_sync_portal(device_name=device_name, room_name=room_name,
                                                               reverb_control="Aggressive")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_reverb_control_aggressive(selected=True).close()
            self.sync_portal.set_reverb_control_in_sync_portal(device_name=device_name, room_name=room_name,
                                                               reverb_control="Normal")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_reverb_control_normal(selected=True).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_reverb_control_device(self, device_name):
        """
        Method to check User can change Reverb Control to Normal, Disabled or Agressive
        Changes reflected in Local Network Access and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_audio(device_name=device_name).click_reverb_control_disabled()
            self.sync_app.verify_reverb_control_disabled(selected=True)
            # Check Reverb Control in device
            self.lna.verify_reverb_control_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                     password=self.lna_pass, reverb_control="Disabled")
            self.sync_app.audio.click_reverb_control_aggressive()
            self.sync_app.verify_reverb_control_aggressive(selected=True)
            # Check Reverb Control in device
            self.lna.verify_reverb_control_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                     password=self.lna_pass, reverb_control="Aggressive")
            self.sync_app.audio.click_reverb_control_normal()
            self.sync_app.verify_reverb_control_normal(selected=True)
            # Set Reverb Control in device
            self.lna.set_reverb_control_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                  password=self.lna_pass, reverb_control="Disabled")
            self.sync_app.verify_reverb_control_disabled(selected=True)
            self.lna.set_reverb_control_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                  password=self.lna_pass, reverb_control="Aggressive")
            self.sync_app.verify_reverb_control_aggressive(selected=True)
            self.lna.set_reverb_control_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                  password=self.lna_pass, reverb_control="Normal")
            self.sync_app.verify_reverb_control_normal(selected=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_microphone_eq(self, device_name):
        """
        Method to check Audio Microphone EQ is set to Normal by default. User can change Microphone EQ to Normal,
        Bass Boost or Voice Boost. Changes persist after disconnect and connect the device
        Changes reflected in Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_audio(device_name=device_name).click_microphone_eq_bass_boost()
            self.sync_app.verify_microphone_eq_bass_boost(selected=True)
            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_audio(device_name=device_name)
            self.sync_app.verify_microphone_eq_bass_boost(selected=True)
            # Check Reverb Control in Sync Portal
            self.sync_portal.verify_microphone_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                                 microphone_eq="Bass Boost")
            self.sync_app.audio.click_microphone_eq_voice_boost()
            self.sync_app.verify_microphone_eq_voice_boost(selected=True)
            # Check Reverb Control in Sync Portal
            self.sync_portal.verify_microphone_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                                 microphone_eq="Voice Boost")
            self.sync_app.audio.click_microphone_eq_normal()
            self.sync_app.verify_microphone_eq_normal(selected=True).close()
            # Set Reverb Control in Sync Portal
            self.sync_portal.set_microphone_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              microphone_eq="Bass Boost")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_microphone_eq_bass_boost(selected=True).close()
            self.sync_portal.set_microphone_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              microphone_eq="Voice Boost")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_microphone_eq_voice_boost(selected=True)
            self.sync_portal.set_microphone_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              microphone_eq="Normal")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_microphone_eq_normal(selected=True).close()

        except Exception as e:
            Report.logException(str(e))

    def tc_audio_microphone_eq_device(self, device_name):
        """
        Method to check User can change Microphone EQ to Normal, Bass Boost or Voice Boost
        Changes reflected in Local Network Access and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_audio(device_name=device_name).click_microphone_eq_bass_boost()
            self.sync_app.verify_microphone_eq_bass_boost(selected=True)
            # Check Microphone EQ in Device
            self.lna.verify_microphone_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                    password=self.lna_pass, microphone_eq="Bass Boost")
            self.sync_app.audio.click_microphone_eq_voice_boost()
            self.sync_app.verify_microphone_eq_voice_boost(selected=True)
            # Check Microphone EQ in Device
            self.lna.verify_microphone_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                    password=self.lna_pass, microphone_eq="Voice Boost")
            self.sync_app.audio.click_microphone_eq_normal()
            self.sync_app.verify_microphone_eq_normal(selected=True)
            # Set Microphone EQ in Device
            self.lna.set_microphone_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                 password=self.lna_pass, microphone_eq="Bass Boost")
            self.sync_app.verify_microphone_eq_bass_boost(selected=True)
            self.lna.set_microphone_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                 password=self.lna_pass, microphone_eq="Voice Boost")
            self.sync_app.verify_microphone_eq_voice_boost(selected=True)
            self.lna.set_microphone_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                 password=self.lna_pass, microphone_eq="Normal")
            self.sync_app.verify_microphone_eq_normal(selected=True).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_audio_speaker_eq(self, device_name):
        """
        Method to check Audio Speaker EQ is set to Normal by default. User can change Speaker EQ to Normal,
        Bass Boost or Voice Boost. Changes persist after disconnect and connect the device
        Changes reflected in Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_audio(device_name=device_name).click_speaker_eq_bass_boost()
            self.sync_app.verify_speaker_eq_bass_boost(selected=True)
            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_eq_bass_boost(selected=True)
            # Check Speaker Eq in Sync Portal
            self.sync_portal.verify_speaker_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              speaker_eq="Bass Boost")
            self.sync_app.audio.click_speaker_eq_voice_boost()
            self.sync_app.verify_speaker_eq_voice_boost(selected=True)
            # Check Speaker Eq in Sync Portal
            self.sync_portal.verify_speaker_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              speaker_eq="Voice Boost")
            self.sync_app.audio.click_speaker_eq_normal()
            self.sync_app.verify_speaker_eq_normal(selected=True).close()
            # Set Speaker Eq in Sync Portal
            self.sync_portal.set_speaker_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                           speaker_eq="Bass Boost")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_eq_bass_boost(selected=True).close()
            self.sync_portal.set_speaker_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                           speaker_eq="Voice Boost")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_eq_voice_boost(selected=True).close()
            self.sync_portal.set_speaker_eq_in_sync_portal(device_name=device_name, room_name=room_name,
                                                           speaker_eq="Normal")
            self.sync_app.open().click_device_audio(device_name=device_name)
            self.sync_app.verify_speaker_eq_normal(selected=True).close()

        except Exception as e:
            Report.logException(str(e))

    def tc_audio_speaker_eq_device(self, device_name):
        """
        Method to check User can change Speaker EQ to Normal, Bass Boost or Voice Boost
        Changes reflected in Local Network Access and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_audio(device_name=device_name).click_speaker_eq_bass_boost()
            self.sync_app.verify_speaker_eq_bass_boost(selected=True)
            # Check Speaker EQ in Device
            self.lna.verify_speaker_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                 password=self.lna_pass, speaker_eq="Bass Boost")
            self.sync_app.audio.click_speaker_eq_voice_boost()
            self.sync_app.verify_speaker_eq_voice_boost(selected=True)
            # Check Speaker EQ in Device
            self.lna.verify_speaker_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                 password=self.lna_pass, speaker_eq="Voice Boost")
            self.sync_app.audio.click_speaker_eq_normal()
            self.sync_app.verify_speaker_eq_normal(selected=True)
            # Set Speaker EQ in Device
            self.lna.set_speaker_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                              password=self.lna_pass, speaker_eq="Bass Boost")
            self.sync_app.verify_speaker_eq_bass_boost(selected=True)
            self.lna.set_speaker_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                              password=self.lna_pass, speaker_eq="Voice Boost")
            self.sync_app.verify_speaker_eq_voice_boost(selected=True)
            self.lna.set_speaker_eq_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                              password=self.lna_pass, speaker_eq="Normal")
            self.sync_app.verify_speaker_eq_normal(selected=True).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_forget_device(self, device_name):
        """
        Method to forget device from Sync App and verify device removed from Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.forget_device(device_name=device_name)
            self.sync_portal.verify_device_deleted_in_sync_portal(device_name=device_name, room_name=room_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_remove_problem_device(self, device_name):
        """
        Method to remove device in error from Sync App and verify device removed from Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.forget_problem_device(device_name=device_name)
            self.sync_portal.verify_device_deleted_in_sync_portal(device_name=device_name, room_name=room_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_remove_problem_device_sync_portal(self, device_name):
        """
        Method to remove device in error from Sync Portal and verify device removed from Sync App

        :param device_name: e.g. Rally Bar Mini
        :return none
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.add_device(device_name=device_name)
            self.sync_app.home.click_device(device_name=device_name)
            disconnect_device(device_name)
            self.sync_app.verify_problem_with_device_message_appears(device_name=device_name)
            self.sync_portal.forget_device_in_sync_portal(room_name=room_name, device_name=device_name)
            self.sync_app.verify_device_removed_from_sync_app(device_name=device_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_update_firmware(self, device_name):
        """
        Method to update firmware for device and verify firmware update is successful

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device(device_name=device_name)
            if self.sync_app.device.verify_firmware_update_failed() or \
                    self.sync_app.device.verify_firmware_update_available():
                Report.logPass("Firmware available for update", screenshot=True)
                self.sync_app.device.click_update()
                verification = self.sync_app.device.verify_update_now_button()
                self.sync_app.report_displayed_or_not("Update Now button", verification)
                verification = self.sync_app.device.verify_schedule_update_button()
                self.sync_app.report_displayed_or_not("Schedule Update button", verification)
                self.sync_app.device.click_update_now()
                i = 3600 if device_name in ("Rally Bar", "Rally Bar Mini") else 1800
                while i > 0:
                    i = i - 1
                    if not self.sync_app.device.verify_back_button():
                        Report.logPass("Update Complete", True)
                        break
                    time.sleep(1)
            else:
                Report.logFail("Firmware Update not available")
            self.sync_app.close()
            time.sleep(5)
        except Exception as e:
            Report.logException(str(e))

    def tc_update_firmware_interrupt(self, device_name):
        """
        Method to interrupt firmware update and check update failed error displays

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            if self.sync_app.open().click_device(device_name=device_name).verify_firmware_update_available():
                Report.logPass("Firmware Update available displayed", screenshot=True)
                self.sync_app.device.click_update().click_update_now()
                time.sleep(30)
                disconnect_device(device_name)
                time.sleep(60)
                connect_device(device_name)
                time.sleep(20)
                self.sync_app.close()
                if self.sync_app.open().click_device(device_name=device_name).verify_firmware_update_failed():
                    Report.logPass("Firmware Update Failed message displayed", True)
                else:
                    Report.logFail("Firmware Updated Failed message not displayed")
            else:
                Report.logFail("Firmware Update not available")
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_rightsight2_in_sync(self, device_name):
        """
        Method to verify RightSight 2 is enabled and Group View is selected by default in Sync App
        User can toggle between Speaker View and Group View, Enable/Disable picture in picture
        Changes in Sync App are reflected in Sync Portal and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_camera(device_name=device_name) \
                .enable_right_sight().click_speaker_view().disable_picture_in_picture()
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_view(enabled=True).verify_picture_in_picture(enabled=False)
            # Check settings in Sync Portal
            self.sync_portal.verify_rightsight2_in_sync_portal(device_name=device_name, room_name=room_name,
                                                               group_view=False, speaker_view=True,
                                                               picture_in_picture=False)
            self.sync_app.camera.click_group_view()
            self.sync_app.verify_group_view(enabled=True).close()
            # Check settings in Sync Portal
            self.sync_portal.verify_rightsight2_in_sync_portal(device_name=device_name, room_name=room_name,
                                                               group_view=True, speaker_view=False)
            # Change settings in Sync Portal and verify in Sync Appp
            self.sync_portal.set_rightsight2_in_sync_portal(device_name=device_name,
                                                            room_name=room_name, group_view=False,
                                                            speaker_view=True, picture_in_picture=True)
            self.sync_app.open()
            self.sync_app.home.click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_view(enabled=True).verify_picture_in_picture(enabled=True)
            # Check defaults after disable and enable of RightSight 2
            self.sync_app.camera.disable_right_sight()
            self.sync_portal.verify_rightsight_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              rightsight=False)
            self.sync_app.camera.enable_right_sight()
            # self.syncApp.verify_right_sight2_enable()
            self.sync_portal.verify_rightsight_in_sync_portal(device_name=device_name, room_name=room_name,
                                                              rightsight=True)
            self.sync_app.camera.click_group_view()
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_rightsight2_device_in_sync(self, device_name):
        """
        Method to verify User can toggle between Speaker View and Group View, Enable/Disable picture in picture
        Changes in Sync App are reflected in Local Network Access and vice versa

        :param :device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            self.sync_app.open().click_device_camera(device_name=device_name) \
                .enable_right_sight().click_speaker_view().disable_picture_in_picture()
            self.sync_app.verify_speaker_view(enabled=True).verify_picture_in_picture(enabled=False)
            # Check settings in Device
            self.lna.verify_rightsight2_options_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                          password=self.lna_pass, group_view=False,
                                                          speaker_view=True, picture_in_picture=False)
            self.sync_app.camera.click_group_view()
            self.sync_app.verify_group_view(enabled=True)
            # Check settings in Device
            self.lna.verify_rightsight2_options_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                          password=self.lna_pass, group_view=True,
                                                          speaker_view=False)
            # Change settings in device and verify in Sync Appp
            self.lna.set_rightsight2_options_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                       password=self.lna_pass, group_view=False,
                                                       speaker_view=True, picture_in_picture=True)
            self.sync_app.verify_speaker_view(enabled=True).verify_picture_in_picture(enabled=True)
            self.lna.set_rightsight2_options_in_device(ip_address=self.lna_ip, user_name=self.lna_user,
                                                       password=self.lna_pass, group_view=True,
                                                       speaker_view=False)
            self.sync_app.verify_group_view(enabled=True).close()
        except Exception as e:
            Report.logException(str(e))

    def tc_speakerview_in_sync(self, device_name: str):
        """
        Method to verify Speaker detection and Framing Speed options in Speaker View
        Changes in Sync App are reflected in Sync Portal and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_camera(device_name=device_name) \
                .click_speaker_view().click_speaker_detection_slower().click_framing_speed_slower()
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_detection_slower(selected=True).verify_framing_speed_slower(selected=True)
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   speaker_detection="Slow",
                                                                                   framing_speed="Slow")
            self.sync_app.camera.click_speaker_detection_faster().click_framing_speed_faster()
            self.sync_app.verify_speaker_detection_faster(selected=True).verify_framing_speed_faster(selected=True)
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   speaker_detection="Fast",
                                                                                   framing_speed="Fast")
            self.sync_app.camera.click_speaker_detection_default().click_framing_speed_default()
            self.sync_app.verify_speaker_detection_default(selected=True).verify_framing_speed_default(selected=True)
            self.sync_app.close()
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   speaker_detection="Default",
                                                                                   framing_speed="Default")
            # Change settings in Sync Portal and verify in Sync Appp
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                speaker_detection="Slow",
                                                                                framing_speed="Slow")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_detection_slower(selected=True).verify_framing_speed_slower(selected=True)
            self.sync_app.close()
            # Change settings in Sync Portal and verify in Sync Appp
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                speaker_detection="Fast",
                                                                                framing_speed="Fast")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_detection_faster(selected=True).verify_framing_speed_faster(selected=True)
            self.sync_app.close()
            # Change settings in Sync Portal and verify in Sync Appp
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                speaker_detection="Default",
                                                                                framing_speed="Default")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_detection_default(selected=True).verify_framing_speed_default(selected=True)
            # Disable Picture in Picture, Disable and Enable RightSight and check persistence
            self.sync_app.camera.disable_picture_in_picture().disable_right_sight()
            self.sync_app.verify_rightsight(enabled=False)
            time.sleep(5)
            self.sync_app.camera.enable_right_sight()
            self.sync_app.verify_rightsight(enabled=True) \
                .verify_speaker_view(enabled=True).verify_picture_in_picture(enabled=False)
            self.sync_app.camera.enable_picture_in_picture().click_group_view()
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_groupview_in_sync(self, device_name: str):
        """
        Method to verify Framing Speed options in Group View
        Changes in Sync App are reflected in Sync Portal and vice versa

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_camera(device_name=device_name) \
                .click_group_view().click_framing_speed_slower()
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name).click_group_view()
            self.sync_app.verify_framing_speed_slower(selected=True)
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   framing_speed="Slow")
            self.sync_app.camera.click_framing_speed_faster()
            self.sync_app.verify_framing_speed_faster(selected=True)
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   framing_speed="Fast")
            self.sync_app.camera.click_framing_speed_default()
            self.sync_app.verify_framing_speed_default(selected=True)
            self.sync_app.close()
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   framing_speed="Default")
            # Change settings in Sync Portal and verify in Sync Appp
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                framing_speed="Slow")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_framing_speed_slower(selected=True)
            self.sync_app.close()
            # Change settings in Sync Portal and verify in Sync Appp
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                framing_speed="Fast")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_framing_speed_faster(selected=True)
            self.sync_app.close()
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                framing_speed="Default")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_framing_speed_default(selected=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_speakerview_groupview_in_sync(self, device_name: str):
        """
        Method to verify Speaker detection and Framing Speed options persist when changing between Speaker View
        and Group View in Sync App and Sync Portal

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            room_name = self.sync_app.open_and_get_room_name()
            self.sync_app.home.click_device_camera(device_name=device_name) \
                .click_group_view().click_framing_speed_faster()
            time.sleep(2)
            self.sync_app.camera.click_speaker_view() \
                .click_speaker_detection_slower().click_framing_speed_slower()
            # Verify Framing Speed for Group View
            self.sync_app.camera.click_group_view()
            self.sync_app.verify_framing_speed_faster(selected=True)
            self.sync_app.camera.click_speaker_view()
            self.sync_app.verify_speaker_detection_slower(selected=True).verify_framing_speed_slower(selected=True)
            self.sync_app.close()
            # Check settings in Sync Portal
            self.sync_portal.verify_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                   speaker_detection="Slow",
                                                                                   framing_speed="Slow", view="Group")
            # Change settings in Sync Portal and verify in Sync App
            self.sync_portal.set_speaker_detection_framing_speed_in_sync_portal(device_name, room_name,
                                                                                speaker_detection="Default",
                                                                                framing_speed="Default", view="Group")
            self.sync_app.open().click_device_camera(device_name=device_name)
            self.sync_app.verify_speaker_detection_default(selected=True) \
                .verify_framing_speed_default(selected=True)
            self.sync_app.camera.click_group_view()
            self.sync_app.verify_framing_speed_default(selected=True)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_manual_color_settings_in_sync(self, device_name):
        """
        Method to check default manual color settings values. User can adjust the color settings and changes
        persist after disconnect and connect the device

        :param Device Name e.g. Rally Bar Mini
        :return none
        """
        try:
            Report.logInfo("Validating manual color settings for device: " + device_name)
            self.sync_app.open().click_device_camera(device_name=device_name).expand_manual_color_settings()
            self.sync_app.verify_default_manual_color_settings(device_name=device_name)
            # Original video stream capture
            original = self.sync_app.camera.get_screenshot_from_video_stream(name='Original')
            [bright_original, cont_original, sat_original, sharp_original] = get_image_settings(original)
            time.sleep(3)
            Report.logInfo("Adjusting manual color settings")
            if device_name == "Rally Bar Huddle":
                brightness_resultant = self.sync_app.camera.set_color_value("brightness", 100)
                contrast_resultant = self.sync_app.camera.set_color_value("contrast", 11)
                saturation_resultant = self.sync_app.camera.set_color_value("saturation", 11)
                sharpness_resultant = self.sync_app.camera.set_color_value("sharpness", 11)
            else:
                brightness_resultant = self.sync_app.camera.set_color_value("brightness", 70)
                contrast_resultant = self.sync_app.camera.set_color_value("contrast", 20)
                saturation_resultant = self.sync_app.camera.set_color_value("saturation", 20)
                sharpness_resultant = self.sync_app.camera.set_color_value("sharpness", 10)
            time.sleep(2)

            updated = self.sync_app.camera.get_screenshot_from_video_stream(name='Updated Color Settings')
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)

            # compare video stream
            self.sync_app.compare_color_settings("Brightness", bright_original, bright_updated, "lesser") \
                .compare_color_settings("Contrast", cont_original, cont_updated, "greater") \
                .compare_color_settings("Saturation", sat_original, sat_updated, "greater") \
                .compare_color_settings("Sharpness", sharp_original, sharp_updated, "greater")

            # Navigate out of video tab and go back to video to check for the Persistence of settings
            self.sync_app.home.click_device(device_name=device_name)
            time.sleep(2)
            self.sync_app.home.click_device_camera(device_name=device_name)
            time.sleep(2)
            Report.logInfo("Validating the Persistence of manual color settings after navigating back to the page")
            self.sync_app.verify_manual_color_setting("brightness", brightness_resultant) \
                .verify_manual_color_setting("contrast", contrast_resultant) \
                .verify_manual_color_setting("saturation", saturation_resultant) \
                .verify_manual_color_setting("sharpness", sharpness_resultant)

            # Persistence of color settings after navigating back to the camera tab
            persistence = self.sync_app.camera.get_screenshot_from_video_stream(name='Persist Color Settings')
            [bright_persistence, cont_persistence, sat_persistence, sharp_persistence] = get_image_settings(persistence)

            self.sync_app.compare_color_settings("Brightness", bright_original, bright_persistence, "lesser") \
                .compare_color_settings("Contrast", cont_original, cont_persistence, "greater") \
                .compare_color_settings("Saturation", sat_original, sat_persistence, "greater") \
                .compare_color_settings("Sharpness", sharp_original, sharp_persistence, "greater")
            self.sync_app.camera.click_reset_manual_color_settings()
            self.sync_app.verify_default_manual_color_settings(device_name=device_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_manual_color_settings_unplug_replug_in_sync(self, device_name):
        """
        Method to check default manual color settings values. User can adjust the color settings and changes
        persist after disconnect and connect the device

        :param Device Name e.g. Rally Bar Mini
        :return none
        """
        try:
            Report.logInfo("Validating persistence of manual color settings for device: " + device_name)
            self.sync_app.open().click_device_camera(device_name=device_name).expand_manual_color_settings()
            # Original video stream capture
            original = self.sync_app.camera.get_screenshot_from_video_stream(name='Original')
            [bright_original, cont_original, sat_original, sharp_original] = get_image_settings(original)
            time.sleep(3)

            Report.logInfo("Adjusting manual color settings")
            brightness_resultant = self.sync_app.camera.set_color_value("brightness", 70)
            contrast_resultant = self.sync_app.camera.set_color_value("contrast", 20)
            saturation_resultant = self.sync_app.camera.set_color_value("saturation", 20)
            sharpness_resultant = self.sync_app.camera.set_color_value("sharpness", 10)
            time.sleep(2)

            # Disconnect & reconnect to check persistence
            self.sync_app.verify_device_connect_disconnect(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name)
            Report.logInfo("Validating the Persistence of manual color settings after navigating back to the page")
            self.sync_app.verify_manual_color_setting("brightness", brightness_resultant) \
                .verify_manual_color_setting("contrast", contrast_resultant) \
                .verify_manual_color_setting("saturation", saturation_resultant) \
                .verify_manual_color_setting("sharpness", sharpness_resultant)
            # Persistence of color settings after navigating back to the camera tab
            persistence = self.sync_app.camera.get_screenshot_from_video_stream(name='Persist Color Settings')
            [bright_persistence, cont_persistence, sat_persistence, sharp_persistence] = get_image_settings(persistence)
            self.sync_app.compare_color_settings("Brightness", bright_original, bright_persistence, "lesser") \
                .compare_color_settings("Contrast", cont_original, cont_persistence, "greater") \
                .compare_color_settings("Saturation", sat_original, sat_persistence, "greater") \
                .compare_color_settings("Sharpness", sharp_original, sharp_persistence, "greater")

            self.sync_app.camera.click_reset_manual_color_settings()
            self.sync_app.verify_default_manual_color_settings(device_name=device_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_camera_settings_stream_in_google_meet(self, device_name: str) -> None:
        """
        Method to check video stream changes in Google Meet when color settings are changed in Sync App for the device

        :param device_name:
        :param Device Name e.g. Rally Bar Mini
        :return none
        """
        try:
            self.meet.create_new_meeting()
            self.meet_driver = global_variables.driver
            self.sync_app.open().click_device_camera(device_name=device_name).expand_manual_color_settings()
            self.sync_driver = global_variables.driver
            self._verify_meet_video_stream_by_sync_changes(color_setting="brightness", percentage=60,
                                                           operator="lesser")
            self._verify_meet_video_stream_by_sync_changes(color_setting="contrast", percentage=30,
                                                           operator="greater")
            self._verify_meet_video_stream_by_sync_changes(color_setting="saturation", percentage=40,
                                                           operator="greater")
            if device_name in ("Rally Bar", "Rally Bar Mini"):
                self._verify_meet_video_stream_by_sync_changes(color_setting="sharpness", percentage=90,
                                                               operator="lesser")
            else:
                self._verify_meet_video_stream_by_sync_changes(color_setting="sharpness", percentage=10,
                                                               operator="greater")
            self.sync_app.close()
            global_variables.driver = self.meet_driver
            self.meet.leave_meeting()
        except Exception as e:
            Report.logException(str(e))

    def _verify_meet_video_stream_by_sync_changes(self, color_setting, percentage, operator) -> None:
        """
        Private method to adjust camera settings based on color setting and percentage
        Capture video stream from Google Meet and compare settings from Sync App

        :param color_setting, percentage, original_value, operator
        :return none
        """
        global_variables.driver = self.meet_driver
        original = self.meet.capture_video_stream()
        [bright_original, contr_original, sat_original, sharp_original] = get_image_settings(original)
        global_variables.driver = self.sync_driver
        self.sync_app.camera.set_color_value(color_setting=color_setting, percentage=percentage)
        global_variables.driver = self.meet_driver
        updated = self.meet.capture_video_stream()
        [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
        if str(color_setting).lower() == 'brightness':
            self.sync_app.compare_color_settings(color_setting, bright_original, bright_updated, operator)
        elif str(color_setting).lower() == 'contrast':
            self.sync_app.compare_color_settings(color_setting, contr_original, cont_updated, operator)
        elif str(color_setting).lower() == 'saturation':
            self.sync_app.compare_color_settings(color_setting, sat_original, sat_updated, operator)
        elif str(color_setting).lower() == 'sharpness':
            self.sync_app.compare_color_settings(color_setting, sharp_original, sharp_updated, operator)
        global_variables.driver = self.sync_driver
        self.sync_app.camera.click_reset_manual_color_settings()

    def tc_camera_settings_grid_mode(self, device_name) -> None:
        """
        Method to check grid lines in Video Preview

        :param Device Name e.g. Rally Bar Mini
        :return none
        """
        try:
            self.sync_app.open() \
                .click_device_camera(device_name=device_name) \
                .turn_on_grid_video_preview()
            time.sleep(2)
            if self.sync_app.camera.verify_grid_lines_video_preview():
                Report.logPass("Grid Lines are turned ON in Video Preview", True)
            else:
                Report.logFail("Grid Lines are turned OFF in Video Preview")
            self.sync_app.camera.turn_off_grid_video_preview()
            if not self.sync_app.camera.verify_grid_lines_video_preview():
                Report.logPass("Grid Lines are turned OFF in Video Preview", True)
            else:
                Report.logFail("Grid Lines are turned ON in Video Preview")
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_camera_settings_floating_window(self, device_name: str) -> None:
        """
        Method to check video displays in floating window when preview minimized
        Changing color settings reflects the video preview in floating window
        Restoring the floating window

        :param device_name: e.g. Rally Bar Mini
        :return :
        """
        try:
            if self.sync_app.open() \
                    .click_device_camera(device_name=device_name) \
                    .collapse_video_preview().verify_video_preview_collapsed():
                Report.logPass("Video Preview Collapsed", True)
            else:
                Report.logFail("Video Preview still expanded")
            self.sync_app.camera.expand_manual_color_settings() \
                .click_reset_manual_color_settings()
            original = self.sync_app.camera.get_screenshot_from_video_stream("original")
            [bright_original, cont_original, sat_original, sharp_original] = get_image_settings(original)
            self.sync_app.camera.set_color_value(color_setting="brightness", percentage=60)
            updated = self.sync_app.camera.get_screenshot_from_video_stream("brightness")
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            self.sync_app.compare_color_settings("Brightness", bright_original, bright_updated, "lesser")
            self.sync_app.camera.click_reset_manual_color_settings()

            self.sync_app.camera.set_color_value(color_setting="contrast", percentage=30)
            updated = self.sync_app.camera.get_screenshot_from_video_stream("contrast")
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            self.sync_app.compare_color_settings("Contrast", cont_original, cont_updated, "greater")
            self.sync_app.camera.click_reset_manual_color_settings()

            self.sync_app.camera.set_color_value(color_setting="saturation", percentage=70)
            updated = self.sync_app.camera.get_screenshot_from_video_stream("saturation")
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            self.sync_app.compare_color_settings("Saturation", sat_original, sat_updated, "lesser")
            self.sync_app.camera.click_reset_manual_color_settings()

            self.sync_app.camera.set_color_value(color_setting="sharpness", percentage=90)
            updated = self.sync_app.camera.get_screenshot_from_video_stream("sharpness")
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            self.sync_app.compare_color_settings("Sharpness", sharp_original, sharp_updated, "lesser")
            self.sync_app.camera.click_reset_manual_color_settings()

            if not self.sync_app.camera.restore_video_preview() \
                    .verify_video_preview_collapsed():
                Report.logPass("Video Preview Expanded", True)
            else:
                Report.logFail("Video Preview still collapsed")
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_camera_settings_forget_and_reconnect_device(self, device_name) -> None:
        """
        Method to check camera settings changes persist after forgetting device and reconnecting

        :param Device Name e.g. Rally Bar Mini
        :return none
        """
        try:
            self.sync_app.open().click_device_camera(device_name=device_name).expand_manual_color_settings()

            # Make changes to color settings
            self.sync_app.camera.set_color_value("brightness", 70)
            self.sync_app.camera.set_color_value("contrast", 20)
            self.sync_app.camera.set_color_value("saturation", 20)
            self.sync_app.camera.set_color_value("sharpness", 10)

            # Forget device and add it back
            self.sync_app.forget_problem_device(device_name=device_name)
            self.sync_app.add_device(device_name=device_name)
            self.sync_app.home.click_device_camera(device_name=device_name).expand_manual_color_settings()

            # Check the settings are reset to default after device reconnected
            self.sync_app.verify_default_manual_color_settings(device_name=device_name)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_camera_adjustments(self, device_name) -> None:
        """
        Method to test Camera Adjustments feature

        :param Device Name e.g. Rally Bar Mini
        :return none
        """
        try:
            def report_video_stream(setting: str, status: bool):
                if status:
                    Report.logPass(f"Video Stream changed as per {setting} settings.")
                else:
                    Report.logFail(f"Video Stream not changed as per {setting} settings")
            self.sync_app.open() \
                .click_device_camera(device_name=device_name) \
                .restore_video_preview() \
                .expand_camera_adjustments() \
                .click_reset_camera_adjustments()
            original = self.sync_app.camera.get_screenshot_from_video_stream("original")
            [bright_original, cont_original, sat_original, sharp_original] = get_image_settings(original)

            # if device_name in ("Rally Bar", "Rally", "Rally Camera"):
            #     self.sync_app.camera.set_camera_adjustments(camera_adjustment="Manual Focus", percentage=10)
            #     updated = self.sync_app.camera.get_screenshot_from_video_stream("manual_focus")
            #     [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            #     report_video_stream("Manual Focus", sharp_updated < sharp_original)
            #     self.sync_app.camera.click_reset_camera_adjustments()
            #     if self.sync_app.camera.verify_auto_focus_enabled():
            #         Report.logPass("Auto Focus is enabled on resetting Camera Adjustments", True)
            #     else:
            #         Report.logFail("Auto Focus is not enabled on resetting Camera Adjustments")

            self.sync_app.camera.set_camera_adjustments(camera_adjustment="Manual Exposure", percentage=10)
            updated = self.sync_app.camera.get_screenshot_from_video_stream("manual_exposure")
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            report_video_stream("Manual Exposure", bright_updated < bright_original and cont_updated < cont_original)
            self.sync_app.camera.click_reset_camera_adjustments()
            if self.sync_app.camera.verify_auto_exposure_enabled():
                Report.logPass("Auto Exposure is enabled on resetting Camera Adjustments", True)
            else:
                Report.logFail("Auto Exposure is not enabled on resetting Camera Adjustments")

            self.sync_app.camera.set_camera_adjustments(camera_adjustment="Manual White Balance", percentage=80)
            updated = self.sync_app.camera.get_screenshot_from_video_stream(name='manual_white_balance')
            [bright_updated, cont_updated, sat_updated, sharp_updated] = get_image_settings(updated)
            report_video_stream("Manual White Balance", sat_updated > sat_original)
            self.sync_app.camera.click_reset_camera_adjustments()
            if self.sync_app.camera.verify_auto_white_balanace_enabled():
                Report.logPass("Auto White Balance is enabled on resetting Camera Adjustments", True)
            else:
                Report.logFail("Auto White Balance is not enabled on resetting Camera Adjustments")
        except Exception as e:
            Report.logException(str(e))
        self.sync_app.close()

    def tc_camera_settings_multiple_devices(self, device_names) -> None:
        """
        Method to check camera settings changes persist after forgetting device and reconnecting

        :param device_names: List of Device Names e.g. ["Rally Bar Mini", "Rally"]
        :return none
        """
        try:
            self.sync_app.open()
            for device in device_names:
                self.sync_app.add_device(device_name=device)
            for device in device_names:
                self.sync_app.home.click_device_camera(device_name=device)\
                    .click_reset_manual_color_settings()\
                    .click_reset_camera_adjustments()
            for device in device_names:
                current_device = device
                self.sync_app.home.click_device_camera(device_name=device)
                Report.logInfo(f"Making updates to Camera Settings for {current_device}")
                brightness_resultant = self.sync_app.camera.set_color_value("brightness", 60)
                contrast_resultant = self.sync_app.camera.set_color_value("contrast", 40)
                saturation_resultant = self.sync_app.camera.set_color_value("saturation", 70)
                sharpness_resultant = self.sync_app.camera.set_color_value("sharpness", 20)
                self.sync_app.camera.disable_auto_white_balanace()\
                    .disable_auto_exposure()
                # if current_device in ("Rally Bar", "Rally", "Rally Camera"):
                #     self.sync_app.camera.disable_auto_focus()
                for other_device in device_names:
                    if other_device != current_device:
                        Report.logInfo(
                            f"Verifying Updates to {current_device} settings did not alter settings for {other_device}")
                        self.sync_app.home.click_device_camera(device_name=other_device)
                        self.sync_app.verify_default_manual_color_settings(device_name=other_device)
                        self.sync_app.verify_default_camera_adjustments(device_name=other_device)
                self.sync_app.home.click_device_camera(device_name=current_device)\
                    .click_reset_manual_color_settings()\
                    .click_reset_camera_adjustments()
            for device in device_names:
                self.sync_app.forget_device(device_name=device)
            self.sync_app.close()
        except Exception as e:
            Report.logException(str(e))

    def tc_connect_to_sync_portal(self, close_browser: bool = True) -> str:
        """
        Method to provision Sync App Host Machine to Sync Portal

        :param close_browser:
        :return room_name:
        """
        org_name = global_variables.SYNC_ROOM[global_variables.SYNC_ENV]
        room_name = self.sync_app.open().get_room_name()
        Report.logInfo(f"Current Room Name: {room_name}")
        now = datetime.now()
        new_room = now.strftime("%Y%m%d%H%M%S") + " Auto-" + get_custom_platform()
        if self.sync_app.rename_room(room_name=new_room).verify_room(room_name=new_room):
            Report.logPass(f"Successfully Renamed Room to {new_room}", True)
        else:
            Report.logFail("Rename Room Failed")
        self.sync_app.connect_to_sync_portal(global_variables.config, global_variables.SYNC_ROLE, org_name).close()
        room_status = self.sync_portal.login_to_sync_portal_and_verify_provisioned_room(config=global_variables.config,
                                                                                        role=global_variables.SYNC_ROLE,
                                                                                        room_name=new_room)
        if room_status:
            Report.logPass(f"Room {new_room} provisioned in Sync Portal", True)
        else:
            Report.logFail(f"Room {new_room} not provisioned in Sync Portal")
        if close_browser:
            self.sync_portal.browser.close_browser()
        return new_room

    def tc_landing_page(self, device_name: str):
        """
        Method to Compare device information displayed in Sync App to Sync Portal

        :param device_name:
        :return :
        """
        try:
            device = device_name.upper().replace(" ", "")
            browser = BrowserClass()
            self.sync_app.open()
            self.sync_app.verify_kebab_options(device_name=device_name)
            self.sync_app.verify_kebab_option_device_update(device_name=device_name)
            browser.prepare_opened_browser()
            self.sync_app.device.click_kebab().click_quick_start_guide()
            self.sync_app.compare_url_with_opened_browser(eval(f"sync_config.{device}_QUICK_START_GUIDE"))
            self.sync_app.device.click_kebab().click_setup_video()
            self.sync_app.compare_url_with_opened_browser(eval(f"sync_config.{device}_SETUP_VIDEO"))
            self.sync_app.device.click_kebab().click_product_support()
            self.sync_app.compare_url_with_opened_browser(eval(f"sync_config.{device}_PRODUCT_SUPPORT"))
            self.sync_app.device.click_kebab().click_order_spare_parts()
            self.sync_app.compare_url_with_opened_browser(eval(f"sync_config.{device}_ORDER_SPARE_PARTS"))
        except Exception as e:
            Report.logException(str(e))
        self.sync_app.close()

    def tc_compare_syncapp_device_info_to_syncportal(self, device_name: str, update: bool = False):
        """
        Method to Compare device information displayed in Sync App to Sync Portal

        :param device_name:
        :param update:
        :return :
        """

        def compare_sync_values(param_name: str, param1: str, param2: str):
            if param1.upper() == param2.upper():
                Report.logPass(f'{param_name} displayed on Sync App and Sync Portal are same: {param1}')
            else:
                Report.logFail(f"{param_name} displayed in Sync App is {param1} and Sync Portal is {param2}")

        room_name = self.sync_app.open_and_get_room_name()
        sync_info = self.sync_app.home.click_device(device_name=device_name) \
            .get_device_information(device_name=device_name)
        try:
            device_info = self.sync_portal.get_device_information(room_name=room_name, device_name=device_name,
                                                                  update_flag=update)
            compare_sync_values("PID", sync_info["PID"], device_info["PID"])
            compare_sync_values("BLE Firmware", sync_info["BLE_Firmware"], device_info["BLE_Firmware"])
            compare_sync_values("EEPROM Firmware", sync_info["EEPROM_Firmware"], device_info["EEPROM_Firmware"])
            compare_sync_values("Video Firmware", sync_info["Video_Firmware"], device_info["Video_Firmware"])
            if device_name.upper() == "MEETUP":
                compare_sync_values("Audio Firmware", sync_info["Audio_Firmware"], device_info["Audio_Firmware"])
                compare_sync_values("Codec Firmware", sync_info["Codec_Firmware"], device_info["Codec_Firmware"])
        except Exception as e:
            Report.logException(str(e))
        self.sync_app.close()