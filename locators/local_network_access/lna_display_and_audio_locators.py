from selenium.webdriver.common.by import By


class LNADisplayAndAudioLocators(object):
    """
    A class containing the Local Network Access Display and Audio page
    element locators.
    """
    AUDIO = (By.XPATH, "//button//*[text()='Audio']")
    AUDIO_EXPAND = (By.XPATH, "//*[text()='Audio']/ancestor::button[contains(@class, 'triggerRoot')]")
    SPEAKER_BOOST = (By.XPATH, "//*[text()='Speaker Boost']/parent::div//input")
    AI_NOISE_SUPPRESSION = (By.XPATH, "//*[text()='AI Noise Suppression']/parent::div//input")
    REVERB_CONTROL_DISABLED = (By.XPATH, "//p[contains(text(),'Reverb Control')]/"
                                         "following-sibling::div[3]//input[@id='Disabled']")
    REVERB_CONTROL_NORMAL = (By.XPATH, "//p[contains(text(),'Reverb Control')]/"
                                       "following-sibling::div[3]//input[@id='Normal (Recommended)']")
    REVERB_CONTROL_AGGRESSIVE = (By.XPATH, "//p[contains(text(),'Reverb Control')]/"
                                           "following-sibling::div[3]//input[@id='Aggressive']")
    MICROPHONE_BASS_BOOST = (By.XPATH, "//p[contains(text(),'Microphone EQ')]/"
                                       "following-sibling::div[2]//input[@id='Bass Boost']")
    MICROPHONE_NORMAL = (By.XPATH, "//p[contains(text(),'Microphone EQ')]/"
                                   "following-sibling::div[2]//input[@id='Normal (Recommended)']")
    MICROPHONE_VOICE_BOOST = (By.XPATH, "//p[contains(text(),'Microphone EQ')]/"
                                        "following-sibling::div[2]//input[@id='Voice Boost']")
    SPEAKER_BASS_BOOST = (By.XPATH, "//p[contains(text(),'Speaker EQ')]/"
                                    "following-sibling::div[2]//input[@id='Bass Boost']")
    SPEAKER_NORMAL = (By.XPATH, "//p[contains(text(),'Speaker EQ')]/"
                                "following-sibling::div[2]//input[@id='Normal (Recommended)']")
    SPEAKER_VOICE_BOOST = (By.XPATH, "//p[contains(text(),'Speaker EQ')]/"
                                     "following-sibling::div[2]//input[@id='Voice Boost']")
    BUTTON_APPLY = (By.XPATH, "//button[text()='Apply']")
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(),'change applied') or contains(text(),'changes applied')]")
