from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes_chained, xpath_by_class


class TunePeoplePageLocators:
    TEAMMATES_TAB_BUTTON = xpath_by_data_testid(El.button, 'people.tab.TEAMMATES.label')
    EVERYONE_TAB_BUTTON = xpath_by_data_testid(El.button, 'people.tab.EVERYONE.label')

    #TEAMMATES TAB:
    USERS_TEAM_BUTTON = xpath_by_data_testid(El.button, 'people.teammates.allTeammates')
    USERS_TEAM_PARAGRAPH = xpath_by_multiple_attributes_chained((El.button, Attr.data_testid,
                                                                 'people.teammates.allTeammates'), (El.p, None, None))
    NEW_TEAM_BUTTON = xpath_by_data_testid(El.button, 'people.teammates.newTeam')
    EDIT_TEAMS_BUTTON = xpath_by_data_testid(El.button, 'people.teammates.editTeams')

    #EVERYONE TAB:
    EVERYONE_SEARCH_BAR = xpath_by_data_testid(El.input, 'people.everyone.userList.search')
    EVERYONE_SEARCH_BAR_DELETE_INPUT_BUTTON = xpath_by_multiple_attributes_chained((El.input, Attr.data_testid, 'people.everyone.userList.search'), (El.parent, None, None), (El.button, None, None))
    EVERYONE_USER_BUTTON = xpath_by_data_testid(El.button, 'undefined.userList.user', strict_check=False)
    NO_USERS_FOUND_LABEL = xpath_by_data_testid(El.p, 'people.everyone.noUsersFound')

    #REFRESH
    DASHBOARD_REFRESH_BUTTON = xpath_by_data_testid(El.button, 'dashboard.agenda.refreshButton')
    DASHBOARD_ICON_LOADER = xpath_by_class(El.div, 'icon-loader-small')

    #CREATE TEAM POPUP
    POPUP_NEW_TEAM_CLOSE_BUTTON = xpath_by_data_testid(El.div, 'people.createNewTeam.close')
    POPUP_NEW_TEAM_INPUT = xpath_by_class(El.input, 'input-icon-text')
    POPUP_NEW_TEAM_CREATE_BUTTON = xpath_by_data_testid(El.button, 'people.createNewTeam.create')


