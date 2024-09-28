import time
from typing import Any, Optional

from apps.tune.devices_base_helpers import TuneDevicePersistency
from apps.tune.headset.headset import HeadsetsParametersWrapper, HeadsetProperties
from apps.tune.headset.headset_default_values import equalizers_presets
from apps.tune.helpers import exception_handler
from apps.tune.TuneElectron import TuneElectron
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import (
    CenturionCommands)
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import (
    Features)

EQUALIZER_MARGIN_OF_ERROR = 10


class TuneHeadsetPersistency(TuneDevicePersistency):
    def __init__(self, headset_name: str,
                 tune_app: Optional[TuneElectron] = None,
                 wired: Optional[bool] = False):
        super().__init__(headset_name, HeadsetsParametersWrapper, tune_app)
        self.headset: HeadsetProperties = self.device
        self.headset_methods = TuneHeadsetMethods(headset_name=headset_name, tune_app=self.tune_app)
        self.device_name_persistency_checker = None
        self.headset_name = headset_name
        self.headset_name_before_change = None
        self.wired = wired

    def _back_button_universal_click(self) -> None:
        if self.tune_app.verify_back_button_cybermorph():
            self.tune_app.click_back_button_cybermorph()
        elif self.tune_app.verify_back_to_device():
            self.tune_app.click_back_to_device()
        elif self.tune_app.verify_button_functions_back():
            self.tune_app.click_button_functions_back()

    @exception_handler
    def check_persistency(self, acroname_automatic: bool = True) -> None:
        self._set_random_adjustments()
        self._reconnect_device(acroname_automatic)
        self._get_adjustments()

    def _set_random_adjustments(self) -> None:
        self.tune_app.click_device(self.headset.name)
        self._get_expected_values_from_settings()

        if self.headset.anti_startle_protection or self.headset.noise_exposure_control:
            self.tune_app.click_health_and_safety_label()
            self._get_expected_values_from_health_and_safety()
            self._back_button_universal_click()

        if self.headset.transparency or self.headset.none or self.headset.noise_cancellation_low or self.headset.noise_cancellation_high:
            self.tune_app.click_anc_button_options()
            self._get_expected_values_from_anc_button_options()
            self._back_button_universal_click()

        if self.headset.auto_mute or self.headset.auto_answer or self.headset.auto_pause:
            self.tune_app.click_on_head_detection()
            self._get_expected_values_from_on_head_detection()
            self._back_button_universal_click()

        if self.headset.single_press or self.headset.double_press or self.headset.long_press:
            self.tune_app.click_button_functions_label()
            self._get_expected_values_from_button_functions()
            self._back_button_universal_click()

    def _get_adjustments(self) -> None:
        self.tune_app.click_device(self.headset.name)

        self._check_if_values_from_settings_persisted()

        if self.headset.anti_startle_protection or self.headset.noise_exposure_control:
            self.tune_app.click_health_and_safety_label()
            self._check_if_values_from_health_and_safety_persisted()
            self._back_button_universal_click()

        if self.headset.transparency or self.headset.none or self.headset.noise_cancellation_low or self.headset.noise_cancellation_high:
            self.tune_app.click_anc_button_options()
            self._check_if_values_from_anc_button_options()
            self._back_button_universal_click()

        if self.headset.auto_mute or self.headset.auto_answer or self.headset.auto_pause:
            self.tune_app.click_on_head_detection()
            self._check_if_values_from_on_head_detection_persisted()
            self._back_button_universal_click()

        if self.headset.single_press or self.headset.double_press or self.headset.long_press:
            self.tune_app.click_button_functions_label()
            self._check_if_values_from_buttons_functions_persisted()
            self._back_button_universal_click()

        self._persistency_results()

    def _get_expected_values_from_settings(self) -> None:
        time.sleep(5)
        # self.device_parameters.append(self._get_expected_value(self.headset.noise_cancellation))

        if self.headset.sidetone:
            self.tune_app.click_sidetone()
            self.device_parameters.append(self._get_expected_value(self.headset.sidetone))
            self.tune_app.click_sidetone_done()

        if self.headset.mic_level:
            self.tune_app.click_mic_level()
            self.device_parameters.append(self._get_expected_value(self.headset.mic_level))
            self.tune_app.click_mic_level_done()

        self.device_parameters.append(self._get_expected_value(self.headset.advanced_call_clarity))

        if get_custom_platform() == "windows" or not self.wired:
            self.device_parameters.append(self._get_expected_value(self.headset.equalizer))

        if self.headset.device_name:
            self.headset_name_before_change = self.tune_app.get_device_name_from_settings_page()
            self.device_name_persistency_checker = self._get_expected_value(self.headset.device_name)
            self.device_parameters.append(self.device_name_persistency_checker)

        self.device_parameters.append(self._get_expected_value(self.headset.sleep_settings))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.rotate_to_mute))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.touch_pad))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.voice_prompts_switch))
        self.device_parameters.append(self._get_expected_value(self.headset.voice_prompts_select))
        self.device_parameters.append(self._get_expected_value(self.headset.connection_priority))

    def _get_expected_values_from_health_and_safety(self) -> None:
        time.sleep(10)
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.anti_startle_protection))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.noise_exposure_control))

    def  _get_expected_values_from_anc_button_options(self) -> None:
        """
        The order of checking parameters is VERY important. Minimum two of the options must be enabled at the same time.
        This is why switchers ment to be turned on are invoked first.
        """
        time.sleep(10)
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.none))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.noise_cancellation_low))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.transparency))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.noise_cancellation_high))
        time.sleep(2)

    def _get_expected_values_from_on_head_detection(self) -> None:
        time.sleep(10)
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.auto_mute))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.auto_answer))
        self.device_parameters.append(self._set_and_get_switch_value(self.headset.auto_pause))
        time.sleep(2)

    def _get_expected_values_from_button_functions(self) -> None:
        time.sleep(10)
        self.device_parameters.append(self._get_expected_value(self.headset.single_press))
        self.device_parameters.append(self._get_expected_value(self.headset.double_press))
        self.device_parameters.append(self._get_expected_value(self.headset.long_press))
        time.sleep(2)

    def _check_if_values_from_settings_persisted(self) -> None:
        time.sleep(5)
        # self._compare_current_value_with_expected(self.headset.noise_cancellation, self.device_parameters)

        if self.headset.sidetone:
            self.tune_app.click_sidetone()
            self._compare_current_value_with_expected(self.headset.sidetone, self.device_parameters)
            self.tune_app.click_sidetone_done()

        if self.headset.mic_level:
            self.tune_app.click_mic_level()
            self._compare_current_value_with_expected(self.headset.mic_level, self.device_parameters,
                                                      margin_of_error=1)
            self.tune_app.click_mic_level_done()

        self._compare_current_value_with_expected(self.headset.advanced_call_clarity, self.device_parameters)

        if get_custom_platform() == "windows" or not self.wired:
            self._compare_current_value_with_expected(self.headset.equalizer, self.device_parameters,
                                                      margin_of_error=EQUALIZER_MARGIN_OF_ERROR)

        self._compare_current_value_with_expected(self.headset.device_name, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.sleep_settings, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.rotate_to_mute, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.touch_pad, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.voice_prompts_switch, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.voice_prompts_select, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.connection_priority, self.device_parameters)

    def _check_if_values_from_health_and_safety_persisted(self) -> None:
        time.sleep(5)
        self._compare_current_value_with_expected(self.headset.anti_startle_protection, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.noise_exposure_control, self.device_parameters)

    def _check_if_values_from_anc_button_options(self) -> None:
        time.sleep(10)
        self._compare_current_value_with_expected(self.headset.transparency, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.none, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.noise_cancellation_low, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.noise_cancellation_high, self.device_parameters)

    def _check_if_values_from_on_head_detection_persisted(self) -> None:
        time.sleep(10)
        self._compare_current_value_with_expected(self.headset.auto_mute, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.auto_answer, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.auto_pause, self.device_parameters)

    def _check_if_values_from_buttons_functions_persisted(self) -> None:
        time.sleep(10)
        self._compare_current_value_with_expected(self.headset.single_press, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.double_press, self.device_parameters)
        self._compare_current_value_with_expected(self.headset.long_press, self.device_parameters)


