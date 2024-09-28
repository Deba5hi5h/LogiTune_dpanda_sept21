from selenium.webdriver.common.by import By

class TuneMobilePersonalEqLocators(object):
    """
    A class containing the Tune Mobile App Personal EQ Screen element locators.
    """
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='gen-arrow-left']"),
            (By.XPATH, "//*[@content-desc='Back']")]
    START = [(By.ID, "start_button"),
             (By.XPATH, "//android.widget.TextView[@text=('Start', 'Iniciar', 'Inizia', 'Iniciar', 'Start', 'Démarrage')]")]
    NEXT_STEP = [(By.ID, "cancel_button"),
                 (By.XPATH, "//android.widget.TextView[@text=('Next step', 'Siguiente paso', 'Passaggio successivo', 'Próxima etapa', 'Nächster Schritt', 'Étape suivante')]")]
    SAVE = [(),
            (By.XPATH, "//android.widget.TextView[@text=('Save', '', '', '', '', '')]")]
    DONE = [(),
            (By.XPATH, "//android.widget.TextView[@text=('Done', '', '', '', '', '')]")]