import time

from apps.tune_mobile.tune_mobile import TuneMobile
from base.base_ui import UIBase
from locators.tune_mobile.tune_mobile_home_locators import TuneMobileHomeLocators


class TuneMobileHome(TuneMobile):

    def click_settings(self):
        """
        Method to click Settings

        :param :
        :return TuneMobileSettings:
        """
        if not self.verify_element(TuneMobileHomeLocators.SETTINGS, timeout=1):
            self.swipe_screen("vertical", 0.8, 0.2)
        self.find_element(TuneMobileHomeLocators.SETTINGS).click()
        if self.verify_element(TuneMobileHomeLocators.SETTINGS, timeout=2):
            self.find_element(TuneMobileHomeLocators.SETTINGS).click()
        from apps.tune_mobile.tune_mobile_settings import TuneMobileSettings
        return TuneMobileSettings()

    def click_settings_no_device(self):
        """
        Method to click Settings

        :param :
        :return TuneMobileSettings:
        """
        self.find_element(TuneMobileHomeLocators.SETTINGS_NO_DEVICE).click()
        from apps.tune_mobile.tune_mobile_settings import TuneMobileSettings
        return TuneMobileSettings()

    def click_equalizer(self):
        """
        Method to click Equalizer

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Equalizer"
        self.find_element(TuneMobileHomeLocators.EQUALIZER).click()
        from apps.tune_mobile.tune_mobile_equalizer import TuneMobileEqualizer
        return TuneMobileEqualizer()

    def click_personal_eq_toggle(self):
        """
        Method to click Personal EQ Toggle

        :param :
        :return TuneMobileSidetone:
        """
        UIBase.elementName = "Personal EQ Toggle"
        if not self.verify_element(TuneMobileHomeLocators.PERSONAL_EQ_TOGGLE, timeout=2):
            self.swipe_screen("vertical", 0.3, 0.6)
        self.find_element(TuneMobileHomeLocators.PERSONAL_EQ_TOGGLE).click()
        from apps.tune_mobile.tune_mobile_personal_eq import TuneMobilePersonalEq
        return TuneMobilePersonalEq()

    def click_device_name(self):
        """
        Method to click Device Name

        :param :
        :return TuneMobileDeviceName:
        """
        UIBase.elementName = "Device Name"
        self.find_element(TuneMobileHomeLocators.DEVICE_NAME_VALUE).click()
        from apps.tune_mobile.tune_mobile_device_name import TuneMobileDeviceName
        return TuneMobileDeviceName()

    def click_button_functions(self):
        """
        Method to click Button Functions

        :param :
        :return TuneMobileButtonFunctions:
        """
        UIBase.elementName = "Device Name"
        self.find_element(TuneMobileHomeLocators.BUTTON_FUNCTIONS).click()
        from apps.tune_mobile.tune_mobile_button_functions import TuneMobileButtonFunctions
        return TuneMobileButtonFunctions()

    def click_sidetone(self):
        """
        Method to click Sidetone

        :param :
        :return TuneMobileSidetone:
        """
        UIBase.elementName = "Sidetone"
        if not self.verify_element(TuneMobileHomeLocators.SIDETONE, timeout=2):
            self.swipe_screen("vertical", 0.3, 0.6)
        self.find_element(TuneMobileHomeLocators.SIDETONE).click()
        from apps.tune_mobile.tune_mobile_sidetone import TuneMobileSidetone
        return TuneMobileSidetone()

    def click_advanced_call_clarity(self):
        """
        Method to click Advanced call clarity

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "Advanced call clarity"
        self.find_element(TuneMobileHomeLocators.ADVANCED_CALL_CLARITY).click()
        from apps.tune_mobile.tune_mobile_advanced_call_clarity import TuneMobileAdvancedCallClarity
        return TuneMobileAdvancedCallClarity()

    def click_sleep_settings(self):
        """
        Method to click Sleep Settings

        :param :
        :return TuneMobileSleepSettings:
        """
        UIBase.elementName = "Sleep Settings"
        self.find_element(TuneMobileHomeLocators.SLEEP_SETTINGS).click()
        from apps.tune_mobile.tune_mobile_sleep_settings import TuneMobileSleepSettings
        return TuneMobileSleepSettings()

    def click_anc_buttion_options(self):
        """
        Method to click ANC button options

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "ANC button options"
        self.find_element(TuneMobileHomeLocators.ANC_BUTTON_OPTIONS).click()
        from apps.tune_mobile.tune_mobile_anc import TuneMobileANC
        return TuneMobileANC()

    def click_on_head_detection(self):
        """
        Method to click On-head detection

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "On-head detection"
        if not self.verify_element(TuneMobileHomeLocators.ON_HEAD_DETCTION, timeout=2):
            self.swipe_screen("vertical", 0.8, 0.2)
        self.find_element(TuneMobileHomeLocators.ON_HEAD_DETCTION).click()
        from apps.tune_mobile.tune_mobile_on_head_detection import TuneMobileOnHeadDetection
        return TuneMobileOnHeadDetection()

    def click_touch_pad(self):
        """
        Method to click Touch Pad

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "Touch Pad"
        if not self.verify_element(TuneMobileHomeLocators.TOUCH_PAD, timeout=2):
            self.swipe_screen("vertical", 0.8, 0.3)
        self.find_element(TuneMobileHomeLocators.TOUCH_PAD).click()
        from apps.tune_mobile.tune_mobile_touch_pad import TuneMobileTouchPad
        return TuneMobileTouchPad()

    def click_voice_prompts(self):
        """
        Method to click Voice Prompts

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "Voice Prompts"
        if not self.verify_element(TuneMobileHomeLocators.VOICE_PROMPTS, timeout=2):
            self.swipe_screen("vertical", 0.8, 0.3)
        self.find_element(TuneMobileHomeLocators.VOICE_PROMPTS).click()
        from apps.tune_mobile.tune_mobile_voice_prompts import TuneMobileVoicePrompts
        return TuneMobileVoicePrompts()

    def click_health_and_safety(self):
        """
        Method to click Health and Safety

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "Health and Safety"
        if not self.verify_element(TuneMobileHomeLocators.HEALTH_AND_SAFETY, timeout=2):
            self.swipe_screen("vertical", 0.8, 0.2)
        self.find_element(TuneMobileHomeLocators.HEALTH_AND_SAFETY).click()
        from apps.tune_mobile.tune_mobile_health_and_safety import TuneMobileHealthAndSafety
        return TuneMobileHealthAndSafety()

    def click_headset_language(self):
        """
        Method to click Headset Language

        :param :
        :return TuneMobileHeadsetLanguage:
        """
        UIBase.elementName = "Headset Language"
        if not self.verify_element(TuneMobileHomeLocators.HEADSET_LANGUAGE, timeout=1):
            self.swipe_screen("vertical", 0.7, 0.2)
        self.find_element(TuneMobileHomeLocators.HEADSET_LANGUAGE).click()
        from apps.tune_mobile.tune_mobile_headset_language import TuneMobileHeadsetLanguage
        return TuneMobileHeadsetLanguage()

    def click_connected_devices(self):
        """
        Method to click Connected Devices

        :param :
        :return TuneMobileConnectedDevices:
        """
        UIBase.elementName = "Connected Devices"
        if not self.verify_element(TuneMobileHomeLocators.CONNECTED_DEVICES, timeout=1):
            self.swipe_screen("vertical", 0.7, 0.2)
        self.find_element(TuneMobileHomeLocators.CONNECTED_DEVICES).click()
        from apps.tune_mobile.tune_mobile_connected_devices import TuneMobileConnectedDevices
        return TuneMobileConnectedDevices()

    def get_equalizer_value(self) -> str:
        """
        Method to get Equalizer value

        :param :
        :return str:
        """
        value = 'value' if self.is_ios_device() else 'text'
        return self.find_element(TuneMobileHomeLocators.EQUALIZER).get_attribute(value)

    def click_back(self):
        """
        Method to get Equalizer value

        :param :
        :return str:
        """
        if self.verify_element(TuneMobileHomeLocators.BACK, timeout=2):
            self.find_element(TuneMobileHomeLocators.BACK).click()

    def get_device_name_value(self) -> str:
        """
        Method to get Device Name value

        :param :
        :return str:
        """
        value = 'value' if self.is_ios_device() else 'text'
        return self.find_element(TuneMobileHomeLocators.DEVICE_NAME_VALUE).get_attribute(value)

    def get_sidetone_value(self) -> str:
        """
        Method to get Sidetone value

        :param :
        :return str:
        """
        value = 'label' if self.is_ios_device() else 'text'
        return self.find_element(TuneMobileHomeLocators.SIDETONE).get_attribute(value)

    def get_sleep_settings_value(self) -> str:
        """
        Method to get Sleep Settings value

        :param :
        :return str:
        """
        value = 'label' if self.is_ios_device() else 'text'
        return self.find_element(TuneMobileHomeLocators.SLEEP_SETTINGS).get_attribute(value)

    def verify_settings_button(self) -> bool:
        """
        Method to verify Settings button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileHomeLocators.SETTINGS)
