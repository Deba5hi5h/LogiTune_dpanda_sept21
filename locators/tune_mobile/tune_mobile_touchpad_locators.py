from selenium.webdriver.common.by import By

class TuneMobileTouchPadLocators(object):
    """
    A class containing the Tune Mobile App On-head detection Screen element locators.
    """
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' or @name='Zurück' or @name='Indietro' or @name='Voltar' or @name='Opções do botão ANC' or @name='Opciones de botón ANC' or @name='ANC button options' or @name='Options du bouton de suppression active du bruit' or @name='Opzioni pulsante ANC' or @name='ANC-Tastenoptionen']"),
            (By.XPATH, "//*[@content-desc='Back']")]
