from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid


class TuneDeskSuccessfullyTransferredPageLocators:
    TIME_LABEL = xpath_by_data_testid(El.p, 'viewBooking.bookingTransferred.time')
    DONE_BUTTON = xpath_by_data_testid(El.button, 'viewBooking.bookingTransferred.done')
