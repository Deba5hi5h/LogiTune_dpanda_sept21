from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr

from locators.locators_templates import xpath_by_data_testid, xpath_by_text, xpath_by_multiple_attributes, xpath_by_class


class TuneHomePageLocators:
    DASHBOARD_TITLE_LABEL = xpath_by_data_testid(El.p, 'dashboard.title')
    DASHBOARD_REFRESH_BUTTON = xpath_by_data_testid(El.button, 'dashboard.agenda.refreshButton')
    DASHBOARD_NOTIFICATIONS_BUTTON = xpath_by_data_testid(El.button, 'path.alerts')
    DASHBOARD_PROFILE_BUTTON = xpath_by_data_testid(El.button, 'path.workAccountProfile.profile')
    DASHBOARD_HOME_TAB = xpath_by_data_testid(El.button, 'dashboard.tab-home')
    DASHBOARD_DEVICES_TAB = xpath_by_data_testid(El.button, 'dashboard.tab-myDevices')
    DASHBOARD_MAPS_TAB = xpath_by_data_testid(El.button, 'dashboard.tab-maps')
    DASHBOARD_PEOPLE_TAB = xpath_by_data_testid(El.button, 'dashboard.tab-people')
    DASHBOARD_ICON_LOADER = xpath_by_class(El.div, 'icon-loader-small')

    # HOME TAB
    HTML_MAIN_WINDOW = xpath_by_multiple_attributes(El.html, (Attr.data_theme, None))
    HOME_TAB_SIGN_IN_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.signInWorkAccount')
    HOME_TAB_BOOK_A_DESK_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.bookings.bookADesk')
    HOME_TAB_BOOK_A_DESK_POPUP_CLOSE_BUTTON = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskBooking.bookADesk.close')
    HOME_TAB_BOOK_A_DESK_BY_LOCATION_BUTTON = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskBooking.byLocation')
    HOME_TAB_BOOK_A_DESK_NEAR_TEAMMATE_BUTTON = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskBooking.nearTeammate')
    HOME_TAB_BOOK_A_DESK_DESK_SELECTION_PREFERENCES_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.preferences')
    HOME_TAB_OPEN_CALENDAR_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.collapse.open')
    HOME_TAB_CLOSE_CALENDAR_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.collapse.close')
    HOME_TAB_BOOKING_CARD = xpath_by_data_testid(El.div, 'dashboard.home.bookings.bookingCard', strict_check=False)
    HOME_TAB_DESK_BOOKING_DETAILS_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.bookings.bookingCard', strict_check=False)
    HOME_TAB_BOOKING_DETAILS_CLOSE_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.bookings.bookingDetails.close')
    HOME_TAB_BOOKING_DETAILS_SHOW_ON_MAPS_BUTTON = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskDetails.showOnMaps')
    HOME_TAB_BOOKING_DETAILS_NOTIFY_TEAMMATES_BUTTON = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskDetails.notifyTeammates')
    HOME_TAB_BOOKING_DETAILS_EDIT_BOOKING_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.bookings.bookingDetails.editBooking')
    HOME_TAB_BOOKING_DETAILS_END_BOOKING_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.bookings.bookingDetails.cancelSession')
    HOME_TAB_BOOKING_DETAILS_END_BOOKING_CONFIRM_YES = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskDetails.endBooking.end')
    HOME_TAB_BOOKING_DETAILS_END_BOOKING_CONFIRM_NO = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskDetails.endBooking.no')
    HOME_TAB_DESK_BOOKING_VALIDATION_ERROR_TITLE_LABEL = xpath_by_data_testid(El.p, 'deskBooking.bookingError.title')
    HOME_TAB_DESK_BOOKING_VALIDATION_ERROR_DESCRIPTION_LABEL = xpath_by_data_testid(El.p, 'deskBooking.bookingError.description')
    HOME_TAB_DESK_BOOKING_VALIDATION_ERROR_OK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.bookingError.ok')
    HOME_TAB_BOOKING_CANCELLED_OK_BUTTON = xpath_by_data_testid(El.button, 'dashboard.deskBooking.deskDetails.endBookingSuccess.ok')
    HOME_TAB_OCCUPANCY_LABEL = xpath_by_data_testid(El.p, 'dashboard.home.occupancyRow.occupancy.building')
    HOME_TAB_OCCUPANCY_TEAMMATES = xpath_by_data_testid(El.p, 'dashboard.home.occupancyRow.occupancy.names')
    HOME_MEETING_CARD_TITLE = xpath_by_data_testid(El.p, 'dashboard.agenda.meetingCard.large.title')
    HOME_MEETING_SMALL_TITLE = xpath_by_data_testid(El.p, 'dashboard.agenda.meetingCard.small.title')
    HOME_MEETING_INFO = xpath_by_data_testid(El.button, 'dashboard.agenda.infoTag.wrapper', El.p)
    HOME_MEETING_WRAPPER = xpath_by_data_testid(El.div, 'dashboard.agenda.meetingCard.wrapper')
    HOME_MEETING_MEETING_TIME = xpath_by_data_testid(El.div, 'dashboard.agenda.meetingCard.time')
    HOME_MEETING_NO_MEETINGS = xpath_by_data_testid(El.div, 'dashboard.agenda.noMeetingsWrapper')
    HOME_ALL_DAY_MEETINGS_EXPAND = xpath_by_data_testid(El.div, 'dashboard.agenda.dropdownNonAllDay')
    HOME_ALL_DAY_MEETINGS_COLLAPSE = xpath_by_data_testid(El.div, 'dashboard.agenda.dashboard.agenda.dropdownAllDay')





    # DEVICES TAB
    DEVICES_TAB_NOT_CONNECTED_LABEL = xpath_by_data_testid(El.p, 'dashboard.devices.supported.openDialog.noDeviceConnected')
    DEVICES_TAB_SUPPORTED_DEVICES_BUTTON = xpath_by_text(El.button, 'Supported devices')
    DEVICES_TAB_SUPPORTED_DEVICES_TITLE_LABEL = xpath_by_data_testid(El.p, 'dialog.title')
    # DEVICES_TAB_SUPPORTED_DEVICES_ITEM = (By.XPATH, "//xxx[@data-testid='xxx']")  # TODO: write locator
    DEVICES_TAB_SUPPORTED_DEVICES_OK_BUTTON = xpath_by_data_testid(El.button, 'dialog.supportedDevices.button.ok')
    # DEVICES_TAB_DEVICE_ITEM = xpath_by_multiple_attributes(El.div, (Attr.data_testid, 'dashboard.devices.device.deviceName'), (Attr.text, 'XXX'))
    DEVICES_TAB_DEVICE_ITEM = xpath_by_data_testid(El.div, 'dashboard.devices.device.contentWrapper')
    DEVICES_TAB_DEVICE_ITEM_CHECKBOX = xpath_by_data_testid(El.input, 'dashboard.devices.device.statusIcon.checkbox')
    DEVICES_TAB_DEVICE_ITEM_SWITCH = xpath_by_data_testid(El.any, 'checkbox.bg')

    # CALENDAR
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date.XXX', 'div')
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV_DIV = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date.XXX', 'div', index=2)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIVS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', 'div', strict_check=False)
    CALENDAR_ELEMENT_BY_DAY_BUTTONS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', strict_check=False)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPH = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date.XXX', 'p')
    CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPHS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', 'p', strict_check=False)

    # SETTINGS
    HOME_MORE_OPTIONS_BUTTON = xpath_by_data_testid(El.div, 'header.settings.button')
    HOME_SETTINGS_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.close')
    ABOUT_SETTINGS_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.about')
    HOME_QUIT_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.quit')

    #POPUPS
    UPDATE_SUCCESS = xpath_by_data_testid(El.button, 'autoupdate.appUpdatedPopup.button.ok')


