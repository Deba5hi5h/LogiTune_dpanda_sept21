import random
from typing import Optional, Any

from selenium.webdriver.common.by import By
from apps.tune.devices_base_helpers import TuneDevicePersistency
from apps.tune.helpers import exception_handler
from apps.tune.streaming_light.streaming_light import StreamingLightParametersWrapper, StreamingLightProperties
from apps.tune.TuneElectron import TuneElectron
from common.usb_switch import *
from extentreport.report import Report
from locators.tunes_ui_locators import TunesAppLocators
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.device_config_litra_beam import litra_beam_presets


class TuneStreamingLightPersistency(TuneDevicePersistency):
    def __init__(self, streaming_light_name: str, tune_app: Optional[TuneElectron] = None):
        super().__init__(streaming_light_name, StreamingLightParametersWrapper, tune_app)
        self.streaming_light: StreamingLightProperties = self.device
        self.streaming_light_methods = TuneStreamingLightMethods(streaming_light_name=streaming_light_name, tune_app=self.tune_app)

    @exception_handler
    def check_persistency(self, acroname_automatic: bool = True) -> None:
        self._set_random_adjustments()
        self._reconnect_device(acroname_automatic)
        self._get_adjustments()

    @exception_handler
    def check_parameters_persistency_after_fw_update(self,
                                                     fw_update: Any,
                                                     file_path_baseline: str,
                                                     file_path_target: str):

        self.tune_app.open_device_in_my_devices_tab(self.streaming_light.name)
        self.tune_app.open_about_the_device(device_name=self.streaming_light.name)
        self.tune_app.update_firmware_with_easter_egg(
            device_file_path=file_path_baseline,
            device_name=self.streaming_light.name,
            timeout=fw_update.timeout,
        )

        if self.tune_app.verify_back_button_to_device_settings():
            self.tune_app.click_back_button_to_device_settings()

        self._set_random_adjustments()

        self.tune_app.open_about_the_device(device_name=self.streaming_light.name)
        self.tune_app.start_update_from_device_tab(device_name=self.streaming_light.name)

        if self.tune_app.verify_back_button_to_device_settings():
            self.tune_app.click_back_button_to_device_settings()

        self._get_adjustments()

    @exception_handler
    def check_parameters_persistency_after_tune_relaunching(self):
        self._set_random_adjustments()
        time.sleep(2)
        self.tune_app.relaunch_tune_app()
        self._get_adjustments()

    @exception_handler
    def check_preset_persistency_after_litra_reconnection(self, acroname_automatic: Optional[bool] = True):
        litra_methods = TuneStreamingLightMethods(streaming_light_name=self.streaming_light.name,
                                                  tune_app=self.tune_app)

        litra_methods.open_tune_open_litra_and_power_on(device_name=self.streaming_light.name)
        litra_methods.change_preset_to_random_one()
        preset_before_reconnection = self.tune_app.get_current_litra_preset_name()

        self._reconnect_device(acroname_automatic=acroname_automatic)

        self.tune_app.click_device(self.streaming_light.name)
        preset_after_reconnection = self.tune_app.get_current_litra_preset_name()

        if preset_before_reconnection == preset_after_reconnection:
            Report.logPass(f'{self.streaming_light.name} preset persisted properly after Litra reconnection.')
        else:
            Report.logFail(f'{self.streaming_light.name} preset NOT persisted properly after Litra reconnection.')

    @exception_handler
    def check_preset_persistency_after_litra_update(self,
                                                    fw_update: Any,
                                                    file_path_baseline: str,
                                                    file_path_target: str):
        litra_methods = TuneStreamingLightMethods(streaming_light_name=self.streaming_light.name,
                                                  tune_app=self.tune_app)

        self.tune_app.open_device_in_my_devices_tab(self.streaming_light.name)
        self.tune_app.open_about_the_device(device_name=self.streaming_light.name)
        self.tune_app.update_firmware_with_easter_egg(
            device_file_path=file_path_baseline,
            device_name=self.streaming_light.name,
            timeout=fw_update.timeout,
        )

        if self.tune_app.verify_back_button_to_device_settings():
            self.tune_app.click_back_button_to_device_settings()

        litra_methods.power_on()
        litra_methods.change_preset_to_random_one()
        preset_before_reconnection = self.tune_app.get_current_litra_preset_name()

        self.tune_app.open_about_the_device(device_name=self.streaming_light.name)
        self.tune_app.start_update_from_device_tab(device_name=self.streaming_light.name)

        if self.tune_app.verify_back_button_to_device_settings():
            self.tune_app.click_back_button_to_device_settings()

        preset_after_reconnection = self.tune_app.get_current_litra_preset_name()

        if preset_before_reconnection == preset_after_reconnection:
            Report.logPass(f'{self.streaming_light.name} preset persisted properly after Litra firmware update.')
        else:
            Report.logFail(f'{self.streaming_light.name} preset NOT persisted properly after Litra firmware update.')

    @exception_handler
    def check_preset_persistency_after_tune_relaunching(self):
        litra_methods = TuneStreamingLightMethods(streaming_light_name=self.streaming_light.name,
                                                  tune_app=self.tune_app)

        litra_methods.open_tune_open_litra_and_power_on(device_name=self.streaming_light.name)
        litra_methods.change_preset_to_random_one()
        preset_before_reconnection = self.tune_app.get_current_litra_preset_name()

        time.sleep(2)
        self.tune_app.relaunch_tune_app()
        self.tune_app.click_device(self.streaming_light.name)
        preset_after_reconnection = self.tune_app.get_current_litra_preset_name()

        if preset_before_reconnection == preset_after_reconnection:
            Report.logPass(f'{self.streaming_light.name} preset persisted properly after Tune relaunching.')
        else:
            Report.logFail(f'{self.streaming_light.name} preset NOT persisted properly after Tune relaunching.')

    def _set_random_adjustments(self) -> None:
        self.tune_app.click_device(self.streaming_light.name)
        self._get_expected_values_from_litra_settings()

    def _get_adjustments(self):
        self.tune_app.click_device(self.streaming_light.name)
        self._check_if_values_persisted()
        self._persistency_results()

    def _get_expected_values_from_litra_settings(self) -> None:
        time.sleep(5)
        self.device_parameters.append(self._set_and_get_switch_value(self.streaming_light.power_on))
        self.device_parameters.append(self._get_expected_value(self.streaming_light.light_temperature))

        max_available_brightness = 240

        self.device_parameters.append(self._get_expected_value(
            self.streaming_light.light_brightness, max_value=max_available_brightness))

    def _check_if_values_persisted(self) -> None:
        time.sleep(5)
        self._compare_current_value_with_expected(self.streaming_light.power_on, self.device_parameters)
        self._compare_current_value_with_expected(self.streaming_light.light_temperature, self.device_parameters)
        self._compare_current_value_with_expected(self.streaming_light.light_brightness, self.device_parameters)


