from selenium.webdriver.common.by import By

class TuneMobileANCLocators(object):
    """
    A class containing the Tune Mobile App ANC button options Screen element locators.
    """
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' or @name='Zurück' or @name='Indietro' or @name='Voltar' or @name='Opções do botão ANC' or @name='Opciones de botón ANC' or @name='ANC button options' or @name='Options du bouton de suppression active du bruit' or @name='Opzioni pulsante ANC' or @name='ANC-Tastenoptionen']"),
            (By.XPATH, "//*[@content-desc='Back']")]
    SHORT_PRESS = [(By.ID, "short_press_label"),
                   (By.XPATH, "//*[@content-desc=('Short Press navigate','Pulsación corta navigate','Pressione breve navigate','Kurzer Tastendruck navigate','Pressione brevemente navigate','Pression brève navigate')]")]

