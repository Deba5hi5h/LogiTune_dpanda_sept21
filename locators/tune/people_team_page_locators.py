from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import (xpath_by_data_testid, xpath_by_multiple_attributes,
                                         xpath_by_multiple_attributes_chained)


class TunePeopleTeamPageLocators:
    BACK_BUTTON = xpath_by_multiple_attributes(El.button, (Attr.data_testid, 'pageHeader'), (Attr.data_testid, 'back'), strict_check=False)
    EDIT_BUTTON = xpath_by_data_testid(El.p, 'people.teammateGroup.editLink')
    SEARCH_BAR = xpath_by_data_testid(El.input, 'people.teammates.search')
    SEARCH_BAR_DELETE_INPUT_BUTTON = xpath_by_multiple_attributes_chained((El.input, Attr.data_testid, 'people.everyone.userList.search'), (El.parent, None, None), (El.button, None, None))
    USER_BUTTON = xpath_by_data_testid(El.button, 'people.teammates', strict_check=False)
    USER_NAME_LABEL = xpath_by_multiple_attributes(El.p, (Attr.data_testid, 'people.teammates'), (Attr.data_testid, '.title'), strict_check=False)
    USER_BOOKINGS_LABEL = xpath_by_multiple_attributes(El.p, (Attr.data_testid, 'people.teammates'), (Attr.data_testid, 'subtitle'), strict_check=False)
    ADD_TEAMMATES_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.addTeammates')
