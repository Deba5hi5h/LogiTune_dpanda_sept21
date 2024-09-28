from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid


class TuneNotificationsSettingsLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Notifications.back')
    MEETING_NOTIFICATION_SWITCH = xpath_by_data_testid(El.button, 'appSettings.notificationSettings.notification.checkbox')
    MEETING_DISMISS_AFTER_BUTTON = xpath_by_data_testid(El.p, 'appSettings.notificationSettings.dismissBtn')
    DISMISS_AFTER_POPUP_CLOSE_BUTTON = xpath_by_data_testid(El.svg, 'dialog.button.close')
    DISMISS_AFTER_POPUP_CHOICE_RADIOBUTTON = xpath_by_data_testid(El.div, 'autoDismissNotificationDialog', strict_check=False)
    DISMISS_AFTER_POPUP_SAVE_BUTTON = xpath_by_data_testid(El.button, 'autoDismissNotificationDialog.button.save')
    MEETING_REMINDER_BUTTON = xpath_by_data_testid(El.p, 'appSettings.notificationSettings.reminderBtn')
    REMINDER_POPUP_CLOSE_BUTTON = xpath_by_data_testid(El.svg, 'dialog.button.close')
    REMINDER_POPUP_CHOICE_RADIOBUTTON = xpath_by_data_testid(El.div, 'notifyAboutMeetingDialog', strict_check=False)
    REMINDER_POPUP_SAVE_BUTTON = xpath_by_data_testid(El.button, 'notifyAboutMeetingDialog.button.save')
    APP_UPDATES_SWITCH = xpath_by_data_testid(El.button, 'appSettings.notificationSettings.appUpdates.checkbox')
    FIRMWARE_UPDATES_SWITCH = xpath_by_data_testid(El.button, 'appSettings.notificationSettings.firmware.checkbox')
    LOW_BATTERY_SWITCH = xpath_by_data_testid(El.button, 'appSettings.notificationSettings.lowBattery.checkbox')
