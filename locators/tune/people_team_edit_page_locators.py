from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_class, xpath_by_data_testid, xpath_by_multiple_attributes_chained
from locators.base.attributes import HtmlAttribute


class TunePeopleTeamEditPageLocators:
    EDIT_NAME_BUTTON = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, 'people.teammateGroup.edit.edit'), (El.button, None, None))
    POPUP_EDIT_NAME_INPUT = xpath_by_class(El.input, 'input-text')
    POPUP_EDIT_NAME_CLOSE_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.popup.close')
    POPUP_EDIT_NAME_UPDATE_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.popup.update')
    DONE_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.done')
    DELETE_USER_BUTTON = xpath_by_multiple_attributes_chained(
        (El.button, HtmlAttribute.data_testid, 'people.teammateGroup.edit'),
        (El.button, None, None),  strict_check=False)
    DELETE_TEAM_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.delete')
    POPUP_DELETE_TEAM_DELETE_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.deletePopup.delete')
    POPUP_DELETE_TEAM_CANCEL_BUTTON = xpath_by_data_testid(El.button, 'people.teammateGroup.edit.deletePopup.cancel')
