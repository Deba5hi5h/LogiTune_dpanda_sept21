from selenium.webdriver.common.by import By

class TuneMobilePeopleLocators(object):
    """
    A class containing the Tune Mobile App People Screen element locators.
    """
    TEAMMATES_TAB = [(By.XPATH, "//XCUIElementTypeButton[@name='TEAMMATES']"),
                     (By.XPATH, "//*[@content-desc='TEAMMATES']")]
    ALL_TEAMMATES = [(By.ID, "All teammates"),
                     (By.ID, "com.logitech.logue:id/tv_all_teammates")]
    EDIT = [(By.ID, "Edit"),
            (By.ID, "com.logitech.logue:id/edit_button")]
    ADD_TEAMMATES = [(By.XPATH, "//XCUIElementTypeButton[@name='Add teammates']"),
                     (By.ID, "com.logitech.logue:id/btn_add_teammates")]
    DELETE_ICON = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']/following-sibling::XCUIElementTypeButton"),
                   (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::*[@resource-id='com.logitech.logue:id/iv_remove']")] #Pass Teammate Name
    TEAMMATE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name,'XXX')]"),
                (By.XPATH, "//*[contains(@text, 'XXX')][@resource-id='com.logitech.logue:id/tv_person_name']")]
    GROUP_NAME = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name,'XXX')]"),
                  (By.XPATH, "//*[contains(@text, 'XXX')][@resource-id='com.logitech.logue:id/tv_group_name']")]
    TEAMMATE_EMAIL = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name,'XXX')]/following-sibling::XCUIElementTypeStaticText"),
                      (By.ID, "com.logitech.logue:id/email")]
    EVERYONE_TAB = [(By.XPATH, "//XCUIElementTypeButton[@name='EVERYONE']"),
                    (By.XPATH, "//*[@content-desc='EVERYONE']")]
    BOOKMARK = [(By.ID, "star filled"),
                (By.ID, "add_teammate_image")]
    REMOVE_FROM_TEAMS = [(By.ID, "REMOVE FROM TEAMS"),
                         (By.ID, "com.logitech.logue:id/tv_remove_from_teams")]
    ADD_TO_TEAM = [(By.ID, "ADD TO TEAM"),
                   (By.ID, "com.logitech.logue:id/tv_add_to_teammates")]
    ADD = [(By.XPATH, "//XCUIElementTypeStaticText[@value='XXX']/following-sibling::XCUIElementTypeButton[@label='ADD']"),
           (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::*[@text='ADD']")]
    ADDED = [(By.XPATH, "//XCUIElementTypeStaticText[@value='XXX']/following-sibling::XCUIElementTypeButton[@label='ADDED']"),
             (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::*[@text='ADDED']")]
    REMOVE_BUTTON = [(By.XPATH, "//XCUIElementTypeStaticText[@value='XXX']/following-sibling::XCUIElementTypeButton[@label='REMOVE']"),
                     (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::*[@resource-id='com.logitech.logue:id/btn_add_remove_team']")]
    DONE = [(By.ID, "Done"),
            (By.ID, "com.logitech.logue:id/done_button")]
    REMOVE_MESSAGE = [(By.XPATH, "//*[contains(@name, 'Remove') and contains(@name, 'from the list of teammates?')]"),
                      (By.XPATH, "//*[contains(@text, 'Remove') and contains(@text, 'from the list of teammates?')]")]
    TEAMMATE_MESSAGE = [(By.XPATH, "//*[@name='Your list of teammates is only visible to you.']"),
                      (By.XPATH, "//*[@text='Your list of teammates is only visible to you.']")]
    REMOVE = [(By.XPATH, "//XCUIElementTypeButton[@name='Remove']"),
              (By.XPATH, "//android.widget.Button[@text='Remove']")]
    CANCEL = [(By.XPATH, "//XCUIElementTypeButton[@name='Cancel']"),
              (By.XPATH, "//android.widget.Button[@text='Cancel']")]
    SEARCH = [(By.CLASS_NAME, "XCUIElementTypeTextField"),
              (By.XPATH, "//android.widget.EditText[contains(@resource-id, 'et_search')]")]
    CLEAR_SEARCH = [(By.XPATH, "//XCUIElementTypeButton[@label='clear large']"),
                    (By.XPATH, "//*[@resource-id='com.logitech.logue:id/text_input_end_icon' or @resource-id='com.logitech.logue:id/iv_clear_search']")]
    NO_RESULTS_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[contains(@name, 'No results found for') or contains(@name, 'No search result for')]"),
                          (By.XPATH, "//*[contains(@text, 'No results found for')]")]
    ALL_BOOKMARKS = [(By.XPATH, "//XCUIElementTypeButton[@name='people bookmark']"),
                     (By.ID, "iv_bookmark")]
    NO_TEAMMATES_MESSAGE = [(By.XPATH, "//*[@name='No teammates added']"),
                            (By.XPATH, "//*[@text='No teammates added']")]
    ADD_TEAMMATES_MESSAGE = [(By.XPATH, "//*[@name='Add people to teammates in order to see their location in the office']"),
                             (By.XPATH, "//*[@text='Add people to teammates in order to see their location in the office']")]
    PEOPLE_SCROLL = [(By.CLASS_NAME, "XCUIElementTypeTable"),
                     ()]
    PEOPLE_LIST = [(By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeImage/following-sibling::XCUIElementTypeStaticText"),
                   (By.ID, "com.logitech.logue:id/tv_person_name")]
    USER_GROUPS_LIST = [(By.XPATH, "//XCUIElementTypeTable//XCUIElementTypeStaticText[2]"),
                        (By.ID, "com.logitech.logue:id/tv_group_name")]
    ADD_TEAMMATES_GROUPS_LIST = [(By.XPATH, "//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText"),
                                 (By.ID, "com.logitech.logue:id/tv_group_name")]
    SEARCH_DONE = [(By.ID, "Done"),
                   ()]
    TEAMMATES_LIST = [(By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[2]"),
                      (By.ID, "com.logitech.logue:id/tv_person_name")]
    # Teammates screen while sign in
    BACK = [(By.XPATH, "//XCUIElementTypeNavigationBar/XCUIElementTypeButton[1]"),
            (By.XPATH, "//*[@resource-id=('com.logitech.logue:id/back_button', 'com.logitech.logue:id/btn_close', 'com.logitech.logue:id/back_button_image', 'com.logitech.logue:id/iv_back_arrow')]")]
    BACK_TO_CUSTOM = [(By.XPATH, "(//XCUIElementTypeNavigationBar/XCUIElementTypeButton[1])[2]"),
                      (By.XPATH, "//*[@resource-id=('com.logitech.logue:id/back_button', 'com.logitech.logue:id/btn_close', 'com.logitech.logue:id/back_button_image', 'com.logitech.logue:id/iv_back_arrow')]")]
    TEAMMATE_TITLE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Teammates']"),
                      (By.XPATH, "//android.widget.TextView[@text='Teammates']")]
    FAVORITE_ICON = [(By.ID, "star-filled"),
                     (By.ID, "com.logitech.logue:id/add_teammate_image")]
    LOCATE_ON_MAP = [(By.XPATH, "//XCUIElementTypeStaticText[@value='LOCATE ON MAP']"),
                     (By.ID, "com.logitech.logue:id/tv_locate_on_map")]
    STATIC_TEXT = [(By.XPATH, "//XCUIElementTypeStaticText[@label='XXX']"),
                   (By.XPATH, "//android.widget.TextView[@text='XXX']")] #Pass Static text
    NO_UPCOMING_BOOKING = [(By.XPATH, "//XCUIElementTypeStaticText[@label='There are no upcoming bookings for this user.']"),
                           (By.XPATH, "//android.widget.TextView[@text='There are no upcoming bookings for this user.']")]
    NO_TEAMMATES_IN_OFFICE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='No teammates in the office']"),
                              (By.XPATH, "//android.widget.TextView[contains(@text, 'No teammates in the office')]")]
    NO_PEOPLE_IN_OFFICE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='No people in the office']"),
                           (By.XPATH, "//android.widget.TextView[@text='No people in the office.']")]
    NO_TEAMMATES_IN_AREA = [(By.XPATH, "//XCUIElementTypeStaticText[@label='No teammates in this area']"),
                              (By.XPATH, "//android.widget.TextView[@text='No teammates in this area.']")]
    NO_PEOPLE_IN_AREA = [(By.XPATH, "//XCUIElementTypeStaticText[@label='No people in this area']"),
                           (By.XPATH, "//android.widget.TextView[@text='No people in this area.']")]
    # Custom Team
    CREATE_NEW_TEAM = [(By.ID, "Create new team"),
                       (By.ID, "com.logitech.logue:id/create_team_title")]
    CLOSE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Create new team' or @name='Edit team']/following-sibling::XCUIElementTypeButton"),
             (By.ID, "com.logitech.logue:id/close_icon")]
    NEW_TEAM = [(By.XPATH, "//XCUIElementTypeButton[@name='NEW TEAM' or @name='New team']"),
                (By.XPATH, "//*[@resource-id=('com.logitech.logue:id/button_create_new_teammate_group','com.logitech.logue:id/skip_notify_teammates')]")]
    TEAM_NAME = [(By.ID, "Team name"),
                 ()]
    TEAM_NAME_TEXTFIELD = [(By.XPATH, "//XCUIElementTypeImage[@name='person-group']/preceding-sibling::XCUIElementTypeTextField"),
                           (By.ID, "com.logitech.logue:id/teammate_group_name")]
    CREATE = [(By.XPATH, "//XCUIElementTypeButton[@name='Create']"),
              (By.ID, "com.logitech.logue:id/button_create")]
    RETURN_KEY = [(By.ID, "Return"),
                  ()]
    TEAM_EMPTY = [(By.ID, "The team is empty"),
                  (By.XPATH, "//android.widget.TextView[@text='The team is empty']")]
    ADD_FEW_TEAMMATES = [(By.ID, "Let’s add a few teammates."),
                         (By.XPATH, "//android.widget.TextView[@text='Let’s add a few teammates.']")]
    CUSTOM_TEAM = [(By.XPATH, "//XCUIElementTypeCell/XCUIElementTypeStaticText[@name='XXX']"),
                   (By.XPATH, "//android.widget.TextView[@resource-id='com.logitech.logue:id/tv_group_name' and @text='XXX']")] #Pass team name
    EDIT_TEAMS = [(By.XPATH, "//XCUIElementTypeButton[@name='EDIT TEAMS']"),
                  (By.ID, "com.logitech.logue:id/tv_edit_teams")]
    EDIT_TEAMS_TITLE = [(By.XPATH, "//XCUIElementTypeNavigationBar[@name='Edit teams']"),
                        (By.ID, "com.logitech.logue:id/edit_teams_title")]
    DELETE_TEAM = [(By.XPATH, "//XCUIElementTypeButton[@name='Delete team']"),
                   (By.ID, "com.logitech.logue:id/btn_delete_teammate_group")]
    DELETE_ALL_TEAMS = [(By.XPATH, "//XCUIElementTypeButton[@name='Button']"),
                        (By.ID, "com.logitech.logue:id/delete")]
    DELETE_BUTTON = [(By.XPATH, "//XCUIElementTypeButton[@name='Delete']"),
                     (By.XPATH, "//android.widget.Button[@text='Delete']")]
    CUSTOM_TEAM_TEAMMATES_LIST = [(By.XPATH, "//XCUIElementTypeTable/XCUIElementTypeCell/XCUIElementTypeStaticText"),
                                  (By.ID, "com.logitech.logue:id/tv_person_name")]
    MANAGE_TEAMS = [(By.ID, "MANAGE TEAMS"),
                    (By.ID, "com.logitech.logue:id/tv_add_to_teammates")]
    TEAM_COUNT = [(By.XPATH, "//XCUIElementTypeStaticText[@name='MANAGE TEAMS' or @name='ADD TO TEAM']/preceding-sibling::XCUIElementTypeStaticText"),
                  (By.ID, "com.logitech.logue:id/tv_amount_teams")]
    TEAM_NAME_TICK_MARK = [(By.ID, "tick"), (By.ID, "com.logitech.logue:id/btn_tick")]
    TEAM_NAME_EDIT = [(By.XPATH, "//XCUIElementTypeButton[@name='tick']/preceding-sibling:: XCUIElementTypeButton[1]"),
                      (By.ID, "com.logitech.logue:id/iv_edit_icon")]
    TEAM_NAME_UPDATE = [(By.XPATH, "//XCUIElementTypeButton[@name='Update']"),
                        (By.XPATH, "//android.widget.Button[@text='Update']")]
    CUSTOM_TEAM_TEAMMATE_COUNT = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']/preceding-sibling::XCUIElementTypeStaticText"),
                                  (By.XPATH, "//android.widget.TextView[@text='XXX']/parent::android.view.ViewGroup//*[@resource-id='com.logitech.logue:id/tv_plus_teammates']")] #Pass Custom team name
    DELETE_TEAM_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Teammates will be removed from the team. This change is visible only for you.']"),
                           (By.XPATH, "//android.widget.TextView[@text='Teammates will be removed from the team. This change is visible only for you.']")]
    DELETE_TEAM_CONFIRM = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Delete the XXX team?']"),
                           (By.XPATH, "//android.widget.TextView[@text='Delete the XXX team?']")]
    PEOPLE_COUNT_IN_TEAM = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']/following-sibling::XCUIElementTypeStaticText"),
                            (By.XPATH, "//android.widget.TextView[@text='XXX']/following-sibling::android.widget.TextView")] #Pass Team Name
    CUSTOM_TEAM_NO_TEAMMATES_MSG = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Add teammates so you can notify them and see when they are in the office.']"),
                                    (By.XPATH, "//android.widget.TextView[@text='Add teammates so you can notify them and see when they are in the office.']")]
    CUSTOM_TEAM_ADD_TEAMMATE = [(By.XPATH, "//XCUIElementTypeButton[@name='ADD TEAMMATE']"),
                                (By.ID, "com.logitech.logue:id/btn_add_teammate")]
    CUSTOM_TEAM_NO_TEAM_MSG = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Quickly view and manage teammates by creating custom teammate groups.']"),
                               (By.XPATH, "//android.widget.TextView[@text='Quickly view and manage teammates by creating custom teammate groups.']")]

