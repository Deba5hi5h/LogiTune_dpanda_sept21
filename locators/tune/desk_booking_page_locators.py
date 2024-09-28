from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, path_by_tag_name


class TuneDeskBookingPageLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Book a desk.back')
    DATE_SELECT_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.dateSelect.open')
    DATE_SELECT_OPTION_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.dateSelect.option', strict_check=False)
    TIME_START_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.timeSelect.start')
    TIME_START_OPTION_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.timeSelect.option.start', strict_check=False)
    TIME_END_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.timeSelect.end')
    TIME_END_OPTION_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.timeSelect.option.end', strict_check=False)
    OFFICE_LOCATION_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.building')
    FLOOR_LOCATION_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.floor')
    COLLAPSABLE_DESKS_LIST = xpath_by_data_testid(El.p, 'deskBooking.deskSelection.desks.collapsableList.XXX', strict_check=False)
    COLLAPSED_DESK_CHECKBOX = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.desks.collapsableList', strict_check=False)
    DETAILS_BUTTON = xpath_by_data_testid(El.p, 'deskBooking.deskSelection.deskDetails')
    DETAILS_BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Desk details.back')
    DETAILS_AVAILABLE_BETWEEN = xpath_by_data_testid(El.p, 'deskBooking.deskSelection.desksDetails.available')
    BOOK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskSelection.book')
    SELECTED_DESK_NAME = xpath_by_data_testid(El.p, 'deskBooking.deskSelection.selected.name')
    POPUP_VALIDATION_ERROR_TITLE_LABEL = xpath_by_data_testid(El.p, 'deskBooking.bookingError.title')
    POPUP_VALIDATION_ERROR_DESCRIPTION_LABEL = xpath_by_data_testid(El.p, 'deskBooking.bookingError.description')
    POPUP_VALIDATION_ERROR_OK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.bookingError.ok')
    NO_DESKS_AVAILABLE_LABEL = xpath_by_data_testid(El.p, "deskBooking.deskSelection.noDesksAvailable")
    NO_DESK_AVAILABLE_POPUP_MSG = xpath_by_data_testid(El.p, "deskBooking.noDesksAvailablePopup.title")
    NO_DESK_AVAILABLE_POPUP_BUTTON = xpath_by_data_testid(El.button, "deskBooking.noDesksAvailablePopup.ok")
    FLOOR_SELECT_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.floorSelection.floor', strict_check=False)

    # Multiple booking confirm popup
    MULTIPLE_BOOKING_CONFIRM_POPUP_TITLE = xpath_by_data_testid(El.p, "deskBooking.multiBookingConfirm.title")
    MULTIPLE_BOOKING_CONFIRM_POPUP_CONFIRM_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.multiBookingConfirm.confirmDays')
    MULTIPLE_BOOKING_CONFIRM_POPUP_CANCEL_BUTTON = xpath_by_data_testid(El.button, "deskBooking.multiBookingConfirm.backToBooking")

    # Map
    AREA_BUTTON = path_by_tag_name('button')
    MAP_CANVAS = path_by_tag_name('canvas')
    SELECTED_DESK_POPUP_NAME = xpath_by_data_testid(El.p, 'deskBooking.deskDetails.name')
    BOOK_A_DESK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskDetails.action')
