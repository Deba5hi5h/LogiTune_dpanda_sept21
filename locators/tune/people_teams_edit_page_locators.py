from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes_chained


class TunePeopleTeamsEditPageLocators:
    DONE_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.done')
    TEAM_DIV = xpath_by_data_testid(El.div, 'people.teammates', strict_check=False)
    DRAG_TEAM_DIV = xpath_by_multiple_attributes_chained((El.div, Attr.draggable, 'true')) # TODO: add when locator ready
    DELETE_TEAM_BUTTON = xpath_by_multiple_attributes_chained((El.div, Attr.data_testid, 'people.teammates'), (El.button, None, None), strict_check=False) # TODO: add when locator ready
    POPUP_DELETE_TEAM_OK_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.deletePopup.delete')
    POPUP_DELETE_TEAM_CANCEL_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.deletePopup.cancel')

