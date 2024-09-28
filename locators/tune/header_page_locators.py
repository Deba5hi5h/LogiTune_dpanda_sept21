from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid


class TuneHeaderLocators:
    MINIMIZE_BUTTON = xpath_by_data_testid(El.div, 'header.minimize')
    CLOSE_BUTTON = xpath_by_data_testid(El.div, 'header.close')
    SETTINGS_BUTTON = xpath_by_data_testid(El.div, 'header.settings.button')
    SETTINGS_POPUP_SETTINGS_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.close')
    SETTINGS_POPUP_SHARE_FEEDBACK_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.shareFeedback')
    SETTINGS_POPUP_SUPPORT_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.support')
    SETTINGS_POPUP_ABOUT_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.about')
    SETTINGS_POPUP_QUIT_BUTTON = xpath_by_data_testid(El.li, 'header.menu.item.quit')
