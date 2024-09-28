from locators.tunes_ui_locators import TunesAppLocators


class StreamingLightWindows:
    streaming_light_settings = 'streaming_light_settings'
    streaming_light_presets = 'streaming_light_presets'


class StreamingLightLocators:
    power_on = {
        'window_name': StreamingLightWindows.streaming_light_settings,
        'name_locator': TunesAppLocators.POWER_ON_TITLE,
        'toggle_locator': TunesAppLocators.POWER_ON_TITLE_TOGGLE,
        'checkbox_locator': TunesAppLocators.POWER_ON_TITLE_CHECKBOX,
    }
    light_temperature = {
        'window_name': StreamingLightWindows.streaming_light_settings,
        'name_locator': TunesAppLocators.LITRA_TEMPERATURE_TITLE,
        'slider_locator': TunesAppLocators.LITRA_TEMPERATURE_SLIDER,
        'scroll_area_locator': TunesAppLocators.LITRA_WINDOW_SCROLL_AREA,
    }
    light_brightness = {
        'window_name': StreamingLightWindows.streaming_light_settings,
        'name_locator': TunesAppLocators.LITRA_BRIGHTNESS_TITLE,
        'slider_locator': TunesAppLocators.LITRA_BRIGHTNESS_SLIDER,
        'scroll_area_locator': TunesAppLocators.LITRA_WINDOW_SCROLL_AREA,
    }
