
from apps.tune.custom import expected_conditions as cec
from datetime import datetime
from typing import Callable, List, Optional, Tuple, Union, Any
from common.platform_helper import get_custom_platform

import selenium.common.exceptions as exc
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from apps.tune.helpers import exception_handler
from extentreport.report import Report

import random
import re
import time
import cv2
import numpy as np


class TuneBasePage:

    def __init__(self, driver: Optional[WebDriver]):
        self._driver = driver
        self._found_element = list()

    @exception_handler
    def _send_keys(self, locator: Tuple[str, str], keys_input: str, timeout: int = 10,
                   locator_parameter: Optional[str] = None, strict_check: bool = True) -> None:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._wait_until_element_visible(locator, timeout).send_keys(keys_input)

    @exception_handler
    def _delete_input(self, locator: Tuple[str, str], timeout: int = 10,
                      locator_parameter: Optional[str] = None, strict_check: bool = True) -> None:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._wait_until_element_visible(locator, timeout).clear()

    @exception_handler
    def _is_checkbox_selected(self, locator: Tuple[str, str], timeout: int = 10,
                              locator_parameter: Optional[str] = None, strict_check: bool = True,
                              skip_exception: bool = False) -> bool:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        return self._wait_until_element_visible(locator, timeout).is_selected()

    @exception_handler
    def _delete_input_manually(self, locator: Tuple[str, str], timeout: int = 10,
                               locator_parameter: Optional[str] = None, strict_check: bool = True) -> None:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        element = self._wait_until_element_visible(locator, timeout)
        element.send_keys(Keys.LEFT_CONTROL + "a" if get_custom_platform() == "windows" else Keys.COMMAND + "a")
        element.send_keys(Keys.DELETE)

    @exception_handler
    def _click(self, locator: Tuple[str, str], timeout: int = 10,
               locator_parameter: Optional[str] = None, strict_check: bool = True,
               skip_exception: bool = False) -> None:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._wait_until_element_clickable(locator, timeout).click()

    @exception_handler
    def _click_with_retry(self, locator: Tuple[str, str], timeout: int = 10,
                          locator_parameter: Optional[str] = None, strict_check: bool = True,
                          skip_exception: bool = False, retries: int = 2) -> None:
        if retries == 0:
            raise exc.ElementNotInteractableException(
                f"Click on element {locator} was not possible")
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        try:
            WebDriverWait(self._driver, timeout).until(ec.element_to_be_clickable(locator)).click()
        except Exception as e:
            Report.logInfo(f'Exception occurred: {repr(e)} - {e}')
            self._click_with_retry(locator, timeout, locator_parameter, strict_check,
                                   skip_exception, retries - 1)

    @exception_handler
    def _get_element_by_text(self, locator: Tuple[str, str], expected_text: str,
                             timeout: int = 10, locator_parameter: Optional[str] = None,
                             strict_check: bool = True, expected_text_strict_check: bool = True,
                             match_case: bool = True, skip_exception: bool = False) -> WebElement:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._wait_until_element_visible(locator, timeout)
        found_elements = self._driver.find_elements(*locator)
        for element in found_elements:
            current_element_text = element.text if match_case else element.text.lower()
            result = current_element_text == expected_text if expected_text_strict_check \
                else expected_text in current_element_text
            if result:
                return element
        raise exc.NoSuchElementException(f'Element not found with text: "{expected_text}"')

    @exception_handler
    def _get_element_from_element(self, element: WebElement, locator: Tuple[str, str],
                                  skip_exception: bool = False) -> WebElement:
        return element.find_element(*locator)

    @exception_handler
    def _click_by_element_text(self, locator: Tuple[str, str], expected_text: str,
                               timeout: int = 10, locator_parameter: Optional[str] = None,
                               strict_check: bool = True, expected_text_strict_check: bool = True,
                               match_case: bool = True, skip_exception: bool = False) -> None:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._get_element_by_text(locator=locator,
                                  timeout=timeout,
                                  expected_text=expected_text,
                                  strict_check=strict_check,
                                  expected_text_strict_check=expected_text_strict_check,
                                  ).click()

    @exception_handler
    def _click_elements_button_by_element_text(self, locator: Tuple[str, str], expected_text: str,
                                               button_relative_locator: Tuple[str, str],
                                               timeout: int = 10, locator_parameter: Optional[str] = None,
                                               strict_check: bool = True, expected_text_strict_check: bool = True,
                                               match_case: bool = True) -> None:

        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._wait_until_element_visible(locator, timeout)
        found_elements = self._driver.find_elements(*locator)
        for element in found_elements:
            current_element_text = element.text if match_case else element.text.lower()
            result = current_element_text == expected_text if expected_text_strict_check \
                else expected_text in current_element_text
            if result:
                found_button = element.find_element(*button_relative_locator)
                return found_button.click()
        Report.logWarning(f'Element not found with text: "{expected_text}"')
        raise exc.NoSuchElementException

    @exception_handler
    def _click_random_element(self, locator: Tuple[str, str], timeout: int = 10,
                              skip_exception: bool = False) -> None:
        elements = self._get_all_available_elements(locator, timeout=timeout)
        element = random.choice(elements)
        element.click()

    @exception_handler
    def _get_text(self, locator: Tuple[str, str], timeout: int = 10,
                  locator_parameter: Optional[str] = None, strict_check: bool = True) -> str:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        return self._wait_until_element_visible(locator, timeout).text

    @exception_handler
    def _is_visible(self, locator: Tuple[str, str], timeout: int = 10,
                    locator_parameter: Optional[str] = None, strict_check: bool = True) -> bool:
        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            self._wait_until_element_visible(locator, timeout)
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _is_clickable_by_text(self, locator: Tuple[str, str],
                              expected_text: str,
                              timeout: int = 10,
                              locator_parameter: Optional[str] = None, strict_check: bool = True) -> bool:
        def clickability_of_element_with_text(_drv: WebDriver):
            elements: List[WebElement] = _drv.find_elements(*locator)
            found_element = [el for el in elements if el.text == expected_text]
            if found_element:
                found_element_web: WebElement = next(iter(found_element))
                return found_element_web.is_enabled() and found_element_web.is_displayed()
            else:
                return False

        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            WebDriverWait(self._driver, timeout).until(clickability_of_element_with_text)
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _is_visible_by_text(self, locator: Tuple[str, str],
                            expected_text: str,
                            timeout: int = 10,
                            locator_parameter: Optional[str] = None,
                            strict_check: bool = True,
                            expected_text_strict_check: bool = True) -> bool:

        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            WebDriverWait(self._driver, timeout).until(
                cec.visibility_of_element_with_text(locator, expected_text, expected_text_strict_check))
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _click_any_element_by_text(self, expected_text: str, timeout: int = 10,
                                   expected_text_strict_check: bool = True) -> None:

        locator = update_xpath_locator(('xpath', f'//*[text()=\'{expected_text}\']'), None,
                                       expected_text_strict_check)
        self._wait_until_element_visible(locator, timeout=timeout).click()

    @exception_handler
    def _is_any_element_by_text(self, expected_text: str, timeout: int = 10,
                                expected_text_strict_check: bool = True) -> bool:

        locator = update_xpath_locator(('xpath', f'//*[text()=\'{expected_text}\']'), None,
                                       expected_text_strict_check)
        return self._is_visible(locator, timeout=timeout)

    @exception_handler
    def _is_not_visible_by_text(self, locator: Tuple[str, str],
                                expected_text: str,
                                timeout: int = 10,
                                locator_parameter: Optional[str] = None,
                                strict_check: bool = True,
                                expected_text_strict_check: bool = True) -> bool:

        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            WebDriverWait(self._driver, timeout).until_not(
                cec.visibility_of_element_with_text(locator, expected_text, expected_text_strict_check))
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _is_any_element_by_text(self, expected_text: str, timeout: int = 10,
                                expected_text_strict_check: bool = True) -> bool:

        locator = update_xpath_locator(('xpath',  f'//*[text()=\'{expected_text}\']'), None,
                                       expected_text_strict_check)
        return self._is_visible(locator, timeout=timeout)

    @exception_handler
    def _is_clickable(self, locator: Tuple[str, str], timeout: int = 10,
                      locator_parameter: Optional[str] = None, strict_check: bool = True) -> bool:
        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            WebDriverWait(self._driver, timeout).until(ec.element_to_be_clickable(locator))
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _is_not_visible(self, locator: Tuple[str, str], timeout: int = 10,
                        locator_parameter: Optional[str] = None, strict_check: bool = True) -> bool:
        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            self._wait_until_element_not_visible(locator, timeout)
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _one_of_provided_is_visible(self, *locators: Tuple[str, str], timeout: int = 10,
                                    locator_parameter: Optional[str] = None,
                                    strict_check: bool = True) -> bool:
        new_locators = list()
        try:
            for base_locators in locators:
                new_locators.append(update_xpath_locator(
                    base_locators, locator_parameter, strict_check))
            WebDriverWait(self._driver, timeout).until(lambda: self._find_element(*new_locators))
            return True
        except exc.TimeoutException:
            return False

    @exception_handler
    def _get_attribute_of_xpath_locator(self, locator: Tuple[str, str],
                                        attribute: str,
                                        timeout: int = 10,
                                        locator_parameter: Optional[str] = None,
                                        strict_check: bool = True) -> Optional[str]:

        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        element = self._wait_until_element_present(locator, timeout)
        return element.get_attribute(attribute)

    @exception_handler
    def _wait_for_attribute_in_element(self, element: WebElement, attribute_name: str,
                                       attribute_value: str,
                                       timeout: float = 10):
        return WebDriverWait(self._driver, timeout).until(lambda driver:
                                                          element.get_attribute(attribute_name) == attribute_value)

    @exception_handler
    def _wait_for_attribute_in_element_by_text(self, locator: Tuple[str, str],
                                               expected_text: str,
                                               attribute_name: str,
                                               attribute_value: str,
                                               timeout: int = 10,
                                               locator_parameter: Optional[str] = None,
                                               strict_check: bool = True,
                                               expected_text_strict_check: bool = True,
                                               ) -> bool:

        element = self._get_element_by_text(locator, expected_text, timeout, locator_parameter,
                                            strict_check, expected_text_strict_check)
        try:
            return self._wait_for_attribute_in_element(element, attribute_name, attribute_value, timeout)
        except exc.TimeoutException:
            return False

    @exception_handler
    def _wait_for_multiple_elements_visibility(self, locator: Tuple[str, str],
                                               timeout: int = 10,
                                               no_elements: int = 1,
                                               comparison: str = "==",
                                               locator_parameter: Optional[str] = None,
                                               strict_check: bool = True) -> List[WebElement]:
        """
        Args:
            locator: A tuple containing the locator strategy and value for locating the elements.
            timeout: An integer specifying the maximum time to wait for the elements to become visible
            (default is 10 seconds).
            no_elements: An integer specifying the number of elements expected to be visible (default is 1).
            comparison: A string indicating the type of comparison to perform for the number of visible elements.
            Valid values are "==", ">", and "<". Default is "==".
            locator_parameter: An optional string parameter that can be used to dynamically update the locator value.
            strict_check: A boolean indicating whether to perform a strict check for visible elements.

        Returns:
            A list of WebElement objects representing the visible elements that match the given locator.

        """

        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            return WebDriverWait(self._driver, timeout).until(cec.visibility_elements_check(
                locator, no_elements, comparison))
        except exc.TimeoutException:
            return []

    @exception_handler
    def _wait_for_multiple_elements_presence(self, locator: Tuple[str, str],
                                             timeout: int = 10,
                                             no_elements: int = 1,
                                             comparison: str = "==",
                                             locator_parameter: Optional[str] = None,
                                             strict_check: bool = True) -> Optional[List[WebElement]]:

        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            return WebDriverWait(self._driver, timeout).until(cec.presence_elements_check(
                locator, no_elements, comparison
            ))

        except exc.TimeoutException:
            return []

    def _scroll_to_element(self, element: WebElement) -> None:
        self._driver.execute_script("arguments[0].scrollIntoView(true);", element)

    @exception_handler
    def _scroll_to_element_by_element_text(self, locator: Tuple[str, str], expected_text: str,
                                           timeout: int = 10,
                                           locator_parameter: Optional[str] = None,
                                           strict_check: bool = True,
                                           expected_text_strict_check: bool = True,
                                           skip_exception: bool = False) -> WebElement:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        self._wait_until_element_visible(locator, timeout)
        found_elements = self._driver.find_elements(*locator)
        for element in found_elements:
            result = element.text == expected_text if expected_text_strict_check \
                else expected_text in element.text
            if result:
                WebDriverWait(self._driver, 2)
                self._scroll_to_element(element)
                return element
        Report.logInfo(f'Element not found with text: "{expected_text}"')

    @exception_handler
    def _get_css_value_of_xpath_locator(self, locator: Tuple[str, str],
                                        attribute: str,
                                        timeout: int = 10,
                                        locator_parameter: Optional[str] = None,
                                        strict_check: bool = True) -> Optional[str]:

        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        element = self._wait_until_element_present(locator, timeout)
        return element.value_of_css_property(attribute)

    @exception_handler
    def _get_element_from_one_of_provided(self, *locators: Tuple[str, str], timeout: int = 10,
                                          locator_parameter: Optional[str] = None,
                                          strict_check: bool = True) -> WebElement:
        new_locators = list()
        for base_locators in locators:
            new_locators.append(update_xpath_locator(
                base_locators, locator_parameter, strict_check))
        WebDriverWait(self._driver, timeout).until(
            lambda: self._find_element(*new_locators, return_element=True))
        return self._found_element.pop(0)

    @exception_handler
    def _get_all_available_elements(self, locator: Tuple[str, str],
                                    boundaries: Tuple[Optional[int], Optional[int]] = (None, None),
                                    locator_parameter: Optional[str] = None,
                                    strict_check: bool = True, timeout: int = 10
                                    ) -> List[WebElement]:
        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            self._wait_until_element_visible(locator, timeout=timeout)
            found_elements: List[WebElement] = self._driver.find_elements(*locator)[slice(*boundaries)]
            return found_elements
        except exc.TimeoutException:
            return []

    @exception_handler
    def _compare_text(self, locator: Tuple[str, str], expected_text: str,
                      strict_text_check: bool = True, timeout: int = 10,
                      locator_parameter: Optional[str] = None, strict_check: bool = True) -> bool:
        locator = update_xpath_locator(locator, locator_parameter, strict_check)
        visible_text = self._wait_until_element_visible(locator, timeout).text

        return expected_text == visible_text if strict_text_check \
            else expected_text in visible_text

    @exception_handler
    def _verify_all_found_elements_values(self, locator: Tuple[str, str],
                                          expected_values: List[Any],
                                          parameter_function: str = 'get_attribute',
                                          parameter_name: str = 'textContent',
                                          timeout: int = 10,
                                          strict_elements_order_check: bool = False,
                                          boundaries: Tuple[Optional[int], Optional[int]] = (None, None),
                                          locator_parameter: Optional[str] = None,
                                          strict_check: bool = True,
                                          expected_text_strict_check: bool = True) -> bool:
        missing_values = list()
        all_elements_present = True
        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            self._wait_until_element_visible(locator, timeout)
            found_elements_raw: List[WebElement] = [element for element
                                                    in self._driver.find_elements(*locator)][slice(*boundaries)]
            found_elements = [element.wrapped_element.__getattribute__(parameter_function)(parameter_name)
                              for element in found_elements_raw]
            if strict_elements_order_check:
                compare_result = found_elements == expected_values
                if not compare_result:
                    Report.logInfo(f"Expected lists: {expected_values} and {found_elements} differ")
                return compare_result
            for expected_value in expected_values:
                if expected_value not in found_elements and expected_text_strict_check:
                    missing_values.append(expected_value)
                    all_elements_present = False
                elif not expected_text_strict_check:
                    missing_element_found = True
                    for found_value in found_elements:
                        if expected_value in found_value:
                            missing_element_found = False
                            break
                    if missing_element_found:
                        missing_values.append(expected_value)
                        all_elements_present = False

            if not all_elements_present:
                Report.logInfo(f"Expected values: {missing_values} not found within found values: "
                               f"{found_elements}")
            return all_elements_present
        except exc.TimeoutException:
            return False

    def _update_driver(self, driver: WebDriver) -> None:
        self._driver = driver

    def _reorder_items(self, locator: Tuple[str, str], item_name: str, order_number: int,
                       drag_locator: Optional[Tuple[str, str]] = None) -> None:
        elements = self._get_all_available_elements(locator)
        if drag_locator is None:
            drag_locator = locator
        drag_elements = self._get_all_available_elements(drag_locator)

        source_element = None
        source_position = None
        for idx, element in enumerate(elements):
            if item_name in element.text:
                source_element = element
                source_position = idx
                break

        if source_element is None:
            raise exc.NoSuchElementException(f"Item '{item_name}' not found")

        if 0 > order_number >= len(elements):
            raise exc.MoveTargetOutOfBoundsException(f"Invalid position {order_number}. Valid "
                                                     f"positions are 0 to {len(elements) - 1}")

        actions = ActionChains(self._driver)
        actions.drag_and_drop(drag_elements[source_position].wrapped_element,
                              elements[order_number].wrapped_element)
        actions.perform()

    @exception_handler
    def wait_for_rounded_minute(self):
        WebDriverWait(self._driver, 60).until(lambda x: datetime.now().second % 60 == 0)
        WebDriverWait(self._driver, 5).until(lambda x: datetime.now().second % 60 != 0)

    @exception_handler
    def wait_seconds_to_pass(self, seconds_to_pass: int):
        time_now = datetime.now()
        WebDriverWait(self._driver, 60).until(
            lambda x: (datetime.now() - time_now).seconds >= seconds_to_pass)

    @exception_handler
    def _find_green_circles_on_element(self, element: WebElement) -> Tuple:
        el_png = element.screenshot_as_png
        image = cv2.imdecode(np.frombuffer(el_png, np.uint8), cv2.IMREAD_COLOR)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_green = np.array([45, 100, 100])
        upper_green = np.array([75, 255, 255])

        mask = cv2.inRange(hsv_image, lower_green, upper_green)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        dot_centers = []
        height, width, _, _ = element.rect.values()

        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            x -= width//2 - 7
            y -= height//2
            if radius > 5:
                dot_centers.append((int(x), int(y)))

        return tuple(dot_centers)

    @exception_handler
    def _drag_and_drop_by_coordinates(self, source: WebElement, target: WebElement,
                                      scroll_visible_area: WebElement, scroll_area: WebElement,
                                      y_offset: int, time_range_box: WebElement,
                                      is_drag_start_locator: bool = False) -> None:
        """
        This method performs drag and drop operation using the specified coordinates.
        It scrolls to a certain point before performing the drag and drop.
        The method waits for 1 second before execution, so all animations will be done on
        the DOM before running this method.

        Args:
            source: WebElement - The element to be dragged.
            target: WebElement - The element where the source element will be dropped.
            scroll_visible_area: WebElement - The visible area where scrolling will be performed.
            scroll_area: WebElement - The scrollable area.
            y_offset: int - The y-coordinate offset for scrolling.
            time_range_box: WebElement - The date range element used for offset calculation.
            is_drag_start_locator: bool (optional) - Flag indicating if the source element is
                                   the drag start locator. Default is False.
        """
        time.sleep(1)

        # Drag constant added, as calculating position of the drag element from other valid elements
        # is always off by some pixels, and adding this "constant" makes it work way better
        drag_constant = 12

        # Calculating drag offset, so the start/end of the time range box will be ideally
        # at the point of the provided start/end time
        offset = drag_constant + source.location.get('y') - time_range_box.location.get('y')

        # Checking, if the drag locator is for the start or the end of the time range
        if not is_drag_start_locator:
            offset -= time_range_box.size.get('height')

        # Calculating middle point of visible scroll area of the source element
        scroll_visible_area_height = scroll_visible_area.size.get('height')
        middle_point = (int(source.location.get('y')) - scroll_area.location.get('y') - int(
            scroll_visible_area_height / 2))

        self._driver.execute_script(f"arguments[0].scrollTo(0, {middle_point});",
                                    scroll_visible_area)

        try:
            # Clicking down on the source element and holding it until release
            action = ActionChains(self._driver)
            action.w3c_actions = ActionBuilder(self._driver)
            action.w3c_actions.pointer_action.move_to_location(**source.location)
            action.w3c_actions.pointer_action.pointer_down()
            action.perform()

            # Calculating middle point of visible scroll area of the target element
            scroll_visible_area_height = scroll_visible_area.size.get('height')
            middle_point = (int(target.location.get('y')) - scroll_area.location.get('y') - int(
                scroll_visible_area_height / 2))
            self._driver.execute_script(f"arguments[0].scrollTo(0, {middle_point});",
                                        scroll_visible_area)

            # Moving source element to the target element and releasing it
            action.w3c_actions.pointer_action.move_to_location(
                target.location.get('x'), target.location.get('y') + y_offset + offset
            )
            action.w3c_actions.pointer_action.pointer_up()
            action.perform()
        except Exception as e:
            Report.logInfo(f'Exception in drag and drop: {repr(e)} - {e}')

    @exception_handler
    def _get_element_by_text(self, locator: Tuple[str, str],
                             expected_text: str,
                             timeout: int = 10,
                             locator_parameter: Optional[str] = None,
                             strict_check: bool = True,
                             expected_text_strict_check: bool = True) -> Optional[WebElement]:

        try:
            locator = update_xpath_locator(locator, locator_parameter, strict_check)
            return WebDriverWait(self._driver, timeout).until(
                                cec.visibility_of_element_with_text(locator, expected_text, expected_text_strict_check))
        except exc.TimeoutException:
            return None

    @exception_handler
    def _get_element_coordinates_and_size(self, locator: Tuple[str, str]) -> dict:
        element = self._wait_until_element_visible(locator)
        return {**element.location, **element.size}

    @exception_handler
    def _scroll_into_view(self, element_locator: Tuple[str, str],
                          scroll_area_locator: Tuple[str, str]) -> None:
        element = self._wait_until_element_visible(element_locator)
        scroll_area = self._wait_until_element_visible(scroll_area_locator)
        self._driver.execute_script("arguments[0].scrollTo(0, 0);", scroll_area)
        self._driver.execute_script(
            "arguments[0].scrollTo(0, arguments[1]);",
            scroll_area,
            element.rect['y'] - scroll_area.rect['y'] - element.rect['height']
        )

    @exception_handler
    def _change_slider_value(self, slider_locator: Tuple[str, str],
                             scroll_area_locator: Tuple[str, str], value: int,
                             slider_inverted: bool = False) -> None:
        self._scroll_into_view(slider_locator, scroll_area_locator)
        self._click_on_slider_for_given_value(slider_locator, value, inverted=slider_inverted)

    @exception_handler
    def _check_slider_value(self, slider_locator: Tuple[str, str]) -> Optional[int]:
        return int(self._wait_until_element_visible(slider_locator).get_attribute('value'))

    def _wait_until_element_visible(self, locator: Tuple[str, str], timeout: int = 10
                                    ) -> WebElement:
        """
        Inner helper method used only within BasePage methods implementation
        Args:
            locator: tuple containing locator of element which should be waited for
            timeout: int (default: 10) in seconds how much time should runner wait before raising
                timeout exception

        Returns:
            WebElement which was found
        """
        return WebDriverWait(self._driver, timeout).until(ec.visibility_of_element_located(locator))

    def _wait_until_element_clickable(self, locator: Tuple[str, str], timeout: int = 10
                                      ) -> WebElement:
        """
        Inner helper method used only within BasePage methods implementation
        Args:
            locator: tuple containing locator of element which should be waited for
            timeout: int (default: 10) in seconds how much time should runner wait before raising
                timeout exception

        Returns:
            WebElement which was found
        """
        return WebDriverWait(self._driver, timeout).until(ec.element_to_be_clickable(locator))

    def _wait_until_statement_is_valid(self, method: Callable,
                                       args: Union[tuple, list, None] = None,
                                       statement_result: bool = True,  timeout: int = 10,
                                       skip_exception: bool = False) -> bool:
        """
        Args:
            method: A function or method to be called repeatedly until a certain condition is met.
            args: Optional. Arguments to be passed to the method.
            statement_result: Optional. The expected result of the method call. Defaults to True.
            timeout: Optional. The maximum time to wait in seconds. Defaults to 10.

        Returns:
            bool: True if the statement becomes valid within the timeout period, False otherwise.
        """
        if args is None:
            args = list()
        try:
            return WebDriverWait(self._driver, timeout).until(
                lambda _: method(*args) is statement_result)
        except exc.TimeoutException as e:
            if not skip_exception:
                raise e

    def _wait_until_element_present(self, locator: Tuple[str, str], timeout: int = 10
                                    ) -> WebElement:
        """
        Inner helper method used only within BasePage methods implementation
        Args:
            locator: tuple containing locator of element which should be waited for
            timeout: int (default: 10) in seconds how much time should runner wait before raising
                timeout exception

        Returns:
            WebElement which was found
        """
        return WebDriverWait(self._driver, timeout).until(ec.presence_of_element_located(locator))

    def _wait_until_element_not_visible(self, locator: Tuple[str, str], timeout: int = 10
                                        ) -> Optional[WebElement]:
        """
        Inner helper method used only within BasePage methods implementation
        Args:
            locator: tuple containing locator of element which should be waited for
            timeout: int (default: 10) in seconds how much time should runner wait before raising
                timeout exception

        Returns:
            WebElement which was found
        """
        try:
            return WebDriverWait(self._driver, timeout).until_not(ec.visibility_of_element_located(locator))
        except exc.TimeoutException:
            return None

    def _find_element(self, *locators: Tuple[str, str], return_element: bool = False) -> bool:
        """
        Inner helper method used only within BasePage methods implementation
        Args:
            locators: tuples containing locators of elements which should be searched for
            return_element: bool used to decide whether return found element in self._found_element
                list or not
        Returns:
            bool - info whether element was found or not
        """
        expected_conditions = [ec.visibility_of_element_located(locator) for locator in locators]
        if any(expected_conditions):
            for locator in locators:
                try:
                    if return_element:
                        self._found_element.append(self._driver.find_element(*locator))
                    return True
                except exc.NoSuchElementException:
                    pass
                except Exception as e:
                    Report.logException(f"Exception {self._find_element.__name__} - {locator}")
                    raise e
            return False
        else:
            return False

    def _click_on_element_with_offset(self, element: WebElement, offset: Tuple[int, int]) -> None:
        ActionChains(self._driver).move_to_element_with_offset(element, *offset).click().perform()

    def _click_on_slider_for_given_value(self, slider_locator: Tuple[str, str], value: int,
                                         inverted: bool = False) -> None:
        """
        Inner helper method used to change slider value by clicking on it at the
        calculated position.

        For inverted slider (rotated 270 degrees - used in headset equalizer settings),
        some tunings were needed to make this method to work.

        Args:
            slider_locator: A Tuple representing the locator of the slider element.
            value: An integer representing the value to set on the slider.
            inverted: A boolean indicating whether the slider is inverted or not. Default is False.

        Returns:
            None
        """
        slider = self._wait_until_element_visible(slider_locator)
        min_border = int(slider.get_attribute('min'))
        max_border = int(slider.get_attribute('max'))
        slider_rect = slider.rect
        a = slider_rect['width'] / (max_border - min_border)
        b = -(a * min_border)
        x = round(a * value + b)
        y_mid = round(slider_rect['height'] / 2)
        if inverted:
            parent_element = slider.find_element('xpath', value="./..")
            slider_base_scale = int(slider.rect['width']*0.9)
            slider = parent_element
            slider_rect = slider.rect
            loc_x, loc_y = slider.location['x'], slider.location['y']
            center_x, center_y = loc_x + slider_rect['width']/2, loc_y + slider_rect['height']/2
            y_max = center_y-slider_base_scale//2
            y_min = center_y+slider_base_scale//2
            value_to_set = value / 100 * abs(y_max - y_min)
            offset_from_middle = slider_rect['height'] // 2
            click_y = value_to_set - offset_from_middle
            ActionChains(self._driver).move_to_element_with_offset(
                slider.wrapped_element, 0, click_y).click().perform()
        else:
            ActionChains(self._driver).move_to_element_with_offset(
                slider.wrapped_element, x - slider_rect['width'] / 2, y_mid).click().perform()


