from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, path_by_tag_name


class TuneMapPageLocators:
    BUILDING_BUTTON = xpath_by_data_testid(El.button, 'maps.buildingName')
    FLOOR_BUTTON = xpath_by_data_testid(El.button, 'maps.floorName')
    FLOOR_LIST_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.floorSelection.', strict_check=False)
    AREA_BUTTON = path_by_tag_name('button')
    MAP_CANVAS = path_by_tag_name('canvas')
    SELECTED_DESK_POPUP_NAME = xpath_by_data_testid(El.p, 'deskBooking.deskDetails.name')
    BOOK_A_DESK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskDetails.action')





