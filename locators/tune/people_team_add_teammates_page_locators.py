from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes_chained, xpath_by_class


class TunePeopleTeamAddTeammatesPageLocators:
    CLOSE_BUTTON = xpath_by_multiple_attributes_chained((El.any, Attr.id, 'close-mask-2'), (El.parent, None, None))
    SEARCH_BAR = xpath_by_data_testid(El.input, 'people.teammates.addToTeammateGroup.userList.search')
    SEARCH_BAR_DELETE_INPUT_BUTTON = xpath_by_multiple_attributes_chained((El.input, Attr.data_testid, 'people.teammates.addToTeammateGroup.userList.search'), (El.parent, None, None), (El.svg, Attr.class_, 'icon-clear'))
    USER_BUTTON = xpath_by_data_testid(El.button, 'undefined.userList.user', strict_check=False)
    ICON_LOADER = xpath_by_class(El.div, 'icon-loader-small')

