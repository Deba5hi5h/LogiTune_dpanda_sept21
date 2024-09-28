from selenium.webdriver.common.by import By

from common.framework_params import PROJECT, COILY_BASECAMP_NAME


class TunesAppLocators(object):
    """
    A class containing the Tunes App element locators.
    """

    #Home
    HOME = (By.XPATH, "//button[@data-testid='dashboard.tab-home']")
    MY_DEVICES = (By.XPATH, "//button[@data-testid='dashboard.tab-myDevices']")
    TAB = (By.XPATH, "//button") #Use element by text and pass text
    DEVICE = (By.XPATH, "//div//p[contains(text(), 'XXX')]")
    DEVICE_VER1 = (By.XPATH, "//div//p[text()='XXX']")  # Pass Device Name
    BACK_TO_DEVICE_SETTINGS = (By.XPATH, "//*[@data-testid='screen.button.back']")
    BACK_TO_MY_DEVICES = (By.XPATH, "//*[@data-testid='dashboard.device.statusBar.backBtn']")
    CLOSE_SCREEN = (By.XPATH, "//*[@data-testid='screen.button.close']")
    BACK_CYBERMORPH = (By.XPATH, '//*[@class="icon icon-back"]')
    NO_DEVICE_CONNECTED = (By.XPATH, "//p[@data-testid='dashboard.devices.supported.openDialog.noDeviceConnected']")
    SUPPORTED_DEVICES_LINK = (By.XPATH, "//button[@data-testid='dashboard.devices.supported.openDialogButton']")
    SUPPORTED_DEVICES_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.devices.list.openSupportDialog']")
    HEADSETS_HEADER = (By.XPATH, "//p[@data-testid='dialog.supportedDevices.devices.common.sections.headsets.title']")
    WEBCAMS_HEADER = (By.XPATH, "//p[@data-testid='dialog.supportedDevices.devices.common.sections.webcams.title']")
    DOCKS_HEADER = (By.XPATH, "//p[@data-testid='dialog.supportedDevices.devices.common.sections.docks.title']")
    MICE_HEADER = (By.XPATH, "//p[@data-testid='dialog.supportedDevices.devices.common.sections.mouses.title']")
    KEYBOARDS_HEADER = (By.XPATH, "//p[@data-testid='dialog.supportedDevices.devices.common.sections.keyboards.title']")
    STREAMING_LIGHT_HEADER = (By.XPATH, "//p[@data-testid='dialog.supportedDevices.devices.common.sections.streamingLights.title']")
    SUPPORTED_DEVICE = (By.XPATH, "//p[contains(text(), 'XXX')]")
    SUPPORTED_DEVICE_VER1 = (By.XPATH, "//p[text()='XXX']") # Pass Device Name

    SUPPORTED_DEVCES_OK_BUTTON = (By.XPATH, "//*[@data-testid='dialog.supportedDevices.button.ok']")
    DEVICE_CONNECTED = (By.XPATH, "//*[@data-testid='dashboard.device.statusBar.statusLabel']")
    SETTINGS_BUTTON = (By.XPATH, "//*[@data-testid='header.settings.button']")
    ABOUT_MENU = (By.CSS_SELECTOR, "#bottom-menu > li:nth-child(4) > div")
    ABOUT_TUNE_MENU = (By.XPATH, "//*[@data-testid='header.menu.item.about']")
    QUIT_MENU = (By.XPATH, "//*[@data-testid='header.menu.item.quit']")
    ABOUT_CONNECTED = (By.XPATH, "//*[@data-testid='aboutapp.button.connected']")
    APP_SETTINGS = (By.XPATH, "//*[@data-testid='header.menu.item.close']")
    CALENDAR_CONNECTION = (By.XPATH, "//p[text()='Calendar connection']")  # deprecated?
    CALENDAR_AND_MEETINGS = (By.XPATH, "//*[@data-testid='appSettings.settingsMain.calendarAndMeetings']")
    DISABLE_CALENDAR = (By.XPATH, "//button[@data-testid='appSettings.calendarAgendaEnabledBody.button.DisableCalendar']")
    DISABLE_AND_RELAUNCH_APP = (By.XPATH, "//button[@data-testid='appSettings.popUps.CalendarAgendaDisabledPopUps.button.disableAndRelaunch']")
    ENABLE_AND_RELAUNCH_APP = (By.XPATH, "//button[@data-testid='appSettings.calendarAgendaDisabledBody.button']")
    CALENDAR_IS_NOT_CONNECT = (By.XPATH, "//p[text()='Calendar is not connected']")  # deprecated?
    WORK_ACCOUNT = (By.XPATH, "//div[@data-testid='appSettings.settingsMain.workAccount']")
    DISCONNECT_BUTTON = (By.XPATH, "//button[@data-testid='profile.workAccount.disconnect']")
    DISCONNECT_ACCOUNT_BUTTON = (By.XPATH, "//button[@data-testid='appSettings.connectedAccount.disconnectDialog.disconnect']")
    NO_MEETING_SOON = (By.XPATH, "//p[contains(.,'No meetings soon')]")  # deprecated?
    SUPPORT = (By.CSS_SELECTOR, "#bottom-menu > li:nth-child(3) > div")
    SHARE_FEEDBACK = (By.CSS_SELECTOR, "#bottom-menu > li:nth-child(2) > div")
    HOME_DEVICE_NAME = (By.XPATH, "//p[@data-testid='dashboard.devices.device.deviceName']")
    HOME_DEVICE_GROUP_MAIN_NAME = (By.XPATH, "//p[@data-testid='dashboard.devices.deviceGroup.nameTypography']")
    STATUSBAR_BATTERY = (By.XPATH, "//div[@data-testid='dashboard.device.statusBar.battery']")
    BATTERY_LEVEL_FOR_DEVICE = (By.XPATH, "//*[@data-testid='dashboard.device.statusBar.battery']//p")
    DEVICE_IS_CHARGING = (By.XPATH, "//*[@id='batteryChargingIcon']")
    DEVICE_IMAGE = (By.XPATH, "//img[@data-testid='dashboard.device.statusBar.image']")
    GO_BACK_HOME = (By.XPATH, "//*[@data-testid='dashboard.device.statusBar.backBtn']")

    # Logi Dock Headset Pairing
    LOGI_DOCK_PAIR_HEADSET = (By.XPATH, "//p[@data-testid='dashboard.devices.device.pairingHeadset.pairingButton.pair']")
    LOGI_DOCK_CONTINUE_BTN = (By.XPATH, "//button[@data-testid='qbertPairUnpair.qbertPairingFlow.pairing.button.continue']")
    LOGI_DOCK_DONE_BTN = (By.XPATH, "//button[@data-testid='qbertPairUnpair.qbertPairingFlow.pairingSuccessful.button.done']")
    LOGI_DOCK_UNPAIR_HEADSET = (By.XPATH, "//p[@data-testid='dashboard.devices.device.pairingHeadset.pairingButton.unpair']")
    LOGI_DOCK_UNPAIR_BTN = (By.XPATH, "//button[@data-testid='qbertPairUnpair.qbertUnpairDialog.button.unpair']")

    # Agenda
    CONNECT_NOW = (By.XPATH, "//button[@data-testid='dashboard.agenda.placeholder.connectButton']")
    GOOGLE = (By.XPATH, "//div[@data-testid='connectCalendar.calendarCard-google']")
    MEETING_TITLE = (By.XPATH, "//div[@title='XXX']")  # Pass Meeting title
    CALENDAR_MEETING_TITLE = (By.XPATH, '//p[@data-testid[contains(., "title") and contains(., "meetingCard")]]')
    OUTLOOK = (By.XPATH, "//div[@data-testid='connectCalendar.calendarCard-outlook']")
    REFRESH_CALENDAR = (By.XPATH, "//button[@data-testid='dashboard.agenda.refreshButton']")
    REFRESHING_FINISHED_SIGN = (By.XPATH, "//button[@data-testid='dashboard.agenda.refreshButton']/*[name()='svg'][@xmlns]")
    ATTENDEES_NUMBER = (By.XPATH, "//button[@data-testid='dashboard.agenda.infoTag.wrapper']")
    MEETING_COPY_LINK_URL = (By.XPATH, "//div[@data-testid='meetingDetail.link.copy']")
    CALENDAR_OPEN_DETAILS = (By.XPATH, "//div[@data-testid='meetingDetail.link.goToExternal']")
    CALENDAR_ATTENDEE_LABEL = (By.XPATH, "//p[@data-testid[contains(., 'meetingDetail.attendeeItem') and contains(., 'name')]]")
    MEETING_DETAIL_BUTTON_BACK = (By.XPATH, "//*[@data-testid='meetingDetail.button.back']")
    MEETING_DETAIL_MEETING_TITLE = (By.XPATH, "//p[@data-testid='meetingDetail.meetingTitle']")

    # Work account
    SIGN_IN = (By.XPATH, "//button[@data-testid='dashboard.home.signInWorkAccount']")
    GOOGLE_WORK_ACCOUNT = (By.XPATH, "//button[@data-testid='workAccountOnboarding.provider.google']")
    OUTLOOK_WORK_ACCOUNT = (By.XPATH, "//button[@data-testid='workAccountOnboarding.provider.outlook']")
    # PRIVACY_ENABLE_BOX = (By.XPATH, '//*[@id="root"]/div/div[2]/div/div[3]/div/button')
    PRIVACY_ENABLE_BOX = (By.XPATH, "//p[text()='I agree that I have read and accept the ']")
    CONTINUE_DESK_BOOKING = (By.XPATH, "//button[@data-testid='workAccountOnboarding.welcome.continue']")
    BASECAMP_SEARCH = (By.XPATH, "//input[@data-testid='basecampSelection.search']")
    BASECAMP_NAME = (By.XPATH, f"//p[contains(@data-testid, '{COILY_BASECAMP_NAME}')]")
    CONTINUE_TEAMMATES = (By.XPATH, "//button[@data-testid='workAccountOnboarding.teammates.continue']")
    DONE_ADD_TEAMMATES = (By.XPATH, "//button[@data-testid='workAccountOnboarding.addTeammates.done']")


    #Video Section
    VIDEO_WINDOW_SCROLL_AREA = (By.XPATH, "//div[@class='simplebar-content-wrapper']")
    IMAGE_ADJUSTMENTS_BACK_BUTTON = (By.XPATH, "//*[@data-testid='colorAdjustments.backBtn']")
    ZOOM_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.video.zoomSlider']//*[@data-testid='dashboard.device.video.zoomSlider.title']")
    ZOOM_SLIDER = (By.XPATH, "//div[@data-testid='dashboard.device.video.zoomSlider']//input")
    IMAGE_ADJUSTMENT_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.video.imgAdjustmentsBtn']//*[@data-testid='sliderRow.title']")
   # FIELD_OF_VIEW = (By.XPATH, "//div[@data-testid='dashboard.device.video.fovToggle']//p[@data-testid='groupRow.title']")
    FIELD_OF_VIEW = (By.XPATH, "//span[contains(text(), 'FoV')]")
    FIELD_OF_VIEW_90 = (By.XPATH, "//button[@data-testid='groupRow.button.90']")
    FIELD_OF_VIEW_78 = (By.XPATH, "//button[@data-testid='groupRow.button.78']")
    FIELD_OF_VIEW_65 = (By.XPATH, "//button[@data-testid='groupRow.button.65']")
    VIDEO_STREAM_GRID = (By.XPATH, "//div[@data-testid='dashboard.device.video.preview.cameraGrid.showButton']")
    VIDEO_STREAM = (By.XPATH, "//div[@data-testid='dashboard.device.video.preview']")
    PAN_TILT_AREA = (By.XPATH, "//div[@data-testid='camera-pan-tilt']")
    PAN_TILT_BACKGROUND = (By.XPATH, "//div[@data-testid='camera-pan-tilt']")
    PAN_TILT_DRAGGABLE = (By.XPATH, "//div[@data-testid='draggable-pan-tilt']")

    SETTINGS_MENU = (By.XPATH, "//div[@data-testid='header.settings.button']")
    SHOW_MODE_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.video.docControl']//*[@data-testid='dashboard.device.video.showMode.toolTip.title']")
    SHOW_MODE_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.video.docControl']//input[@data-testid='switchRow.checkbox']")
    SHOW_MODE_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.video.docControl']//span[@data-testid='checkbox.thumb']")

    BUILT_IN_MICROPHONE_LABEL = (By.XPATH, "//*[@data-testid='dashboard.device.video.builtinMicrophone.toggleCheckbox.tooltip.title']")
    BUILT_IN_MICROPHONE_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.video.micControlBtn']//input[@data-testid='switchRow.checkbox']")
    BUILT_IN_MICROPHONE_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.video.micControlBtn']//span[@data-testid='checkbox.thumb']")
    BUILT_IN_MIC_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.video.micControlBtn']//input[@data-testid='switchRow.checkbox']")

    LED_IN_USE = (By.XPATH, "//div[@data-testid='dashboard.device.video.ledControl']//span[@data-testid='switchRow.title']")
    MIC_REBOOT_TITLE = (By.XPATH, "//p[@data-testid='app.micEnabledDialog.title']")
    MIC_REBOOT_MESSAGE = (By.XPATH, "//p[@data-testid='app.micEnabledDialog.message']")
    REBOOT_DEACTIVATE_MIC = (By.XPATH, "//button[@data-testid='app.micEnabledDialog.button.reboot']")
    REBOOT_ACTIVATE_MIC = (By.XPATH, "//button[@data-testid='app.micEnabledDialog.button.reboot']")
    MIC_REBOOT = (By.XPATH, "//button[@data-testid='app.micEnabledDialog.button.reboot']")
    MIC_REBOOT_CANCEL = (By.XPATH, "//button[@data-testid='app.micEnabledDialog.button.cancel']")
    ANTI_FLICKER_NTSC = (By.XPATH, "//div[@data-testid='dashboard.device.videoSettings.antiFlickerPopup-60']//div[@data-testid='radioButton.label']")
    ANTI_FLICKER_PAL = (By.XPATH, "//div[@data-testid='dashboard.device.videoSettings.antiFlickerPopup-50']//div[@data-testid='radioButton.label']")

    #Image adjustments
    COLOR_FILTERS_TAB = (By.XPATH, "//button[@data-testid='tabs.tab.1']")
    COLOR_ADJUSTMENTS_TAB = (By.XPATH, "//button[@data-testid='tabs.tab.0']")
    ADJUSTMENTS_WINDOW_SCROLL_AREA = (By.XPATH, "//div[@data-testid='tab.0']//div[@class='simplebar-content-wrapper']")
    COLOR_FILTER_TITLE = (By.XPATH, "//div[@data-testid='colorAdjustments.filters.XXX.wrapper']//p[@data-testid='previewRow.title']")
    COLOR_FILTER_RADIO = (By.XPATH, "//div[@data-testid='colorAdjustments.filters.XXX.wrapper']//input[@data-testid='radioButton.element']")

    ADJUSTMENTS_FOCUS_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoFocus']//*[@data-testid='switchRow.title']")
    ADJUSTMENTS_FOCUS_CHECKBOX = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoFocus']//input[@data-testid='switchRow.checkbox']")
    ADJUSTMENTS_FOCUS_TOGGLE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoFocus']//span[@data-testid='checkbox.thumb']")
    ADJUSTMENTS_FOCUS_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.manualFocus']//input")
    ADJUSTMENTS_FOCUS_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.manualFocus']//span[@data-testid='sliderRow.subTitle']")

    ANTI_FLICKER_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.value.antiFlicker']//*[@data-testid='colorAdjustments.adjustments.value.antiFlicker.toolTip.title']")
    ANTI_FLICKER_CURRENT_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.value.antiFlicker']//p[@data-testid='valueRow.value']")
    ANTI_FLICKER_SAVE = (By.XPATH, "//button[@data-testid='dashboard.device.videoSettings.antiFlickerPopup.saveBtn']")
    ANTI_FLICKER_VALUE = (By.XPATH, "//p[@data-testid='colorAdjustments.adjustments.value.antiFlicker.value']")
    PAL_50HZ = (By.XPATH, "//div[@data-testid='dashboard.device.videoSettings.antiFlickerPopup-50']//input[@data-testid='radioButton.element']")
    NTSC_60HZ = (By.XPATH, "//div[@data-testid='dashboard.device.videoSettings.antiFlickerPopup-60']//input[@data-testid='radioButton.element']")

    ADJUSTMENTS_EXPOSURE_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoExposure']//*[@data-testid='colorAdjustments.adjustments.switcher.autoExposure.toolTip.title']")
    ADJUSTMENTS_EXPOSURE_CHECKBOX = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoExposure']//input[@data-testid='switchRow.checkbox']")
    ADJUSTMENTS_EXPOSURE_TOGGLE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoExposure']//span[@data-testid='checkbox.thumb']")
    ADJUSTMENTS_EXPOSURE_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposure']//input")
    ADJUSTMENTS_EXPOSURE_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposure']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_GAIN_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.gain']//span[@data-testid='colorAdjustments.adjustments.slider.gain.title']")
    ADJUSTMENTS_GAIN_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.gain']//input")
    ADJUSTMENTS_GAIN_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.gain']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_EXPOSURE_COMPENSATION_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposureCompensation']//*[@data-testid='colorAdjustments.adjustments.slider.exposureCompensation.title']")
    ADJUSTMENTS_EXPOSURE_COMPENSATION_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposureCompensation']//input")
    ADJUSTMENTS_EXPOSURE_COMPENSATION_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposureCompensation']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_SHUTTER_SPEED_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposureShutterSpeed']//*[@data-testid='colorAdjustments.adjustments.slider.exposureShutterSpeed.title']")
    ADJUSTMENTS_SHUTTER_SPEED_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposureShutterSpeed']//input")
    ADJUSTMENTS_SHUTTER_SPEED_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.exposureShutterSpeed']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_ISO_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.gain']//*[@data-testid='colorAdjustments.adjustments.slider.gain.title']")
    ADJUSTMENTS_ISO_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.gain']//input")
    ADJUSTMENTS_ISO_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.gain']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_LOW_LIGHT_COMPENSATION_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.lowLightCompensation']//*[@data-testid='colorAdjustments.adjustments.switcher.lowLightCompensation.tooltip.title']")
    ADJUSTMENTS_LOW_LIGHT_COMPENSATION_CHECKBOX = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.lowLightCompensation']//input[@data-testid='switchRow.checkbox']")
    ADJUSTMENTS_LOW_LIGHT_COMPENSATION_TOGGLE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.lowLightCompensation']//span[@data-testid='checkbox.thumb']")

    ADJUSTMENTS_WHITE_BALANCE_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoWhiteBalance']//*[@data-testid='switchRow.title']")
    ADJUSTMENTS_WHITE_BALANCE_CHECKBOX = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoWhiteBalance']//input[@data-testid='switchRow.checkbox']")
    ADJUSTMENTS_WHITE_BALANCE_TOGGLE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.autoWhiteBalance']//span[@data-testid='checkbox.thumb']")

    ADJUSTMENTS_TEMPERATURE_COMPENSATION_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.whiteBalanceOffset']//*[@data-testid='colorAdjustments.adjustments.slider.whiteBalanceOffset.title']")
    ADJUSTMENTS_TEMPERATURE_COMPENSATION_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.whiteBalanceOffset']//input")
    ADJUSTMENTS_TEMPERATURE_COMPENSATION_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.whiteBalanceOffset']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_TEMPERATURE_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.whiteBalance']//*[@data-testid='colorAdjustments.adjustments.slider.whiteBalance.title']")
    ADJUSTMENTS_TEMPERATURE_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.whiteBalance']//input")
    ADJUSTMENTS_TEMPERATURE_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.whiteBalance']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_TINT_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.tint']//*[@data-testid='colorAdjustments.adjustments.slider.tint.title']")
    ADJUSTMENTS_TINT_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.tint']//input")
    ADJUSTMENTS_TINT_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.tint']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_HDR_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.hdr']//*[@data-testid='colorAdjustments.adjustments.switcher.hdr.toolTip.title']")
    ADJUSTMENTS_HDR_CHECKBOX = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.hdr']//input[@data-testid='switchRow.checkbox']")
    ADJUSTMENTS_HDR_TOGGLE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.switcher.hdr']//span[@data-testid='checkbox.thumb']")

    ADJUSTMENTS_BRIGHTNESS_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.brightness']//*[@data-testid='colorAdjustments.adjustments.slider.brightness.title']")
    ADJUSTMENTS_BRIGHTNESS_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.brightness']//input")
    ADJUSTMENTS_BRIGHTNESS_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.brightness']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_CONTRAST_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.contrast']//*[@data-testid='colorAdjustments.adjustments.slider.contrast.title']")
    ADJUSTMENTS_CONTRAST_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.contrast']//input")
    ADJUSTMENTS_CONTRAST_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.contrast']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_SATURATION_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.saturation']//*[@data-testid='colorAdjustments.adjustments.slider.saturation.title']")
    ADJUSTMENTS_SATURATION_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.saturation']//input")
    ADJUSTMENTS_SATURATION_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.saturation']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_VIBRANCE_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.vibrance']//*[@data-testid='colorAdjustments.adjustments.slider.vibrance.title']")
    ADJUSTMENTS_VIBRANCE_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.vibrance']//input")
    ADJUSTMENTS_VIBRANCE_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.vibrance']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_SHARPNESS_LABEL = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.sharpness']//*[@data-testid='colorAdjustments.adjustments.slider.sharpness.title']")
    ADJUSTMENTS_SHARPNESS_SLIDER = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.sharpness']//input")
    ADJUSTMENTS_SHARPNESS_VALUE = (By.XPATH, "//div[@data-testid='colorAdjustments.adjustments.slider.sharpness']//span[@data-testid='sliderRow.subTitle']")

    ADJUSTMENTS_INTERACTIVE_SCROLLBAR = (By.XPATH, "//div[@data-testid='scrollbar.interactiveScrollbar']")
    ADJUSTMENTS_RESET_TO_DEFAULT = (By.XPATH, "//button[@data-testid='colorAdjustments.adjustments.button.resetToDefault']")

    #Sound Section
    DEVICE_BACK = (By.XPATH, "//div[@data-testid='windowPage.widget.header']//*[@class='icon icon-back']")
    DEVICE_BUTTON_FUNCTIONS_BACK = (By.XPATH, "//*[@data-testid='screen.button.back']")

    SIDETONE_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.soundMenu.sidetone.title']")
    SIDETONE_VALUE = (By.XPATH, "//p[@data-testid='dashboard.device.soundMenu.sidetone.percentage']")
    SIDETONE_SLIDER_AREA = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.sidetone.dialog.slider']")
    SIDETONE_SLIDER = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.sidetone.dialog.slider']//input")
    SIDETONE_DONE = (By.XPATH, "//button[@data-testid='dashboard.device.soundMenu.sidetone.dialog.doneButton']")

    MIC_LEVEL_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.microphone']/p")
    MIC_LEVEL_VALUE = (By.XPATH, "//p[@data-testid='dashboard.device.soundMenu.microphone.microphoneLevel']")
    MIC_LEVEL_DONE = (By.XPATH, "//button[@data-testid='dashboard.device.soundMenu.microphone.dialog.doneButton']")
    MIC_LEVEL_SLIDER_AREA = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.microphone.dialog.micLevel.slider']")
    MIC_LEVEL_SLIDER = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.microphone.dialog.micLevel.slider']//input")

    EQUALIZER = (By.XPATH, "//p[@data-testid='dashboard.device.soundMenu.equalizer.title']")
    EQUALIZER_BOX_PROFILE_NAME = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.equalizer.selector']")
    EQUALIZER_BACK = (By.XPATH, '//*[@class="icon icon-back"]')
    EQUALIZER_ADD_CUSTOM_PRESET = (By.XPATH, "//button[@data-testid='equalizer.body.button.saveCustomPreset']")
    EQUALIZER_ADD_CUSTOM_PRESET_NAME = (By.XPATH, "//input[@data-testid='equalizer.presetForm.element.preset']")
    EQUALIZER_ADD_CUSTOM_PRESET_SAVE = (By.XPATH, "//button[@data-testid='equalizer.presetForm.button.save']")
    EQUALIZER_EDIT = (By.XPATH, "//button[@data-testid='equalizer.footer.button.editPresets']")
    EQUALIZER_EDIT_DONE = (By.XPATH, "//button[@data-testid='equalizer.presetEditForm.button.done']")
    EQUALIZER_MAX_PRESET_PROMPT = (By.ID, 'win_equalizer_main_preset_error')
    EQUALIZER_MAX_PRESET_PROMPT_OK_BUTTON = (By.XPATH, "//button[@data-testid='equalizer.presetLimitError.button.okay']")
    EQ_SLIDERS_SCROLL_AREA = (By.XPATH, "//div[@class='window-page-body window-page-body-scroll']")
    EQ_SLIDER_0 = (By.XPATH, "//div[@data-testid='slider.0']//input[@data-testid='slider.input']")
    EQ_SLIDER_1 = (By.XPATH, "//div[@data-testid='slider.1']//input[@data-testid='slider.input']")
    EQ_SLIDER_2 = (By.XPATH, "//div[@data-testid='slider.2']//input[@data-testid='slider.input']")
    EQ_SLIDER_3 = (By.XPATH, "//div[@data-testid='slider.3']//input[@data-testid='slider.input']")
    EQ_SLIDER_4 = (By.XPATH, "//div[@data-testid='slider.4']//input[@data-testid='slider.input']")
    EQ_AXIS_TIPS_BASS = (By.XPATH, "//div[@class='equaliser-axis-tips']//div[1]")
    EQ_AXIS_TIPS_MIDS = (By.XPATH, "//div[@class='equaliser-axis-tips']//div[2]")
    EQ_AXIS_TIPS_TREBLE = (By.XPATH, "//div[@class='equaliser-axis-tips']//div[3]")
    EQ_PRESET_DEFAULT_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][1]//*[@data-testid='element.title']")
    EQ_PRESET_DEFAULT_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][1]//*[@data-testid='element.radio']")
    EQ_PRESET_VOLBOOST_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][2]//*[@data-testid='element.title']")
    EQ_PRESET_VOLBOOST_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][2]//*[@data-testid='element.radio']")
    EQ_PRESET_PODCAST_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][3]//*[@data-testid='element.title']")
    EQ_PRESET_PODCAST_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][3]//*[@data-testid='element.radio']")
    EQ_PRESET_BASSBOOST_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][4]//*[@data-testid='element.title']")
    EQ_PRESET_BASSBOOST_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][4]//*[@data-testid='element.radio']")
    EQ_PRESET_CUSTOM_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][5]//*[@data-testid='element.title']")
    EQ_PRESET_CUSTOM_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][5]//*[@data-testid='element.radio']")
    EQ_PRESET_CUSTOM_USER_1_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][6]//*[@data-testid='element.title']")
    EQ_PRESET_CUSTOM_USER_1_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][6]//*[@data-testid='element.radio']")
    EQ_PRESET_CUSTOM_USER_1_DELETE_LABEL = (By.XPATH, "//div[@id='win_equalizer_main_preset_edit']//div[@class='element-delete'][6]//*[@data-testid='element.title']")
    EQ_PRESET_CUSTOM_USER_1_DELETE_BUTTON = (By.XPATH, "//div[@id='win_equalizer_main_preset_edit']//div[@class='element-delete'][6]//*[@data-testid='element.button.delete']")
    EQ_PRESET_CUSTOM_USER_2_LABEL = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][7]//*[@data-testid='element.title']")
    EQ_PRESET_CUSTOM_USER_2_RADIO = (By.XPATH, "//div[@data-testid='equalizer.main.windowPage']//div[@class='element-radio'][7]//*[@data-testid='element.radio']")
    EQ_PRESET_CUSTOM_USER_2_DELETE_LABEL = (By.XPATH, "//div[@id='win_equalizer_main_preset_edit']//div[@class='element-delete'][7]//*[@data-testid='element.title']")
    EQ_PRESET_CUSTOM_USER_2_DELETE_BUTTON = (By.XPATH, "//div[@id='win_equalizer_main_preset_edit']//div[@class='element-delete'][7]//*[@data-testid='element.button.delete']")

    DEVICE_NAME_RENAME = (By.XPATH, "//p[@data-testid='dashboard.device.settings.rename.openDialogButton']")
    DEVICE_NAME_MAIN_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.rename.title']")
    DEVICE_NAME_SURPRISE = (By.XPATH, "//button[@data-testid='dashboard.device.settings.renameDialog.form.surpriseMeButton']")
    DEVICE_NAME_UPDATE = (By.XPATH, "//button[@data-testid='dashboard.device.settings.renameDialog.form.submitButton']")
    DEVICE_NAME_INPUT = (By.XPATH, "//input[@data-testid='dashboard.device.settings.renameDialog.form.nameInput']")
    DEVICE_NAME_ERROR = (By.XPATH, "//form[@data-testid='dashboard.device.settings.renameDialog.form']/div[1]/div[1]")

    SLEEP_SETTINGS_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.sleep.title']")
    SLEEP_SETTINGS_VALUE = (By.XPATH, "//p[@data-testid='dashboard.device.settings.sleep.openDialogButton']")
    SLEEP_TIMEOUT_SAVE = (By.XPATH, "//button[@data-testid='dashboard.device.settings.sleepDialog.saveButton']")
    SLEEP_5_MIN_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.5']//div[@data-testid='radioButton.label']")
    SLEEP_5_MIN_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.5']//*[@data-testid='radioButton.element']")
    SLEEP_10_MIN_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.10']//div[@data-testid='radioButton.label']")
    SLEEP_10_MIN_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.10']//*[@data-testid='radioButton.element']")
    SLEEP_15_MIN_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.15']//div[@data-testid='radioButton.label']")
    SLEEP_15_MIN_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.15']//*[@data-testid='radioButton.element']")
    SLEEP_30_MIN_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.30']//div[@data-testid='radioButton.label']")
    SLEEP_30_MIN_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.30']//*[@data-testid='radioButton.element']")
    SLEEP_1_H_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.60']//div[@data-testid='radioButton.label']")
    SLEEP_1_H_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.60']//*[@data-testid='radioButton.element']")
    SLEEP_2_H_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.120']//div[@data-testid='radioButton.label']")
    SLEEP_2_H_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.120']//*[@data-testid='radioButton.element']")
    SLEEP_4_H_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.240']//div[@data-testid='radioButton.label']")
    SLEEP_4_H_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.240']//*[@data-testid='radioButton.element']")
    SLEEP_NEVER_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.0']//div[@data-testid='radioButton.label']")
    SLEEP_NEVER_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.0']//*[@data-testid='radioButton.element']")

    SLEEP_TIMEOUT_INPUT = (By.XPATH, "//div[@data-testid='dashboard.device.settings.sleepDialog.buttonGroup.XXX']//input")

    CONNECTION_PRIORITY_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.connectionPriority.title']")
    CONNECTION_PRIORITY_VALUE = (By.XPATH, "//span[contains(@data-testid, 'dashboard.device.settings.connectionPriority.select')]")
    CONNECTION_PRIORITY_STABLE_CONNECTION = (By.XPATH, "//div[@data-testid='dashboard.device.settings.connectionPriorityDialog.stableConnection.checkbox']/label")
    CONNECTION_PRIORITY_STABLE_CONNECTION_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.connectionPriorityDialog.stableConnection.checkbox']//input[@data-testid='element.radio']")
    CONNECTION_PRIORITY_SOUND_QUALITY = (By.XPATH, "//div[@data-testid='dashboard.device.settings.connectionPriorityDialog.soundQuality.checkbox']/label")
    CONNECTION_PRIORITY_SOUND_QUALITY_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.connectionPriorityDialog.soundQuality.checkbox']//input[@data-testid='element.radio']")
    CONNECTION_PRIORITY_SAVE = (By.XPATH, "//button[@data-testid='dashboard.device.settings.connectionPriorityDialog.saveBtn']")

    CONNECTED_DEVICES_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.connection.title']")
    CONNECTED_DEVICES_NAME = (By.XPATH, "//div[@data-testid='connectionhistory.historyItem.name']")
    CONNECTED_DEVICE_CLOSE = (By.XPATH, '//*[@class="icon icon-back"]')

    BUTTON_FUNCTIONS_LABEL = (By.XPATH, "//p[@data-testid='settingsmenu.settings.button.title']")
    BUTTON_FUNCTIONS_SINGLE_PRESS_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.headsetButtonFunctions.singlePress.button']//p[@data-testid='valueRow.title']")
    BUTTON_FUNCTIONS_SINGLE_PRESS_VALUE = (By.XPATH, "//div[@data-testid='buttonFunctions.headsetButtonFunctions.singlePress.button']//p[@data-testid='valueRow.value']")
    BUTTON_FUNCTIONS_DOUBLE_PRESS_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.headsetButtonFunctions.doublePress.button']//p[@data-testid='valueRow.title']")
    BUTTON_FUNCTIONS_DOUBLE_PRESS_VALUE = (By.XPATH, "//div[@data-testid='buttonFunctions.headsetButtonFunctions.doublePress.button']//p[@data-testid='valueRow.value']")
    BUTTON_FUNCTIONS_LONG_PRESS_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.headsetButtonFunctions.longPress.button']//p[@data-testid='valueRow.title']")
    BUTTON_FUNCTIONS_LONG_PRESS_VALUE = (By.XPATH, "//div[@data-testid='buttonFunctions.headsetButtonFunctions.longPress.button']//p[@data-testid='valueRow.value']")
    BUTTON_FUNCTIONS_SAVE_BUTTON = (By.XPATH, "//button[@data-testid='buttonFunctions.customizationDialog.button.save']")
    BUTTON_FUNCTIONS_RESTORE_DEFAULTS = (By.XPATH, "//button[@data-testid='buttonFunctions.headsetButtonFunctions.button.restore']")
    BUTTON_FUNCTIONS_RESTORE_DEFAULTS_CONFIRM = (By.XPATH, "//button[@data-testid='buttonFunctions.restoreDefaultDialog.button.resetDefaults']")
    SOUND_BACK_BUTTON = (By.XPATH, "//svg[@data-testid='screen.button.back']")

    BUTTON_FUNCTIONS_RADIO_0_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-0']//*[@data-testid='element.title']")
    BUTTON_FUNCTIONS_RADIO_0_RADIO = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-0']//*[@data-testid='element.radio']")
    BUTTON_FUNCTIONS_RADIO_1_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-1']//*[@data-testid='element.title']")
    BUTTON_FUNCTIONS_RADIO_1_RADIO = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-1']//*[@data-testid='element.radio']")
    BUTTON_FUNCTIONS_RADIO_3_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-3']//*[@data-testid='element.title']")
    BUTTON_FUNCTIONS_RADIO_3_RADIO = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-3']//*[@data-testid='element.radio']")
    BUTTON_FUNCTIONS_RADIO_4_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-4']//*[@data-testid='element.title']")
    BUTTON_FUNCTIONS_RADIO_4_RADIO = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-4']//*[@data-testid='element.radio']")
    BUTTON_FUNCTIONS_RADIO_5_LABEL = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-5']//*[@data-testid='element.title']")
    BUTTON_FUNCTIONS_RADIO_5_RADIO = (By.XPATH, "//div[@data-testid='buttonFunctions.customizationDialog.elementRadio-5']//*[@data-testid='element.radio']")

    ROTATE_TO_MUTE_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.rotateToMute']/p")
    ROTATE_TO_MUTE_CHECKBOX = (By.XPATH, "//input[@data-testid='dashboard.device.settings.rotateToMute.checkbox']")
    ROTATE_TO_MUTE_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.settings.rotateToMute']/div/label/span[2]")

    TOUCH_PAD_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.settings.touchDetection']//p[@data-testid='switchRow.title']")
    TOUCH_PAD_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.settings.touchDetection']//input[@data-testid='switchRow.checkbox']")
    TOUCH_PAD_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.settings.touchDetection']//span[@data-testid='checkbox.thumb']")

    PERSONAL_EQ_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.settings.personalizedEQ']//span[@data-testid='switchRow.title']")
    PERSONAL_EQ_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.settings.personalizedEQ']//input[@data-testid='switchRow.checkbox']")
    PERSONAL_EQ_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.settings.personalizedEQ']//span[@data-testid='checkbox.thumb']")

    ANC_BUTTON_GROUP = (By.XPATH, "//p[@data-testid='dashboard.device.soundMenu.ancButtonGroup']")
    ANC_BUTTON_GROUP_DIV = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.ancButtonGroup']")
    ANC_DISABLED = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.ancButton.disabled']")
    ANC_AMBIENCE_TRANSPARENCY = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.ancButton.ambienceTransparency']")
    ANC_LOW = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.ancButton.noiseCancellationGroup.noiseCancellationLow']")
    ANC_HIGH = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.ancButton.noiseCancellationGroup.noiseCancellationHigh']")

    NOISE_CANCELLATION_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.soundMenu.ancToggle.title']")
    NOISE_CANCELLATION_CHECKBOX = (By.XPATH, "//input[@data-testid='dashboard.device.soundMenu.ancToggle.checkbox']")
    NOISE_CANCELLATION_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.ancToggle']/label/span[2]")

    ANC_BUTTON_OPTIONS = (By.XPATH, "//p[@data-testid='dashboard.device.settings.ancButtonCustomization.title']")
    ANC_BUTTON_OPTIONS_TRANSPARENCY_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.ambienceTransparency']//span[@data-testid='switchRow.title']")
    ANC_BUTTON_OPTIONS_TRANSPARENCY_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.ambienceTransparency']//input[@data-testid='switchRow.checkbox']")
    ANC_BUTTON_OPTIONS_TRANSPARENCY_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.ambienceTransparency']//span[@data-testid='checkbox.thumb']")
    ANC_BUTTON_OPTIONS_NONE_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.disabled']//span[@data-testid='switchRow.title']")
    ANC_BUTTON_OPTIONS_NONE_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.disabled']//input[@data-testid='switchRow.checkbox']")
    ANC_BUTTON_OPTIONS_NONE_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.disabled']//span[@data-testid='checkbox.thumb']")
    ANC_BUTTON_OPTIONS_ANC_LOW_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.noiseCancellationLow']//span[@data-testid='switchRow.title']")
    ANC_BUTTON_OPTIONS_ANC_LOW_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.noiseCancellationLow']//input[@data-testid='switchRow.checkbox']")
    ANC_BUTTON_OPTIONS_ANC_LOW_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.noiseCancellationLow']//span[@data-testid='checkbox.thumb']")
    ANC_BUTTON_OPTIONS_ANC_HIGH_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.noiseCancellationHigh']//span[@data-testid='switchRow.title']")
    ANC_BUTTON_OPTIONS_ANC_HIGH_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.noiseCancellationHigh']//input[@data-testid='switchRow.checkbox']")
    ANC_BUTTON_OPTIONS_ANC_HIGH_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.ancButtonCustomization.switch.noiseCancellationHigh']//span[@data-testid='checkbox.thumb']")

    VOICE_PROMPTS_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.voicePrompts.title']")
    VOICE_PROMPTS_CHECKBOX = (By.XPATH, "//input[@data-testid='dashboard.device.settings.voicePrompts.checkbox']")
    VOICE_PROMPTS_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePrompts']/div/label/span[2]")

    VOICE_PROMPTS_3_LEVEL_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.threeStateVoicePrompts.title']")
    VOICE_PROMPTS_3_LEVEL_NAME = (By.XPATH, "//p[@data-testid='dashboard.device.settings.threeStateVoicePrompts.openDialogButton']")
    VOICE_PROMPTS_3_SAVE_DIALOG = (By.XPATH, "//button[@data-testid='dashboard.device.settings.voicePromptsDialog.saveButton']")

    VOICE_PROMPTS_3_VOICE_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePromptsDialog.buttonGroup.1']//div[@data-testid='radioButton.label']")
    VOICE_PROMPTS_3_VOICE_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePromptsDialog.buttonGroup.1']//*[@data-testid='radioButton.element']")
    VOICE_PROMPTS_3_TONES_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePromptsDialog.buttonGroup.0']//div[@data-testid='radioButton.label']")
    VOICE_PROMPTS_3_TONES_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePromptsDialog.buttonGroup.0']//*[@data-testid='radioButton.element']")
    VOICE_PROMPTS_3_OFF_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePromptsDialog.buttonGroup.2']//div[@data-testid='radioButton.label']")
    VOICE_PROMPTS_3_OFF_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePromptsDialog.buttonGroup.2']//*[@data-testid='radioButton.element']")

    HEALTH_AND_SAFETY_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.healthAndSafety.container.title']")
    ANTI_STARTLE_PROTECTION_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.healthAndSafety.antiStartleControl']//span[@data-testid='switchRow.title']")
    ANTI_STARTLE_PROTECTION_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.healthAndSafety.antiStartleControl']//input[@data-testid='switchRow.checkbox']")
    ANTI_STARTLE_PROTECTION_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.healthAndSafety.antiStartleControl']//span[@data-testid='checkbox.thumb']")
    DASHBOARD_ANTI_STARTLE_PROTECTION_LABEL = (By.XPATH,
                                     "//span[@data-testid='dashboard.device.healthAndSafety.antiStartleControl.toolTip.title']")
    DASHBOARD_ANTI_STARTLE_PROTECTION_CHECKBOX = (By.XPATH,
                                        "//div[@data-testid='dashboard.device.healthAndSafety.antiStartleControl']//input[@data-testid='switchRow.checkbox']")
    DASHBOARD_ANTI_STARTLE_PROTECTION_TOGGLE = (By.XPATH,
                                      "//div[@data-testid='dashboard.device.healthAndSafety.antiStartleControl']//span[@data-testid='checkbox.thumb']")
    NOISE_EXPOSURE_CONTROL_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.healthAndSafety.noiseExposureControl']//span[@data-testid='switchRow.title']")
    NOISE_EXPOSURE_CONTROL_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.healthAndSafety.noiseExposureControl']//input[@data-testid='switchRow.checkbox']")
    NOISE_EXPOSURE_CONTROL_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.healthAndSafety.noiseExposureControl']//span[@data-testid='checkbox.thumb']")

    ON_HEAD_DETECTION_LABEL = (By.XPATH, "//p[@data-testid='dashboard.device.settings.onHeadDetection.title']")
    AUTO_MUTE_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoMuteControl']//span[@data-testid='switchRow.title']")
    AUTO_MUTE_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoMuteControl']//label//input[@data-testid='switchRow.checkbox']")
    AUTO_MUTE_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoMuteControl']//label/span[2]")
    AUTO_ANSWER_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoAnswerControl']//span[@data-testid='switchRow.title']")
    AUTO_ANSWER_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoAnswerControl']//label/input")
    AUTO_ANSWER_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoAnswerControl']//label/span[2]")
    AUTO_PAUSE_LABEL = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoPauseControl']//span[@data-testid='switchRow.title']")
    AUTO_PAUSE_CHECKBOX = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoPauseControl']//label/input")
    AUTO_PAUSE_TOGGLE = (By.XPATH, "//div[@data-testid='headsetSettings.onHeadDetection.autoPauseControl']//label/span[2]")

    ADVANCED_CALL_CLARITY_LABEL = (By.XPATH, "//span[@data-testid='dashboard.device.settings.noiseReduction.tooltip.title']")
    ADVANCED_CALL_CLARITY_LEVEL_NAME = (By.XPATH, "//p[@data-testid='dashboard.device.settings.noiseReductionLevel.openDialogButton']")
    ADVANCED_CALL_CLARITY_LEVEL_SAVE_DIALOG = (By.XPATH, "//button[@data-testid='dashboard.device.settings.noiseReductionLevelForm.saveButton']")
    ADVANCED_CALL_CLARITY_LEVEL_LABEL = (By.XPATH, "//div[@data-testid='radioButton.label']")
    ADVANCED_CALL_CLARITY_LEVEL_RADIO = (By.XPATH, "//input[@data-testid='radioButton.element']")
    ADVANCED_CALL_CLARITY_LEVEL_OFF_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.noiseReductionLevelForm.buttonGroup.0']//div[@data-testid='radioButton.label']")
    ADVANCED_CALL_CLARITY_LEVEL_OFF_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.noiseReductionLevelForm.buttonGroup.0']//input[@data-testid='radioButton.element']")
    ADVANCED_CALL_CLARITY_LEVEL_LOW_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.noiseReductionLevelForm.buttonGroup.1']//div[@data-testid='radioButton.label']")
    ADVANCED_CALL_CLARITY_LEVEL_LOW_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.noiseReductionLevelForm.buttonGroup.1']//input[@data-testid='radioButton.element']")
    ADVANCED_CALL_CLARITY_LEVEL_HIGH_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.settings.noiseReductionLevelForm.buttonGroup.3']//div[@data-testid='radioButton.label']")
    ADVANCED_CALL_CLARITY_LEVEL_HIGH_RADIO = (By.XPATH, "//div[@data-testid='dashboard.device.settings.noiseReductionLevelForm.buttonGroup.3']//input[@data-testid='radioButton.element']")

    HEADSET_DIAGNOSTICS_LABEL = (By.XPATH, "//div[@data-testid='dashboard.device.soundMenu.headsetDiagnostics']")
    HEADSET_DIAGNOSTICS_BTN = (By.XPATH, "//button[@data-testid='dashboard.device.soundMenu.headsetDiagnostics.runTestButton']")
    HEADSET_DIAGNOSTICS_RINGTONE_DIAGRAM = (By.XPATH, "//canvas[@data-testid='headsetdiagnostics.diagram]")
    HEADSET_DIAGNOSTICS_SPEAKER_TEST_YES_BTN = (By.XPATH, "//button[@data-testid='headsetdiagnostics.testSpeaker.button.yes']")
    HEADSET_DIAGNOSTICS_SPEAKER_TEST_NO_BTN = (By.XPATH, "//button[@data-testid='headsetdiagnostics.testSpeaker.button.no']")
    HEADSET_DIAGNOSTICS_RECORD_BTN = (By.XPATH, "//div[@data-testid='headsetdiagnostics.testMicrophone.button.startRecording']")
    HEADSET_DIAGNOSTICS_RECORD_STOP_BTN = (By.XPATH, "recording inprocess")
    HEADSET_DIAGNOSTICS_MIC_TEST_YES_BTN = (By.XPATH, "//button[@data-testid='headsetdiagnostics.testMicrophone.button.yes']")
    HEADSET_DIAGNOSTICS_MIC_TEST_NO_BTN = (By.XPATH, "//button[@data-testid='headsetdiagnostics.testMicrophone.button.no']")
    HEADSET_DIAGNOSTICS_MIC_SPEAKER_OK_LABEL = (By.XPATH, "//p[text()='Microphone and speaker OK.']")  # ticket created
    HEADSET_DIAGNOSTICS_MIC_SPEAKER_BROKEN_LABEL = (By.XPATH, "//p[text()='Update or restart your']")  # ticket created
    HEADSET_DIAGNOSTICS_CONNECTIVITY_LABEL = (By.XPATH, "//p[text()='Headset and Internet connection ok']")  # ticket created
    HEADSET_DIAGNOSTICS_SOFTPHONE_LABEL = (By.XPATH, "//p[text()='In app settings, confirm ']")  # ticket created
    HEADSET_DIAGNOSTICS_CLOSE_BTN = (By.XPATH, "//*[@data-testid='header.button.close']")
    HEADSET_DIAGNOSTICS_START_TESTING_BTN = (By.XPATH, "//*[@data-testid='headsetdiagnostics.main.button.startTest']")

    MEETING_ALERT_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.hubSettings.toggleMeetingAlert']//p[@data-testid='switchRow.title']")
    MEETING_ALERT_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.hubSettings.toggleMeetingAlert']//input[@data-testid='switchRow.checkbox']")
    MEETING_ALERT_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.hubSettings.toggleMeetingAlert']//span[@data-testid='checkbox.thumb']")
    MEETING_EVENT_NAME = (By.XPATH, "//*[@data-testid='dashboard.agenda.meetingCard.large.title']")
    MEETING_CARD = (By.XPATH, "//div[@data-testid='dashboard.agenda.meetingCard.wrapper']")
    MEETING_COUNTDOWN_LABEL = (By.XPATH, "//button[@data-testid='dashboard.agenda.infoTag.wrapper']")
    MEETING_TIME_LABEL = (By.XPATH, "//div[@data-testid='dashboard.agenda.meetingCard.time']")
    MEETING_JOIN_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.agenda.meetingCard.large.link']")
    TOMORROW_LABEL = (By.XPATH, "//*[@data-testid='dashboard.agenda.title.typography']")
    MEETING_TOMORROW_EVENT_NAME = (By.XPATH, "//*[@data-testid='dashboard.agenda.meetingCard.small.title']")
    CALENDAR_DAY_LABEL = (By.XPATH, "//button[contains(@data-testid, 'dashboard.home.dateRow.date')]/div")
    COLLAPSE_CALENDAR = (By.XPATH, "//button[@data-testid='dashboard.home.dateRow.collapse.open']")
    COLLAPSE_CALENDAR_CLOSE = (By.XPATH, "//button[@data-testid='dashboard.home.dateRow.collapse.close']")


    HI_SPEED_USB_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.hubSettings.hispeedUsbToggle']//span[@data-testid='switchRow.title']")
    HI_SPEED_USB_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.hubSettings.hispeedUsbToggle']//input[@data-testid='switchRow.checkbox']")
    HI_SPEED_USB_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.hubSettings.hispeedUsbToggle']//span[@data-testid='checkbox.thumb']")

    LOGI_DOCK_RECONNECTING_DIALOG = (By.XPATH, "//p[@data-testid='app.reconnectDeviceDialog.title']")

    IN_EAR_DETECTION = (By.XPATH, "//div[@data-testid='dashboard.device.headphone']//p[@data-testid='switchRow.title']")
    IN_EAR_DETECTION_CHECKBOX = (By.XPATH,
                                 "//div[@data-testid='dashboard.device.headphone']//p[@data-testid='switchRow.title']/following-sibling::label/input[@data-testid='switchRow.checkbox']")
    IN_EAR_DETECTION_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.headphone']//p[@data-testid='switchRow.title']/following-sibling::label/span[2]")
    ENABLE_RECEIVER_CONNECTION = (By.XPATH, "//span[@data-testid='dashboard.device.settings.dongleConnectionPriority.tooltip.title']")

    #ABOUT THE DEVICE
    FIRMWARE_VERSION_BOX = (By.XPATH, "//p[@data-testid='aboutDevice.fwBox.details']")
    FACTORY_RESET = (By.XPATH, "//button[@data-testid='aboutDevice.reset.factoryResetBtn']")
    PROCEED_TO_FACTORY_RESET = (By.XPATH, "//button[@data-testid='aboutDevice.reset.proceedBtn']")
    RECONNECT_DEVICE = (By.XPATH, "//p[@data-testid='resetProgress.dialog.title']")
    MORE_DETAILS = (By.XPATH, "//button[@data-testid='aboutDevice.moreDetailsBtn']")

    #DEVICE STATUS
    CONNECTED = (By.XPATH, "//p[@data-testid='dashboard.device.statusBar.statusLabel']")
    DEVICE_NAME = (By.XPATH, "")
    BATTERY_SIGN = (By.XPATH, "//p[contains(., '%')]")

    #INFO PAGE
    INFO_BUTTON = (By.XPATH, "//div[@data-testid='dashboard.device.statusBar.infoBtn']")
    RECEIVER = (By.XPATH, "//p[contains(., 'Receiver')]")
    FIRMWARE_VERSION = (By.XPATH, "//p[contains(., 'Firmware')]/../../p")

    #APP UPDATE
    TUNE_UPDATED_OK_BUTTON = (By.XPATH, "//button[@data-testid='autoupdate.appUpdatedPopup.button.ok']")
    UPDATE_OK = (By.XPATH, "//button[@data-testid='autoupdate.appUpdatedPopup.button.ok']")
    APP_VERSION = (By.XPATH, "//p[@data-testid='aboutapp.title']")
    UPDATE_REQUIRED_LABEL = (By.XPATH, "//p[@data-testid='dashboard.fwuDialog.updateRequired']")
    UPDATE_APP_NOW = (By.XPATH, "//button[@data-testid='autoupdate.appUpdateAvailablePopup.button.updateNow']")
    UPDATE_APP_BUTTON = (By.XPATH, "//button[@data-testid='aboutapp.button.updateApp']")
    UPDATE_APP_LATER_BUTTON = (By.XPATH, "//button[@data-testid='autoupdate.appUpdateAvailablePopup.button.RemideMeLater']")


    # FIRMWARE UPDATE
    UPDATE = (By.XPATH, "//button[text()='update' and @data-testid='aboutDevice.fwBox.updateBtn']")
    START_UPDATE = (By.XPATH, "//button[@data-testid='fwuFlow.info.firmwareInfo.button.update']")
    UPDATE_VERSION = (By.XPATH, "//p[@data-testid='fwuFlow.info.releaseNoteInfo.caption']")
    FW_UPDATE_REQUIRED = (By.XPATH, "//p[@data-testid='dashboard.fwuDialog.updateRequired']")
    FW_UPDATE_UPDATE_BTN = (By.XPATH, "//button[@data-testid='dashboard.fwuDialog.updateButton']")
    FWU_DONE = (By.XPATH, "//button[@data-testid='fwuFlow.updateSuccessful.button.done']")

    #EASTER EGG
    EASTER_EGG_MENU_OPEN = (By.XPATH, "//p[contains(., 'Firmware')]/../../p")
    EASTER_EGG_TITLE = (By.XPATH, "//*[text()='Easter Egg']")
    HEADSET_PATH_EASTER_EGG = (By.XPATH, '//*[@id="win_easter_egg_firmware_popup"]/div[3]/div[1]/input')
    DEVICE_PATH_EASTER_EGG = (By.XPATH, '//*[@id="win_easter_egg_firmware_popup"]/div[3]/div[1]/input')
    RECEIVER_PATH_EASTER_EGG = (By.XPATH, '//*[@id="win_easter_egg_firmware_popup"]/div[3]/div[2]/input')
    EASTER_EGG_UPDATE = (By.XPATH, '//button[contains(@class, "fw-update-headset")]')
    DEVICE_EASTER_EGG_UPDATE = (By.XPATH, '//button[contains(@class, "fw-update-headset")]')
    RECEIVER_EASTER_EGG_UPDATE = (By.XPATH, '//button[contains(@class, "fw-update-receiver")]')
    UPDATE_FAILED = (By.XPATH, "//button[@data-testid='fwuFlow.updateFailed.button.updateAgain']")

    # MORE DETAILS
    MORE_DETAILS_TITLE = (By.XPATH, "//p[@data-testid='aboutDevice.detailsDialog.title']")
    MORE_DETAILS_TEXT = (By.XPATH, "//p[@data-testid='aboutDevice.detailsDialog.text']")
    MORE_DETAILS_CLOSE = (By.XPATH, "//*[@data-testid='dialog.button.close']")

    #LANGUAGE
    LANGUAGE_TAB = (By.XPATH, "//p[@data-testid='dashboard.device.settings.voicePrompts.language.select']")
    LANGUAGE_TITLE = (By.XPATH, "//p[@data-testid='dashboard.device.settings.voicePrompts.language.title']")
    LANGUAGE_TAB_HEADER = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.windowPage']//div[@data-testid='header.title']")
    LANGUAGE_NAME_SETTINGS_TAB = (By.XPATH, "//p[@data-testid='dashboard.device.settings.voicePrompts.language.select']")
    FRENCH_BUTTON = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.button-LANGUAGE_FRENCH']/button")
    FRENCH_RADIO = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.radio-LANGUAGE_FRENCH']/label/input")
    SPANISH_BUTTON = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.button-LANGUAGE_SPANISH']/button")
    SPANISH_RADIO = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.radio-LANGUAGE_SPANISH']/label/input")
    GERMAN_BUTTON = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.button-LANGUAGE_GERMAN']/button")
    GERMAN_RADIO = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.radio-LANGUAGE_GERMAN']/label/input")
    ITALIAN_BUTTON = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.button-LANGUAGE_ITALIAN']/button")
    ITALIAN_RADIO = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.radio-LANGUAGE_ITALIAN']/label/input")
    PORTUGUESE_BUTTON = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.button-LANGUAGE_PORTUGUESE']/button")
    PORTUGUESE_RADIO = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.radio-LANGUAGE_PORTUGUESE']/label/input")
    ENGLISH_BUTTON = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.button-LANGUAGE_ENGLISH_US']/button")
    ENGLISH_RADIO = (By.XPATH, "//div[@data-testid='settingsmenu.language.Main.radio-LANGUAGE_ENGLISH_US']/label/input")
    LANGUAGE_INSTALL = (By.XPATH, "//button[@data-testid='settingsmenu.language.downloadInfo.button.install']")
    LANGUAGE_DONE = (By.XPATH, "//button[@data-testid='settingsmenu.language.downloadSuccessful.button.done']")

    #LITRA BEAM
    POWER_ON_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.powerOnSwitch']//p[@data-testid='switchRow.title']")
    POWER_ON_TITLE_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.powerOnSwitch']//input[@data-testid='switchRow.checkbox']")
    POWER_ON_TITLE_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.powerOnSwitch']//span[@data-testid='checkbox.thumb']")
    LITRA_WINDOW_SCROLL_AREA = (By.XPATH, "//div[@class='simplebar-content-wrapper']")

    LITRA_LABEL_NAME = (By.XPATH, "//p[@data-testid='dashboard.device.settings.illuminationPreset.title']")
    LITRA_LABEL_PRESET_NAME = (By.XPATH, "//p[@data-testid='dashboard.device.settings.illuminationPreset.selected']")
    LITRA_PRESETS_WINDOW = (By.XPATH, "//div[@role='dialog']")
    LITRA_PRESET_CLOSE = (By.XPATH, "//*[@data-testid='dialog.button.close']")

    LITRA_TEMPERATURE_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.temperatureSlider']//span")
    LITRA_TEMPERATURE_SLIDER = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.temperatureSlider']//input")
    LITRA_TEMP_PLUS = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.temperatureSlider']//*[@data-testid='sliderRow.button.plus']")
    LITRA_TEMP_MINUS = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.temperatureSlider']//*[@data-testid='sliderRow.button.minus']")

    LITRA_BRIGHTNESS_TITLE = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.brightnessSlider']//span")
    LITRA_BRIGHTNESS_SLIDER = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.brightnessSlider']//input")
    LITRA_BRIGHTNESS_PLUS = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.brightnessSlider']//*[@data-testid='sliderRow.button.plus']")
    LITRA_BRIGHTNESS_MINUS = (By.XPATH, "//div[@data-testid='dashboard.device.streamingLight.brightnessSlider']//*[@data-testid='sliderRow.button.minus']")

    LITRA_DEVICE_NAME_POPUP = (By.XPATH, "//div[@id='rename-popup']")
    LITRA_DEVICE_NAME_POPUP_CLOSE = (By.XPATH, "//*[@data-testid='header.button.close']")

    LITRA_POWER_WARRNING = (By.XPATH, "//div[@data-testid='streamingLight.brightness.iconError']")

    LITRA_FACTORY_RESET_DONE = (By.XPATH, "//*[text()='Done']")  # ticket created

    # Receiver
    DONGLE_PAIR_HEADSET = (By.XPATH, "//button[@data-testid='receiverFlow.receiver.button.pairHeadset']")
    DONGLE_CONTINUE_BUTTON = (By.XPATH, "//button[@data-testid='receiverFlow.pairDialog.button.continue']")
    DONGLE_PAIR_DONE_BUTTON = (By.XPATH, "//button[@data-testid='receiverFlow.connectionSuccessful.button.done']")


