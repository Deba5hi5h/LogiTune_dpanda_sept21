from selenium.webdriver.common.by import By

class TuneMobileEqualizerLocators(object):
    """
    A class containing the Tune Mobile App Home Screen element locators.
    """
    DEFAULT_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Default']"),
                     (By.XPATH, "//*[@content-desc='Default label']")]
    VOLUME_BOOST_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Volume Boost']"),
                          (By.XPATH, "//*[@content-desc='Volume Boost label']")]
    PODCAST_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Podcast']"),
                     (By.XPATH, "//*[@content-desc='Podcast label']")]
    BASS_BOOST_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Bass Boost']"),
                        (By.XPATH, "//*[@content-desc='Bass Boost label']")]
    CUSTOM_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Custom']"),
                    (By.XPATH, "//*[@content-desc='Custom label']")]
    DEFAULT = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Default']/following-sibling::XCUIElementTypeButton"),
               (By.XPATH, "//*[@content-desc='Default label']/following-sibling::android.view.View")]
    # EQ_SCROLL = [(By.XPATH, "//XCUIElementTypeCollectionView"),
    #              (By.XPATH, "//android.widget.ScrollView")]
    EQ_SCROLL = [(By.XPATH, "//XCUIElementTypeOther[contains(@name, 'Vertical scroll bar')]"),
                 (By.XPATH, "//android.widget.ScrollView")]
    VOLUME_BOOST = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Volume Boost']/following-sibling::XCUIElementTypeButton"),
                    (By.XPATH, "//*[@content-desc='Volume Boost label']/following-sibling::android.view.View")]
    PODCAST = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Podcast']/following-sibling::XCUIElementTypeButton"),
               (By.XPATH, "//*[@content-desc='Podcast label']/following-sibling::android.view.View")]
    BASS_BOOST = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Bass Boost']/following-sibling::XCUIElementTypeButton"),
                  (By.XPATH, "//*[@content-desc='Bass Boost label']/following-sibling::android.view.View")]
    CUSTOM = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Custom']/following-sibling::XCUIElementTypeButton"),
              (By.XPATH, "//*[@content-desc='Custom label']/following-sibling::android.view.View")]
    BACK = [(By.XPATH, "//XCUIElementTypeButton[@name='Back' or @name='Atrás' or @name='Précédent' "
                       "or @name='Zurück' or @name='Indietro' or @name='Voltar']"),
            (By.XPATH, "//*[@content-desc='Back']")]
    EQ_SLIDER_1 = [(By.XPATH, "//XCUIElementTypeStaticText[@name='Bass']/preceding-sibling:: XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]"),
                   (By.ID, "com.logitech.logue:id/bass_eq")]
    EQ_SLIDER_2 = [(By.XPATH,"//XCUIElementTypeStaticText[@name='Bass']/preceding-sibling:: XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]"),
                   (By.ID, "com.logitech.logue:id/mid_bass_eq")]
    EQ_SLIDER_3 = [(By.XPATH,"//XCUIElementTypeStaticText[@name='Bass']/preceding-sibling:: XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]"),
                   (By.ID, "com.logitech.logue:id/mid_eq")]
    EQ_SLIDER_4 = [(By.XPATH,"//XCUIElementTypeStaticText[@name='Bass']/preceding-sibling:: XCUIElementTypeOther/XCUIElementTypeOther[4]/XCUIElementTypeOther[2]"),
                   (By.ID, "com.logitech.logue:id/mid_treble_eq")]
    EQ_SLIDER_5 = [(By.XPATH,"//XCUIElementTypeStaticText[@name='Bass']/preceding-sibling:: XCUIElementTypeOther/XCUIElementTypeOther[5]/XCUIElementTypeOther[2]"),
                   (By.ID, "com.logitech.logue:id/treble_eq")]
    SAVE_CUSTOM_PRESET = [(By.ID, "save_custom_preset_button"),
                          (By.XPATH, "//*[@content-desc='Save custom preset label']")]
    PRESET_NAME_EDITBOX = [(By.ID, "preset_rename_textfield"),
                           (By.XPATH, "//android.widget.EditText")]
    SURPRISE_ME = [(By.ID, "surprise_me_preset_button"),
                   (By.XPATH, "//*[@content-desc='Surprise me label']")]
    SAVE_BUTTON = [(By.ID, "surprise_me_preset_save_button"),
                   (By.XPATH, "//*[@text='Save']/following-sibling::android.widget.Button")]
    CUSTOM_PRESET_LABEL = [(By.XPATH, "//XCUIElementTypeStaticText[@name='XXX']"),
                           (By.XPATH, "//*[@content-desc='XXX label']")]
    EDIT_PRESETS = [(By.ID, "edit_preset_button"),
                    (By.XPATH, "//*[@content-desc='Edit Presets']")]
    DELETE_PRESET = [(By.ID, "XXX_delete_button"),
                     (By.XPATH, "//*[@content-desc='XXX label']/following-sibling::*[@content-desc='Preset Selection']")]
    DELETE_ALL_PRESETS = [(By.XPATH, "//XCUIElementTypeButton[@label='clear_purple']"),
                          (By.XPATH, "//*[@content-desc='Preset Selection']")]
    DONE = [(By.ID, "done_preset_button"),
            (By.XPATH, "//*[@text='Done']/following-sibling::android.widget.Button")]
    CLOSE_PRESET = [(By.ID, "close_preset_button"),
                    (By.XPATH, "//*[@content-desc='Close Save custom preset BottomSheet']")]
    GOT_IT = [(By.ID, "ok_preset_button"),
              (By.XPATH, "//*[@text='Got it']/following-sibling::android.widget.Button")]
    PRESET_LIMIT_MESSAGE = [(By.XPATH, "//XCUIElementTypeStaticText[@label='You can create up to 3 custom presets. Delete a custom preset and try again.']"),
                            (By.XPATH, "//*[@text='You can create up to 3 custom presets. Delete a custom preset and try again.']")]
    PRESET_LIMIT_POPUP = [(By.XPATH, "//XCUIElementTypeStaticText[@label='Preset limit reached']"),
                          (By.XPATH, "//*[@text='Preset limit reached']")]
