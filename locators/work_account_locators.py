from selenium.webdriver.common.by import By


class WorkAccountTunesAppLocators:
    """
    A class containing locators for Work Account windows in Logi Tune
    """

    TEMPLATE = (By.XPATH, "//xxx[@data-testid='xxx']")
    # ONBOARDING WELCOME WINDOW
    ONBOARDING_WELCOME_TITLE = (By.XPATH, "//p[@data-testid='workAccountOnboarding.welcome.title']")
    ONBOARDING_WELCOME_DESCRIPTION = (By.XPATH, "//p[@data-testid='workAccountOnboarding.welcome.description']")
    ONBOARDING_CONTINUE_BUTTON = (By.XPATH, "//button[@data-testid='workAccountOnboarding.welcome.continue']")
    # BASECAMP SELECTION WINDOW
    BASECAMP_SELECTION_TITLE = (By.XPATH, "//p[@data-testid='pageHeader.Choose your basecamp.title']")
    BASECAMP_SELECTION_SEARCH_INPUT = (By.XPATH, "//input[@data-testid='basecampSelection.search']")
    BASECAMP_SELECTION_LOCATION_TOGGLE = (By.XPATH, "//button[contains(@data-testid, 'basecampSelection.collapsableList') and contains(@data-testid, 'toggle')]")
    BASECAMP_SELECTION_LOCATION_ITEM = (By.XPATH, "//button[contains(@data-testid, 'basecampSelection.collapsableList') and contains(@data-testid, 'item')]")
    BASECAMP_SELECTION_LOCATION_TITLE = (By.XPATH, "//button[contains(@data-testid, 'basecampSelection.collapsableList') and contains(@data-testid, 'title')]")
    # ONBOARDING TEAMMATES WINDOW
    ONBOARDING_TEAMMATES_SKIP_BUTTON = (By.XPATH, "//button[@data-testid='workAccountOnboarding.teammates.skip']")
    ONBOARDING_TEAMMATES_TITLE = (By.XPATH, "//p[@data-testid='workAccountOnboarding.teammates.title']")
    ONBOARDING_TEAMMATES_DESCRIPTION = (By.XPATH, "//p[@data-testid='workAccountOnboarding.teammates.description']")
    ONBOARDING_TEAMMATES_CONTINUE_BUTTON = (By.XPATH, "//button[@data-testid='workAccountOnboarding.teammates.continue']")
    ONBOARDING_ADD_TEAMMATES_BACK_BUTTON = (By.XPATH, "//button[@data-testid='pageHeader.Add teammates.back']")
    ONBOARDING_ADD_TEAMMATES_TITLE = (By.XPATH, "//p[@data-testid='pageHeader.Add teammates.title']")
    ONBOARDING_ADD_TEAMMATES_SEARCH_INPUT = (By.XPATH, "//input[@data-testid='workAccountOnboarding.addTeammates.userList.search']")
    ONBOARDING_ADD_TEAMMATES_USERS_TOGGLE = (By.XPATH, "//button[contains(@data-testid, 'workAccountOnboarding.addTeammates.collapsableList') and contains(@data-testid, 'toggle')]")
    # ONBOARDING_ADD_TEAMMATES_ADD = (By.XPATH, "//button[@data-testid='xxx']")  # TODO: locators are different for different search methods/user groups
    ONBOARDING_ADD_TEAMMATES_ADD_WITHOUT_GROUP = (By.XPATH, "//button[contains(@data-testid, 'false.userList.user')]")  # TODO: locator when searchbar has any input or no group of users
    ONBOARDING_ADD_TEAMMATES_ADD_WITHOUT_GROUP_TITLE = (By.XPATH, "//p[contains(@data-testid, 'false.userList.user') and contains(@data-testid, 'title')]")  # TODO: locator when searchbar has any input or no group of users
    ONBOARDING_ADD_TEAMMATES_ADD_FROM_GROUP = (By.XPATH, "//button[contains(@data-testid, 'workAccountOnboarding.addTeammates')]")  # TODO: locator when group of users are present
    ONBOARDING_ADD_TEAMMATES_ADD_FROM_GROUP_TITLE = (By.XPATH, "//p[contains(@data-testid, 'workAccountOnboarding.addTeammates') and contains(@data-testid, 'title')]")  # TODO: locator when group of users are present
    ONBOARDING_ADD_TEAMMATES_DONE_BUTTON = (By.XPATH, "//button[@data-testid='workAccountOnboarding.addTeammates.done']")
    # MAIN DASHBOARD WINDOW
    DASHBOARD_AGENDA_REFRESH_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.agenda.refreshButton']")
    DASHBOARD_AGENDA_NOTIFICATIONS_BUTTON = (By.XPATH, "//button[@data-testid='path.alerts']")
    DASHBOARD_AGENDA_PROFILE_BUTTON = (By.XPATH, "//button[@data-testid='path.workAccountProfile.profile']")
    DASHBOARD_AGENDA_HOME_TAB = (By.XPATH, "//button[@data-testid='dashboard.tab-home']")
    DASHBOARD_AGENDA_DEVICES_TAB = (By.XPATH, "//button[@data-testid='dashboard.tab-myDevices']")
    DASHBOARD_AGENDA_PEOPLE_TAB = (By.XPATH, "//button[@data-testid='dashboard.tab-people']")
    # TODO: CALENDAR LOCATORS
    DASHBOARD_BOOK_A_DESK_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.home.bookings.bookADesk']")
    # DESK BOOKING
    DESK_BOOKING_CLOSE_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.deskBooking.deskBooking.bookADesk.close']")
    DESK_BOOKING_BY_LOCATION_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.deskBooking.deskBooking.byLocation']")
    DESK_BOOKING_NEAR_TEAMMATE_BUTTON = (By.XPATH, "//button[@data-testid='dashboard.deskBooking.deskBooking.nearTeammate']")
    DESK_BOOKING_DESK_SELECTION_PREFERENCES_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.deskSelection.preferences']")
    # TODO: PREFERENCES LOCATORS
    DESK_BOOKING_DESK_SELECTION_DATE_SELECT_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.deskSelection.dateSelect.open']")
    DESK_BOOKING_DESK_SELECTION_DATE_SELECT_OPTION_BUTTON = (By.XPATH, "//button[contains(@data-testid, 'deskBooking.deskSelection.dateSelect.option')]")
    DESK_BOOKING_DESK_SELECTION_TIME_START_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.deskSelection.timeSelect.start']")
    DESK_BOOKING_DESK_SELECTION_TIME_START_OPTION_BUTTON = (By.XPATH, "//button[contains(@data-testid, 'deskBooking.deskSelection.timeSelect.option.start')]")
    DESK_BOOKING_DESK_SELECTION_TIME_END_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.deskSelection.timeSelect.end']")
    DESK_BOOKING_DESK_SELECTION_TIME_END_OPTION_BUTTON = (By.XPATH, "//button[contains(@data-testid, 'deskBooking.deskSelection.timeSelect.option.end')]")
    # TODO: OFFICE AND FLOOR LOCATORS
    DESK_BOOKING_DESK_SELECTION_DETAILS = (By.XPATH, "//p[@data-testid='deskBooking.deskSelection.deskDetails']")
    DESK_BOOKING_DESK_SELECTION_DETAILS_BACK = (By.XPATH, "//button[@data-testid='pageHeader.Desk details.back']")
    DESK_BOOKING_DESK_SELECTION_DETAILS_AVAILABLE_BETWEEN = (By.XPATH, "//p[@data-testid='deskBooking.deskSelection.desksDetails.available']")
    DESK_BOOKING_DESK_SELECTION_BOOK_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.deskSelection.book']")
    DESK_BOOKING_DESK_SELECTION_SELECTED_DESK_NAME = (By.XPATH, "//p[@data-testid='deskBooking.deskSelection.selected.name']")
    DESK_BOOKING_NOTIFY_TEAMMATES_SKIP_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.notifyTeammates.skip']")
    DESK_BOOKING_NOTIFY_TEAMMATES_CANCEL_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.notifyTeammates.cancelBooking']")
    DESK_BOOKING_NOTIFY_TEAMMATES_CANCEL_YES_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.notifyTeammates.cancelBooking.yesCancel']")
    DESK_BOOKING_NOTIFY_TEAMMATES_CANCEL_NO_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.notifyTeammates.cancelBooking.noKeep']")
    DESK_BOOKING_NOTIFY_TEAMMATES_SELECTION = (By.XPATH, "//button[contains(@data-testid, 'deskBooking.notifyTeammates.teammates')]")
    DESK_BOOKING_NOTIFY_TEAMMATES_SELECTION_NAME = (By.XPATH, "//p[contains(@data-testid, 'deskBooking.notifyTeammates.teammates') and contains(@data-testid, 'title')]")
    DESK_BOOKING_NOTIFY_TEAMMATES_OPTIONAL_MESSAGE_TEXT_AREA = (By.XPATH, "//textarea[@data-testid='deskBooking.notifyTeammates.messageBox']")
    DESK_BOOKING_NOTIFY_TEAMMATES_NOTIFY_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.notifyTeammates.notify']")
    DESK_BOOKING_DESK_BOOKED_TIME = (By.XPATH, "//p[@data-testid='deskBooking.deskBooked.time']")
    DESK_BOOKING_DESK_BOOKED_DONE_BUTTON = (By.XPATH, "//button[@data-testid='deskBooking.deskBooked.done']")
    TEMPLATE = (By.XPATH, "//xxx[@data-testid='xxx']")


