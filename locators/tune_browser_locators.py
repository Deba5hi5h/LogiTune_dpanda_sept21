from selenium.webdriver.common.by import By

from common.framework_params import PROJECT


class TunesBrowserLocators(object):
    """
    A class containing the Browser element locators opened through Tune App
    """

    #Login
    USE_ANOTHER_ACCOUNT = (By.XPATH, "//div[text()='Use another account']")
    EMAIL = (By.XPATH, "//input[@type='email']")
    NEXT = (By.XPATH, '//*[@id="identifierNext"]/div/button')
    PASSWORD = (By.XPATH, "//input[@type='password']")
    PASSWORD_NEXT = (By.XPATH, '//*[@id="passwordNext"]/div/button')
    EMPLOYEE_ID = (By.XPATH, "//input[@name='EmployeeId']")
    EMPLOYEE_ID_NEXT = (By.XPATH, '//button')
    CHECK_BOX = (By.XPATH, "//input[@type='checkbox']")
    CONTINUE = (By.XPATH, "//span[text()='Continue']")
    ALLOW = (By.XPATH, "//span[text()='Allow']")
    YOU_CAN_CLOSE_WINDOW = (By.XPATH, "//*[text()='You can close this window now.]")
    AUTHENTICATION_COMPLETED = (By.XPATH, "//*[text()='The authentication flow has completed. You may close this window.']")
    SUBMIT = (By.XPATH, "//input[@type = 'submit']")
    ACCEPT = (By.XPATH, "//div[text()='ACCEPT']")
    STAY_SIGNED_IN = (By.XPATH, "//button[@type='submit' and @id='acceptButton']")
    ACCEPT_PERMISSION_TO_TUNE = (By.XPATH, "//input[@type='submit' and @id='idSIButton9']")
    STAY_SIGNED_IN_FINAL = (By.XPATH, "//*[@type='submit' and (@id='acceptButton' or @id='idSIButton9')]")
    NO = (By.XPATH, "//input[@type='button' and @id='idBtn_Back']")
    REDIRECTING_TO_LOGI_TUNE = (By.XPATH, "//div/h1[contains(text(),'Redirecting to Logi Tune')]")
    OUTLOOK_ACCEPT = (By.XPATH, "//input[@name='ucaccept']")

    #Create Events
    NOTHING_PLANNED_FOR_THE_DAY = (By.XPATH, "//span[contains(text(), 'Nothing planned for the day')]")
    NEW_EVENT = (By.XPATH, "//span[text()='New event']")
    ADD_A_TITLE = (By.XPATH, "//input[@placeholder='Add a title']")
    SAVE = (By.XPATH, "//span[text()='Save']")

    #Delete Events
    TUNE_MEETING = (By.XPATH, "//div[contains(@title, 'Tune Meeting')]")
    DELETE = (By.XPATH, "//span[text()='Delete']")
    DELETE_EVENT = (By.XPATH, "(//span[text()='Delete'])[2]")

    #Support webpage
    GETTING_STARTED_LOGI_TUNE = (By.XPATH, "//h1[contains(text(), 'Getting Started - Logi Tune')]")
    
    #Share feedback webpage
    GIVE_FEEDBACK = (By.XPATH, "//button/descendant::span[text() = 'Give feedback']")
