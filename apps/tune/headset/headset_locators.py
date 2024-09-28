from locators.tunes_ui_locators import TunesAppLocators


class HeadsetWindows:
    anc_button_options = 'anc_button_options'
    button_functions = 'button_functions'
    equalizer = 'equalizer'
    headset_settings = 'headset_settings'
    health_and_safety = 'health_and_safety'
    on_head_detection = 'on_head_detection'


class HeadsetLocators:
    noise_cancellation_select = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.ANC_BUTTON_GROUP_DIV,
        'nc_buttons_locators': (
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ANC_HIGH,
                'button_locator': TunesAppLocators.ANC_HIGH
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ANC_LOW,
                'button_locator': TunesAppLocators.ANC_LOW
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ANC_DISABLED,
                'button_locator': TunesAppLocators.ANC_DISABLED
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ANC_AMBIENCE_TRANSPARENCY,
                'button_locator': TunesAppLocators.ANC_AMBIENCE_TRANSPARENCY
            },
        )
    }
    noise_cancellation_switch = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.NOISE_CANCELLATION_LABEL,
        'toggle_locator': TunesAppLocators.NOISE_CANCELLATION_TOGGLE,
        'checkbox_locator': TunesAppLocators.NOISE_CANCELLATION_CHECKBOX
    }
    sidetone = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.SIDETONE_LABEL,
        'save_locator': TunesAppLocators.SIDETONE_DONE,
        'value_locator': TunesAppLocators.SIDETONE_VALUE,
        'slider_locator': TunesAppLocators.SIDETONE_SLIDER,
        'scroll_area_locator': TunesAppLocators.VIDEO_WINDOW_SCROLL_AREA
    }
    mic_level = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.MIC_LEVEL_LABEL,
        'save_locator': TunesAppLocators.MIC_LEVEL_DONE,
        'value_locator': TunesAppLocators.MIC_LEVEL_VALUE,
        'slider_locator': TunesAppLocators.MIC_LEVEL_SLIDER,
        'scroll_area_locator': TunesAppLocators.VIDEO_WINDOW_SCROLL_AREA
    }
    advanced_call_clarity = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LABEL,
        'save_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_SAVE_DIALOG,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_OFF_LABEL,
                'radio_button_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_OFF_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_LOW_LABEL,
                'radio_button_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_LOW_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_HIGH_LABEL,
                'radio_button_locator': TunesAppLocators.ADVANCED_CALL_CLARITY_LEVEL_HIGH_RADIO
            }
        )
    }
    equalizer = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.EQUALIZER,
        'save_locator': TunesAppLocators.EQUALIZER_BACK,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_PRESET_DEFAULT_LABEL,
                'radio_button_locator': TunesAppLocators.EQ_PRESET_DEFAULT_RADIO
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_PRESET_VOLBOOST_LABEL,
                'radio_button_locator': TunesAppLocators.EQ_PRESET_VOLBOOST_RADIO
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_PRESET_PODCAST_LABEL,
                'radio_button_locator': TunesAppLocators.EQ_PRESET_PODCAST_RADIO
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_PRESET_BASSBOOST_LABEL,
                'radio_button_locator': TunesAppLocators.EQ_PRESET_BASSBOOST_RADIO
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_PRESET_CUSTOM_LABEL,
                'radio_button_locator': TunesAppLocators.EQ_PRESET_CUSTOM_LABEL
            }
        ),
        'sliders_locators': (
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_AXIS_TIPS_BASS,
                'slider_locator': TunesAppLocators.EQ_SLIDER_0,
                'scroll_area_locator': TunesAppLocators.EQ_SLIDERS_SCROLL_AREA,
                'inverted': True
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_AXIS_TIPS_BASS,
                'slider_locator': TunesAppLocators.EQ_SLIDER_1,
                'scroll_area_locator': TunesAppLocators.EQ_SLIDERS_SCROLL_AREA,
                'inverted': True
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_AXIS_TIPS_MIDS,
                'slider_locator': TunesAppLocators.EQ_SLIDER_2,
                'scroll_area_locator': TunesAppLocators.EQ_SLIDERS_SCROLL_AREA,
                'inverted': True
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_AXIS_TIPS_MIDS,
                'slider_locator': TunesAppLocators.EQ_SLIDER_3,
                'scroll_area_locator': TunesAppLocators.EQ_SLIDERS_SCROLL_AREA,
                'inverted': True
            },
            {
                'window_name': HeadsetWindows.equalizer,
                'name_locator': TunesAppLocators.EQ_AXIS_TIPS_TREBLE,
                'slider_locator': TunesAppLocators.EQ_SLIDER_4,
                'scroll_area_locator': TunesAppLocators.EQ_SLIDERS_SCROLL_AREA,
                'inverted': True
            }
        )
    }
    device_name = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.DEVICE_NAME_MAIN_LABEL,
        'value_locator': TunesAppLocators.DEVICE_NAME_RENAME,
        'save_locator': TunesAppLocators.DEVICE_NAME_UPDATE,
        'scroll_area_locator': TunesAppLocators.VIDEO_WINDOW_SCROLL_AREA
    }
    single_press = {
        'window_name': HeadsetWindows.button_functions,
        'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_SINGLE_PRESS_LABEL,
        'save_locator': TunesAppLocators.BUTTON_FUNCTIONS_SAVE_BUTTON,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_0_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_0_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_3_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_3_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_4_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_4_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_5_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_5_RADIO
            },
        )
    }
    double_press = {
        'window_name': HeadsetWindows.button_functions,
        'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_DOUBLE_PRESS_VALUE,
        'save_locator': TunesAppLocators.BUTTON_FUNCTIONS_SAVE_BUTTON,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_0_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_0_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_1_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_1_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_4_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_4_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_5_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_5_RADIO
            },
        )
    }
    long_press = {
        'window_name': HeadsetWindows.button_functions,
        'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_LONG_PRESS_VALUE,
        'save_locator': TunesAppLocators.BUTTON_FUNCTIONS_SAVE_BUTTON,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_4_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_4_RADIO
            },
            {
                'window_name': HeadsetWindows.button_functions,
                'name_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_5_LABEL,
                'radio_button_locator': TunesAppLocators.BUTTON_FUNCTIONS_RADIO_5_RADIO
            },
        )
    }
    sleep_settings = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.SLEEP_SETTINGS_LABEL,
        'save_locator': TunesAppLocators.SLEEP_TIMEOUT_SAVE,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_5_MIN_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_5_MIN_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_10_MIN_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_10_MIN_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_15_MIN_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_15_MIN_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_30_MIN_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_30_MIN_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_1_H_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_1_H_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_2_H_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_1_H_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_2_H_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_2_H_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.SLEEP_NEVER_LABEL,
                'radio_button_locator': TunesAppLocators.SLEEP_NEVER_RADIO
            },
        )
    }
    rotate_to_mute = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.ROTATE_TO_MUTE_LABEL,
        'toggle_locator': TunesAppLocators.ROTATE_TO_MUTE_TOGGLE,
        'checkbox_locator': TunesAppLocators.ROTATE_TO_MUTE_CHECKBOX
    }
    voice_prompts_switch = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.VOICE_PROMPTS_LABEL,
        'toggle_locator': TunesAppLocators.VOICE_PROMPTS_TOGGLE,
        'checkbox_locator': TunesAppLocators.VOICE_PROMPTS_CHECKBOX
    }
    voice_prompts_select = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.VOICE_PROMPTS_3_LEVEL_LABEL,
        'save_locator': TunesAppLocators.VOICE_PROMPTS_3_SAVE_DIALOG,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.VOICE_PROMPTS_3_VOICE_LABEL,
                'radio_button_locator': TunesAppLocators.VOICE_PROMPTS_3_VOICE_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.VOICE_PROMPTS_3_TONES_LABEL,
                'radio_button_locator': TunesAppLocators.VOICE_PROMPTS_3_TONES_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.VOICE_PROMPTS_3_OFF_LABEL,
                'radio_button_locator': TunesAppLocators.VOICE_PROMPTS_3_OFF_RADIO
            },
        )
    }
    anti_startle_protection = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.ANTI_STARTLE_PROTECTION_LABEL,
        'toggle_locator': TunesAppLocators.ANTI_STARTLE_PROTECTION_TOGGLE,
        'checkbox_locator': TunesAppLocators.ANTI_STARTLE_PROTECTION_CHECKBOX
    }
    dasboard_anti_startle_protection = {
        'window_name': HeadsetWindows.health_and_safety,
        'name_locator': TunesAppLocators.DASHBOARD_ANTI_STARTLE_PROTECTION_LABEL,
        'toggle_locator': TunesAppLocators.DASHBOARD_ANTI_STARTLE_PROTECTION_TOGGLE,
        'checkbox_locator': TunesAppLocators.DASHBOARD_ANTI_STARTLE_PROTECTION_CHECKBOX
    }
    noise_exposure_control = {
        'window_name': HeadsetWindows.health_and_safety,
        'name_locator': TunesAppLocators.NOISE_EXPOSURE_CONTROL_LABEL,
        'toggle_locator': TunesAppLocators.NOISE_EXPOSURE_CONTROL_TOGGLE,
        'checkbox_locator': TunesAppLocators.NOISE_EXPOSURE_CONTROL_CHECKBOX
    }
    transparency = {
        'window_name': HeadsetWindows.anc_button_options,
        'name_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_LABEL,
        'toggle_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_TOGGLE,
        'checkbox_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_TRANSPARENCY_CHECKBOX
    }
    none = {
        'window_name': HeadsetWindows.anc_button_options,
        'name_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_LABEL,
        'toggle_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_TOGGLE,
        'checkbox_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_NONE_CHECKBOX
    }
    noise_cancellation_low = {
        'window_name': HeadsetWindows.anc_button_options,
        'name_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_LABEL,
        'toggle_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_TOGGLE,
        'checkbox_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_LOW_CHECKBOX
    }
    noise_cancellation_high = {
        'window_name': HeadsetWindows.anc_button_options,
        'name_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_LABEL,
        'toggle_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_TOGGLE,
        'checkbox_locator': TunesAppLocators.ANC_BUTTON_OPTIONS_ANC_HIGH_CHECKBOX
    }
    auto_mute = {
        'window_name': HeadsetWindows.on_head_detection,
        'name_locator': TunesAppLocators.AUTO_MUTE_LABEL,
        'toggle_locator': TunesAppLocators.AUTO_MUTE_TOGGLE,
        'checkbox_locator': TunesAppLocators.AUTO_MUTE_CHECKBOX
    }
    auto_answer = {
        'window_name': HeadsetWindows.on_head_detection,
        'name_locator': TunesAppLocators.AUTO_ANSWER_LABEL,
        'toggle_locator': TunesAppLocators.AUTO_ANSWER_TOGGLE,
        'checkbox_locator': TunesAppLocators.AUTO_ANSWER_CHECKBOX
    }
    auto_pause = {
        'window_name': HeadsetWindows.on_head_detection,
        'name_locator': TunesAppLocators.AUTO_PAUSE_LABEL,
        'toggle_locator': TunesAppLocators.AUTO_PAUSE_TOGGLE,
        'checkbox_locator': TunesAppLocators.AUTO_PAUSE_CHECKBOX
    }
    touch_pad = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.TOUCH_PAD_TITLE,
        'toggle_locator': TunesAppLocators.TOUCH_PAD_TOGGLE,
        'checkbox_locator': TunesAppLocators.TOUCH_PAD_CHECKBOX
    }
    connection_priority = {
        'window_name': HeadsetWindows.headset_settings,
        'name_locator': TunesAppLocators.CONNECTION_PRIORITY_LABEL,
        'save_locator': TunesAppLocators.CONNECTION_PRIORITY_SAVE,
        'radio_buttons_locators': (
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.CONNECTION_PRIORITY_STABLE_CONNECTION,
                'radio_button_locator': TunesAppLocators.CONNECTION_PRIORITY_STABLE_CONNECTION_RADIO
            },
            {
                'window_name': HeadsetWindows.headset_settings,
                'name_locator': TunesAppLocators.CONNECTION_PRIORITY_SOUND_QUALITY,
                'radio_button_locator': TunesAppLocators.CONNECTION_PRIORITY_SOUND_QUALITY_RADIO
            }
        )
    }
