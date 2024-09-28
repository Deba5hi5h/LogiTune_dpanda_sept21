from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes


class TuneBasecampPageLocators:
    CHOOSE_BASECAMP_TITLE_LABEL = xpath_by_data_testid(El.p, 'pageHeader.Choose your basecamp.title')
    CHANGE_BASECAMP_TITLE_LABEL = xpath_by_data_testid(El.p, 'pageHeader.Change basecamp.title')
    SEARCH_INPUT = xpath_by_data_testid(El.input, 'basecampSelection.search')
    LOCATION_TOGGLE = xpath_by_multiple_attributes(El.button, (Attr.data_testid, 'basecampSelection.collapsableList'), (Attr.data_testid, 'toggle'), strict_check=False)
    LOCATION_ITEM = xpath_by_multiple_attributes(El.button, (Attr.data_testid, 'basecampSelection.collapsableList'), (Attr.data_testid, 'item'), strict_check=False)
    # LOCATION_TITLE = xpath_by_multiple_attributes(El.button, (Attr.data_testid, 'basecampSelection.collapsableList'), (Attr.data_testid, 'title'), strict_check=False)
