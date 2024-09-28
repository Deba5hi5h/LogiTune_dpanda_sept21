from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid


class TuneSignInLocators:
    BACK_BUTTON = xpath_by_data_testid(El.button, 'pageHeader.Sign in.back')
    PRIVACY_POLICY_AGREEMENT_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.agreement.click', 'div[2]')
    GOOGLE_ACCOUNT_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.provider.google')
    OUTLOOK_ACCOUNT_BUTTON = xpath_by_data_testid(El.button, 'workAccountOnboarding.provider.outlook')
