from typing import Optional

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from apps.tune.helpers import get_python_version
if get_python_version() >= 312:
    from apps.win_app_driver_reworked import WinAppDriverAppiumOptions, element_json_to_web_element


class GetDriverForOpenApp:
    def __init__(self):
        self.driver = None
        self.desired_cap = {"app": "Root"}

    def getDriver(self, app_name: str) -> Optional[WebDriver]:
        if get_python_version() < 312:
            return self._get_driver_37(app_name)
        else:
            return self._get_driver_312(app_name)

    def getBrowserDriver(self) -> Optional[WebDriver]:
        if get_python_version() < 312:
            return self._get_browser_driver_37()
        else:
            return self._get_browser_driver_312()

    def _get_driver_37(self, app_name: str) -> Optional[WebDriver]:
        desktop_session = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                           desired_capabilities=self.desired_cap)
        app = desktop_session.find_element(By.NAME, app_name)
        win_handle = int(app.get_attribute("NativeWindowHandle"))
        win_handle_hex = f"{win_handle:x}"

        desired_cap_app_window = {"appTopLevelWindow": win_handle_hex}
        try:
            self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                           desired_capabilities=desired_cap_app_window)
        except Exception:
            return None
        return self.driver

    def _get_driver_312(self, app_name: str) -> Optional[WebDriver]:
        options_root = WinAppDriverAppiumOptions().load_capabilities(self.desired_cap)
        desktop_session = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                           direct_connection=False, options=options_root)

        app = desktop_session.find_element(By.NAME, app_name)
        app = element_json_to_web_element(desktop_session, app)
        win_handle = int(app.get_attribute("NativeWindowHandle"))
        win_handle_hex = f"{win_handle:x}"
        desired_cap_app_window = {"appTopLevelWindow": win_handle_hex}
        options_control = WinAppDriverAppiumOptions().load_capabilities(desired_cap_app_window)
        try:
            self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                           direct_connection=False, options=options_control)
        except Exception:
            return None
        return self.driver

    def _get_browser_driver_37(self) -> Optional[WebDriver]:
        desktop_session = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                           desired_capabilities=self.desired_cap)
        app = desktop_session.find_element(By.XPATH, "//*[@ClassName='Chrome_WidgetWin_1']")
        win_handle = int(app.get_attribute("NativeWindowHandle"))
        win_handle_hex = f"{win_handle:x}"

        desired_cap_app_window = {"appTopLevelWindow": win_handle_hex}
        self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                       desired_capabilities=desired_cap_app_window)
        return self.driver

    def _get_browser_driver_312(self) -> Optional[WebDriver]:
        options_root = WinAppDriverAppiumOptions().load_capabilities(self.desired_cap)
        desktop_session = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                           direct_connection=False, options=options_root)
        app = desktop_session.find_element(By.XPATH, "//*[@ClassName='Chrome_WidgetWin_1']")
        win_handle = int(app.get_attribute("NativeWindowHandle"))
        win_handle_hex = f"{win_handle:x}"

        desired_cap_app_window = {"appTopLevelWindow": win_handle_hex}
        options_control = WinAppDriverAppiumOptions().load_capabilities(desired_cap_app_window)
        self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                                       direct_connection=False, options=options_control)
        return self.driver
