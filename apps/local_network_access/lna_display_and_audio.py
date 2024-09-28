import time

from base.base_ui import UIBase
from extentreport.report import Report
from locators.local_network_access.lna_display_and_audio_locators import LNADisplayAndAudioLocators


class LNADisplayAndAudio(UIBase):
    """
    LNA Display and Audio page methods
    """

    def click_apply(self):
        """
        Method to click on Apply button which appears when settings changed
        :param :
        :return :
        """
        time.sleep(1)
        self.look_element(LNADisplayAndAudioLocators.BUTTON_APPLY).click()
        while self.verify_element(LNADisplayAndAudioLocators.BUTTON_APPLY, timeunit=2):
            time.sleep(1)
        return LNADisplayAndAudio()

    def expand_audio_section(self):
        """
        Method to expand Audio section
        :param :
        :return :LNADisplayAndAudio
        """
        e = self.look_element(LNADisplayAndAudioLocators.AUDIO_EXPAND)
        if "open" not in e.get_attribute('className'):
            Report.logInfo("Expanding Audio section")
            self.look_element(LNADisplayAndAudioLocators.AUDIO).click()
            time.sleep(2)
        return LNADisplayAndAudio()

    def enable_speaker_boost(self):
        """
        Method to Enable Speaker Boost Setting

        :param :
        :return :LNADisplayAndAudio
        """
        if not self.verify_speaker_boost_enabled():
            Report.logInfo("Enabling Speaker Boost in Device")
            self.look_element(LNADisplayAndAudioLocators.SPEAKER_BOOST).click()
            self.click_apply()
            if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
                Report.logPass("Changes applied Message displayed", True)
            else:
                Report.logWarning("Changes applied Message not displayed")
            time.sleep(2)
        return LNADisplayAndAudio()

    def disable_speaker_boost(self):
        """
        Method to Disable Speaker Boost Setting

        :param :
        :return :LNADisplayAndAudio
        """
        if self.verify_speaker_boost_enabled():
            Report.logInfo("Disabling Speaker Boost in Device")
            self.look_element(LNADisplayAndAudioLocators.SPEAKER_BOOST).click()
            self.click_apply()
            if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
                Report.logPass("Changes applied Message displayed", True)
            else:
                Report.logWarning("Changes applied Message not displayed")
            time.sleep(2)
        return LNADisplayAndAudio()

    def verify_speaker_boost_enabled(self) -> bool:
        """
        Method to Verify Speaker Boost Enabled
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.SPEAKER_BOOST)
        return e.is_selected()

    def toggle_ai_noise_suppression(self, noise_suppression: str):
        """
        Method to Toggle AI Noise Suppression Setting

        :param noise_suppression:
        :return :
        """
        try:
            if (noise_suppression.upper() == "ON" and not self.verify_ai_noise_suppression_enabled()) or \
                    (noise_suppression.upper() == "OFF" and self.verify_ai_noise_suppression_enabled()):
                Report.logInfo("Changing AI Noise Suppression in Device")
                self.look_element(LNADisplayAndAudioLocators.AI_NOISE_SUPPRESSION).click()
                self.click_apply()
                if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
                    Report.logPass("Changes applied Message displayed", True)
                else:
                    Report.logFail("Changes applied Message not displayed")
                time.sleep(2)
        except Exception as e:
            Report.logException(str(e))
            raise e

    def verify_ai_noise_suppression_enabled(self) -> bool:
        """
        Method to Verify AI Noise Suppression Enabled
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.AI_NOISE_SUPPRESSION)
        return e.is_selected()

    def verify_ai_noise_suppression_disable(self) -> bool:
        """
        Method to Verify AI Noise Suppression Disabled
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.AI_NOISE_SUPPRESSION)
        return e.is_selected()

    def set_reverb_control_disable(self):
        """
        Method to set Reverb Control Disable
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Reverb Control to Disable in Device")
        self.look_element(LNADisplayAndAudioLocators.REVERB_CONTROL_DISABLED).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_reverb_control_disable_selected(self) -> bool:
        """
        Method to Verify Reverb Control Disable is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.REVERB_CONTROL_DISABLED)
        return True if e.get_attribute('checked') == 'true' else False

    def set_reverb_control_normal(self):
        """
        Method to set Reverb Control to Normal
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Reverb Control to Normal in Device")
        time.sleep(1)
        self.look_element(LNADisplayAndAudioLocators.REVERB_CONTROL_NORMAL).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_reverb_control_normal_selected(self):
        """
        Method to Verify Reverb Control Normal is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.REVERB_CONTROL_NORMAL)
        return True if e.get_attribute('checked') == 'true' else False

    def set_reverb_control_aggressive(self):
        """
        Method to set Reverb Control to Aggressive
        :param :
        :return :LNADisplayAndAudio
        """
        self.look_element(LNADisplayAndAudioLocators.REVERB_CONTROL_AGGRESSIVE).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_reverb_control_aggressive_selected(self) -> bool:
        """
        Method to Verify Reverb Control Aggressive is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.REVERB_CONTROL_AGGRESSIVE)
        return True if e.get_attribute('checked') == 'true' else False

    def set_speaker_bass_boost(self):
        """
        Method to set Speaker EQ to Bass Boost
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Speaker EQ to Bass Boost in Device")
        self.look_element(LNADisplayAndAudioLocators.SPEAKER_BASS_BOOST).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_speaker_bass_boost_selected(self) -> bool:
        """
        Method to Verify Speaker EQ Bass Boost is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.SPEAKER_BASS_BOOST)
        return True if e.get_attribute('checked') == 'true' else False

    def set_speaker_normal(self):
        """
        Method to set Speaker EQ to Normal
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Speaker EQ to Normal in Device")
        self.look_element(LNADisplayAndAudioLocators.SPEAKER_NORMAL).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_speaker_normal_selected(self) -> bool:
        """
        Method to Verify Speaker Normal is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.SPEAKER_NORMAL)
        return True if e.get_attribute('checked') == 'true' else False

    def set_speaker_voice_boost(self):
        """
        Method to set Speaker EQ to Voice Boost
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Speaker EQ to Voice Boost in Device")
        self.look_element(LNADisplayAndAudioLocators.SPEAKER_VOICE_BOOST).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_speaker_voice_boost_selected(self) -> bool:
        """
        Method to Verify Speaker EQ Voice Boost is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.SPEAKER_VOICE_BOOST)
        return True if e.get_attribute('checked') == 'true' else False

    def set_microphone_bass_boost(self):
        """
        Method to set Microphone EQ to Bass Boost
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Microphone EQ to Bass Boost in Device")
        self.look_element(LNADisplayAndAudioLocators.MICROPHONE_BASS_BOOST).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_microphone_bass_boost_selected(self) -> bool:
        """
        Method to Verify Microphone EQ Bass Boost is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.MICROPHONE_BASS_BOOST)
        return True if e.get_attribute('checked') == 'true' else False

    def set_microphone_normal(self):
        """
        Method to set Microphone EQ to Normal
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Microphone EQ to Normal in Device")
        self.look_element(LNADisplayAndAudioLocators.MICROPHONE_NORMAL).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_microphone_normal_selected(self) -> bool:
        """
        Method to Verify Microphone Normal is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.MICROPHONE_NORMAL)
        return True if e.get_attribute('checked') == 'true' else False

    def set_microphone_voice_boost(self):
        """
        Method to set Microphone EQ to Voice Boost
        :param :
        :return :LNADisplayAndAudio
        """
        Report.logInfo("Setting Microphone EQ to Voice Boost in Device")
        self.look_element(LNADisplayAndAudioLocators.MICROPHONE_VOICE_BOOST).click()
        self.click_apply()
        if self.verify_element(LNADisplayAndAudioLocators.SUCCESS_MESSAGE, timeunit=15):
            Report.logPass("Changes applied Message displayed", True)
        else:
            Report.logWarning("Changes applied Message not displayed")
        time.sleep(2)
        return LNADisplayAndAudio()

    def verify_microphone_voice_boost_selected(self) -> bool:
        """
        Method to Verify Microphone EQ Voice Boost is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNADisplayAndAudioLocators.MICROPHONE_VOICE_BOOST)
        return True if e.get_attribute('checked') == 'true' else False
