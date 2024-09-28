import time
from typing import Optional, List

from apps.tune.pages.base_page import TuneBasePage, WebDriver, WebElement
from locators.tune.light_page_locators import TuneLightPageLocators
from datetime import datetime, timedelta

import calendar


class TuneLightPage(TuneBasePage):
    def __init__(self, driver: Optional[WebDriver] = None):
        super().__init__(driver)
        self._window_name = 'Light Page'
        self._cameras_aliases = {
            'Brio': 'Logitech BRIO',
        }

    def click_back_button(self) -> None:
        self._click(TuneLightPageLocators.BACK_BUTTON)

    def click_about_the_device_button(self) -> None:
        self._click(TuneLightPageLocators.ABOUT_THE_DEVICE_BUTTON)

    def click_camera_for_preview(self, camera_name: str) -> None:
        self._click(TuneLightPageLocators.SHOW_CAMERA_LIST_BUTTON)
        cameras = self._get_all_available_elements(TuneLightPageLocators.CHOOSE_CAMERA_BUTTON)
        camera_name = self._cameras_aliases.get(camera_name, camera_name)
        for camera in cameras:
            if camera.text.lower() == camera_name.lower():
                camera.click()
                return

    def get_available_cameras(self) -> List[str]:
        self._click(TuneLightPageLocators.SHOW_CAMERA_LIST_BUTTON)
        cameras = self._get_all_available_elements(TuneLightPageLocators.CHOOSE_CAMERA_BUTTON)
        # Camo Studio shows up as available camera
        cameras_names = [camera.text for camera in cameras if camera.text != "Camo"]
        cameras[0].click()
        return cameras_names

    def click_power_on_switch(self) -> None:
        self._click(TuneLightPageLocators.POWER_ON_SWITCH)

    def verify_power_switch_state(self) -> bool:
        return self._is_checkbox_selected(TuneLightPageLocators.POWER_ON_CHECKBOX)

    def verify_smart_activation_chosen_state(self, current_state: str) -> bool:
        smart_activation_state = self._get_text(TuneLightPageLocators.SMART_ACTIVATION_BUTTON)
        return current_state == smart_activation_state

    def click_smart_activation_button(self) -> None:
        self._click(TuneLightPageLocators.SMART_ACTIVATION_BUTTON)

    def click_smart_activation_popup_close_button(self) -> None:
        self._click(TuneLightPageLocators.SMART_ACTIVATION_POPUP_CLOSE)

    def click_smart_activation_popup_save_button(self) -> None:
        self._click(TuneLightPageLocators.SMART_ACTIVATION_POPUP_SAVE)

    def click_smart_activation_popup_disabled_radio(self) -> None:
        self._click(TuneLightPageLocators.SMART_ACTIVATION_POPUP_DISABLED_RADIO)

    def click_smart_activation_popup_any_camera_radio(self) -> None:
        self._click(TuneLightPageLocators.SMART_ACTIVATION_POPUP_ANY_CAMERA_RADIO)

    def click_smart_activation_popup_available_cameras_checkbox_by_name(self, *cameras_names: str
                                                                        ) -> None:
        cameras = self._get_all_available_elements(
            TuneLightPageLocators.SMART_ACTIVATION_POPUP_UNIQUE_CAMERA_CHECKBOX)
        parsed_cam_names = [self._cameras_aliases.get(name, name).lower() for name in cameras_names]
        cameras_to_be_clicked = [camera.text for camera in cameras
                                 if camera.text.lower() in parsed_cam_names]
        for camera in cameras:
            if camera.get_attribute("data-testid") is None:
                continue
            camera_checkbox_state = camera.get_attribute("data-testid").split('.')[-1]
            if camera_checkbox_state == 'unchecked' and camera.text in cameras_to_be_clicked:
                camera.click()
            elif camera_checkbox_state == 'checked' and camera.text not in cameras_to_be_clicked:
                camera.click()
            time.sleep(0.5)

    def click_device_name_button(self) -> None:
        self._click(TuneLightPageLocators.DEVICE_NAME_BUTTON)

    def click_device_name_popup_close_button(self) -> None:
        self._click(TuneLightPageLocators.DEVICE_NAME_POPUP_CLOSE_BUTTON)

    def input_device_name(self, device_name: str) -> None:
        self._delete_input(TuneLightPageLocators.DEVICE_NAME_POPUP_NAME_INPUT)
        self._send_keys(TuneLightPageLocators.DEVICE_NAME_POPUP_NAME_INPUT, device_name)

    def click_device_name_popup_surprise_me_button(self) -> None:
        self._click(TuneLightPageLocators.DEVICE_NAME_POPUP_SURPRISE_ME_BUTTON)

    def click_device_name_popup_update_button(self) -> None:
        self._click(TuneLightPageLocators.DEVICE_NAME_POPUP_UPDATE_BUTTON)

    def click_presets_button(self) -> None:
        self._click(TuneLightPageLocators.PRESETS_BUTTON)

    def click_presets_popup_close_button(self) -> None:
        self._click(TuneLightPageLocators.PRESETS_POPUP_CLOSE_BUTTON)

    def get_all_presets_names(self) -> List[str]:
        presets = self._get_all_available_elements(TuneLightPageLocators.PRESETS_POPUP_OPTION_RADIO)
        return [preset.text for preset in presets]

    def click_presets_popup_preset_radio_by_name(self, preset_name: str) -> None:
        self._click_by_element_text(TuneLightPageLocators.PRESETS_POPUP_OPTION_RADIO, preset_name)

    def set_temperature_slider(self, value: int) -> None:
        self._change_slider_value(TuneLightPageLocators.TEMPERATURE_SLIDER,
                                  TuneLightPageLocators.SCROLL_AREA, value)

    def verify_temperature_slider_value(self) -> None:
        self._check_slider_value(TuneLightPageLocators.TEMPERATURE_SLIDER)

    def set_brightness_slider(self, value: int) -> None:
        self._change_slider_value(TuneLightPageLocators.BRIGHTNESS_SLIDER,
                                  TuneLightPageLocators.SCROLL_AREA, value)

    def verify_brightness_slider_value(self) -> None:
        self._check_slider_value(TuneLightPageLocators.BRIGHTNESS_SLIDER)
