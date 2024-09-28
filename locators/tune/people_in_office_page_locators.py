from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_class, xpath_by_multiple_attributes_chained
from locators.base.attributes import HtmlAttribute


class TunePeopleInOfficePageLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, '.back', strict_check=False)
    TEAMMATES_BUTTON = xpath_by_data_testid(El.button, 'peopleOccupancy.tab.TEAMMATES.label')
    EVERYONE_BUTTON = xpath_by_data_testid(El.button, 'peopleOccupancy.tab.EVERYONE.label')
    NO_TEAMMATES_LABEL = xpath_by_data_testid(El.p, 'peopleOccupancy.teammates.noTeammates')
    TEAMMATE_USER_BUTTON = xpath_by_data_testid(El.button, 'peopleOccupancy.teammates.', strict_check=False)
    EVERYONE_USER_BUTTON = xpath_by_data_testid(El.button, 'undefined.userList.user.', strict_check=False)
    EVERYONE_INPUT_SEARCH = xpath_by_data_testid(El.input, 'peopleOccupancy.everyone.userList.search')

    RESERVATION_BUTTON_BY_ID_PARAGRAPH_EVERYONE = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, "undefined.userList.user.XXX"),
        (El.p, None, None)
    )

    RESERVATION_BUTTON_BY_ID_PARAGRAPH_TEAMMATES = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, "peopleOccupancy.teammates.XXX"),
        (El.p, None, None)
    )
