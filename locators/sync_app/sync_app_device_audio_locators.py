from selenium.webdriver.common.by import By


class SyncAppDeviceAudioLocators(object):
    """
    A class containing the Sync App Device Screen element locators.
    """
    AUDIO_TAB_TEXT = (By.XPATH, "//p[contains(text(), 'Test mics and speakers')]")
    TEST_MIC_BUTTON = (By.XPATH, "//button/span[contains(text(), 'Test Mic')]")
    STOP_RECORDING_BUTTON = (By.XPATH, "//button/span[contains(text(), 'Stop Recording')]")
    STOP_PLAYING_BUTTON = (By.XPATH, "//button/span[contains(text(), 'Stop Playing')]")
    TEST_SPEAKER1 = (By.XPATH, "//*[@LocalizedControlType='button' and contains(@Name, 'Test Speaker')]")
    TEST_SPEAKER = (By.XPATH, "//button/span[contains(text(),'Test') and contains(text(), 'peaker')]")
    REFER_TO_FAQ = (By.XPATH, "//a[text()='refer to our FAQs']")
    SPEAKER_BOOST = (By.XPATH, "//p[text()='Speaker Boost']/following-sibling::div[1]//input")
    AI_NOISE_SUPPRESSION = (By.XPATH, "//p[text()='AI Noise Suppression']/following-sibling::div[1]//input")
    REVERB_DISABLE_RADIO = (By.XPATH, "//p[text()='Reverb Control']/following-sibling::div[1]//p[text()='Disabled']"
                                      "/parent::div/preceding-sibling::span//input")
    REVERB_NORMAL_RADIO = (By.XPATH, "//p[text()='Reverb Control']/following-sibling::div[1]//"
                                     "p[text()='Normal (Recommended)']/parent::div/preceding-sibling::span//input")
    REVERB_AGGRESSIVE_RADIO = (By.XPATH, "//p[text()='Reverb Control']/following-sibling::div[1]"
                                         "//p[text()='Aggressive']/parent::div/preceding-sibling::span//input")
    MICROPHONE_BASS_BOOST = (By.XPATH, "//p[text()='Microphone EQ']/following-sibling::div[1]//"
                                       "p[text()='Bass Boost']/parent::div/preceding-sibling::span//input")
    MICROPHONE_NORMAL = (By.XPATH, "//p[text()='Microphone EQ']/following-sibling::div[1]//"
                                   "p[text()='Normal (Recommended)']/parent::div/preceding-sibling::span//input")
    MICROPHONE_VOICE_BOOST = (By.XPATH, "//p[text()='Microphone EQ']/following-sibling::div[1]//"
                                        "p[text()='Voice Boost']/parent::div/preceding-sibling::span//input")
    SPEAKER_BASS_BOOST = (By.XPATH, "//p[text()='Speaker EQ']/following-sibling::div[1]//"
                                    "p[text()='Bass Boost']/parent::div/preceding-sibling::span//input")
    SPEAKER_NORMAL = (By.XPATH, "//p[text()='Speaker EQ']/following-sibling::div[1]//"
                                "p[text()='Normal (Recommended)']/parent::div/preceding-sibling::span//input")
    SPEAKER_VOICE_BOOST = (By.XPATH, "//p[text()='Speaker EQ']/following-sibling::div[1]//"
                                     "p[text()='Voice Boost']/parent::div/preceding-sibling::span//input")