class TuneStreamingLightMethods:
    # ------ Methods ------
    def __init__(self, streaming_light_name: str, tune_app: Optional[TuneElectron] = None):
        self.tune_app = tune_app if tune_app else TuneElectron()
        self.streaming_light: StreamingLightProperties = StreamingLightParametersWrapper(self.tune_app).get_by_name(streaming_light_name)

    def get_max_available_brightness(self, responsiveness_check: bool = False) -> int:
        """
        Method to get maximal available brightness
        @param responsiveness_check: True is method is used in responsiveness check. Otherwise False
        and maximal available brightness is based on information whether brightness plus button
        is clickable.
        """
        max_brightness = self.tune_app.get_litra_max_defined_brightness()
        power_warning = self.tune_app.verify_litra_power_warning()
        if power_warning:
            if not responsiveness_check:
                while self.tune_app.verify_litra_brightness_up_enable():
                    self.tune_app.click_litra_brightness_up()
            else:
                self.streaming_light.light_brightness.change_to_exact_value(int(max_brightness))

            max_available_brightness = self.tune_app.get_current_litra_brightness()
        else:
            Report.logInfo('Litra power supply warning not found')
            max_available_brightness = max_brightness

        return int(max_available_brightness)

    def open_tune_open_litra_and_power_on(self, device_name: Optional[str] = 'Litra Beam') -> None:
        self.tune_app.connect_tune_app(device_name=device_name)
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=device_name)
        time.sleep(1)
        self.power_on()

    def power_on(self):
        state = self.tune_app.get_power_on_state()
        Report.logInfo(f"Power On state is: {state}")

        time.sleep(0.5)
        if not state:
            self.tune_app.click_power_on_toggle()
            time.sleep(1)
            new_state = self.tune_app.get_power_on_state()
            Report.logInfo(f"Power On state is: {new_state}")

    def change_preset_to_random_one(self) -> None:
        self.tune_app.click_litra_label_name('Presets')
        random_preset = random.choice(list(litra_beam_presets.keys()))
        self.tune_app.click_litra_preset(preset_name=random_preset)
        self.tune_app.close_litra_presets()
        time.sleep(1)

    # ------ Test Cases ------
    @exception_handler
    def tc_connect_litra_beam(self, device_name: str, acroname_automatic: Optional[bool] = True) -> None:
        if acroname_automatic:
            connect_device(device_name=device_name)
        self.tune_app.open_tune_app(clean_logs=True)
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=device_name)
        if self.tune_app.verify_device_connected() and self.tune_app.verify_device_name_displayed(device_name):
            Report.logPass(f"{device_name} - Connected displayed")
        else:
            Report.logFail(f"{device_name} - Connected not displayed")

        if self.tune_app.verify_power_on_displayed():
            Report.logPass("Power On displayed")
        else:
            Report.logFail("Power On NOT displayed")

        if self.tune_app.verify_device_name_label_displayed():
            Report.logPass("Device Name displayed")
        else:
            Report.logFail("Device Name NOT displayed")

        if self.tune_app.verify_device_image():
            Report.logPass("Device Image displayed")
        else:
            Report.logFail("Device Image NOT displayed")

        if self.tune_app.verify_device_info_button():
            Report.logPass("Device Info button displayed")
        else:
            Report.logFail("Device Info button NOT displayed")

        if self.tune_app.verify_go_back_home_button():
            Report.logPass("Device Go back home button displayed")
        else:
            Report.logFail("Device Go back home button NOT displayed")

        enable_port_if_not_connected(device_name=device_name)

    @exception_handler
    def tc_power_on_off_litra_beam(self, device_name: str) -> None:
        """Method to check Power On button functions for Litra Beam

        @param device_name: device name
        @return: None
        """
        self.tune_app.connect_tune_app()
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=device_name)
        self.tune_app.verify_power_on_displayed()

        time.sleep(1)
        state = self.tune_app.get_power_on_state()
        Report.logInfo(f"Power On state is: {state}")

        self.tune_app.click_power_on_toggle()
        time.sleep(1)
        new_state = self.tune_app.get_power_on_state()
        Report.logInfo(f"Power On state is: {new_state}")

        if new_state != state:
            Report.logPass(f"Power On state changed correctly.", True)
        else:
            Report.logFail(f"Power On NOT state changed correctly.")

        if new_state:
            self.tune_app.verify_litra_temperature_title_displayed()
            self.tune_app.verify_litra_brightness_title_displayed()

        self.tune_app.click_power_on_toggle()
        time.sleep(1)
        new_state_2 = self.tune_app.get_power_on_state()
        Report.logInfo(f"Power On state is: {new_state_2}")

        if new_state_2 != new_state:
            Report.logPass(f"Power On state changed correctly.", True)
        else:
            Report.logFail(f"Power On NOT state changed correctly.")

        if new_state_2:
            self.tune_app.verify_litra_temperature_title_displayed()
            self.tune_app.verify_litra_brightness_title_displayed()

    @exception_handler
    def tc_litra_beam_factory_reset(self, device_name: str) -> None:
        """Method to check params state after Litra Beam factory reset

        @param device_name: device name
        @return:
        """
        self.open_tune_open_litra_and_power_on()
        self.change_preset_to_random_one()

        Report.logInfo(f'Factory reset')
        self.tune_app.click_info_button()

        self.tune_app.click_factory_reset()
        time.sleep(1)
        self.tune_app.click_proceed_to_factory_reset()
        time.sleep(5)
        self.tune_app.click_litra_beam_factory_reset_done_button()

        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=device_name)
        time.sleep(5)

        state_after_factory_reset = self.tune_app.get_power_on_state()
        Report.logInfo(f"Power On state is: {state_after_factory_reset}")
        if not state_after_factory_reset:
            Report.logPass(f"Power On state changed correctly after factory reset.", True)
        else:
            Report.logFail(f"Power On state changed NOT correctly after factory reset.")

        device_name_factory_reset = self.tune_app.get_device_name_from_settings_page()
        if device_name_factory_reset == "Litra Beam":
            Report.logPass(f"Device name displayed correctly on Settings page.", True)
        else:
            Report.logFail(f"Device name NOT displayed correctly on Settings page: {device_name_factory_reset}")

        if not self.tune_app.get_power_on_state():
            self.tune_app.click_power_on_toggle()
            time.sleep(1)
            new_state = self.tune_app.get_power_on_state()
            Report.logInfo(f"Power On state is: {new_state}")

        if self.tune_app.look_element_by_text(TunesAppLocators.LITRA_LABEL_PRESET_NAME, "Manual Adjustment"):
            Report.logPass(f"Device preset displayed correctly on Settings page.", True)
        else:
            presets_locator = self.tune_app.look_element_by_text(TunesAppLocators.LITRA_LABEL_NAME, 'Presets')
            current_preset_name = presets_locator.find_element(By.XPATH, '..//p[@data-testid="dashboard.device.settings.illuminationPreset.selected"]')
            Report.logFail(f"Device preset NOT displayed correctly on Settings page: {current_preset_name.text}")

    @exception_handler
    def tc_litra_presets_test(self, device_name: Optional[str] = 'Litra Beam') -> None:
        """Method to check whether Litra Beam presets have correct values.

        @param device_name: device name
        """
        fails = list()

        # Open Logi Tune app
        self.open_tune_open_litra_and_power_on(device_name=device_name)

        # Make factory reset to get default values of manual adjustment
        Report.logInfo(f'Factory reset')
        self.tune_app.click_info_button()
        self.tune_app.click_factory_reset()
        time.sleep(1)
        self.tune_app.click_proceed_to_factory_reset()
        time.sleep(5)
        self.tune_app.click_litra_beam_factory_reset_done_button()

        # Open device settings
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=device_name)
        time.sleep(1)

        # Turn on the light
        if not self.tune_app.get_power_on_state():
            self.tune_app.click_power_on_toggle()
            time.sleep(1)
            new_state = self.tune_app.get_power_on_state()
            Report.logInfo(f"Power On state is: {new_state}")

        # Check presets values
        for preset in litra_beam_presets.keys():
            self.tune_app.open_litra_presets()
            self.tune_app.click_litra_preset(preset_name=preset)
            self.tune_app.close_litra_presets()
            time.sleep(1)

            temperature = self.tune_app.get_current_litra_temperature()
            brightness = self.tune_app.get_current_litra_brightness()
            preset_name_from_tune = self.tune_app.get_current_litra_preset_name()
            
            if preset_name_from_tune == preset:
                Report.logPass(f'For {preset} name OK')
            else:
                fails.append(f'{preset} name: {preset_name_from_tune} instead of {preset}')
                Report.logFail(f'{preset} name: {preset_name_from_tune} instead of {preset}')

            if -temperature == litra_beam_presets[preset]['temperature']:
                Report.logPass(f'For {preset} temperature OK')
            else:
                fails.append(f'{preset} temperature: {-temperature} instead of {litra_beam_presets[preset]["temperature"]}')
                Report.logFail(f'For {preset} temperature NOK: {-temperature} instead of {litra_beam_presets[preset]["temperature"]}')

            if brightness == litra_beam_presets[preset]['brightness']:
                Report.logPass(f'For {preset} brightness OK')
            else:
                fails.append(f'{preset} brightness: {brightness} instead of {litra_beam_presets[preset]["brightness"]}')
                Report.logFail(f'For {preset} brightness NOK: {brightness} instead of {litra_beam_presets[preset]["brightness"]}')

        if len(fails):
            Report.logInfo('Not all the presets are set properly:', bold=True)
            [Report.logInfo(fail) for fail in fails]
        else:
            Report.logPass('All the presets are set properly.')

    @exception_handler
    def tc_litra_beam_responsiveness(self, device_name: Optional[str] = 'Litra Beam') -> None:
        fails = list()

        # Open Logi Tune app
        self.open_tune_open_litra_and_power_on(device_name=device_name)

        # Check power on state
        old_power_on_state = self.tune_app.get_power_on_state()
        self.tune_app.click_power_on_toggle()
        time.sleep(1)
        new_power_on_state = self.tune_app.get_power_on_state()

        if new_power_on_state != old_power_on_state:
            Report.logPass('Power on toggle changed state after click')
        else:
            fails.append('Power on toggle DID NOT change state after click')
            Report.logFail('Power on toggle DID NOT change state after click')

        if not new_power_on_state:
            self.tune_app.click_power_on_toggle()
            time.sleep(1)

        # Check device name window
        self.tune_app.click_litra_device_name('Device name')
        device_name_popup = self.tune_app.look_element(TunesAppLocators.LITRA_DEVICE_NAME_POPUP, skip_exception=True)

        if device_name_popup:
            Report.logPass('Device name popup appeard after click')
            self.tune_app.close_litra_device_name_change()
        else:
            fails.append('Device name popup NOT appeard after click')
            Report.logFail('Device name popup NOT appeard after click')

        # Check presets window
        self.tune_app.click_litra_label_name('Presets')
        presets_popup = self.tune_app.look_element(TunesAppLocators.LITRA_PRESETS_WINDOW, skip_exception=True)

        if presets_popup:
            Report.logPass('Presets popup appeard after click')
            self.tune_app.close_litra_presets()
        else:
            fails.append('Presets popup NOT appeard after click')
            Report.logFail('Presets popup NOT appeard after click')

        # Check temperature
        min_temperature = self.tune_app.get_litra_min_defined_temperature()
        max_temperature = self.tune_app.get_litra_max_defined_temperature()

        self.streaming_light.light_temperature.change_to_exact_value(max_temperature)
        curr_value = self.tune_app.get_current_litra_temperature()

        if curr_value != max_temperature:
            fails.append(f'Maximal ({max_temperature}) temperature value NOT achieved. Got {curr_value} instead.')
            Report.logFail(f'Maximal ({max_temperature}) temperature value NOT achieved. Got {curr_value} instead.')
        else:
            Report.logPass('Maximal temperature value achieved properly')

        self.streaming_light.light_temperature.change_to_exact_value(min_temperature)
        curr_value = self.tune_app.get_current_litra_temperature()

        if curr_value != min_temperature:
            fails.append(f'Minimal ({min_temperature}) temperature value NOT achieved. Got {curr_value} instead.')
            Report.logFail(f'Minimal ({min_temperature}) temperature value NOT achieved. Got {curr_value} instead.')
        else:
            Report.logPass('Minimal temperature value achieved properly')

        self.tune_app.look_element(TunesAppLocators.LITRA_TEMPERATURE_SLIDER).click()
        time.sleep(1)
        curr_value = self.tune_app.get_current_litra_temperature()
        if curr_value != min_temperature and curr_value != max_temperature:
            Report.logPass('Temperature slider clickable')
        else:
            fails.append('Temperature slider NOT clickable')
            Report.logFail('Temperature slider NOT clickable')

        # Check brightness
        min_brightness = self.tune_app.get_litra_min_defined_brightness()
        max_brightness = self.get_max_available_brightness(responsiveness_check=True)

        self.streaming_light.light_brightness.change_to_exact_value(max_brightness)
        curr_value = self.tune_app.get_current_litra_brightness()

        if curr_value != max_brightness:
            fails.append(f'Maximal ({max_brightness}) brightness value NOT achieved. Got {curr_value} instead.')
            Report.logFail(f'Maximal ({max_brightness}) brightness value NOT achieved. Got {curr_value} instead.')
        else:
            Report.logPass('Maximal brightness value achieved properly')

        self.streaming_light.light_brightness.change_to_exact_value(min_brightness)
        curr_value = self.tune_app.get_current_litra_brightness()

        if curr_value != min_brightness:
            fails.append(f'Minimal ({min_brightness}) brightness value NOT achieved. Got {curr_value} instead.')
            Report.logFail(f'Minimal ({min_brightness}) brightness value NOT achieved. Got {curr_value} instead.')
        else:
            Report.logPass('Minimal brightness value achieved properly')

        self.tune_app.look_element(TunesAppLocators.LITRA_BRIGHTNESS_SLIDER).click()
        time.sleep(1)
        curr_value = self.tune_app.get_current_litra_brightness()
        if curr_value != min_brightness and curr_value != max_brightness:
            Report.logPass('Brightness slider clickable')
        else:
            fails.append('Brightness slider NOT clickable')
            Report.logFail('Brightness slider NOT clickable')

        if len(fails):
            Report.logInfo(f'Not all the elements of GUI are responsive:', bold=True)
            [print(fail) for fail in fails]
        else:
            Report.logPass(f'All the elements of GUI are responsive.')

    @exception_handler
    def tc_change_preset_name_after_changing_slider(self, device_name: Optional[str] = 'Litra Beam') -> None:
        self.open_tune_open_litra_and_power_on(device_name=device_name)

        # Temperature
        while True:
            self.change_preset_to_random_one()
            if self.tune_app.get_current_litra_preset_name() != 'Manual Adjustment':
                break

        self.tune_app.click_litra_temperature_up()
        self.tune_app.click_litra_temperature_up()
        self.tune_app.click_litra_temperature_down()

        current_preset_name = self.tune_app.get_current_litra_preset_name()

        if current_preset_name == 'Manual Adjustment':
            Report.logPass('After changing temperature preset name changed back to Manual Adjustment properly')
        else:
            Report.logFail(
                f'After changing temperature preset name NOT changed back to Manual Adjustment properly. '
                f'Current preset name: {current_preset_name}.'
            )

        # Brightness
        while True:
            self.change_preset_to_random_one()
            if self.tune_app.get_current_litra_preset_name() != 'Manual Adjustment':
                break

        self.tune_app.click_litra_brightness_up()
        self.tune_app.click_litra_brightness_up()
        self.tune_app.click_litra_brightness_down()

        current_preset_name = self.tune_app.get_current_litra_preset_name()

        if current_preset_name == 'Manual Adjustment':
            Report.logPass('After changing brightness preset name changed back to Manual Adjustment properly')
        else:
            Report.logFail(
                f'After changing brightness preset name NOT changed back to Manual Adjustment properly. '
                f'Current preset name: {current_preset_name}.'
            )
        self.tune_app.click_back_button_to_my_devices()
