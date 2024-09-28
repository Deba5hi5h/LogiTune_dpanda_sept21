from apps.tune_mobile.tune_mobile import TuneMobile
from apps.tune_mobile.tune_mobile_home import TuneMobileHome
from locators.tune_mobile.tune_mobile_voice_prompts_locators import TuneMobileVoicePromptsLocators


class TuneMobileVoicePrompts(TuneMobile):

    def click_close(self) -> TuneMobileHome:
        """
        Method to click Close

        :param :
        :return TuneMobileHome:
        """
        self.find_element(TuneMobileVoicePromptsLocators.CLOSE).click()
        return TuneMobileHome()

