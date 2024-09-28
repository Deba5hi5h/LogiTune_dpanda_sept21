import time

from apps.collabos.coily.coily_methods import TuneCoilyMethods
from locators.coily_locators import TuneCoilySettingsLocators
from extentreport.report import Report
from typing import Tuple
from appium.webdriver.webdriver import MobileWebElement
from apps.collabos.coily.tune_coily_config import FORMAT_24H, FORMAT_AMPM


def enter_exit_settings_decorator(fnc):
    try:
        def wrapper(*args, **kwargs):
            args[0].open_coily_settings_from_authenticated_page()
            res = fnc(*args, **kwargs)
            args[0].close_settings_page()
            return res
        return wrapper
    except Exception as e:
        Report.logInfo("Exception in Settings Decoraotr")
        raise e


class CoilyBaseElement:
    def __init__(self, locator: Tuple[str, str],
                 coily_methods: TuneCoilyMethods):

        self.coily_methods = coily_methods
        self.driver_object: MobileWebElement = coily_methods.find_element_collabos(locator)


class CoilyCheckBox(CoilyBaseElement):
    def __init__(self, locator: Tuple[str, str],
                 coily_methods: TuneCoilyMethods):
        super().__init__(locator, coily_methods)

    @staticmethod
    def get_element_attribute_bool(checkbox: MobileWebElement, attribute: str):
        time.sleep(1)
        attr = checkbox.get_attribute(attribute)
        if attr == 'true':
            return True
        else:
            return False

    def manipulate_checkbox(self, value: bool):
        current_value = self.get_element_attribute_bool(self.driver_object, 'checked')
        if value != current_value:
            self.driver_object.click()

    def toggle_checkbox(self):
        self.driver_object.click()

    def get_checkbox_value(self) -> bool:
        current_value = self.get_element_attribute_bool(self.driver_object, 'checked')
        return current_value


class CoilySlider(CoilyBaseElement):
    def __init__(self, locator: Tuple[str, str],
                 coily_methods: TuneCoilyMethods):
        super().__init__(locator, coily_methods)

    def manipulate_slider(self, value: int):
        self.driver_object.send_keys(f"{value}.0")

    def get_slider_value(self) -> int:
        time.sleep(1)
        current_value = self.driver_object.text
        return int(float(current_value))


class TuneCoilySettingsPage:
    def __init__(self, coily_methods: TuneCoilyMethods):
        self.methods = coily_methods
        self._time_format = None
        self._show_agenda = None
        self._privacy_mode = None
        self._brightness_slider = None

    def open_coily_settings_from_authenticated_page(self):
        header_present = self.methods.verify_element_present_currently_collabos(TuneCoilySettingsLocators.SETTINGS_HEADER)
        if header_present:
            return
        self.methods.find_element_collabos(TuneCoilySettingsLocators.SETTINGS_FROM_MAIN_MENU).click()
        header_present = self.methods.verify_element_present_currently_collabos(TuneCoilySettingsLocators.SETTINGS_HEADER)

        if header_present:
            self._time_format = CoilyCheckBox(TuneCoilySettingsLocators.TIME_FORMAT, self.methods)
            self._show_agenda = CoilyCheckBox(TuneCoilySettingsLocators.SHOW_AGENDA, self.methods)
            self._privacy_mode = CoilyCheckBox(TuneCoilySettingsLocators.PRIVATE_AGENDA_ITEMS, self.methods)
            self._brightness_slider = CoilySlider(TuneCoilySettingsLocators.BRIGHTNESS_BAR, self.methods)
            Report.logInfo("Succesfully entered Coily Settings Page")

    def close_settings_page(self):
        self.methods.find_element_collabos(TuneCoilySettingsLocators.CLOSE_BUTTON).click()
        clock_present = self.methods.verify_element_collabos(TuneCoilySettingsLocators.CLOCK_MAIN_PAGE)
        if clock_present:
            Report.logInfo("Succesfully entered Coily Main Page")

    @enter_exit_settings_decorator
    def get_current_settings_dict(self):
        current_settings = dict(
            agenda_enabled=self._show_agenda.get_checkbox_value(),
            privacy_mode_enabled=self._privacy_mode.get_checkbox_value(),
            screen_brightness=self._brightness_slider.get_slider_value(),
            time_format=str(24 if self._time_format.get_checkbox_value() else 12))
        Report.logInfo(f"Current settings values in Coily: {current_settings}", is_collabos=True, screenshot=True)
        return current_settings

    @enter_exit_settings_decorator
    def get_current_time_format(self):
        time_format = self._time_format.get_checkbox_value()
        Report.logInfo(f"Current time_format24 on Coily: {time_format}", is_collabos=True, screenshot=True)
        if time_format:
            return FORMAT_24H
        else:
            return FORMAT_AMPM

    @enter_exit_settings_decorator
    def set_time_format(self, value: str):
        if value == FORMAT_24H:
            self._time_format.manipulate_checkbox(True)
        else:
            self._time_format.manipulate_checkbox(False)

    @enter_exit_settings_decorator
    def toggle_time_format(self):
        self._time_format.toggle_checkbox()

    @enter_exit_settings_decorator
    def get_current_show_agenda_status(self):
        show_agenda = self._show_agenda.get_checkbox_value()
        Report.logInfo(f"Current show_agenda on Coily: {show_agenda}", is_collabos=True, screenshot=True)
        return show_agenda

    @enter_exit_settings_decorator
    def set_show_agenda(self, value: bool):
        self._show_agenda.manipulate_checkbox(value)

    @enter_exit_settings_decorator
    def toggle_show_agenda(self):
        self._show_agenda.toggle_checkbox()

    def verify_privacy_mode(self, value: bool):
        current_value = self.get_current_privacy_mode_status()
        if current_value is not value:
            Report.logInfo(f"Privacy mode in Tune ({value}) "
                           f"differs from privacy mode in Coily ({current_value}).",
                           screenshot=True,
                           color='red')
            Report.logFail(f"Privacy mode in Tune ({value}) "
                           f"differs from privacy mode in Coily ({current_value}).",
                           is_collabos=True)
        else:
            Report.logInfo("Privacy mode in Tune is same as Privacy Mode in Coily.")

    @enter_exit_settings_decorator
    def get_current_privacy_mode_status(self):
        privacy_mode = self._privacy_mode.get_checkbox_value()
        Report.logInfo(f"Current privacy_mode on Coily: {privacy_mode}", is_collabos=True, screenshot=True)
        return privacy_mode

    @enter_exit_settings_decorator
    def set_privacy_mode(self, value: bool):
        self._privacy_mode.manipulate_checkbox(value)

    @enter_exit_settings_decorator
    def toggle_privacy_mode(self):
        self._privacy_mode.toggle_checkbox()

    @enter_exit_settings_decorator
    def get_current_brightness(self):
        brightness = self._brightness_slider.get_slider_value()
        Report.logInfo(f"Current brightness on Coily: {brightness}", is_collabos=True, screenshot=True)
        return brightness

    @enter_exit_settings_decorator
    def set_brightness_value(self, value: int):
        self._brightness_slider.manipulate_slider(value)
