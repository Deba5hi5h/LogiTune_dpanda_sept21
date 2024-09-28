from selenium.webdriver.common.by import By

class TuneMobileHealthAndSafetyLocators(object):
    """
    A class containing the Tune Mobile App Health and Safety Screen element locators.
    """
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' or @name='Zurück' or @name='Indietro' or @name='Voltar']"),
            (By.XPATH, "//*[@content-desc='Back']")]
