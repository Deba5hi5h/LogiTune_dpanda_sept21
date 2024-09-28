from apps.tune.tune_elements import TuneSlider, TuneSwitcher, TuneInput
from apps.collabos.coily.coily_logitune_settings_locators import TuneCoilySettingsLocators
from apps.collabos.coily.tune_coily_config import FORMAT_24H, FORMAT_AMPM
from typing import Union, Tuple
from apps.tune.TuneElectron import TuneElectron
from extentreport.report import Report
from base import global_variables
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

import selenium.common.exceptions
import base.base_settings
import random


def coily_settings_page_visible(fnc):
    try:
        def wrapper(*args, **kwargs):
            obj_inst: LogiTuneCoilyDeviceSettingsPage = args[0]
            if not obj_inst.check_if_in_coily_settings():
                obj_inst.open_coily_settings()
            res = fnc(*args, **kwargs)
            return res
        return wrapper
    except Exception as e:
        Report.logInfo("Exception in Settings Decoraotr")
        raise e


class LogiTuneCoilyDeviceSettingsPage:
    locators = TuneCoilySettingsLocators
    device_name = "Logi Dock Flex"

    def __init__(self, tune_app: TuneElectron):
        self.tune_app = tune_app
        self.brightness_slider = TuneSlider(self.tune_app,
                                            **self.locators.brightness_slider)
        self.privacy_mode_checkbox = TuneSwitcher(self.tune_app,
                                                  **self.locators.privacy_mode_switch)
        self.time_format_checkbox = TuneSwitcher(self.tune_app,
                                                 **self.locators.time_format_switch)

        self.away_message_input = TuneInput(self.tune_app,
                                            **self.locators.away_message)

    @staticmethod
    def check_if_locator_element_present_on_current_page(element: Tuple[str, str]) -> bool:
        verdict = True
        try:
            global_variables.driver.implicitly_wait(1)
            global_variables.driver.find_element(*element)
        except selenium.common.exceptions.NoSuchElementException:
            verdict = False
        finally:
            global_variables.driver.implicitly_wait(base.base_settings.IMPLICIT_WAIT)
            return verdict

    @staticmethod
    def dict_prettier(data: dict) -> str:
        return "</br>".join(f"{key}: {value}" for key, value in data.items())

    def check_if_in_coily_settings(self):
        for setting_element in {self.brightness_slider, self.privacy_mode_checkbox, self.time_format_checkbox,
                                self.away_message_input}:

            if not self.check_if_locator_element_present_on_current_page(setting_element.name_locator):
                return False
        return True

    def open_coily_settings(self):
        self.tune_app.open_device_in_my_devices_tab(self.device_name)

    def close_coily_settings(self):
        if self.check_if_in_coily_settings():
            self.tune_app.click_back_button_to_my_devices()

    @staticmethod
    def coily_brightness_to_tune_brightness(value: int) -> int:
        return int(value/255 * 99 + 1)

    @coily_settings_page_visible
    def set_initial_values(self, initial_values: Union[None, dict] = None):

        self.toggle_time_format()
        self.toggle_privacy_mode()
        self.set_brightness(random.randint(40, 60))

        if initial_values is None:
            initial_values = {
                "privacy_mode_enabled": False,
                "screen_brightness": 100,
                "time_format": FORMAT_AMPM
            }
        Report.logInfo("Setting Initial values for Logi Tune Coily Settings Page before tests: "
                       f"{initial_values}")
        self.set_privacy_mode(initial_values['privacy_mode_enabled'])
        self.set_brightness(self.coily_brightness_to_tune_brightness(initial_values['screen_brightness']))
        self.set_time_format(initial_values['time_format'])
        Report.logInfo(f"Values in Tune Coily set to {self.dict_prettier(initial_values)}", screenshot=True)

    @coily_settings_page_visible
    def get_current_settings_dict(self):
        current_settings = dict(
            privacy_mode_enabled=self.get_current_privacy_mode(),
            screen_brightness=self.get_current_brightness(),
            time_format=str(24 if self.time_format_checkbox.check_value() else 12))
        formatted_settings = "</br>" + self.dict_prettier(current_settings)
        Report.logInfo(f"Current settings in Logi Tune Coily: {formatted_settings}", screenshot=True)

        return current_settings

    def open_tune_app(self):
        self.tune_app.open_tune_app()

    @coily_settings_page_visible
    def get_current_brightness(self):
        return self.brightness_slider.check_value()

    @coily_settings_page_visible
    def set_brightness(self, value: int):
        self.brightness_slider.change_value(value)

    @coily_settings_page_visible
    def get_current_time_format(self):
        time_format = self.time_format_checkbox.check_value()
        if time_format:
            return FORMAT_24H
        else:
            return FORMAT_AMPM

    @coily_settings_page_visible
    def set_time_format(self, value: str):
        if value not in (FORMAT_24H, FORMAT_AMPM):
            Report.logException(f"Wrong time format provided! Expected values: {FORMAT_24H},{FORMAT_AMPM}")
        if value == FORMAT_24H:
            self.time_format_checkbox.switch_on()
        else:
            self.time_format_checkbox.switch_off()

    @coily_settings_page_visible
    def toggle_time_format(self):
        return self.time_format_checkbox.toggle()

    @coily_settings_page_visible
    def get_current_privacy_mode(self):
        return self.privacy_mode_checkbox.check_value()

    @coily_settings_page_visible
    def set_privacy_mode(self, value: bool):
        if value:
            self.privacy_mode_checkbox.switch_on()
        else:
            self.privacy_mode_checkbox.switch_off()

    @coily_settings_page_visible
    def toggle_privacy_mode(self) -> bool:
        return self.privacy_mode_checkbox.toggle()

    @coily_settings_page_visible
    def set_away_message(self, message: Union[str, None]):
        Report.logInfo(f"Setting away message to: {message}")
        self.open_away_message_popup()
        self.away_message_input.set_value(message)

    @coily_settings_page_visible
    def get_away_message(self):
        return self.away_message_input.get_value()

    @coily_settings_page_visible
    def open_away_message_popup(self):
        self.away_message_input.open_input_window()

    @coily_settings_page_visible
    def close_away_message_popup(self):
        self.away_message_input.close_without_submitting()

    @coily_settings_page_visible
    def set_away_message_and_submit(self, message: str):
        if message:
            Report.logInfo(f"Setting away message to:{message} and submiting")
            self.open_away_message_popup()
            self.away_message_input.set_value(message)
            self.away_message_input.submit_value()

    @coily_settings_page_visible
    def check_invalid_format_notification(self):
        self.away_message_input.tune_app.look_element(TuneCoilySettingsLocators)

    @coily_settings_page_visible
    def set_random_message_and_submit(self, msg_len: int):
        Report.logInfo(f"Setting away message to random with {msg_len} length.")
        return self.away_message_input.set_random_value(msg_len)

    @coily_settings_page_visible
    def verify_away_message_popup_page(self):
        self.open_away_message_popup()
        elements_to_check = {
            "Input Field": self.away_message_input.name_locator,
            "Close Button": self.away_message_input.close_without_submit,
            "Submit Button": self.away_message_input.submit_locator
        }
        Report.logInfo(f"Checking if {', '.join(elements_to_check.keys())} are present in away PopUp.")
        for name, locator in elements_to_check.items():
            element_present = self.tune_app.verify_element(locator)
            if not element_present:
                Report.logFail(f"Element {name} not present in Away Message PopUp")
            else:
                Report.logPass(f"Element {name} present in Away Message PopUp")

        self.close_away_message_popup()

    @coily_settings_page_visible
    def check_invalid_away_message(self):
        invalid_popup = self.away_message_input.check_invalid_away_message_popup()
        if not invalid_popup:
            Report.logFail("Invalid Away message popup not present when input empty", is_collabos=True)

        else:
            Report.logPass("Invalid Away message popup present when input empty", is_collabos=True)

        submit_clickable = self.away_message_input.check_if_submit_clickable()
        if submit_clickable:
            Report.logFail("Submit button is clickable even when the input is empty", is_collabos=True)
        else:
            Report.logPass("Submit button is not clickable", is_collabos=True)
        self.close_away_message_popup()
        self.close_coily_settings()

    @coily_settings_page_visible
    def check_if_clickable_by_locator(self, locator: Tuple[str, str]) -> bool:
        element: WebElement = self.tune_app.look_element(locator)
        return element.get_attribute('disabled') != 'true'

    @coily_settings_page_visible
    def check_if_brightness_increase_is_clickable(self, clickable: bool) -> None:
        if self.check_if_clickable_by_locator(self.brightness_slider.plus_locator) is clickable:
            Report.logPass(f"Brightness increase button Clickable Status is: {clickable} as intended")
        else:
            Report.logFail(f"Brightness increase button Clickable Status is not: {clickable} as intended")

    @coily_settings_page_visible
    def check_if_brightness_decrease_is_clickable(self, clickable: bool) -> None:
        if self.check_if_clickable_by_locator(self.brightness_slider.minus_locator) is clickable:
            Report.logPass(f"Brightness decrease button Clickable Status is: {clickable} as intended")
        else:
            Report.logFail(f"Brightness decrease button Clickable Status is not: {clickable} as intended")

    @coily_settings_page_visible
    def verify_parameters_persistence_after_reopening_settings(self):
        Report.logInfo("Checking Coily settings before closing settings window")
        before_closing_parameters = self.get_current_settings_dict()
        Report.logInfo(f"Settings before closing {before_closing_parameters:}")
        self.close_coily_settings()
        after_closing_parameters = self.get_current_settings_dict()
        Report.logInfo(f"Settings after reopening {after_closing_parameters}")

        if after_closing_parameters != before_closing_parameters:
            Report.logFail("Parameters after reopening Coily settings do not match")

        else:
            Report.logPass("Parameters after reopening Coily Settings persisted")

    @coily_settings_page_visible
    def set_away_message_with_emoji(self, message: str):
        Report.logInfo(f"Setting away message with emoji to: {message}")
        self.open_away_message_popup()
        raw_input = self.away_message_input.get_input_element()
        global_variables.driver.execute_script("arguments[0].value = '{}'".format(message), raw_input)
        raw_input.click()
        raw_input.send_keys(Keys.END)
        raw_input.send_keys(Keys.SPACE)
        raw_input.send_keys(Keys.BACKSPACE)
        self.away_message_input.submit_value()

    def set_settings_values_from_dict(self, values: dict) -> dict:

        formatted_settings = self.dict_prettier(values)
        Report.logInfo(f"Settings values in Logi Tune Coily Settings to: </br> {formatted_settings}")

        privacy_mode = values.get('privacy_mode_enabled')
        time_format = values.get('time_format')
        screen_brightness = values.get('screen_brightness')

        if privacy_mode:
            self.set_privacy_mode(privacy_mode)
        if time_format:
            self.set_time_format(time_format)
        if screen_brightness:
            self.set_brightness(screen_brightness)

        return self.get_current_settings_dict()




