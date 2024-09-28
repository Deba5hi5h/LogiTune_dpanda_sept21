from selenium.webdriver.common.by import By

class TuneMobileHeadsetLanguageLocators(object):
    """
    A class containing the Tune Mobile App Sleep Settings Screen element locators.
    """
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' "
                       "or @name='Zurück' or @name='Indietro' or @name='Voltar']"),
            (By.XPATH, "//*[@content-desc='Back']")]
    CANCEL = [(),
              (By.XPATH, "//android.widget.Button")]



