from apps.local_network_access.lna_home import LNAHome
from base.base_ui import UIBase
from extentreport.report import Report
from locators.local_network_access.lna_home_locators import LNAHomeLocators
from locators.local_network_access.lna_login_locators import LNALoginLocators


class LNALogin(UIBase):
    """
    LNA Login page methods
    """

    def login(self, user_name: str, password: str) -> LNAHome:
        """
        Method to log in to Local Network Access

        :param password:
        :param user_name:

        :return: LNAHome
        """
        try:
            if self.verify_element(LNALoginLocators.SECURITY_ADVANCED, timeunit=2):
                self.look_element(LNALoginLocators.SECURITY_ADVANCED).click()
                self.look_element(LNALoginLocators.SECURITY_PROCEED).click()
            self.look_element(LNALoginLocators.USER_NAME).send_keys(user_name)
            self.look_element(LNALoginLocators.PASSWORD).send_keys(password)
            self.look_element(LNALoginLocators.LOGIN).click()
            self.verify_element(LNAHomeLocators.LOCAL_NETWORK_LABEL, timeunit=10)
            return LNAHome()
        except Exception as e:
            Report.logException(str(e))
            raise e
