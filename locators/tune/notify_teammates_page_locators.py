from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import (xpath_by_data_testid, xpath_by_multiple_attributes,
                                         xpath_by_multiple_attributes_chained)


class TuneNotifyTeammatesPageLocators:
    SKIP_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.skip')
    NOTIFY_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.notify')
    CANCEL_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.cancelBooking')
    CANCEL_YES_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.cancelBooking.yesCancel')
    CANCEL_NO_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.cancelBooking.noKeep')
    CLEAR_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.clear')
    SELECTION = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.teammates', strict_check=False)
    SELECTION_NAME = xpath_by_multiple_attributes(El.p, (Attr.data_testid, 'deskBooking.notifyTeammates.teammates'), (Attr.data_testid, 'title'), strict_check=False)
    # SELECTION_NAME = (By.XPATH, "//p[contains(@data-testid, 'deskBooking.notifyTeammates.teammates') and contains(@data-testid, 'title')]")
    OPTIONAL_MESSAGE_TEXT_AREA = xpath_by_data_testid(El.textarea, 'deskBooking.notifyTeammates.messageBox')
    TEAM_CARD = xpath_by_data_testid(El.div, 'deskBooking.notifyTeammates.teammateGroup', strict_check=False)
    TEAM_CARD_BUTTON = 'xpath', './/button'
    TEAM_CLOSE_BUTTON = xpath_by_multiple_attributes_chained((El.button, None, None),
                                                             (El.defs, None, None), (El.parent, None, None))
    NOTIFY_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.notifyTeammates.notify')
