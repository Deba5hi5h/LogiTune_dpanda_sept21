from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from typing import List, Tuple


class visibility_elements_check:
    def __init__(self, locator: Tuple[str, str], no_elements: int, comparison: str):
        self.locator = locator
        self.no_elements = no_elements
        self.comparison = comparison

    def __call__(self, driver: WebDriver):
        elements: List[WebElement] = driver.find_elements(*self.locator)
        visible_elements: List[WebElement] = [el for el in elements if el.is_displayed()]
        if self.comparison == ">":
            return visible_elements if len(visible_elements) > self.no_elements else None
        elif self.comparison == "<":
            return visible_elements if len(visible_elements) < self.no_elements else None
        else:
            return visible_elements if len(visible_elements) == self.no_elements else None


class presence_elements_check:
    def __init__(self, locator: Tuple[str, str], no_elements: int, comparison: str):
        self.locator = locator
        self.no_elements = no_elements
        self.comparison = comparison

    def __call__(self, driver: WebDriver):
        elements: List[WebElement] = driver.find_elements(*self.locator)
        if self.comparison == ">":
            return elements if len(elements) > self.no_elements else None
        elif self.comparison == "<":
            return elements if len(elements) < self.no_elements else None
        else:
            return elements if len(elements) == self.no_elements else None


class visibility_of_element_with_text:
    def __init__(self, locator: Tuple[str, str], expected_text: str, expected_text_strict_check: bool):
        self.locator = locator
        self.expected_text = expected_text
        self.expected_text_strict_check = expected_text_strict_check

    def __call__(self, driver: WebDriver):
        elements: List[WebElement] = driver.find_elements(*self.locator)
        found_element = [el for el in elements if (lambda x: self.expected_text == x.text
                                                   if self.expected_text_strict_check
                                                   else self.expected_text in x.text)(el)]
        if found_element:
            found_element_web: WebElement = next(iter(found_element))
            if found_element_web.is_enabled() and found_element_web.is_displayed():
                return found_element_web
        else:
            return False
