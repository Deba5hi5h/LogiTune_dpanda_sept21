from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr

from locators.locators_templates import (xpath_by_data_testid, xpath_by_class,
                                         xpath_by_multiple_attributes_chained)


class TuneLightPageLocators:
    SCROLL_AREA = xpath_by_class(El.div, 'simplebar-content-wrapper')
    BACK_BUTTON = xpath_by_data_testid(El.any, 'dashboard.device.statusBar.backBtn')
    ABOUT_THE_DEVICE_BUTTON = xpath_by_data_testid(El.div, 'dashboard.device.statusBar.infoBtn')
    SHOW_CAMERA_LIST_BUTTON = xpath_by_data_testid(El.div, 'dashboard.device.streamingLight.showCameraListButton')
    CHOOSE_CAMERA_BUTTON = xpath_by_data_testid(El.p, 'dashboard.device.streamingLight.cameraPopup.label')
    POWER_ON_LABEL = xpath_by_data_testid(El.p, 'switchRow.title')
    POWER_ON_CHECKBOX = xpath_by_data_testid(El.input, 'switchRow.checkbox')
    POWER_ON_SWITCH = xpath_by_data_testid(El.any, 'checkbox.bg')
    SMART_ACTIVATION_LABEL = xpath_by_data_testid(El.any, 'dashboard.device.light.cameraSync.tooltip.title')
    SMART_ACTIVATION_BUTTON = xpath_by_data_testid(El.p, 'dashboard.device.light.cameraSync.openDialogButton')
    SMART_ACTIVATION_POPUP_CLOSE = xpath_by_data_testid(El.div, 'dialog.button.close')
    SMART_ACTIVATION_POPUP_SAVE = xpath_by_data_testid(El.button, 'dashboard.device.streamingLight.cameraSyncDialog.saveButton')
    SMART_ACTIVATION_POPUP_DISABLED_RADIO = xpath_by_data_testid(El.div, 'dashboard.device.streamingLight.cameraSyncDialog.buttonGroup.DISABLED')
    SMART_ACTIVATION_POPUP_ANY_CAMERA_RADIO = xpath_by_data_testid(El.div, 'dashboard.device.streamingLight.cameraSyncDialog.buttonGroup.ANY_CAMERA')
    SMART_ACTIVATION_POPUP_UNIQUE_CAMERA_CHECKBOX = xpath_by_data_testid(El.any, 'element.title', '..')
    DEVICE_NAME_LABEL = xpath_by_data_testid(El.p, 'dashboard.device.settings.rename.title')
    DEVICE_NAME_BUTTON = xpath_by_data_testid(El.p, 'dashboard.device.settings.rename.openDialogButton')
    DEVICE_NAME_POPUP_CLOSE_BUTTON = xpath_by_data_testid(El.div, 'header.button.close')
    DEVICE_NAME_POPUP_NAME_INPUT = xpath_by_data_testid(El.input, 'dashboard.device.settings.renameDialog.form.nameInput')
    DEVICE_NAME_POPUP_SURPRISE_ME_BUTTON = xpath_by_data_testid(El.div, 'dashboard.device.settings.renameDialog.form.surpriseMeButton')
    DEVICE_NAME_POPUP_UPDATE_BUTTON = xpath_by_data_testid(El.button, 'dashboard.device.settings.renameDialog.form.submitButton')
    PRESETS_LABEL = xpath_by_data_testid(El.p, 'dashboard.device.settings.illuminationPreset.title')
    PRESETS_BUTTON = xpath_by_data_testid(El.p, 'dashboard.device.settings.illuminationPreset.selected')
    PRESETS_POPUP_CLOSE_BUTTON = xpath_by_data_testid(El.div, 'dialog.button.close')
    PRESETS_POPUP_OPTION_RADIO = xpath_by_data_testid(El.div, 'settingsmenu.illuminationPreset.popup', strict_check=False)
    TEMPERATURE_LABEL = xpath_by_data_testid(El.any, 'dashboard.device.streamingLight.temperatureSlider.title')
    TEMPERATURE_SLIDER = xpath_by_multiple_attributes_chained((El.div, Attr.data_testid, 'dashboard.device.streamingLight.temperatureSlider'), (El.input, None, None))
    BRIGHTNESS_LABEL = xpath_by_data_testid(El.any, 'dashboard.device.streamingLight.brightness.title')
    BRIGHTNESS_SLIDER = xpath_by_multiple_attributes_chained((El.div, Attr.data_testid, 'dashboard.device.streamingLight.brightnessSlider'), (El.input, None, None))