class TunesInstallerLocators(object):
    """
    A class containing the Installer
    element locators.
    """
    WELCOME_INSTALL = (By.NAME, "Welcome to Logi Tune installer")
    INSTALL = (By.NAME, "Install Logi Tune")
    CONFIRM = (By.NAME, "Confirm")
    WELCOME_LAUNCH = (By.NAME, "Welcome to Logi Tune")
    LAUNCH = (By.NAME, "Launch Logi Tune")
    ACCEPT_TERMS = (By.NAME, "I accept the terms of the License Agreement")

    CANCEL = (By.NAME, "Cancel")
    FINISH = (By.XPATH, "//Button[@ClassName ='Button'][@Name='Finish']")
    REBOOT_LATER = (By.NAME, "I want to manually reboot later")

    UNINSTALL_PROGRAM = (By.NAME, "Uninstall a program")
    UNINSTALL_SEARCH = (By.XPATH, "//*[@LocalizedControlType='edit']")  # Search Box
    LOGI_TUNE = (By.NAME, "Logi Tune")
    UNINSTALL_APP = (By.NAME, "Uninstall app")
    UNINSTALL_DONE = (By.NAME, "Done")
    UNINSTALL_REBOOT_LATER = (By.NAME, "Reboot later")


class TuneCoilyLocators:
    """
    A class containing locators for Logi Dock Flex features in Logi Tune
    """

    BRIGHTNESS_LABEL = (By.XPATH, "//span[@data-testid='undefined.title']")
    BRIGHTNESS_SLIDER = (By.XPATH, "//div[@data-testid='dashboard.device.coily.brightnessSlider']//input")
    BRIGHTNESS_SLIDER_SCROLL_AREA = (By.XPATH, "//div[@class='simplebar-content-wrapper']")

    PRIVACY_MODE_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.coily.privacyMode']//input[@data-testid='switchRow.checkbox']")
    PRIVACY_MODE_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.coily.privacyMode']//span[@data-testid='checkbox.thumb']")
    PRIVACY_MODE_TITLE = (By.XPATH, "//div[@data-testid='dashboard.coily.privacyMode']//span[@data-testid='switchRow.title']")

    TIME_FORMAT_CHECKBOX = (By.XPATH, "//div[@data-testid='dashboard.coily.timeFormat']//input[@data-testid='switchRow.checkbox']")
    TIME_FORMAT_TOGGLE = (By.XPATH, "//div[@data-testid='dashboard.coily.timeFormat']//span[@data-testid='checkbox.thumb']")
    TIME_FORMAT_TITLE = (By.XPATH, "//div[@data-testid='dashboard.coily.timeFormat']//p[@data-testid='switchRow.title']")

    LANGUAGE_BUTTON = (By.XPATH, "//div[@data-testid='dashboard.device.settings.voicePrompts.language']/p[@data-testid='dashboard.coily.language.select']")
    INVALID_AWAY_MESSAGE = (By.XPATH, "//div[text()='The away message format is invalid']") # ticket create

    #AWAY MESSAGE POPUP SCREEN
    AWAY_MESSAGE_RENAME = (By.XPATH, "//div/p[@data-testid='dashboard.coily.awayMessage.select']")
    AWAY_MESSAGE_MAIN_LABEL = (By.XPATH, "//p[@data-testid='dashboard.coily.awayMessage.title']")
    AWAY_MESSAGE_SUBMIT_BUTTON = (By.XPATH, "//div[@id='rename-popup']//button[@data-testid='dashboard.coily.awayMessage.form.save']")
    AWAY_MESSAGE_POPUP_TEXT_INPUT = (By.XPATH, "//div[@id='rename-popup']//input[@data-testid='dashboard.coily.awayMessage.form.inputMessage']")

    AWAY_MESSAGE_CLOSE_BUTTON = (By.XPATH, "//div[@data-testid='header.button.close']")
    AWAY_MESSAGE_SCROLL_AREA = (By.XPATH, "//div[@class='simplebar-content-wrapper']")
