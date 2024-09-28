from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_class, xpath_by_text


class TuneNotificationsPageLocators:
    BACK_TO_DASHBOARD_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Notifications.back')
    CLEAR_ALERTS_BUTTON = xpath_by_data_testid(El.button, 'alerts.clear')
    CLEAR_ALERTS_BUTTON_CONFIRM = xpath_by_data_testid(El.button, 'alerts.clearAll.clearAll')
    CLEAR_ALERTS_BUTTON_CANCEL = xpath_by_data_testid(El.button, 'alerts.clearAll.cancel')
    NOTIFICATION_CARD = xpath_by_data_testid(El.div, 'notifications', strict_check=False)
    NOTIFICATIONS_LOADER = xpath_by_class(El.div, 'icon-loader-small')
    NO_NOTIFICATIONS_LABEL = xpath_by_text(El.any, 'No notifications', strict_check=False)
    NOTIFICATIONS_PAGE_HEADER = xpath_by_data_testid(El.p, 'pageHeader.Notifications.title')
