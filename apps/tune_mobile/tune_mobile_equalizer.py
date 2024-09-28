import time

from apps.tune_mobile.config import tune_mobile_config
from apps.tune_mobile.tune_mobile import TuneMobile
from base.base_ui import UIBase
from locators.tune_mobile.tune_mobile_equalizer_locators import TuneMobileEqualizerLocators


class TuneMobileEqualizer(TuneMobile):

    def click_default(self):
        """
        Method to click default raido button

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Default"
        element = None
        if self.is_android_device():
            element = self.find_element(TuneMobileEqualizerLocators.EQ_SCROLL)
        for _ in range(6):
            if self.verify_element(TuneMobileEqualizerLocators.DEFAULT, timeout=2):
                break
            self.swipe(direction="down", element=element)
        self.find_element(TuneMobileEqualizerLocators.DEFAULT).click()
        return self

    def click_volume_boost(self):
        """
        Method to click Volume Boost raido button

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Volume Boost"
        self.find_element(TuneMobileEqualizerLocators.VOLUME_BOOST).click()
        return self

    def click_podcast(self):
        """
        Method to click Podcast raido button

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Podcast"
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.PODCAST_LABEL, timeout=1):
                break
            self.swipe_screen(direction="vertical", start=0.8, end=0.65)
        self.find_element(TuneMobileEqualizerLocators.PODCAST).click()
        return self

    def click_bass_boost(self):
        """
        Method to click Bass Boost raido button

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Bass Boost"
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.BASS_BOOST_LABEL, timeout=1):
                break
            self.swipe_screen(direction="vertical", start=0.8, end=0.65)
        self.find_element(TuneMobileEqualizerLocators.BASS_BOOST).click()
        time.sleep(1)
        self.find_element(TuneMobileEqualizerLocators.BASS_BOOST).click()
        return self

    def click_back(self):
        """
        Method to click Back navigation

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileEqualizerLocators.BACK).click()
        from apps.tune_mobile.tune_mobile_home import TuneMobileHome
        return TuneMobileHome()

    def get_eq_slider1_value(self):
        """
        Method to get Equalizer Slider 1 value

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_1)
        if self.is_android_device():
            return int(float(element.text)) - 128
        return 180 - element.location['y']

    def get_eq_slider2_value(self):
        """
        Method to get Equalizer Slider 2 value

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_2)
        if self.is_android_device():
            return int(float(element.text)) - 128
        return 180 - element.location['y']

    def get_eq_slider3_value(self):
        """
        Method to get Equalizer Slider 3 value

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_3)
        if self.is_android_device():
            return int(float(element.text)) - 128
        return 180 - element.location['y']

    def get_eq_slider4_value(self):
        """
        Method to get Equalizer Slider 4 value

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_4)
        if self.is_android_device():
            return int(float(element.text)) - 128
        return 180 - element.location['y']

    def get_eq_slider5_value(self):
        """
        Method to get Equalizer Slider 5 value

        :param :
        :return str:
        """
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_5)
        if self.is_android_device():
            return int(float(element.text)) - 128
        return 180 - element.location['y']

    def adjust_eq_slider1(self, value: int):
        """
        Method to adjust Equalizer Slider 1 Up or Down by value based on positive or negative respectively

        :param value:
        :return TuneMobileEqualizer:
        """
        if value == 0:
            return self
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_1)
        if self.is_android_device():
            self.adjust_slider_android(element=element, value=value)
        else:
            value *= 0.9
            self.adjust_slider(element=element, value=value)
        return self

    def adjust_eq_slider2(self, value: int):
        """
        Method to adjust Equalizer Slider 2 Up or Down by value based on positive or negative respectively

        :param value:
        :return TuneMobileEqualizer:
        """
        if value == 0:
            return self
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_2)
        if self.is_android_device():
            self.adjust_slider_android(element=element, value=value)
        else:
            value *= 0.9
            self.adjust_slider(element=element, value=value)
        return self

    def adjust_eq_slider3(self, value: int):
        """
        Method to adjust Equalizer Slider 3 Up or Down by value based on positive or negative respectively

        :param value:
        :return TuneMobileEqualizer:
        """
        if value == 0:
            return self
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_3)
        if self.is_android_device():
            self.adjust_slider_android(element=element, value=value)
        else:
            value *= 0.9
            self.adjust_slider(element=element, value=value)
        return self

    def adjust_eq_slider4(self, value: int):
        """
        Method to adjust Equalizer Slider 4 Up or Down by value based on positive or negative respectively

        :param value:
        :return TuneMobileEqualizer:
        """
        if value == 0:
            return self
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_4)
        if self.is_android_device():
            self.adjust_slider_android(element=element, value=value)
        else:
            value *= 0.9
            self.adjust_slider(element=element, value=value)
        return self

    def adjust_eq_slider5(self, value: int):
        """
        Method to adjust Equalizer Slider 5 Up or Down by value based on positive or negative respectively

        :param value:
        :return TuneMobileEqualizer:
        """
        if value == 0:
            return self
        element = self.find_element(TuneMobileEqualizerLocators.EQ_SLIDER_5)
        if self.is_android_device():
            self.adjust_slider_android(element=element, value=value)
        else:
            value *= 0.9
            self.adjust_slider(element=element, value=value)
        return self

    def verify_default_option(self) -> bool:
        """
        Method to verify Equalizer Default option displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.DEFAULT_LABEL)

    def verify_volume_boost_option(self) -> bool:
        """
        Method to verify Equalizer Volume Boost option displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.VOLUME_BOOST_LABEL)

    def verify_podcast_option(self) -> bool:
        """
        Method to verify Equalizer Podcast option displayed

        :param :
        :return bool:
        """
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.PODCAST_LABEL, timeout=1):
                return True
            self.swipe_screen(direction="vertical", start=0.8, end=0.65)
        return self.verify_element(TuneMobileEqualizerLocators.PODCAST_LABEL)

    def verify_bass_boost_option(self) -> bool:
        """
        Method to verify Equalizer Bass Boost option displayed

        :param :
        :return bool:
        """
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.BASS_BOOST_LABEL, timeout=1):
                return True
            self.swipe_screen(direction="vertical", start=0.8, end=0.65)
        return self.verify_element(TuneMobileEqualizerLocators.BASS_BOOST_LABEL)

    def verify_custom_option(self) -> bool:
        """
        Method to verify Equalizer Custom option displayed

        :param :
        :return bool:
        """
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.CUSTOM_LABEL, timeout=2):
                return True
            self.swipe_screen(direction="vertical", start=0.8, end=0.65)
        return self.verify_element(TuneMobileEqualizerLocators.CUSTOM_LABEL)

    def click_save_custom_preset(self):
        """
        Method to click Save Custom Preset link

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Save Custom Preset"
        self.find_element(TuneMobileEqualizerLocators.SAVE_CUSTOM_PRESET).click()
        return self

    def verify_save_custom_preset_displayed(self) -> bool:
        """
        Method to verify Save Custom Eq preset link displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.SAVE_CUSTOM_PRESET)

    def type_preset_name(self, preset_name: str):
        """
        Method to enter Preset Name

        :param preset_name:
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Preset Name"
        self.find_element(TuneMobileEqualizerLocators.PRESET_NAME_EDITBOX).send_keys(preset_name)
        return self

    def get_preset_name(self) -> str:
        """
        Method to get Preset Name

        :param :
        :return str:
        """
        value = 'value' if self.is_ios_device() else 'text'
        return self.find_element(TuneMobileEqualizerLocators.PRESET_NAME_EDITBOX).get_attribute(value)

    def click_save_button(self):
        """
        Method to click Save Custom Preset link

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Save"
        self.find_element(TuneMobileEqualizerLocators.SAVE_BUTTON).click()
        return self

    def click_surprise_me(self):
        """
        Method to click Surprise Me link

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Surprise me"
        self.find_element(TuneMobileEqualizerLocators.SURPRISE_ME).click()
        return self

    def click_close_preset(self):
        """
        Method to click close button

        :param :
        :return TuneMobileEqualizer:
        """
        UIBase.elementName = "Close"
        self.find_element(TuneMobileEqualizerLocators.CLOSE_PRESET).click()
        return self

    def verify_custom_preset(self, preset_name: str) -> bool:
        """
        Method to verify preset_name option displayed

        :param preset_name:
        :return bool:
        """
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.CUSTOM_PRESET_LABEL, param=preset_name, timeout=1):
                break
            self.swipe_screen(direction="vertical", start=0.8, end=0.5)
        return self.verify_element(TuneMobileEqualizerLocators.CUSTOM_PRESET_LABEL, param=preset_name, timeout=1)

    def click_edit_presets(self):
        """
        Method to click Edit Presets button

        :param :
        :return TuneMobileEqualizer:
        """
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.EDIT_PRESETS, timeout=1):
                break
            self.swipe_screen(direction="vertical", start=0.8, end=0.5)
        self.find_element(TuneMobileEqualizerLocators.EDIT_PRESETS).click()
        if self.verify_element(TuneMobileEqualizerLocators.EDIT_PRESETS, timeout=1):
            self.find_element(TuneMobileEqualizerLocators.EDIT_PRESETS).click()
        return self

    def click_delete_preset(self, preset_name: str):
        """
        Method to click delete preset_name

        :param preset_name:
        :return TuneMobileEqualizer:
        """
        self.find_element(TuneMobileEqualizerLocators.DELETE_PRESET, param=preset_name).click()
        return self

    def click_all_delete_presets(self):
        """
        Method to click all custom presets delete button

        :param :
        :return TuneMobileEqualizer:
        """
        elements = self.find_elements(TuneMobileEqualizerLocators.DELETE_ALL_PRESETS)
        while len(elements) >= 1:
            elements[0].click()
            time.sleep(1)
            elements = self.find_elements(TuneMobileEqualizerLocators.DELETE_ALL_PRESETS)
        return self

    def click_done(self):
        """
        Method to click Done button

        :param :
        :return TuneMobileEqualizer:
        """
        self.find_element(TuneMobileEqualizerLocators.DONE).click()
        return self

    def verify_done_displayed(self) -> bool:
        """
        Method to verify Done button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.DONE, timeout=3)

    def verify_save_displayed(self) -> bool:
        """
        Method to verify Save button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.SAVE_BUTTON, timeout=3)

    def verify_close_preset_displayed(self) -> bool:
        """
        Method to verify Close button displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.CLOSE_PRESET, timeout=3)

    def verify_surprise_me_displayed(self) -> bool:
        """
        Method to verify Surprise Me link displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.SURPRISE_ME)

    def verify_preset_name_textfield_displayed(self) -> bool:
        """
        Method to verify Preset Name Textfield displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.PRESET_NAME_EDITBOX)

    def click_got_it(self):
        """
        Method to click Got it button

        :param :
        :return TuneMobileEqualizer:
        """
        self.find_element(TuneMobileEqualizerLocators.GOT_IT).click()
        return self

    def verify_preset_limit_popup(self) -> bool:
        """
        Method to verify Preset Limit pop up displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.PRESET_LIMIT_POPUP)

    def verify_preset_limit_message(self) -> bool:
        """
        Method to verify Preset Limit message displayed

        :param :
        :return bool:
        """
        return self.verify_element(TuneMobileEqualizerLocators.PRESET_LIMIT_MESSAGE)

    def verify_edit_presets_displayed(self) -> bool:
        """
        Method to verify Preset Limit message displayed

        :param :
        :return bool:
        """
        for _ in range(2):
            if self.verify_element(TuneMobileEqualizerLocators.EDIT_PRESETS, timeout=1):
                break
            self.swipe_screen(direction="vertical", start=0.8, end=0.5)
        return self.verify_element(TuneMobileEqualizerLocators.EDIT_PRESETS)
