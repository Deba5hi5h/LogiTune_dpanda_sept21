from locators.tunes_ui_locators import TunesAppLocators


class CameraWindows:
    camera_settings = 'camera_settings'
    image_adjustments = 'image_adjustments'
    image_filters = 'image_filters'


class CameraLocators:
    pan_tilt = {
        'window_name': CameraWindows.camera_settings,
        'name_locator': TunesAppLocators.PAN_TILT_AREA,
        'pan_tilt_background_locator': {
            'window_name': CameraWindows.camera_settings,
            'element_locator': TunesAppLocators.PAN_TILT_BACKGROUND,
        },
        'pan_tilt_draggable_locator': {
            'window_name': CameraWindows.camera_settings,
            'element_locator': TunesAppLocators.PAN_TILT_DRAGGABLE,
        },
    }
    fov = {
        'window_name': CameraWindows.camera_settings,
        'name_locator': TunesAppLocators.FIELD_OF_VIEW,
        'fov_buttons_locators': (
            {
                'window_name': CameraWindows.camera_settings,
                'name_locator': TunesAppLocators.FIELD_OF_VIEW_65,
                'button_locator': TunesAppLocators.FIELD_OF_VIEW_65
            },
            {
                'window_name': CameraWindows.camera_settings,
                'name_locator': TunesAppLocators.FIELD_OF_VIEW_78,
                'button_locator': TunesAppLocators.FIELD_OF_VIEW_78
            },
            {
                'window_name': CameraWindows.camera_settings,
                'name_locator': TunesAppLocators.FIELD_OF_VIEW_90,
                'button_locator': TunesAppLocators.FIELD_OF_VIEW_90
            },
        )
    }
    zoom = {
        'window_name': CameraWindows.camera_settings,
        'name_locator': TunesAppLocators.ZOOM_LABEL,
        'slider_locator': TunesAppLocators.ZOOM_SLIDER,
        'scroll_area_locator': TunesAppLocators.VIDEO_WINDOW_SCROLL_AREA,
    }
    show_mode = {
        'window_name': CameraWindows.camera_settings,
        'name_locator': TunesAppLocators.SHOW_MODE_LABEL,
        'toggle_locator': TunesAppLocators.SHOW_MODE_TOGGLE,
        'checkbox_locator': TunesAppLocators.SHOW_MODE_CHECKBOX,
    }
    built_in_microphone = {
        'window_name': CameraWindows.camera_settings,
        'name_locator': TunesAppLocators.BUILT_IN_MICROPHONE_LABEL,
        'toggle_locator': TunesAppLocators.BUILT_IN_MICROPHONE_TOGGLE,
        'checkbox_locator': TunesAppLocators.BUILT_IN_MICROPHONE_CHECKBOX,
    }
    hdr = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_HDR_LABEL,
        'toggle_locator': TunesAppLocators.ADJUSTMENTS_HDR_TOGGLE,
        'checkbox_locator': TunesAppLocators.ADJUSTMENTS_HDR_CHECKBOX,
    }
    anti_flicker = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ANTI_FLICKER_LABEL,
        'save_locator': TunesAppLocators.ANTI_FLICKER_SAVE,
        'value_locator': TunesAppLocators.ANTI_FLICKER_VALUE,
        'radio_buttons_locators': (
            {
                'window_name': CameraWindows.image_adjustments,
                'name_locator': TunesAppLocators.ANTI_FLICKER_NTSC,
                'radio_button_locator': TunesAppLocators.NTSC_60HZ
            },
            {
                'window_name': CameraWindows.image_adjustments,
                'name_locator': TunesAppLocators.ANTI_FLICKER_PAL,
                'radio_button_locator': TunesAppLocators.PAL_50HZ
            },
        ),
    }
    auto_focus = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_FOCUS_LABEL,
        'toggle_locator': TunesAppLocators.ADJUSTMENTS_FOCUS_TOGGLE,
        'checkbox_locator': TunesAppLocators.ADJUSTMENTS_FOCUS_CHECKBOX,
    }
    manual_focus = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_FOCUS_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_FOCUS_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    auto_exposure = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_LABEL,
        'toggle_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_TOGGLE,
        'checkbox_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_CHECKBOX,
    }
    shutter_speed = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_SHUTTER_SPEED_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_SHUTTER_SPEED_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    iso = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_ISO_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_ISO_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    exposure_compensation = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_COMPENSATION_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_COMPENSATION_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    low_light_compensation = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_LOW_LIGHT_COMPENSATION_LABEL,
        'toggle_locator': TunesAppLocators.ADJUSTMENTS_LOW_LIGHT_COMPENSATION_TOGGLE,
        'checkbox_locator': TunesAppLocators.ADJUSTMENTS_LOW_LIGHT_COMPENSATION_CHECKBOX,
    }
    manual_exposure = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_EXPOSURE_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    gain = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_GAIN_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_GAIN_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    auto_white_balance = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_WHITE_BALANCE_LABEL,
        'toggle_locator': TunesAppLocators.ADJUSTMENTS_WHITE_BALANCE_TOGGLE,
        'checkbox_locator': TunesAppLocators.ADJUSTMENTS_WHITE_BALANCE_CHECKBOX,
    }
    temperature_compensation = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_TEMPERATURE_COMPENSATION_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_TEMPERATURE_COMPENSATION_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    temperature = {
    'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_TEMPERATURE_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_TEMPERATURE_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    tint = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_TINT_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_TINT_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    brightness = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_BRIGHTNESS_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_BRIGHTNESS_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    contrast = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_CONTRAST_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_CONTRAST_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    saturation = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_SATURATION_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_SATURATION_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    vibrance = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_VIBRANCE_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_VIBRANCE_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
    sharpness = {
        'window_name': CameraWindows.image_adjustments,
        'name_locator': TunesAppLocators.ADJUSTMENTS_SHARPNESS_LABEL,
        'slider_locator': TunesAppLocators.ADJUSTMENTS_SHARPNESS_SLIDER,
        'scroll_area_locator': TunesAppLocators.ADJUSTMENTS_WINDOW_SCROLL_AREA,
    }
