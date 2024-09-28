from selenium.webdriver.common.by import By

class TuneMobileButtonFunctionsLocators(object):
    """
    A class containing the Tune Mobile App Sleep Settings Screen element locators.
    """
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' or @name='Zurück' or @name='Indietro' or @name='Voltar']"),
            (By.XPATH, "//*[@content-desc='Back']")]
    LEFT_EAR_BUD = [(By.ID, "tab0"),
                    (By.XPATH, "//*[@content-desc=('LEFT EARBUD label','ÉCOUTEUR GAUCHE label','LINKER EARBUD label','AURICULAR IZQUIERDO label','AURICOLARE SINISTRO label','FONE DE OUVIDO ESQUERDO label')]")]
    RIGHT_EAR_BUD = [(By.ID, "tab1"),
                     (By.XPATH, "//*[@content-desc=('RIGHT EARBUD label','ÉCOUTEUR DROITE label','RECHTER EARBUD label','AURICULAR DERECHO label','AURICOLARE DESTRO label','FONE DE OUVIDO DIREITO label')]")]
    SHORT_PRESS = [(By.ID, "action_single_press"),
                   (By.XPATH, "//*[@content-desc=('Short Press Row','Pression brève Row','Kurzer Tastendruck Row','Pulsación corta Row','Pressione breve Row','Pressione brevemente Row')]")]
    LONG_PRESS = [(By.ID, "action_long_press"),
                  (By.XPATH, "//*[@content-desc=('Long Press Row','Pression longue Row','Langer Tastendruck Row','Pulsación larga Row','Pressione prolungata Row','Pressionamento longo Row')]")]
    DOUBLE_TAP = [(By.ID, "action_double_tap"),
                  (By.XPATH, "//*[@content-desc=('Double Tap Row','Double tapotement Row','Doppeltippen Row','Doble toque Row','Doppio tocco Row','Toque duplo Row')]")]
    CLOSE = [(By.ID, "close-bottom-sheet"),
             (By.XPATH, "//*[contains(@content-desc, 'Close') and contains(@content-desc, 'BottomSheet')]")]


