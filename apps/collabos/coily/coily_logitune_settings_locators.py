from locators.tunes_ui_locators import TuneCoilyLocators


class TuneCoilySettingCommon:
    window_name = "Logi Dock Flex"


class TuneCoilySettingsLocators(TuneCoilySettingCommon):

    brightness_slider = {
        "window_name": TuneCoilySettingCommon.window_name,
        "plus_locator": None,
        "minus_locator": None,
        "slider_locator": TuneCoilyLocators.BRIGHTNESS_SLIDER,
        "scroll_area_locator": TuneCoilyLocators.BRIGHTNESS_SLIDER_SCROLL_AREA,
        "name_locator": TuneCoilyLocators.BRIGHTNESS_SLIDER
    }
    away_message = {
        'window_name': TuneCoilySettingCommon.window_name,
        'name_locator': TuneCoilyLocators.AWAY_MESSAGE_MAIN_LABEL,
        'popup_window_locator': TuneCoilyLocators.AWAY_MESSAGE_RENAME,
        'input_area_locator': TuneCoilyLocators.AWAY_MESSAGE_POPUP_TEXT_INPUT,
        'submit_locator': TuneCoilyLocators.AWAY_MESSAGE_SUBMIT_BUTTON,
        'scroll_area_locator': TuneCoilyLocators.AWAY_MESSAGE_SCROLL_AREA,
        'close_without_submitting': TuneCoilyLocators.AWAY_MESSAGE_CLOSE_BUTTON,
        'notification_invalid': TuneCoilyLocators.INVALID_AWAY_MESSAGE
    }

    privacy_mode_switch = {
        'window_name': TuneCoilySettingCommon.window_name,
        'name_locator': TuneCoilyLocators.PRIVACY_MODE_TITLE,
        'toggle_locator': TuneCoilyLocators.PRIVACY_MODE_TOGGLE,
        'checkbox_locator': TuneCoilyLocators.PRIVACY_MODE_CHECKBOX,
    }

    time_format_switch = {
        'window_name': TuneCoilySettingCommon.window_name,
        'name_locator': TuneCoilyLocators.TIME_FORMAT_TITLE,
        'toggle_locator': TuneCoilyLocators.TIME_FORMAT_TOGGLE,
        'checkbox_locator': TuneCoilyLocators.TIME_FORMAT_CHECKBOX,
    }