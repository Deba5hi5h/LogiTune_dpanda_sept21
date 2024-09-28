from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_class, xpath_by_multiple_attributes_chained
from locators.base.attributes import HtmlAttribute


class TunePeopleUserPageLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.back')
    REFRESH_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.refresh')
    USER_NAME_LABEL = xpath_by_data_testid(El.p, 'people.teammate.name')
    USER_EMAIL_LABEL = xpath_by_data_testid(El.p, 'people.teammate.email')
    USER_GROUPS_LABEL = xpath_by_data_testid(El.p, 'people.teammate.tenants', strict_check=False) #TODO: check if working
    USER_BUILDING_LABEL = xpath_by_data_testid(El.p, 'people.teammate.buildingName')
    MANAGE_TEAMS_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.manageTeams')
    MANAGE_TEAMS_BUTTON_PARAGRAPH = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, "people.teammate.manageTeams"),
        (El.p, None, None)
    )
    ADD_TO_TEAMMATES_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.addToTeammates')
    REMOVE_FROM_TEAMMATES_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.removeFromTeammates')
    POPUP_REMOVE_FROM_TEAMMATES_OK_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.removeTeammateDialog.remove')
    POPUP_REMOVE_FROM_TEAMMATES_CANCEL_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.removeTeammateDialog.cancel')
    RESERVATION_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.reservation', strict_check=False)
    RESERVATION_BUTTON_BY_ID = xpath_by_data_testid(El.button, 'people.teammate.reservation.XXX')
    RESERVATION_BUTTON_BY_ID_PARAGRAPH = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, "people.teammate.reservation.XXX"),
        (El.p, None, None)
    )
    NO_BOOKINGS_FOR_USER_LABEL = xpath_by_data_testid(El.p, 'people.teammate.bookings.noBookings')

    DASHBOARD_REFRESH_BUTTON = xpath_by_data_testid(El.any, 'people.teammate.refresh')
    DASHBOARD_ICON_LOADER = xpath_by_class(El.div, 'icon-loader-small')
