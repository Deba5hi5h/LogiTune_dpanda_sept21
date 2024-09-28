import time

from apps.browser_methods import BrowserClass
from apps.local_network_access.lna_home import LNAHome
from apps.local_network_access.lna_login import LNALogin
from apps.local_network_access.lna_methods import LNAMethods
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report


class LNASyncAppMethods(LNAMethods):
    """
    LNA test methods
    """

    def verify_rightsight2_options_in_device(self, ip_address: str, user_name: str, password: str,
                                             group_view: bool, speaker_view: bool, picture_in_picture: bool = None):
        """
        Method to verify Speaker View or Group View is selected and picture in picture is enabled or disabled in
        Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param picture_in_picture:
        :param speaker_view:
        :param group_view:
        :return :
        """
        driver = global_variables.driver
        try:
            camera_page = self.login_to_local_network_access(ip_address=ip_address,
                                                             user_name=user_name, password=password) \
                .click_camera().expand_rightsight_section()
            if group_view:
                if camera_page.verify_group_view_selected():
                    Report.logPass("Group View is selected", True)
                else:
                    Report.logFail("Group View is not selected")
            if speaker_view:
                if camera_page.verify_speaker_view_selected():
                    Report.logPass("Speaker View is selected", True)
                else:
                    Report.logFail("Speaker View is not selected")
            if picture_in_picture is not None and picture_in_picture:
                if camera_page.verify_picture_in_picture_enabled():
                    Report.logPass("Picture in picture is enabled", True)
                else:
                    Report.logFail("Picture in picture is disabled")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_rightsight2_options_in_device(self, ip_address: str, user_name: str, password: str,
                                          group_view: bool, speaker_view: bool, picture_in_picture: bool = None):
        """
        Method to set Speaker View or Group View and picture in picture enabled/disabled in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param picture_in_picture:
        :param speaker_view:
        :param group_view:
        :return :
        """
        driver = global_variables.driver
        try:
            camera_page = self.login_to_local_network_access(ip_address=ip_address,
                                                             user_name=user_name, password=password) \
                .click_camera().expand_rightsight_section()
            if group_view:
                camera_page.set_group_view()
            if speaker_view:
                camera_page.set_speaker_view()
                if picture_in_picture:
                    time.sleep(5)
                    camera_page.enable_picture_in_picture()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_rightsight_in_device(self, ip_address: str, user_name: str, password: str, rightsight: bool):
        """
        Method to verify RightSight Enable/Disable in Local Network Access

        :param ip_address:
        :param user_name:
        :param password:
        :param rightsight:
        :return :
        """
        driver = global_variables.driver
        try:
            camera_page = self.login_to_local_network_access(ip_address=ip_address,
                                                             user_name=user_name, password=password) \
                .click_camera().expand_rightsight_section()
            if rightsight:
                if camera_page.verify_rightsight_enabled():
                    Report.logPass("Right Sight is enabled", True)
                else:
                    Report.logFail("Right Sight is disabled")
            else:
                if not camera_page.verify_rightsight_enabled():
                    Report.logPass("Right Sight is disabled", True)
                else:
                    Report.logFail("Right Sight is enabled")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_bluetooth_in_device(self, ip_address: str, user_name: str, password: str, bluetooth: str):
        """
        Method to verify bluetooth is ON/OFF in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param bluetooth: ON or OFF
        :return :
        """
        driver = global_variables.driver
        try:
            connectivity_page = self.login_to_local_network_access(ip_address=ip_address,
                                                                   user_name=user_name, password=password) \
                .click_connectivity().expand_bluetooth_section()
            time.sleep(2)
            if str(bluetooth).upper() == "ON":
                if connectivity_page.verify_bluetooth_enabled():
                    Report.logPass("Bluetooth is enabled in device", True)
                else:
                    Report.logFail("Bluetooth is disabled in device")
            else:
                if not connectivity_page.verify_bluetooth_enabled():
                    Report.logPass("Bluetooth is disabled in device", True)
                else:
                    Report.logFail("Bluetooth is enabled in device")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def toggle_bluetooth_in_device(self, ip_address: str, user_name: str, password: str, bluetooth: str):
        """
        Method to toggle bluetooth in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param bluetooth: ON or OFF
        """
        driver = global_variables.driver
        try:
            connectivity_page = self.login_to_local_network_access(ip_address=ip_address,
                                                                   user_name=user_name, password=password) \
                .click_connectivity().expand_bluetooth_section()
            if str(bluetooth).upper() == "ON":
                connectivity_page.enable_bluetooth()
            else:
                connectivity_page.disable_bluetooth()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_speaker_boost_in_device(self, ip_address: str, user_name: str, password: str, speaker_boost: str):
        """
        Method to verify Speaker Boost is ON/OFF in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param speaker_boost: ON or OFF
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(speaker_boost).upper() == "ON":
                if audio_page.verify_speaker_boost_enabled():
                    Report.logPass("Speaker Boost is enabled in Device", True)
                else:
                    Report.logFail("Speaker Boost is disabled in Device")
            else:
                if not audio_page.verify_speaker_boost_enabled():
                    Report.logPass("Speaker Boost is disabled in Device", True)
                else:
                    Report.logFail("Speaker Boost is enabled in Device")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def toggle_speaker_boost_in_device(self, ip_address: str, user_name: str, password: str, speaker_boost: str):
        """
        Method to toggle Speaker Boost to ON or OFF in Local Network Access
        
        :param ip_address: 
        :param user_name:
        :param password:
        :param speaker_boost: ON or OFF
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if speaker_boost.upper() == "ON":
                audio_page.enable_speaker_boost()
            else:
                audio_page.disable_speaker_boost()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_ai_noise_suppression_in_device(self, ip_address: str, user_name: str, password: str,
                                              noise_suppression: str):
        """
        Method to check Audio AI Noise Suppression ON/OFF in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param noise_suppression: ON/OFF
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(noise_suppression).upper() == "ON":
                if audio_page.verify_ai_noise_suppression_enabled():
                    Report.logPass("AI Noise Suppression is enabled in Device", True)
                else:
                    Report.logFail("AI Noise Suppression is disabled in Device")
            else:
                if not audio_page.verify_ai_noise_suppression_enabled():
                    Report.logPass("AI Noise Suppression is disabled in Device", True)
                else:
                    Report.logFail("AI Noise Suppression is enabled in Device")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def toggle_ai_noise_suppression_in_device(self, ip_address: str, user_name: str, password: str,
                                              noise_suppression: str):
        """
        Method to toggle AI Noise Suppression to ON or OFF in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param noise_suppression: ON or OFF
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            audio_page.toggle_ai_noise_suppression(noise_suppression=noise_suppression)
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_reverb_control_in_device(self, ip_address: str, user_name: str, password: str, reverb_control: str):
        """
        Method to check Audio Reverb Control Disabled/Normal/Agressive in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param reverb_control: Disabled/Normal/Agressive
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(reverb_control).upper() == "DISABLED":
                if audio_page.verify_reverb_control_disable_selected():
                    Report.logPass("Reverb Control is set to disabled in Device", True)
                else:
                    Report.logFail("Reverb Control is not set to disabled in Device")
            elif str(reverb_control).upper() == "NORMAL":
                if audio_page.verify_reverb_control_normal_selected():
                    Report.logPass("Reverb Control is set to Normal in Device", True)
                else:
                    Report.logFail("Reverb Control is not set to Normal in Device")
            elif str(reverb_control).upper() == "AGGRESSIVE":
                if audio_page.verify_reverb_control_aggressive_selected():
                    Report.logPass("Reverb Control is set to Aggressive in Device", True)
                else:
                    Report.logFail("Reverb Control is not set to Aggressive in Device")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_reverb_control_in_device(self, ip_address: str, user_name: str, password: str, reverb_control: str):
        """
        Method to set Audio Reverb Control to Disabled/Normal/Agressive in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param reverb_control: Disabled/Normal/Agressive
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(reverb_control).upper() == "DISABLED":
                audio_page.set_reverb_control_disable()
            elif str(reverb_control).upper() == "NORMAL":
                audio_page.set_reverb_control_normal()
            elif str(reverb_control).upper() == "AGGRESSIVE":
                audio_page.set_reverb_control_aggressive()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_microphone_eq_in_device(self, ip_address: str, user_name: str, password: str, microphone_eq: str):
        """
        Method to check Audio Microphone EQ Bass Boost/Normal/Voice Boost in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param microphone_eq: Bass Boost/Normal/Voice Boost
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(microphone_eq).upper() == "BASS BOOST":
                if audio_page.verify_microphone_bass_boost_selected():
                    Report.logPass("Microphone EQ Settings is set to Bass Boost in Device", True)
                else:
                    Report.logFail("Microphone EQ Settings is not set to Bass Boost in Device")
            elif str(microphone_eq).upper() == "NORMAL":
                if audio_page.verify_microphone_normal_selected():
                    Report.logPass("Microphone EQ Settings is set to Normal in Device", True)
                else:
                    Report.logFail("Microphone EQ Settings is not set to Normal in Device")
            elif str(microphone_eq).upper() == "VOICE BOOST":
                if audio_page.verify_microphone_voice_boost_selected():
                    Report.logPass("Microphone EQ Settings is set to Voice Boost in Device", True)
                else:
                    Report.logFail("Microphone EQ Settings is not set to Voice Boost in Device")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_microphone_eq_in_device(self, ip_address: str, user_name: str, password: str, microphone_eq: str):
        """
        Method to set Audio Microphone EQ to Bass Boost/Normal/Voice Boost in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param microphone_eq: Bass Boost/Normal/Voice Boost
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(microphone_eq).upper() == "BASS BOOST":
                audio_page.set_microphone_bass_boost()
            elif str(microphone_eq).upper() == "NORMAL":
                audio_page.set_microphone_normal()
            elif str(microphone_eq).upper() == "VOICE BOOST":
                audio_page.set_microphone_voice_boost()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def verify_speaker_eq_in_device(self, ip_address: str, user_name: str, password: str, speaker_eq: str):
        """
        Method to check Audio Speaker EQ Bass Boost/Normal/Voice Boost in Local Network Access

        :param ip_address: 
        :param user_name:
        :param password:
        :param speaker_eq: Boost/Normal/Voice Boost
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(speaker_eq).upper() == "BASS BOOST":
                if audio_page.verify_speaker_bass_boost_selected():
                    Report.logPass("Speaker EQ Settings is set to Bass Boost in Device", True)
                else:
                    Report.logFail("Speaker EQ Settings is not set to Bass Boost in Device")
            elif str(speaker_eq).upper() == "NORMAL":
                if audio_page.verify_speaker_normal_selected():
                    Report.logPass("Speaker EQ Settings is set to Normal in Device", True)
                else:
                    Report.logFail("Speaker EQ Settings is not set to Normal in Device")
            elif str(speaker_eq).upper() == "VOICE BOOST":
                if audio_page.verify_speaker_voice_boost_selected():
                    Report.logPass("Speaker EQ Settings is set to Voice Boost in Device", True)
                else:
                    Report.logFail("Speaker EQ Settings is not set to Voice Boost in Device")
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver

    def set_speaker_eq_in_device(self, ip_address: str, user_name: str, password: str, speaker_eq: str):
        """
        Method to set Audio Speaker EQ to Bass Boost/Normal/Voice Boost in Local Network Access
        
        :param ip_address: 
        :param user_name:
        :param password:
        :param speaker_eq: Boost/Normal/Voice Boost
        :return :
        """
        driver = global_variables.driver
        try:
            audio_page = self.login_to_local_network_access(ip_address=ip_address,
                                                            user_name=user_name, password=password) \
                .click_display_and_audio().expand_audio_section()
            if str(speaker_eq).upper() == "BASS BOOST":
                audio_page.set_speaker_bass_boost()
            elif str(speaker_eq).upper() == "NORMAL":
                audio_page.set_speaker_normal()
            elif str(speaker_eq).upper() == "VOICE BOOST":
                audio_page.set_speaker_voice_boost()
        except Exception as e:
            Report.logException(str(e))
        self.browser.close_browser()
        global_variables.driver = driver
