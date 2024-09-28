from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes_chained, xpath_by_class
from locators.base.attributes import HtmlAttribute


class TuneProfileLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'profile.back')
    PROFILE_NAME = xpath_by_data_testid(El.p, "profile.name")
    PROFILE_BASECAMP_NAME = xpath_by_data_testid(El.p, "profile.basecamp.name")

    KEEP_BOOKINGS_HIDDEN_LABEL = xpath_by_data_testid(El.button, "profile.actions.keepBookingsPrivate")
    KEEP_BOOKINGS_HIDDEN_CHECKBOX = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, "profile.actions.keepBookingsPrivate"),
        (El.input, None, None)
    )
    KEEP_BOOKINGS_HIDDEN_TOGGLE = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, "profile.actions.keepBookingsPrivate"),
        (El.any, HtmlAttribute.data_testid, 'checkbox.thumb')
    )

    PROFILE_CALENDAR_SETTINGS = xpath_by_data_testid(El.button, "profile.actions.calendarSettings")
    PROFILE_NOTIFICATION_SETTINGS = xpath_by_data_testid(El.button, "profile.actions.notifications")
    PROFILE_CONNECTED_ACCOUNT_SETTINGS = xpath_by_data_testid(El.button, "profile.actions.workAccount")
    PROFILE_PRIVACY_SETTINGS = xpath_by_data_testid(El.button, "profile.actions.privacyAndUsage")

    BUTTON_LOADER = xpath_by_class(El.div, 'icon-loader-small')