class TuneHeadsetMethods:
    def __init__(self, headset_name: str, tune_app: Optional[TuneElectron] = None):
        self.tune_app = tune_app if tune_app else TuneElectron()
        self.headset: HeadsetProperties = HeadsetsParametersWrapper(self.tune_app).get_by_name(headset_name)

    def _open_my_devices(self) -> None:
        self.tune_app.open_tune_app(clean_logs=True)
        self.tune_app.click_my_devices()
        self.tune_app.click_device(device_name=self.headset.name)

    def _verify_sidetone_level(self, conn_type: str, level: int) -> None:
        """ Method to verify sidetone level on device over centurion++

        @param conn_type: type of connection, i.e. BT, DONGLE
        @param level: sidetone level
        @return: None
        """
        self.centurion = CenturionCommands(device_name=self.headset.name,
                                           conn_type=conn_type)
        self.features = Features(self.centurion)
        response = self.features.headset_audio_feature.get_sidetone_level()
        self.features.headset_audio_feature.verify_get_sidetone_level(response,
                                                                      level)
        self.centurion.close_port()

    def _open_parameter(self, parameter: Any) -> None:
        Report.logInfo(f'Opening "{parameter.name}" popup')
        try:
            locator = parameter.value_locator if parameter.value_locator is not None \
                else parameter.name_locator
        except AttributeError:
            locator = parameter.name_locator
        self.tune_app.look_element(locator).click()

    def _save_parameter(self, parameter: Any) -> None:
        Report.logInfo(f'Saving "{parameter.name}"')
        self.tune_app.look_element(parameter.save_locator).click()

    def _add_custom_presets(self, first_eq_name: str = 'Custom First',
                            second_eq_name: str = 'Custom Second') -> None:
        first_eq_values = self.headset.equalizer.create_random_equalizer(first_eq_name)
        checked_name_first = self.headset.equalizer.check_selection()
        checked_val_first = self.headset.equalizer.check_current_preset_values()
        if checked_name_first != first_eq_name:
            Report.logException(f'Invalid checked name - '
                                f'expected: {first_eq_name}, observed: {checked_name_first}')
        elif first_eq_values != checked_val_first:
            Report.logException(f'Invalid equalizer values - '
                                f'expected: {first_eq_values}, observed: {checked_val_first}')
        else:
            Report.logPass(f'First custom equalizer added correctly with values: {first_eq_values}')

        second_eq_values = self.headset.equalizer.create_random_equalizer(second_eq_name)
        checked_name_second = self.headset.equalizer.check_selection()
        checked_val_sec = self.headset.equalizer.check_current_preset_values()
        
        if checked_name_second != second_eq_name:
            Report.logException(f'Invalid checked name - '
                                f'expected: {second_eq_name}, observed: {checked_name_second}')
        elif second_eq_values != checked_val_sec:
            Report.logException(f'Invalid equalizer values - '
                                f'expected: {second_eq_values}, observed: {checked_val_sec}')
        else:
            Report.logPass(
                f'Second custom equalizer added correctly with values: {second_eq_values}')

    def _delete_custom_presets(self, first_eq_name: str = 'Custom First',
                               second_eq_name: str = 'Custom Second') -> None:
        self.headset.equalizer.initialize_custom_radio_buttons()
        self.headset.equalizer.delete_custom_equalizer(first_eq_name)
        if not self.headset.equalizer.check_custom_equalizer_existence_by_name(first_eq_name):
            Report.logPass(
                f'Custom equalizer preset "{first_eq_name}" has been deleted successfully!')
        else:
            Report.logException(f'Unable to delete equalizer: "{first_eq_name}"')

        self.headset.equalizer.delete_custom_equalizer(second_eq_name)
        if not self.headset.equalizer.check_custom_equalizer_existence_by_name(second_eq_name):
            Report.logPass(
                f'Custom equalizer preset "{second_eq_name}" has been deleted successfully!')
        else:
            Report.logException(f'Unable to delete equalizer: "{second_eq_name}"')

    def tc_sidetone(self, conn_type: str) -> None:
        self._open_my_devices()
        if self.headset.name in ("Zone Wireless 2", "Zone 950"):
            time.sleep(10)
        self._open_parameter(self.headset.sidetone)
        value = self.headset.sidetone.check_value()
        Report.logInfo(f'Current sidetone value: {value}%')
        random_value = self.headset.sidetone.set_random_value(custom_step=10)
        Report.logInfo(f'New sidetone value: {random_value}%')
        if self.headset.name in ("Zone Wireless 2", "Zone 950"):
            time.sleep(5)
        self._save_parameter(self.headset.sidetone)
        time.sleep(3)
        self._open_parameter(self.headset.sidetone)
        new_value = self.headset.sidetone.check_value()
        self._save_parameter(self.headset.sidetone)
        assert new_value == random_value, (
            Report.logException(f'Sidetone value is different than set - '
                                f'Expected: {random_value}%, Observed: {new_value}%'))
        Report.logInfo(f'Sidetone value set correctly to {new_value}%')
        self._verify_sidetone_level(conn_type=conn_type, level=int(new_value / 10))

    def tc_mic_level(self) -> None:
        self._open_my_devices()
        if self.headset.name in ("Zone Wireless 2", "Zone 950"):
            time.sleep(10)
        self._open_parameter(self.headset.mic_level)
        value = self.headset.mic_level.check_value()
        Report.logInfo(f'Current mic level value: {value}%')
        random_value = self.headset.mic_level.set_random_value()
        Report.logInfo(f'New mic level value: {random_value}%')
        if self.headset.name in ("Zone Wireless 2", "Zone 950"):
            time.sleep(5)
        self._save_parameter(self.headset.mic_level)
        time.sleep(3)
        self._open_parameter(self.headset.mic_level)
        new_value = self.headset.mic_level.check_value()
        self._save_parameter(self.headset.mic_level)
        self.tune_app.verify_mic_level_value(str(new_value), self.headset.name)
        Report.logInfo(f'Mic level value set correctly to {new_value}%')

    def tc_equalizer_max_preset_name_length(self) -> None:
        name = 'Very long equalizer preset name for testing purposes'
        self._open_my_devices()
        self.headset.equalizer.wait_for_equalizer_to_load()
        self.headset.equalizer.set_random_sliders_values([], open_equalizer=True)
        Report.logInfo(f'Setting "{name}" as equalizer preset name.')
        self.headset.equalizer.input_equalizer_name(name, save_equalizer=True)
        time.sleep(3)
        cut_name = self.headset.equalizer.check_current_equalizer_preset_chosen()
        if len(cut_name) == 30:
            Report.logPass(f'Equalizer preset name "{cut_name}" has {len(cut_name)} characters')
        else:
            Report.logException(f'Equalizer preset name length is not equal to 30 -'
                                f' "{cut_name}" has {len(cut_name)} characters!')
        self.headset.equalizer.delete_custom_equalizer(cut_name)

    def tc_equalizer_add_and_delete_custom_presets(self) -> None:
        self._open_my_devices()
        self.headset.equalizer.wait_for_equalizer_to_load()
        self._add_custom_presets()
        self._delete_custom_presets()

    def tc_equalizer_check_max_custom_presets_prompt(self) -> None:
        self._open_my_devices()
        self.headset.equalizer.wait_for_equalizer_to_load()
        names = list()
        custom_existence = self.headset.equalizer.check_custom_equalizers_existence()
        for idx in range(2):
            if not all(custom_existence):
                name = f'Temporary{idx}'
                names.append(name)
                self.headset.equalizer.create_random_equalizer(name)
                custom_existence = self.headset.equalizer.check_custom_equalizers_existence()
            else:
                break
        self.headset.equalizer.create_random_equalizer('Temporary', verify_max_presets_prompt=True)
        if self.headset.equalizer.verify_max_presets_prompt():
            Report.logPass('Max presets prompt has been shown properly!')
        else:
            Report.logException('Max presets prompt not visible.')
        self._delete_custom_presets(*names)

    def tc_equalizer_check_default_presets_values(self) -> None:
        fail_flag = False
        self._open_my_devices()
        self.headset.equalizer.wait_for_equalizer_to_load()
        for preset in equalizers_presets:
            self.headset.equalizer.select_and_save(preset.name)
            time.sleep(3)
            preset_name_visible = self.headset.equalizer.check_current_equalizer_preset_chosen()
            if preset_name_visible == preset.name:
                Report.logInfo(f'Equalizer preset "{preset.name}" changed correctly!')
            else:
                fail_flag = True
                Report.logException(f'Wrong preset name shown in Tune. '
                                    f'Expected: {preset.name}, Observed: {preset_name_visible}')

            observed = self.headset.equalizer.check_current_preset_values()
            if observed == preset.default_values or (
                    preset.default_values_wired and observed == preset.default_values_wired):
                Report.logInfo(f'Equalizer preset "{preset.name}" has correct '
                               f'default values: {preset.default_values}')
            else:
                fail_flag = True
                Report.logException(f'Equalizer preset "{preset.name}" has wrong default values.'
                                    f' Expected: {preset.default_values}, Observed: {observed}')

        if not fail_flag:
            Report.logPass("Default presets' values are correct!")
