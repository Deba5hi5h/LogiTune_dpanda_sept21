from dataclasses import dataclass
from typing import Optional, Tuple, List
from selenium.webdriver.common.by import By
from locators.tunes_ui_locators import TunesAppLocators


@dataclass
class TuneEnv:
    prod: str = 'prod'
    qa: str = 'qa'
    qa2: str = 'qa2'
    dev: str = 'dev'
    dev2: str = 'dev2'


@dataclass
class Device:
    device_name: str
    ota_api_product_name: str
    baseline_device_version: str
    target_device_version: str
    repeats: int
    baseline_dongle_version: Optional[str] = None
    target_dongle_version: Optional[str] = None
    dongle_address: Optional[str] = None
    baseline_eeprom_version: Optional[str] = None
    target_eeprom_version: Optional[str] = None
    baseline_tahiti_version: Optional[str] = None
    target_tahiti_version: Optional[str] = None
    jenkins_tune_env: Optional[str] = None

    def is_initialized(self, skip_dongle=False):
        errors = list()
        for attr, value in self.__dict__.items():
            if not value and value is not None:
                if (not skip_dongle and 'dongle' in attr) or 'dongle' not in attr:
                    errors.append(attr)
        if errors:
            raise AttributeError(f'There is missing value for attributes: {errors}')


@dataclass
class LanguageLocators:
    language_name: str
    button_locator: Tuple[str, str]
    radio_locator: Tuple[str, str]


class Languages:
    french = LanguageLocators(language_name="French",
                              button_locator=TunesAppLocators.FRENCH_BUTTON,
                              radio_locator=TunesAppLocators.FRENCH_RADIO)
    spanish = LanguageLocators(language_name="Spanish",
                               button_locator=TunesAppLocators.SPANISH_BUTTON,
                               radio_locator=TunesAppLocators.SPANISH_RADIO)
    german = LanguageLocators(language_name="German",
                              button_locator=TunesAppLocators.GERMAN_BUTTON,
                              radio_locator=TunesAppLocators.GERMAN_RADIO)
    italian = LanguageLocators(language_name="Italian",
                               button_locator=TunesAppLocators.ITALIAN_BUTTON,
                               radio_locator=TunesAppLocators.ITALIAN_RADIO)
    portuguese = LanguageLocators(language_name="Portuguese",
                                  button_locator=TunesAppLocators.PORTUGUESE_BUTTON,
                                  radio_locator=TunesAppLocators.PORTUGUESE_RADIO)
    english = LanguageLocators(language_name="English",
                               button_locator=TunesAppLocators.ENGLISH_BUTTON,
                               radio_locator=TunesAppLocators.ENGLISH_RADIO)


@dataclass
class LanguageUpdate:
    device_name: str
    repeats: int
    languages: List[Languages]
