import random
import string
import time
from typing import Any, Dict, Optional, Tuple, Union, Callable

import selenium.common.exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
from selenium.webdriver.common.keys import Keys

from apps.tune.TuneElectron import TuneElectron
from extentreport.report import Report
from locators.tunes_ui_locators import TunesAppLocators
from common.platform_helper import get_custom_platform


def is_element_initialized(func) -> Any:
    def wrapper(*args, **kwargs) -> Any:
        args[0].is_initialized()
        time.sleep(0.5)
        dont_switch = 'do_not_switch_to_dependent'
        switch = True
        if dont_switch in kwargs and kwargs.get(dont_switch) is True:
            switch = False
        if switch:
            args[0].switch_dependency_to_valid_one()
        return func(*args, **kwargs)
    return wrapper


class TuneBaseElement:
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 dependent_on_switch: Optional[tuple]):
        self.tune_app = tune_app
        self.window_name = window_name
        self.name_locator = name_locator
        self.dependent_on_switch = dependent_on_switch
        self.initialized = False
        self.name = None

    def __repr__(self):
        return (f"{self.__class__.__name__}(window_name='{self.window_name}', "
                f"name_locator='{self.name_locator}')")

    def is_initialized(self) -> None:
        """
            Method which checks whether Tune Element has been initialized and skipping it if so,
            otherwise running initializations methods
        Returns:
            None
        """
        if not self.initialized:
            switch_back = self.switch_dependency_to_valid_one()
            self.switch_dependency_to_valid_one()
            self._get_name()
            self._initialize_element()
            self.initialized = True
            if switch_back:
                self.switch_back_dependency()

    def switch_dependency_to_valid_one(self) -> Optional[bool]:
        if self.dependent_on_switch is not None:
            parameter, value = self.dependent_on_switch
            if parameter.check_value(silent_check=True) != value:
                parameter.toggle()
                return True
            else:
                return False

    def switch_back_dependency(self) -> None:
        if self.dependent_on_switch is not None:
            parameter, _ = self.dependent_on_switch
            parameter.toggle()

    def _initialize_element(self) -> None:
        """
            Method which should be overridden in child class.
            Used to properly initialize Tune element before usage
        Returns:
            None
        """
        pass

    def _find_element(self, element_locator: Tuple[str, str],
                      default_scroll_into_view: bool = False,
                      skip_exception: bool = False) -> Union[WebElement, EventFiringWebElement]:
        return self.tune_app.look_element(element_locator, scroll_flag=default_scroll_into_view,
                                          skip_exception=skip_exception)

    @is_element_initialized
    def is_visible(self) -> bool:
        return self.tune_app.verify_element(self.name_locator)

    def _get_name(self) -> None:
        self.name = self.tune_app.look_element(self.name_locator).text

    def set_random_value(self) -> Union[int, bool, str]:
        pass

    def check_value(self) -> Union[int, bool, str]:
        pass