def update_xpath_locator(locator: Tuple[str, str],
                         locator_parameter: Optional[str],
                         strict_check: bool) -> Tuple[str, str]:
    """
    Function used for updating xpath locator - replacing locator parameter of
    the xpath (if available - replacing 'XXX' string) and recreating xpath for
    strict ('=') or loose ('contains()') check.
    Args:
        locator: Tuple of By.XPATH element and xpath string
        locator_parameter: String with parameter to replace 'XXX' string in xpath
        strict_check: Boolean flag to choose between strict (True) and loose (False) check

    Returns:
        Tuple of By.XPATH element and updated xpath string
    """
    if locator_parameter is not None:
        locator = _create_locator_with_parameter(locator, locator_parameter)
    if not strict_check:
        locator = _create_loose_checking_of_xpath_locator(locator)
    return locator


def _create_locator_with_parameter(locator: Tuple[str, str],
                                   locator_parameter: Optional[str]) -> Tuple[str, str]:
    try:
        locator_by_element, locator_string_element = locator
        if 'XXX' not in locator_string_element:
            # TODO: implement custom exceptions and change it after
            raise ValueError("Provided locator doesn't have 'XXX' substring.")
        return locator_by_element, locator_string_element.replace('XXX', locator_parameter)
    except Exception as e:
        Report.logException(f'{_create_locator_with_parameter.__name__} - {repr(e)}')
        raise e


def _create_loose_checking_of_xpath_locator(locator: Tuple[str, str]) -> Tuple[str, str]:
    """
    Function used for recreating xpath to use strict ('=') or loose ('contains()') check.
    Args:
        locator: Tuple of By.XPATH element and xpath string

    Returns:
        Tuple of By.XPATH element and updated xpath string
    """
    try:
        locator_by_element, locator_string_element = locator
        expression, attr, value = re.search(r"\[((.*)='(.*)')]", locator_string_element).groups()
        new_element = locator_string_element.replace(expression, f"contains({attr}, '{value}')")
        return locator_by_element, new_element
    except Exception as e:
        Report.logException(f'{_create_loose_checking_of_xpath_locator.__name__} - {repr(e)}')
        raise e
