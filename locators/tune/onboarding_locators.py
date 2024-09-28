from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes


class TuneOnboardingPageLocators:
    WELCOME_TITLE = xpath_by_data_testid(El.p, 'workAccountOnboarding.welcome.title')
    WELCOME_DESCRIPTION = xpath_by_data_testid(El.p, 'workAccountOnboarding.welcome.description')
    CONTINUE_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.welcome.continue')

    TEAMMATES_SKIP_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.teammates.skip')
    TEAMMATES_TITLE = xpath_by_data_testid(El.p, 'workAccountOnboarding.teammates.title')
    TEAMMATES_DESCRIPTION = xpath_by_data_testid(El.p, 'workAccountOnboarding.teammates.description')
    TEAMMATES_CONTINUE_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.teammates.continue')
    ADD_TEAMMATES_BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Add teammates.back')
    ADD_TEAMMATES_TITLE = xpath_by_data_testid(El.p, 'pageHeader.Add teammates.title')
    ADD_TEAMMATES_SEARCH_INPUT = xpath_by_data_testid(El.input, 'workAccountOnboarding.addTeammates.userList.search')
    # ADD_TEAMMATES_USERS_TOGGLE = (By.XPATH, "//button[contains(@data-testid, 'workAccountOnboarding.addTeammates.collapsableList') and contains(@data-testid, 'toggle')]")
    ADD_TEAMMATES_USERS_TOGGLE = xpath_by_multiple_attributes(El.button, (Attr.data_testid, 'workAccountOnboarding.addTeammates.collapsableList'), (Attr.data_testid, 'toggle'), strict_check=False)
    # ADD_TEAMMATES_ADD = (By.XPATH, "//button[@data-testid='xxx']")  # TODO: locators are different for different search methods/user groups
    ADD_TEAMMATES_WITHOUT_GROUP = xpath_by_data_testid(El.button, 'false.userList.user', strict_check=False)  # TODO: locator when searchbar has any input or no group of users
    # ADD_TEAMMATES_WITHOUT_GROUP_TITLE = (By.XPATH, "//p[contains(@data-testid, 'false.userList.user') and contains(@data-testid, 'title')]")  # TODO: locator when searchbar has any input or no group of users
    ADD_TEAMMATES_WITHOUT_GROUP_TITLE = xpath_by_multiple_attributes(El.p, (Attr.data_testid, 'false.userList.user'), (Attr.data_testid, 'title'), strict_check=False)  # TODO: locator when searchbar has any input or no group of users
    ADD_TEAMMATES_FROM_GROUP = xpath_by_data_testid(El.button, 'workAccountOnboarding.addTeammates', strict_check=False)  # TODO: locator when group of users are present
    # ADD_TEAMMATES_FROM_GROUP_TITLE = (By.XPATH, "//p[contains(@data-testid, 'workAccountOnboarding.addTeammates') and contains(@data-testid, 'title')]")  # TODO: locator when group of users are present
    ADD_TEAMMATES_FROM_GROUP_TITLE = xpath_by_multiple_attributes(El.p, (Attr.data_testid, 'workAccountOnboarding.addTeammates'), (Attr.data_testid, 'title'), strict_check=False)  # TODO: locator when group of users are present
    ADD_TEAMMATES_DONE_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.addTeammates.done')