class TunePanTilt(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 pan_tilt_background_locator: dict, pan_tilt_draggable_locator: dict,
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.pan_tilt_background = pan_tilt_background_locator
        self.pan_tilt_draggable = pan_tilt_draggable_locator

    def __repr__(self):
        return f"TunePanTilt(name='{self.name}')"

    @property
    def _background_element(self) -> WebElement:
        return self._find_element(self.pan_tilt_background['element_locator'])

    @property
    def _draggable_element(self) -> WebElement:
        return self._find_element(self.pan_tilt_draggable['element_locator'])

    def _move_draggable(self, dest_x: int, dest_y: int) -> None:
        (ActionChains(self.tune_app.driver).click_and_hold(self._draggable_element)
         .move_to_element_with_offset(self._background_element, dest_x, dest_y).release()).perform()

    def move_draggable_to_center(self) -> None:
        self._move_draggable(0, 0)

    def get_draggable_position(self) -> Tuple[int, int]:
        draggable_rect = self._draggable_element.rect
        background_rect = self._background_element.rect
        pos_x = draggable_rect.get('x') - background_rect.get('x') + draggable_rect.get('width') / 2
        pos_y = draggable_rect.get('y') - background_rect.get('y') + draggable_rect.get('height') / 2

        return int(pos_x), int(pos_y)

    def set_draggable_position_percent(self, percent_x: int, percent_y: int) -> None:
        draggable_rect = self._draggable_element.rect
        background_rect = self._background_element.rect

        x_offset = draggable_rect.get('width') / 2 - background_rect.get('width') / 2
        y_offset = draggable_rect.get('height') / 2 - background_rect.get('height') / 2

        target_x = x_offset + percent_x * (background_rect.get('width') - draggable_rect.get('width')) / 100
        target_y = y_offset + percent_y * (background_rect.get('height') - draggable_rect.get('height')) / 100

        self._move_draggable(int(target_x), int(target_y))
        time.sleep(2)

    def _initialize_element(self) -> None:
        self._set_pan_tilt_name_after_initialization()

    def _set_pan_tilt_name_after_initialization(self) -> None:
        self.name = 'Pan and Tilt'

    @is_element_initialized
    def set_random_pan_and_tilt(self) -> None:
        pass


class TuneFov(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 fov_buttons_locators: Tuple[dict], dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.fov_buttons_locators = fov_buttons_locators
        self.fov_buttons = dict()

    def __repr__(self):
        return f"TuneFov({self.window_name})"

    def _initialize_element(self) -> None:
        for fov_button_locator in self.fov_buttons_locators:
            fov_button = TuneButton(self.tune_app, **fov_button_locator)
            fov_button.is_initialized()
            self.fov_buttons[fov_button.name] = fov_button

    @is_element_initialized
    def set_fov(self, value: int) -> None:
        valid_fov_values = list(self.fov_buttons.keys())
        value = f'{value}°'
        if value in valid_fov_values:
            self.fov_buttons.get(value).click()
            Report.logInfo(f'FOV value set to {value}')
        else:
            Report.logInfo(f'Invalid FOV value: {value}. It must be one of these values:',
                           valid_fov_values)

    @is_element_initialized
    def set_random_fov(self) -> int:
        valid_fov_values = {int(fov_value.replace('°', ''))
                            for fov_value in self.fov_buttons.keys()}
        current_fov_value = self.check_fov()
        valid_fov_values.remove(current_fov_value)
        if 90 in valid_fov_values:
            valid_fov_values.remove(90)
        new_fov_value = random.choice(list(valid_fov_values))
        self.set_fov(new_fov_value)
        return new_fov_value

    @is_element_initialized
    def check_fov(self) -> int:
        selected_dark = ('rgba(159, 139, 255, 1)', 'rgba(129, 79, 251, 1)')
        selected_light = ('rgba(129, 78, 250, 1)', 'rgba(103, 62, 200, 1)')

        param_name_color = self._find_element(self.name_locator).value_of_css_property('color')
        dark_theme = True if 'rgba(244, 244, 244, 1)' in param_name_color else False
        selected_button_attribute_color = selected_dark if dark_theme else selected_light

        for fov_value, fov_button in self.fov_buttons.items():
            attributes = self._find_element(fov_button.button_locator
                                            ).value_of_css_property('background-color')
            if attributes in selected_button_attribute_color:
                Report.logInfo(f'Currently chosen FOV value is {fov_value}')
                return int(fov_value.replace('°', ''))

    def check_value(self) -> Union[int, bool, str]:
        return self.check_fov()

    def set_random_value(self) -> Union[int, bool, str]:
        return self.set_random_fov()


class TuneNoiseCancellation(TuneBaseElement):
    # TODO: Prepare class for noise cancelling persistency check or modify TuneFov class
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 nc_buttons_locators: Tuple[dict], dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.nc_buttons_locators = nc_buttons_locators
        self.nc_buttons = dict()

    def __repr__(self):
        return f"TuneNoiseCancellation(name='{self.name}')"

    def _initialize_element(self) -> None:
        pass

    def check_value(self) -> Union[int, bool, str]:
        pass

    def set_random_value(self) -> Union[int, bool, str]:
        pass


class TuneButton(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 button_locator: Tuple[str, str], button_name: Optional[str] = None,
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.button_locator = button_locator
        self.button_name = button_name

    def __repr__(self):
        return f"TuneButton(name='{self.name}')"

    @is_element_initialized
    def click(self) -> None:
        self._verify_name()
        self._find_element(self.button_locator).click()
        Report.logInfo(f'Clicked "{self.name}" button')

    def _verify_name(self) -> None:
        if not self.name:
            self.name = self.button_name

    @property
    @is_element_initialized
    def is_clickable(self) -> bool:
        return self._find_element(self.button_locator).is_enabled()


class TuneSwitcher(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 toggle_locator: Tuple[str, str], checkbox_locator: Tuple[str, str],
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.toggle_locator = toggle_locator
        self.checkbox_locator = checkbox_locator

    def __repr__(self):
        return f"TuneSwitcher(name='{self.name}')"

    @is_element_initialized
    def toggle(self) -> bool:
        Report.logInfo(f'Toggling "{self.name}" switch')
        switch_value = self.check_value(silent_check=True)
        self._find_element(self.toggle_locator, default_scroll_into_view=True).click()
        return not switch_value

    @is_element_initialized
    def switch_on(self) -> None:
        Report.logInfo(f'Switching ON "{self.name}"')
        if not self.check_value(silent_check=True):
            self._find_element(self.toggle_locator, default_scroll_into_view=True).click()

    @is_element_initialized
    def switch_off(self) -> None:
        Report.logInfo(f'Switching OFF "{self.name}"')
        if self.check_value(silent_check=True):
            self._find_element(self.toggle_locator, default_scroll_into_view=True).click()

    @is_element_initialized
    def check_value(self, silent_check: bool = False) -> Optional[bool]:
        try:
            checkbox = self._find_element(self.checkbox_locator, skip_exception=True)
            if not silent_check:
                Report.logInfo(
                    f'"{self.name}" switch is {"" if checkbox.is_selected() else "NOT "}selected')
            return checkbox.is_selected()
        except AttributeError:
            msg = f'[{self}.check_value()] - Unable to find element {self.checkbox_locator}'
            raise selenium.common.exceptions.TimeoutException(msg)


class TuneRadioButton(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 radio_button_locator: Tuple[str, str],
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.radio_button_locator = radio_button_locator
        self.is_initialized()

    def __repr__(self):
        return f"TuneRadioButton(name='{self.name}')"

    @is_element_initialized
    def click(self) -> None:
        self._find_element(self.radio_button_locator).click()

    @is_element_initialized
    def check_value(self) -> bool:
        return self._find_element(self.radio_button_locator).is_selected()


class TuneElementsSelection(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 save_locator: Tuple[str, str], radio_buttons_locators: Tuple[dict],
                 value_locator: Optional[Tuple[str, str]] = None,
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.save_locator = save_locator
        self.value_locator = value_locator
        self.radio_buttons_locators = radio_buttons_locators
        self.radio_buttons = dict()

    def __repr__(self):
        return f"TuneElementsSelection(name='{self.name}')"

    def _open(self) -> None:
        Report.logInfo(f'Opening "{self.name}" selection menu')
        locator = self.value_locator if self.value_locator is not None else self.name_locator
        self._find_element(locator).click()

    def _save(self) -> None:
        Report.logInfo(f'Saving "{self.name}" selection')
        self._find_element(self.save_locator).click()

    def _verify_radio_buttons(self, silent_check=False) -> None:
        for radio_button_locator in self.radio_buttons_locators:
            radio_button = TuneRadioButton(self.tune_app, **radio_button_locator)
            if radio_button.initialized:
                self.radio_buttons[radio_button.name] = radio_button
        if not silent_check:
            Report.logInfo(f'In "{self.name}" selection menu these options are available: '
                           f'{list(self.radio_buttons.keys())}')

    @is_element_initialized
    def check_selection(self) -> str:
        selected = None
        self._open()
        time.sleep(1)
        if not self.radio_buttons:
            self._verify_radio_buttons()
        for radio_button in self.radio_buttons.values():
            if radio_button.check_value():
                selected = radio_button.name
                Report.logInfo(f'Radio button "{radio_button.name}" is selected in '
                               f'"{self.name}" selection window')
        self._save()
        return selected

    @is_element_initialized
    def select_random(self) -> str:
        self._open()
        if not self.radio_buttons:
            self._verify_radio_buttons(silent_check=True)
        new_selection = random.choice(list(self.radio_buttons.values()))
        new_selection.click()
        self._save()
        return new_selection.name

    @is_element_initialized
    def select_and_save(self, selector_name: str) -> None:
        self._open()
        if not self.radio_buttons:
            self._verify_radio_buttons(silent_check=True)
        if selector_name in self.radio_buttons:
            self.radio_buttons.get(selector_name).click()
            time.sleep(1)
        self._save()

    def check_value(self) -> Union[int, bool, str]:
        return self.check_selection()

    def set_random_value(self) -> Union[int, bool, str]:
        return self.select_random()


class TuneEqualizer(TuneElementsSelection):
    MAX_CUSTOM_EQ_NUMBER = 2

    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 save_locator: Tuple[str, str], radio_buttons_locators: Tuple[dict],
                 sliders_locators: Tuple[dict], dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, save_locator,
                         radio_buttons_locators, dependent_on_switch)
        self.sliders_locators = sliders_locators
        self.sliders: Optional[Dict[str, TuneSlider]] = dict()
        self.custom_presets = list()
        self.sliders_initialized = False
        self.name_locator_first = TunesAppLocators.EQ_PRESET_CUSTOM_USER_1_LABEL
        self.name_locator_second = TunesAppLocators.EQ_PRESET_CUSTOM_USER_2_LABEL

    def __repr__(self):
        return f"TuneEqualizer(name='{self.name}')"

    def _initialize_sliders(self) -> None:
        if not self.sliders_initialized:
            for idx, slider_locator in enumerate(self.sliders_locators):
                self.sliders[f'slider_{idx}'] = TuneSlider(self.tune_app, **slider_locator)
            self.sliders_initialized = True

    def _get_slider_value(self, slider_id: int) -> Optional[int]:
        return self.sliders[f'slider_{slider_id}'].check_value()

    @is_element_initialized
    def create_random_equalizer(self, equalizer_preset_name: Optional[str] = None,
                                verify_max_presets_prompt: bool = False) -> Optional[tuple]:
        self._open()
        eq_values = list()
        self.set_random_sliders_values(eq_values)
        if equalizer_preset_name:
            if not verify_max_presets_prompt:
                self.input_equalizer_name(equalizer_preset_name)
                self.custom_presets.append(equalizer_preset_name)
                self._initialize_custom_radio_button(len(self.custom_presets))
                Report.logInfo(f'Equalizer "{equalizer_preset_name}" has been saved.')
            else:
                self.tune_app.look_element(TunesAppLocators.EQUALIZER_ADD_CUSTOM_PRESET).click()
                Report.logInfo(f'Checking max presets prompt.')
                return
        else:
            Report.logInfo('"Custom" equalizer has been changed.')
        self._save()

        return tuple(eq_values)

    def wait_for_equalizer_to_load(self) -> None:
        self._open()
        self.tune_app.wait_and_check_the_presence_of_element(
            TunesAppLocators.EQ_PRESET_CUSTOM_LABEL)
        time.sleep(3)
        self._save()

    def set_random_sliders_values(self, equalizer_values: list, open_equalizer: bool = False,
                                  save_equalizer: bool = False) -> None:
        if open_equalizer:
            self._open()
        self._initialize_sliders()
        for slider in self.sliders.values():
            slider.set_random_value(min_value=0, max_value=100)
            equalizer_values.append(slider.check_value())
        if save_equalizer:
            self._save()

    def input_equalizer_name(self, equalizer_preset_name: str, open_equalizer: bool = False,
                             save_equalizer: bool = False) -> None:
        if open_equalizer:
            self._open()
        self.tune_app.look_element(TunesAppLocators.EQUALIZER_ADD_CUSTOM_PRESET).click()
        self.tune_app.look_element(
            TunesAppLocators.EQUALIZER_ADD_CUSTOM_PRESET_NAME).send_keys(equalizer_preset_name)
        self.tune_app.look_element(TunesAppLocators.EQUALIZER_ADD_CUSTOM_PRESET_SAVE).click()
        if save_equalizer:
            self._save()

    def verify_max_presets_prompt(self) -> bool:
        if self.tune_app.verify_element(TunesAppLocators.EQUALIZER_MAX_PRESET_PROMPT):
            button_locator = TunesAppLocators.EQUALIZER_MAX_PRESET_PROMPT_OK_BUTTON
            Report.logInfo('Max presets prompt shown properly!')
            self.tune_app.look_element(button_locator).click()
            self._save()
            return True
        Report.logFail('Max presets prompt not visible!')
        return False

    @is_element_initialized
    def delete_custom_equalizer(self, equalizer_preset_name: str) -> None:
        self._open()
        self.tune_app.look_element(TunesAppLocators.EQUALIZER_EDIT).click()
        for idx in range(2):
            name_locator = getattr(TunesAppLocators,
                                   f'EQ_PRESET_CUSTOM_USER_{idx + 1}_DELETE_LABEL')
            if equalizer_preset_name == self.tune_app.look_element(name_locator).text.strip():
                button_locator = getattr(TunesAppLocators,
                                         f'EQ_PRESET_CUSTOM_USER_{idx + 1}_DELETE_BUTTON')
                self.tune_app.look_element(button_locator).click()
                self.tune_app.look_element(TunesAppLocators.EQUALIZER_EDIT_DONE).click()
                try:
                    self.custom_presets.pop(self.custom_presets.index(equalizer_preset_name))
                except ValueError:
                    pass
                Report.logInfo(f'Equalizer "{equalizer_preset_name}" has been deleted.')
                self._save()
                return

    def check_custom_equalizers_existence(self) -> Tuple[bool, bool]:
        self._open()
        found_first_element = self.tune_app.verify_element(self.name_locator_first, timeunit=5)
        found_second_element = self.tune_app.verify_element(self.name_locator_second, timeunit=5)
        self._save()
        return found_first_element, found_second_element
    
    def check_custom_equalizer_existence_by_name(self, equalizer_preset_name: str) -> bool:
        found_first_element, found_second_element = self.check_custom_equalizers_existence()
        self._open()
        if found_first_element:
            if self.tune_app.look_element(self.name_locator_first).text == equalizer_preset_name:
                self._save()
                return True
        if found_second_element:
            if self.tune_app.look_element(self.name_locator_second).text == equalizer_preset_name:
                self._save()
                return True
        self._save()
        return False

    def initialize_custom_radio_buttons(self) -> None:
        self._open()
        for idx in range(2):
            try:
                self._initialize_custom_radio_button(idx+1)
            except selenium.common.exceptions.TimeoutException:
                pass
        self._save()

    def check_current_equalizer_preset_chosen(self) -> str:
        return self.tune_app.look_element(TunesAppLocators.EQUALIZER_BOX_PROFILE_NAME).text

    def _initialize_custom_radio_button(self, custom_radio_button_index: int) -> None:
        name_locator = getattr(TunesAppLocators,
                               f'EQ_PRESET_CUSTOM_USER_{custom_radio_button_index}_LABEL')
        radio_button_locator = getattr(TunesAppLocators,
                                       f'EQ_PRESET_CUSTOM_USER_{custom_radio_button_index}_RADIO')
        custom_radio_button = TuneRadioButton(self.tune_app, 'equalizer', name_locator,
                                              radio_button_locator)
        if not self.radio_buttons:
            self._verify_radio_buttons()
        if custom_radio_button.initialized:
            self.radio_buttons[custom_radio_button.name] = custom_radio_button

    @is_element_initialized
    def check_current_preset_values(self) -> Tuple[Optional[int], ...]:
        self._open()
        self._initialize_sliders()

        eq_values = list()
        for slider in self.sliders.values():
            eq_values.append(slider.check_value())
        self._save()

        return tuple(eq_values)

    def set_random_value(self) -> Union[int, bool, str, tuple]:
        return self.create_random_equalizer()

    def check_value(self) -> Union[int, bool, str, tuple]:
        return self.check_current_preset_values()


class TuneSlider(TuneBaseElement):
    def __init__(self, tune_app: TuneElectron, window_name: str, name_locator: Tuple[str, str],
                 slider_locator: Tuple[str, str], scroll_area_locator: Tuple[str, str],
                 plus_locator: Optional[Tuple[str, str]] = None,
                 minus_locator: Optional[Tuple[str, str]] = None,
                 save_locator: Optional[Tuple[str, str]] = None,
                 value_locator: Optional[Tuple[str, str]] = None,
                 dependent_on_switch: Optional[tuple] = None, inverted: bool = False):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.slider_locator = slider_locator
        self.scroll_area_locator = scroll_area_locator
        self.plus_locator = plus_locator
        self.minus_locator = minus_locator
        self.save_locator = save_locator
        self.value_locator = value_locator
        self.inverted = inverted
        self.min_border = None
        self.max_border = None
        self.step = None

    def __repr__(self):
        return f"TuneSlider(name='{self.name}')"

    def _initialize_element(self) -> None:
        self._scroll_to_slider_element()
        self._get_borders()
        if self.plus_locator and self.minus_locator:
            self._get_step()

    @is_element_initialized
    def change_value(self, value: int) -> None:
        Report.logInfo(f'Changing "{self.name}" slider value to {value}')
        self._scroll_to_slider_element()
        self._click_on_slider_for_given_value(value)
        if self.step:
            self._tune_slider_value(value)

    @is_element_initialized
    def change_to_exact_value(self, value: int) -> int:
        Report.logInfo(f'Changing "{self.name}" slider value to {value}')
        self._click_on_slider_for_given_value(value)
        slider: WebElement = self._find_element(self.slider_locator)
        while True:
            current_value = int(slider.get_attribute('value'))
            if current_value == value:
                return current_value
            elif current_value < value:
                slider.send_keys(Keys.ARROW_RIGHT)
            else:
                slider.send_keys(Keys.ARROW_LEFT)

    @is_element_initialized
    def change_value_randomly(self, min_custom_value: Optional[int] = None,
                              max_custom_value: Optional[int] = None, minimal_change: int = 1,
                              custom_step: Optional[int] = None) -> int:
        min_value = min_custom_value if min_custom_value is not None else self.min_border
        max_value = max_custom_value if max_custom_value is not None else self.max_border

        if custom_step:
            step = custom_step
        else:
            step = self.step if self.step else 1
        current_value = self.check_value(silent_check=True)
        random_value = current_value
        while abs(random_value - current_value) < minimal_change:
            random_value = random.randrange(min_value, max_value, step)
        self.change_value(random_value)
        return random_value

    @is_element_initialized
    def check_value(self, silent_check: bool = False) -> Optional[int]:
        try:
            value = int(self._find_element(self.slider_locator, skip_exception=True
                                           ).get_attribute('value'))
            if not silent_check:
                Report.logInfo(f'Value of the "{self.name}" slider is {value}')
            return value
        except AttributeError:
            msg = f'[{self}.check_value()] - Unable to find element {self.slider_locator}'
            raise selenium.common.exceptions.TimeoutException(msg)

    @is_element_initialized
    def is_slider_visible(self, do_not_switch_to_dependent: bool = False) -> bool:
        if do_not_switch_to_dependent:
            Report.logInfo('Not switching dependent element to provided value')
        return self.tune_app.verify_element(self.slider_locator)

    def _get_borders(self) -> None:
        try:
            self.min_border = int(self._find_element(self.slider_locator).get_attribute('min'))
            self.max_border = int(self._find_element(self.slider_locator).get_attribute('max'))
            Report.logInfo(f'Found slider range: {self.min_border}-{self.max_border}')
        except ValueError:
            Report.logInfo('Min/max values of slider not found. Assuming values in range 0-100')
            self.min_border = 0
            self.max_border = 100

    def _get_step(self) -> None:
        start_value = int(self._find_element(self.slider_locator).get_attribute('value'))
        middle_value = round((self.max_border - self.min_border) / 2) + self.min_border
        locator_to_click = self.plus_locator if start_value < middle_value else self.minus_locator
        locator_to_click_back = self.plus_locator if locator_to_click == self.minus_locator \
            else self.minus_locator
        self._find_element(locator_to_click).click()
        time.sleep(1)
        new_value = int(self._find_element(self.slider_locator).get_attribute('value'))
        self.step = abs(new_value - start_value)
        self._find_element(locator_to_click_back).click()

    def _scroll_to_slider_element(self) -> None:
        slider = self._find_element(self.slider_locator)
        self.tune_app.scroll_into_view(slider, self.scroll_area_locator)

    def _click_on_slider_for_given_value(self, value: int) -> None:
        """
            Method used to change slider value by clicking on it at the calculated position.

            For inverted slider (rotated 270 degrees - used in headset equalizer settings),
            some tunings were needed to make this method to work.

            Returns:
                None
        """
        slider = self._find_element(self.slider_locator)
        slider_parent = slider.find_element('xpath', './../..')
        slider_rect = slider_parent.rect if not self.inverted else slider.rect
        a = slider_rect['width'] / (self.max_border - self.min_border)
        b = -(a * self.min_border)
        x = round(a * value + b)
        y_mid = round(slider_rect['height'] / 2)
        if self.inverted:
            parent_element = slider.find_element('xpath', value="./..")
            slider_base_scale = int(slider.rect['width']*0.9)
            slider = parent_element
            slider_rect = slider.rect
            loc_x, loc_y = slider.location['x'], slider.location['y']
            center_x, center_y = loc_x + slider_rect['width']/2, loc_y + slider_rect['height']/2
            y_max = center_y-slider_base_scale//2
            y_min = center_y+slider_base_scale//2
            y_dest = y_max + int(value / 100 * abs(y_max - y_min))
            value_to_set = value / 100 * abs(y_max - y_min)
            offset_from_middle = slider_rect['height'] // 2
            click_y = value_to_set - offset_from_middle
            ActionChains(self.tune_app.driver).move_to_element_with_offset(
                slider.wrapped_element, 0, click_y).click().perform()
            # self._draw_dot(center_x, y_dest)  # Uncomment only for debugging purposes

        else:
            (ActionChains(self.tune_app.driver).
             move_to_element_with_offset(slider_parent, x - slider_rect.get('width')/2, 0).click().perform())

    def _draw_dot(self, x: int, y: int) -> None:
        # helper function for debugging clicking on Tune DOM
        # Execute JavaScript code to create a dot at the specified (x, y) coordinate
        self.tune_app.driver.execute_script(f'''
            var dot = document.createElement('div');
            dot.style.width = '10px';
            dot.style.height = '10px';
            dot.style.borderRadius = '50%';
            dot.style.background = 'red';
            dot.style.position = 'absolute';
            dot.style.left = '{x-5}px';
            dot.style.top = '{y-5}px';
            document.body.appendChild(dot);
        ''')

    def _tune_slider_value(self, value: int) -> None:
        self._scroll_to_slider_element()
        time.sleep(0.5)
        slider_value = int(self._find_element(self.slider_locator).get_attribute('value'))
        delta = value - slider_value
        steps = round(abs(delta) / self.step)
        adjust_locator = self.minus_locator if delta < 0 else self.plus_locator
        for _ in range(steps):
            self._find_element(adjust_locator).click()
            time.sleep(0.1)

    def set_random_value(self,
                         min_value: Optional[int] = None, max_value: Optional[int] = None,
                         minimal_change: int = 1, custom_step: Optional[int] = None
                         ) -> Union[int, bool, str]:
        return self.change_value_randomly(min_value, max_value, minimal_change, custom_step)


class TuneDeviceName(TuneBaseElement):
    def __init__(self,
                 tune_app: TuneElectron,
                 window_name: str,
                 name_locator: Tuple[str, str],
                 value_locator: Tuple[str, str],
                 save_locator: Tuple[str, str],
                 scroll_area_locator: Tuple[str, str],
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.value_locator = value_locator
        self.save_locator = save_locator
        self.scroll_area_locator = scroll_area_locator

    def __repr__(self):
        return f"TuneDeviceName(name='{self.name}')"

    def _initialize_element(self) -> None:
        self._scroll_to_slider_element()

    def _scroll_to_slider_element(self) -> None:
        slider = self._find_element(self.name_locator)
        self.tune_app.scroll_into_view(slider, self.scroll_area_locator)

    @is_element_initialized
    def set_random_value(self) -> str:
        self.tune_app.click_device_name_rename()
        time.sleep(1)

        current_name = self.check_value(silent_check=True)
        chars = string.ascii_uppercase + string.digits
        new_name_with_suffix = f"{current_name} {''.join(random.choice(chars) for _ in range(40))}"

        self.tune_app.clear_device_name()
        self.tune_app.set_new_device_name(new_name_with_suffix)

        actual_new_name = self.check_value(silent_check=True)

        Report.logInfo(f'{current_name}\'s new name is {actual_new_name}')

        return actual_new_name

    @is_element_initialized
    def check_value(self, silent_check: bool = False) -> Optional[str]:
        try:
            displayed_name = self._find_element(self.value_locator, skip_exception=True).text
            if not silent_check:
                Report.logInfo(f'Displayed device name is {displayed_name}')
            return displayed_name
        except AttributeError:
            msg = f'[{self}.check_value()] - Unable to find element {self.value_locator}'
            raise selenium.common.exceptions.TimeoutException(msg)


class TuneInput(TuneBaseElement):
    def __init__(self,
                 tune_app: TuneElectron,
                 window_name: str,
                 name_locator: Tuple[str, str],
                 popup_window_locator: Tuple[str, str],
                 input_area_locator: Tuple[str, str],
                 submit_locator: Tuple[str, str],
                 scroll_area_locator: Tuple[str, str],
                 close_without_submitting: Tuple[str, str],
                 notification_invalid: Optional[Tuple[str, str]] = None,
                 dependent_on_switch: Optional[tuple] = None):
        super().__init__(tune_app, window_name, name_locator, dependent_on_switch)
        self.input_area_locator = input_area_locator
        self.submit_locator = submit_locator
        self.scroll_area_locator = scroll_area_locator
        self.popup_window_locator = popup_window_locator
        self.close_without_submit = close_without_submitting
        self.invalid_away_message = notification_invalid

    def __repr__(self):
        return f"TuneInput(name='{self.name}')"

    def _initialize_element(self) -> None:
        self._scroll_to_slider_element()

    def _scroll_to_slider_element(self) -> None:
        slider = self._find_element(self.name_locator)
        self.tune_app.scroll_into_view(slider, self.scroll_area_locator)

    def get_input_element(self):
        return self.tune_app.look_element(self.input_area_locator)

    def open_input_window(self):
        self.tune_app.look_element(self.popup_window_locator).click()

    @is_element_initialized
    def set_value(self, value):
        time.sleep(1)
        input_element = self.get_input_element()
        input_element.clear()
        if value:
            input_element.send_keys(value)

    @is_element_initialized
    def submit_value(self):
        submit = self.tune_app.look_element(self.submit_locator)
        submit.click()

    def clear_input_manually(self) -> None:

        el = self.get_input_element()
        el.click()

        if get_custom_platform() == "windows":
            el.send_keys(Keys.CONTROL + "a")
        else:
            el.send_keys(Keys.COMMAND + "a")

        el.send_keys(Keys.DELETE)

    @is_element_initialized
    def check_if_submit_clickable(self):
        submit = self.tune_app.look_element(self.submit_locator)
        return submit.is_enabled()

    @is_element_initialized
    def close_without_submitting(self):
        submit = self.tune_app.look_element(self.close_without_submit)
        submit.click()

    @is_element_initialized
    def check_invalid_away_message_popup(self):
        Report.logInfo("Checking if invalid message popup is present "
                       "when no text in away message input", is_collabos=True)
        popup = self.tune_app.verify_element(self.invalid_away_message)
        return popup

    @is_element_initialized
    def get_value(self):
        self.open_input_window()
        time.sleep(1)
        input_element = self.get_input_element()
        value = input_element.get_attribute('value')
        self.close_without_submitting()
        return value

    @is_element_initialized
    def set_random_value(self, value_len: int):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        random_msg = ''.join([random.choice(chars) for _ in range(value_len)])
        self.open_input_window()
        self.set_value(random_msg)
        self.submit_value()

        return random_msg


TuneElements = Union[TuneFov, TunePanTilt, TuneElementsSelection, TuneSlider, TuneSwitcher,
                     TuneDeviceName, TuneEqualizer, TuneInput]
TuneElementsClass = [TuneFov, TunePanTilt, TuneElementsSelection, TuneSlider, TuneSwitcher,
                     TuneDeviceName, TuneEqualizer, TuneInput]
