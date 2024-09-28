from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes
from locators.base.attributes import HtmlAttribute


class AboutPageLocators:
    CLOSE_BUTTON = xpath_by_data_testid(El.svg, 'screen.button.close')
    UPDATE_APP_BUTTON = xpath_by_data_testid(El.button, 'aboutapp.button.updateApp')
    TUNE_VERSION_LABEL = xpath_by_data_testid(El.p, 'aboutapp.title')
