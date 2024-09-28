from locators.base.attributes import HtmlAttribute as Attr
from locators.base.elements import HtmlElement as El
from locators.locators_templates import (xpath_by_class, xpath_by_data_testid,
                                         xpath_by_multiple_attributes)


class TuneDeskBookingTimeSelectionPageLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.undefined.back')
    SINGLE_TAB_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.dateTimeSelect.tab.Single.label')
    MULTIPLE_TAB_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.dateTimeSelect.tab.Multiple.label')
    OPEN_CALENDAR_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.collapse.open')
    CLOSE_CALENDAR_BUTTON = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.collapse.close')
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date.XXX', El.div)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV_DIV = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date.XXX', El.div, El.div)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIVS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', El.div, strict_check=False)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_DIV_PARAGRAPHS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', El.div, El.p, El.parent, strict_check=False)
    CALENDAR_ELEMENT_BY_DAY_BUTTONS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', strict_check=False)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPH = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date.XXX', El.p)
    CALENDAR_ELEMENT_BY_DAY_BUTTON_PARAGRAPHS = xpath_by_data_testid(El.button, 'dashboard.home.dateRow.date', El.p, strict_check=False)
    # TODO: Remember about more 'g' elements (3 for now at the end)
    CALENDAR_LINES = xpath_by_multiple_attributes(El.any, (Attr.name, 'g'), (Attr.transform, None))
    TIME_DRAG_START_DIV = xpath_by_data_testid(El.any, 'start.drag')
    TIME_DRAG_END_DIV = xpath_by_data_testid(El.any, 'end.drag')
    TIME_RANGE_LABEL = xpath_by_data_testid(El.any, 'deskBooking.calendar.booking.label')
    TIME_RANGE_BOX = xpath_by_data_testid(El.any, 'deskBooking.calendar.booking.label', El.parent)
    SCROLL_VISIBLE_AREA = xpath_by_class(El.any, 'simplebar-content-wrapper')
    SCROLL_AREA = xpath_by_class(El.any, 'simplebar-content')
    CONFIRM_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.dateTimeSelect.confirm')
    UPDATE_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.editBooking.update')
    BOOKING_UPDATED_OK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.bookingUpdated.ok')
