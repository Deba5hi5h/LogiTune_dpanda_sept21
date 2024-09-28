import time

from apps.sync.sync_config import SyncConfig
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_app.sync_app_device_audio_locators import SyncAppDeviceAudioLocators


class SyncDeviceAudio(UIBase):

    def click_test_mic(self):
        """
        Method to click on Test Mic button

        :param :
        :return SyncDeviceAudio:
        """
        self.look_element(SyncAppDeviceAudioLocators.TEST_MIC_BUTTON).click()
        return SyncDeviceAudio

    def click_test_speaker(self):
        """
        Method to click on Test Speaker button

        :param :
        :return SyncDeviceAudio:
        """
        self.look_element(SyncAppDeviceAudioLocators.TEST_SPEAKER).click()
        return SyncDeviceAudio

    def click_stop_playing(self):
        """
        Method to click on Test Speaker button

        :param :
        :return SyncDeviceAudio:
        """
        self.look_element(SyncAppDeviceAudioLocators.STOP_PLAYING_BUTTON, wait_for_visibility=True).click()
        return SyncDeviceAudio

    def enable_speaker_boost(self):
        """
        Method to enable Speaker Boost

        :param :
        :return SyncDeviceAudio:
        """
        if self.verify_speaker_boost_enabled(timeout=1, enabled=False):
            Report.logInfo("Enabling Speaker Boost")
            self.look_element(SyncAppDeviceAudioLocators.SPEAKER_BOOST).click()
            time.sleep(1)
            self.verify_speaker_boost_enabled()
        return SyncDeviceAudio()

    def disable_speaker_boost(self):
        """
        Method to disable Speaker Boost

        :param :
        :return SyncDeviceAudio:
        """
        if self.verify_speaker_boost_enabled(timeout=1, enabled=True):
            Report.logInfo("Disabling Speaker Boost")
            self.look_element(SyncAppDeviceAudioLocators.SPEAKER_BOOST).click()
            time.sleep(1)
            self.verify_speaker_boost_enabled(enabled=False)
        return SyncDeviceAudio()

    def enable_ai_noise_suppression(self):
        """
        Method to enable AI Noise Suppression

        :param :
        :return SyncDeviceAudio:
        """
        if self.verify_ai_noise_suppression_enabled(timeout=1, enabled=False):
            Report.logInfo("Enabling AI Noise Suppression")
            self.look_element(SyncAppDeviceAudioLocators.AI_NOISE_SUPPRESSION).click()
            time.sleep(1)
            self.verify_ai_noise_suppression_enabled()
        return SyncDeviceAudio()

    def disable_ai_noise_suppression(self):
        """
        Method to disable AI Noise Suppression

        :param :
        :return SyncDeviceAudio:
        """
        if self.verify_ai_noise_suppression_enabled(timeout=1, enabled=True):
            Report.logInfo("Disabling AI Noise Suppression")
            self.look_element(SyncAppDeviceAudioLocators.AI_NOISE_SUPPRESSION).click()
            time.sleep(1)
            self.verify_ai_noise_suppression_enabled(enabled=False)
        return SyncDeviceAudio()

    def click_reverb_control_disabled(self):
        """
        Method to click on Reverb Control Disabled Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Reverb Control Disabled"
        e = self.look_element(SyncAppDeviceAudioLocators.REVERB_DISABLE_RADIO)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_reverb_control_normal(self):
        """
        Method to click on Reverb Control Normal Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Reverb Control Normal"
        e = self.look_element(SyncAppDeviceAudioLocators.REVERB_NORMAL_RADIO)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_reverb_control_aggressive(self):
        """
        Method to click on Reverb Control Aggressive Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Reverb Control Aggressive"
        e = self.look_element(SyncAppDeviceAudioLocators.REVERB_AGGRESSIVE_RADIO)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_microphone_eq_bass_boost(self):
        """
        Method to click on Microphone Eq Bass Boost Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Microphone Eq Bass Boost"
        e = self.look_element(SyncAppDeviceAudioLocators.MICROPHONE_BASS_BOOST)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_microphone_eq_normal(self):
        """
        Method to click on Microphone Eq Normal Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Microphone Eq Normal"
        e = self.look_element(SyncAppDeviceAudioLocators.MICROPHONE_NORMAL)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_microphone_eq_voice_boost(self):
        """
        Method to click on Microphone Eq Voice Boost Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Microphone Eq Voice Boost"
        e = self.look_element(SyncAppDeviceAudioLocators.MICROPHONE_VOICE_BOOST)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_speaker_eq_bass_boost(self):
        """
        Method to click on Speaker Eq Bass Boost Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker Eq Bass Boost"
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_BASS_BOOST)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_speaker_eq_normal(self):
        """
        Method to click on Speaker Eq Normal Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker Eq Normal"
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_NORMAL)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def click_speaker_eq_voice_boost(self):
        """
        Method to click on Speaker Eq Voice Boost Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker Eq Voice Boost"
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_VOICE_BOOST)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceAudio()

    def verify_stop_recording(self) -> bool:
        """
        Method to verify Stop Recording button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceAudioLocators.STOP_RECORDING_BUTTON, wait_for_visibility=True)

    def verify_test_mic(self) -> bool:
        """
        Method to verify Test Mic button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceAudioLocators.TEST_MIC_BUTTON, wait_for_visibility=True)

    def verify_test_speaker(self) -> bool:
        """
        Method to verify Test Speaker button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceAudioLocators.TEST_SPEAKER, wait_for_visibility=True)

    def verify_stop_playing(self) -> bool:
        """
        Method to verify Stop Playing button displayed

        :param :
        :return bool:
        """
        return self.verify_element(SyncAppDeviceAudioLocators.STOP_PLAYING_BUTTON, wait_for_visibility=True)

    def verify_speaker_boost_enabled(self, timeout: int = None, enabled: bool = True) -> bool:
        """
        Method to verify Framing Speed Default is Enabled

        :param timeout:
        :param enabled:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_BOOST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=enabled)

    def verify_ai_noise_suppression_enabled(self, timeout: int = None, enabled: bool = True) -> bool:
        """
        Method to verify AI Noise Suppression is Enabled

        :param timeout:
        :param enabled:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.AI_NOISE_SUPPRESSION)
        return SyncConfig.is_selected(e, timeout=timeout, selected=enabled)

    def verify_reverb_control_disabled_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Reverb Control Disabled is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.REVERB_DISABLE_RADIO)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_reverb_control_normal_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Reverb Control Normal is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.REVERB_NORMAL_RADIO)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_reverb_control_aggressive_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Reverb Control Aggressive is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.REVERB_AGGRESSIVE_RADIO)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_microphone_eq_bass_boost_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Microphone EQ Bass Boost is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.MICROPHONE_BASS_BOOST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_microphone_eq_normal_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Microphone EQ Normal is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.MICROPHONE_NORMAL)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_microphone_eq_voice_boost_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Microphone EQ Voice Boost is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.MICROPHONE_VOICE_BOOST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_speaker_eq_bass_boost_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Speaker EQ Bass Boost is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_BASS_BOOST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_speaker_eq_normal_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Speaker EQ Normal is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_NORMAL)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_speaker_eq_voice_boost_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to Speaker EQ Voice Boost is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceAudioLocators.SPEAKER_VOICE_BOOST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

