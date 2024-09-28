from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, path_by_tag_name


class TuneDeskOnMapLocators:
    AREA_BUTTON = path_by_tag_name('button')
    MAP_CANVAS = path_by_tag_name('canvas')
    SELECTED_DESK_POPUP_NAME = xpath_by_data_testid(El.p, 'deskBooking.deskDetails.name')
    TRANSFER_A_DESK_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.viewDeskBooking.transfer')
    TRANSFER_DESK_POPUP_DESCRIPTION = xpath_by_data_testid(El.p, 'viewBooking.transferPopup.description')
    TRANSFER_DESK_POPUP_CANCEL = xpath_by_data_testid(El.button, 'deskBooking.viewDeskBooking.cancel')
    TRANSFER_DESK_POPUP_CONFIRM = xpath_by_data_testid(El.button, 'deskBooking.viewDeskBooking.transfer')




