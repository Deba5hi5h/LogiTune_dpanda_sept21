from appium.webdriver.webdriver import WebDriver
from appium.options.common.base import AppiumOptions, T
from appium.webdriver.webelement import WebElement
import copy

from typing import Any, Dict, Union


class WinAppDriverAppiumOptions(AppiumOptions):
    def set_capability(self: T, name: str, value: Any) -> T:
        w3c_name = name
        if value is None:
            if w3c_name in self._caps:
                del self._caps[w3c_name]
        else:
            self._caps[w3c_name] = value
        return self

    def get_capability(self, name: str) -> Any:
        """Fetches capability value or None if the capability is not set"""
        return self._caps[name]

    @staticmethod
    def as_w3c(capabilities: Dict) -> Dict:
        """
        Formats given capabilities to a valid W3C session request object

        :param capabilities: Capabilities mapping
        :return: W3C session request object
        """

        def process_key(k: str) -> str:
            key = AppiumOptions._OSS_W3C_CONVERSION.get(k, k)
            if key in AppiumOptions.W3C_CAPABILITY_NAMES:
                return key
            return key if ':' in key else f'{key}'

        processed_caps = {process_key(k): v for k, v in copy.deepcopy(capabilities).items()}
        return {'desiredCapabilities': processed_caps,
                'capabilities': {'firstMatch': [processed_caps]}}

    def to_capabilities(self) -> T:
        return self

    def to_w3c(self) -> Dict:
        """
        Formats the instance to a valid W3C session request object

        :return: W3C session request object
        """
        return self.as_w3c(self.to_caps())

    def to_caps(self) -> Dict:
        return copy.copy(self._caps)


def element_json_to_web_element(session: WebDriver, element: Union[dict, WebElement]
                                ) -> Union[WebElement, dict, list]:
    if isinstance(element, dict):
        valid_app = {'element-6066-11e4-a52e-4f735466cecf': element.get('ELEMENT')}
        return session._unwrap_value(valid_app)
    return element
