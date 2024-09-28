from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid


class TuneDeskSuccessfullyBookedPageLocators:
    TIME_LABEL = xpath_by_data_testid(El.p, 'deskBooking.deskBooked.time')
    DONE_BUTTON = xpath_by_data_testid(El.button, 'deskBooking.deskBooked.done')
