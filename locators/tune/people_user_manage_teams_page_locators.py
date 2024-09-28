from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import (xpath_by_class, xpath_by_data_testid, xpath_by_multiple_attributes_chained,
                                         path_by_tag_name, xpath_by_multiple_attributes)


class TunePeopleUserManageTeamsPageLocators:
    DONE_BUTTON = xpath_by_data_testid(El.p, 'people.teammate.addToGroupDialog.close')
    TEAM_DIV = xpath_by_data_testid(El.div, 'people.teammate.addToGroupDialog.teammateGroup', strict_check=False)
    TEAM_ACTION_BUTTON = xpath_by_multiple_attributes_chained(
        (El.div, Attr.data_testid, 'people.teammate.addToGroupDialog.teammateGroup'),
        (El.button, None, None), strict_check=False)
    TEAM_ACTION_BUTTON_RELATIVE = path_by_tag_name('button')
    NEW_TEAM_BUTTON = xpath_by_data_testid(El.button, 'people.teammate.addToGroupDialog.newTeam')
    POPUP_NEW_TEAM_CLOSE_BUTTON = xpath_by_data_testid(El.button, 'people.createNewTeam.close')
    POPUP_NEW_TEAM_INPUT = xpath_by_class(El.input, 'input-icon-text')
    POPUP_NEW_TEAM_CREATE_BUTTON = xpath_by_data_testid(El.button, 'people.createNewTeam.create')

