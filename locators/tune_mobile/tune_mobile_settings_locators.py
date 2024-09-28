from selenium.webdriver.common.by import By

class TuneMobileSettingsLocators(object):
    """
    A class containing the Tune Mobile App Home Screen element locators.
    """
    SIGNIN = [(By.ID, "Sign in with work account"),
              (By.XPATH, "//android.widget.TextView[@content-desc='Sign in with work account label']")]
    GOOGLE = [(By.ID, "google_logo"),
              (By.XPATH, "//android.view.View[@content-desc='Google Icon']")]
    SIGNIN_CLOSE = [(),
                    (By.ID, "com.android.chrome:id/close_button")]
    MICROSOFT = [(By.ID, "microsoft_office_outlook"),
                 (By.XPATH, "//android.view.View[@content-desc='Office 365 Icon']")]
    #French='Continuer', DE='Weiter',IT='Continua',PT='Continuar',ES='Continuar'
    CONTINUE = [(By.XPATH, "//XCUIElementTypeButton[@label='Continue' or @label='Continuer' or @label='Weiter' or @label='Continua' or @label='Continuar']"),
                (By.XPATH, "//android.widget.Button[@text='Continue']")]
    SIGNIN_TO_LOGITUNE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Sign in to Logi Tune']"),
              (By.XPATH, "//android.widget.TextView[@text='Sign in to Logi Tune']")]
    ACCEPT = [(By.ID, "Accept"),
              (By.XPATH, "//android.widget.Button")]
    ALLOW = [(By.XPATH, "//XCUIElementTypeButton[@name='Allow']"),
             (By.XPATH, "//android.widget.Button[@text='Allow']")]
    GRANT_PERMISSION = [(By.XPATH, "//XCUIElementTypeButton[contains(@name,'Grant permission')]"),
                        (By.XPATH, "//android.widget.TextView[@text='Grant permission']")]
    OK_BUTTON = [(By.XPATH, "//XCUIElementTypeButton[@name='OK']"),
                 (By.ID, "com.logitech.logue:id/btn_request_permission")]
    GOOGLE_EMAIL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"),
                    (By.XPATH, "//*[@text='XXX']")]
    MICROSOFT_EMAIL = [(By.XPATH, "//XCUIElementTypeButton[contains(@name,'XXX')]"),
                       (By.XPATH, "//android.widget.Button[contains(@text, 'XXX')]")]
    CONFIRM = [(By.XPATH, "//XCUIElementTypeButton[@name='Confirm']"),
               (By.XPATH, "//android.widget.Button[@text='Confirm']")]
    DONE = [(By.XPATH, "//XCUIElementTypeButton[@label='Done' or @label='Terminé' or @label='Fertig' or @label='Fatto' or @label='Concluído' or @label='Listo']"),
            (By.XPATH, "//android.widget.Button[@text='Done']")]
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' or @name='Zurück' or @name='Indietro' or @name='Voltar' or @name='gen-arrow-left' or @label='Logi Tune']"),
            (By.XPATH, "//*[@content-desc='Back']")]
    SIGNIN_WORK_ACCOUNT = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Connect your work account']"),
                           (By.XPATH, "//android.widget.TextView[@text='Connect your work account']")]
    ENROLL_DEVICE_MSG = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Enroll this device for enterprise features.')]"),
                         (By.XPATH, "//android.widget.TextView[contains(@text, 'Enroll this device for enterprise features.')]")]
    PRIVACY_POLICY_MSG = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'I agree that I have read and accept the Terms of Use and the Privacy Policy.')]"),
                         (By.XPATH, "//android.widget.TextView[contains(@text, 'I agree that I have read and accept the Terms of Use and the Privacy Policy.')]")]
    PRIVACY_POLICY_CHECKBOX = [(By.CLASS_NAME, "XCUIElementTypeSwitch"),
                               (By.CLASS_NAME, "android.widget.CheckBox")]
    SIGNIN_WITH_GOOGLE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Sign in with Google']"),
                          (By.XPATH, "//*[@text='Sign in with Google']")]
    SIGNIN_WITH_MICROSOFT = [(By.XPATH, "//XCUIElementTypeImage[@label='Microsoft']"),
                             (By.XPATH, "//android.widget.Image[@text='Microsoft']")]
    SIGNIN_MICROSOFT_TEXTFIELD = [(By.ID, "Enter your email, phone, or Skype."),
                                  (By.CLASS_NAME, "android.widget.EditText")]
    MICROSOFT_PICK_ACCOUNT = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Pick an account']"),
                              (By.XPATH, "//android.widget.TextView[@text='Pick an account']")]
    MICROSOFT_ACCESS_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'app access your info')]"),
                                (By.XPATH, "")]
    GOOGLE_ACCESS_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Logi Tune wants') and contains(@label, 'access to your Google Account')]"),
                             (By.XPATH, "//*[contains(@text, 'Logi Tune wants') and contains(@text, 'access to your Google Account')]")]
    GOOGLE_ALLOW_MESSAGE = [(By.XPATH,"//XCUIElementTypeStaticText[contains(@label, 'wants to access your Google Account')]"),
                             (By.XPATH,"//*[contains(@text, 'wants to access your Google Account')]")]
    WELCOME_SCREEN = [(By.XPATH, "//XCUIElementTypeStaticText[@value='Welcome to Logitech Desk Booking']"),
                      (By.XPATH, "//android.widget.TextView[@text='Welcome to Logitech Desk Booking']")]
    WELCOME_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Book desks in the office, find where your teammates sit, check your agenda, join meetings, and manage Logitech devices.']"),
                       (By.XPATH, "//android.widget.TextView[@text='Book desks in the office, find where your teammates sit, check your agenda, join meetings, and manage Logitech devices.']")]
    BASECAMP_SCREEN = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label,'Choose a basecamp')]"),
                       (By.XPATH, "//android.widget.TextView[contains(@text,'Choose a basecamp')]")]
    BUILDING = [(By.ID, "building"),
                (By.ID, "com.logitech.logue:id/icon_building")]
    BUILDING_NAME = [(By.XPATH, "//XCUIElementTypeImage[@name='building']/following-sibling:: XCUIElementTypeStaticText"),
                     (By.ID, "com.logitech.logue:id/label_building")]
    BASECAMP_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@label, 'Select the office where you work most')]"),
                        (By.XPATH, "//android.widget.TextView[@text='Select the office where you work most of the time. You can change your home office later.']")]
    WHOS_ON_TEAM = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Who’s on your team?']"),
                    (By.XPATH, "//android.widget.TextView[@text='Who’s on your team?']")]
    WHOS_ON_TEAM_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Add coworkers as teammates so you can see their location in the office']"),
                            (By.XPATH, "//android.widget.TextView[@text='Add coworkers as teammates so you can see their location in the office']")]
    ADD_TEAMMATES = [(By.XPATH, "//XCUIElementTypeButton/preceding-sibling:: XCUIElementTypeOther//XCUIElementTypeImage[@name='chevron-right']"),
                     (By.ID, "com.logitech.logue:id/icon_chevron")]
    TEAMMATES_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@label='XXX']"),
                       (By.ID, "com.logitech.logue:id/label_building")]
    SKIP = [(By.ID, "Skip"),
            (By.ID, "com.logitech.logue:id/btn_skip")]
    NO_ACCESS_TITLE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='No access']"),
                       (By.XPATH, "//android.widget.TextView[@text='No access to desk booking']")]
    NO_ACCESS_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='You (or your company) currently doesn’t have access to this feature - please contact IT personnel for details.']"),
                         (By.XPATH, "//android.widget.TextView[@text='You (or your company) currently doesn’t have access to this feature - please contact IT personnel for details.']")]
    NO_BASECAMP_TITLE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Sorry, no basecamps found']"),
                       (By.XPATH, "//android.widget.TextView[@text='Sorry, no basecamps found']")]
    NO_BASECAMP_MESSAGE = [(By.XPATH,"//XCUIElementTypeStaticText[@label='It seems that you have not been granted access to any basecamps yet, so we have logged you out. Please contact your IT team for assistance and check back again later.']"),
                         (By.XPATH,"//android.widget.TextView[@text='It seems that you have not been granted access to any basecamps yet, so we have logged you out. Please contact your IT team for assistance and check back again later.']")]
    GOT_IT = [(By.XPATH, "//XCUIElementTypeButton[@label='Got it']"),
              (By.XPATH, "//android.widget.Button[@text='Got it']")]
    ASK_LATER = [(By.XPATH, "//XCUIElementTypeButton[@label='Ask later']"),
                 ()]
    NEXT = [(By.XPATH, "//XCUIElementTypeButton[@name='Next']"),
            (By.XPATH, "//android.widget.Button[@text='Next']")]
    START_TESTING = [(By.XPATH, "//XCUIElementTypeButton[@name='Start Testing']"),
                     ()]
    DISMISS = [(), (By.XPATH, "//android.widget.Button[@text='Dismiss']")]

