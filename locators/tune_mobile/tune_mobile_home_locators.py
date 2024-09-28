from selenium.webdriver.common.by import By

class TuneMobileHomeLocators(object):
    """
    A class containing the Tune Mobile App Home Screen element locators.
    """
    HEADSET_ICON = [(),
                (By.XPATH, "//android.widget.ImageView[@content-desc='Headset icon']")]
    GRANT_PERMISSION = [(By.XPATH, "//*[@text='Grant permission']"),
                        (By.XPATH, "//*[@text='Grant permission' or contains(@text,'erteilen') or contains(@text,'autorisation') or contains(@text,'Conceder') or contains(@text,'Concedi')]/following-sibling::android.widget.Button")]
    ALLOW = [(),
             (By.XPATH, "//android.widget.Button[@text='Allow' or @text='Permitir' or @text='Autoriser' or @text='Zulassen' or @text='Consenti']")]
    EQUALIZER = [(By.ID, "equalizer_name_text"),
                 (By.XPATH, "//*[@content-desc=('Equalizer value','Ecualizador value','Égaliseur value','Equalizador value','Equalizzatore value')]")]
    PERSONAL_EQ_TOGGLE = [(By.XPATH, "//XCUIElementTypeSwitch[@name='PEQ-button_ option_label']/XCUIElementTypeSwitch"),
                          (By.XPATH, "//*[@content-desc=('Personal EQ switch','EQ personal switch','EQ personale switch','EQ pessoal switch','Persönlicher EQ switch','Égaliseur personnel switch')]")]
    DEVICE_NAME = [(By.ID, "device_name_label"),
                   (By.XPATH, "//*[@content-desc='Device name label']")]
    DEVICE_NAME_VALUE = [(By.ID, "device_name_text"),
                         (By.XPATH, "//*[@content-desc=('Device name value','Nombre del dispositivo value','Nome do dispositivo value','Nome dispositivo value','Nom du dispositif value','Gerätename value')]")]
    BUTTON_FUNCTIONS = [(By.ID, "button_functions_label"),
                        (By.XPATH, "//*[@content-desc=('Button functions navigate','Fonctions du bouton navigate','Tastenfunktionen navigate','Funciones de botones navigate','Funzioni pulsanti navigate','Funções do botão navigate')]")]
    CONNECTED_DEVICES = [(By.ID, "connected_devices_label"),
                         (By.XPATH, "//*[@content-desc=('Connected devices navigate','Dispositifs connectés navigate','Verbundene Geräte navigate','Dispositivos conectados navigate','Periferiche collegate navigate','Dispositivos conectados navigate')]")]
    SLEEP_SETTINGS = [(By.ID, "sleep_settings_text"),
                      (By.XPATH, "//*[@content-desc=('Sleep Settings value','Paramètres de veille value','Schlafmodus-Einstellungen value','Ajustes de suspensión value','Impostazioni di sospensione value','Definições de suspensão value')]")]
    SIDETONE = [(By.ID, "sidetone_text"),
                (By.XPATH, "//*[@content-desc=('Sidetone value','Effet local value','Tono lateral value','Riverbero value')]")]
    ADVANCED_CALL_CLARITY = [(By.ID, "noise_suppression_label"),
                             (By.XPATH, "//*[@content-desc=('Advanced call clarity label','Claridad de llamadas avanzada label','Nitidezza delle chiamate avanzata label','Erweiterte Anrufqualität label', 'Clareza de chamada avançada label','Un son clair pour les appels label')]")]
    ANC_BUTTON_OPTIONS = [(By.ID, "ANC-button_ option_label"),
                          (By.XPATH, "//*[(contains(@content-desc, 'ANC') or contains(@content-desc, 'Options')) and contains(@content-desc, 'label')]")]
    ON_HEAD_DETCTION = [(By.ID, "On-head_ detection_label"),
                        (By.XPATH, "//*[@content-desc=('On-head detection label','Detección de auriculares puestos label','Rilevamento quando indossata label','Detecção na cabeça label','On-Head-Erkennung label','Détection sur la tête label')]")]
    TOUCH_PAD = [(By.ID, "touchpad_customization_label"),
                 (By.XPATH, "//*[@content-desc=('Touch pad label','Panel táctil label','Touchpad label','Touch pad label','Touchpad label','Pavé tactile label')]")]
    VOICE_PROMPTS = [(By.ID, "enable_voiceprompt_label"),
                     (By.XPATH, "//*[@content-desc=('Voice prompts label','Mensajes de voz label','Messaggi vocali label','Notificações por voz label','Sprachausgabe label','Annonces vocales label')]")]
    HEALTH_AND_SAFETY = [(By.ID, "health_ safety_label"),
                         (By.XPATH, "//*[@content-desc=('Health and safety label','Salud y seguridad label','Salute e sicurezza label','Saúde e segurança label','Arbeitsschutz label','Santé et sécurité label')]")]
    HEADSET_LANGUAGE = [(By.ID, "headset_language"),
                        (By.XPATH, "//*[@content-desc=('Headset language value','Casque langue value','Headset Sprache value','Idioma Auriculares con micrófono value','Lingua Cuffia con microfono value','Headset idioma value')]")]
    NOISE_CANCELLATION = [(By.XPATH, "//*[@name='noise_cancellation_label']/XCUIElementTypeSwitch"),
                          (By.XPATH, "//*[@content-desc='Noise cancellation switch']")]
    ROTATE_TO_MUTE = [(By.XPATH, "//*[@name='rotate_to_mute_label']/XCUIElementTypeSwitch"),
                      (By.XPATH, "//*[@content-desc='Rotate to mute switch']")]
    # VOICE_PROMPTS = [(By.XPATH, "//*[@name='enable_voiceprompt_label']/XCUIElementTypeSwitch"),
    #                  (By.XPATH, "//*[@content-desc='Enable voice prompts switch']")]
    SETTINGS_NO_DEVICE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Configuración' or @name='Settings' or @name='Paramètres' or @name='Configurações' or @name='Einstellungen' or @name='Impostazioni']"),
                          (By.XPATH, "//*[@content-desc=('Settings','Configuración','Paramètres','Configurações','Einstellungen','Impostazioni')]")]
    SETTINGS = [(By.ID, "Settings"),
                (By.XPATH, "//*[@content-desc=('Settings','Settings icon','Configuración icon','Paramètres icon','Configurações icon','Einstellungen icon','Impostazioni icon')]")]
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back']"),
            (By.XPATH, "//*[@content-desc='Back']")]



