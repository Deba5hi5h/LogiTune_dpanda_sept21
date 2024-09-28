from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid


class TuneConnectedAccountSettingsLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Connected account.back')
    DISCONNECT_BUTTON = xpath_by_data_testid(El.button, 'profile.workAccount.disconnect')
    DISCONNECT_ACCOUNT_POPUP_DISCONNECT_BUTTON = xpath_by_data_testid(El.button, 'appSettings.connectedAccount.disconnectDialog.disconnect')
    DISCONNECT_ACCOUNT_POPUP_CANCEL_BUTTON = xpath_by_data_testid(El.button, 'appSettings.connectedAccount.disconnectDialog.cancel')
