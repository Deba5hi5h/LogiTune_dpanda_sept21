from typing import Tuple, Optional, Union

from selenium.webdriver.common.by import By

from locators.base.attributes import HtmlAttribute
from locators.base.elements import HtmlElement


def path_by_tag_name(tag_name_str: str) -> Tuple[str, str]:
    """
    Args:
        tag_name_str (str): The name of the HTML tag to locate.

    Returns:
        Tuple[str, str]: A tuple containing two strings. The first string is
        the locator strategy 'By.TAG_NAME', and the second string is the value of 'tag_name_str'.
    """
    return By.TAG_NAME, tag_name_str


def xpath_by_class(element: HtmlElement, attribute_value: str, *child_locators: str,
                   strict_check: bool = True) -> Tuple[str, str]:
    """
    Function for creating locator tuple used by Selenium to locate element in Tune.
    By default, xpath attribute looks for "class"
    Args:
        element: HtmlElement - Frontend element which should be located
        attribute_value: str - value of the "class" attribute which should be located
        child_locators: str - child locators of the main locator
        strict_check: bool - defines if attribute_value should be equal ('=')
                      or should be contained ('contains()') within searched locator

    Returns: Tuple[str, str] - valid locator used by Selenium to locate element
    """
    return By.XPATH, _attribute_xpath(element, HtmlAttribute.class_,
                                      attribute_value, *child_locators,
                                      strict_check=strict_check)


def xpath_by_data_testid(element: HtmlElement, attribute_value: str, *child_locators: Union[HtmlElement, str],
                         strict_check: bool = True, index: Optional[int] = None) -> Tuple[str, str]:
    """
    Function for creating locator tuple used by Selenium to locate element in Tune.
    By default, xpath attribute looks for "data-testid"
    Args:
        element: HtmlElement - Frontend element which should be located
        attribute_value: str - value of the "data-testid" attribute which should be located
        child_locators: Union[HtmlElement, str] - child locators of the main locator
        strict_check: bool - defines if attribute_value should be equal ('=')
                      or should be contained ('contains()') within searched locator
        index: bool - index of the found element if found multiple

    Returns: Tuple[str, str] - valid locator used by Selenium to locate element
    """
    return By.XPATH, _attribute_xpath(element, HtmlAttribute.data_testid,
                                      attribute_value, *child_locators,
                                      strict_check=strict_check,
                                      index=index)


def xpath_by_id(element: HtmlElement, attribute_value: str, *child_locators: str,
                strict_check: bool = True) -> Tuple[str, str]:
    """
    Function for creating locator tuple used by Selenium to locate element in Tune.
    By default, xpath attribute looks for "id"
    Args:
        element: HtmlElement - Frontend element which should be located
        attribute_value: str - value of the "id" attribute which should be located
        child_locators: str - child locators of the main locator
        strict_check: bool - defines if attribute_value should be equal ('=')
                      or should be contained ('contains()') within searched locator

    Returns: Tuple[str, str] - valid locator used by Selenium to locate element
    """
    return By.XPATH, _attribute_xpath(element, HtmlAttribute.id,
                                      attribute_value, *child_locators,
                                      strict_check=strict_check)


def xpath_by_text(element: HtmlElement, attribute_value: str, *child_locators: str,
                  strict_check: bool = True) -> Tuple[str, str]:
    """
    Function for creating locator tuple used by Selenium to locate element in Tune.
    By default, xpath looks for "text" inside element
    Args:
        element: HtmlElement - Frontend element which should be located
        attribute_value: str - value of the "text" inside element which should be located
        child_locators: str - child locators of the main locator
        strict_check: bool - defines if attribute_value should be equal ('=')
                      or should be contained ('contains()') within searched locator

    Returns: Tuple[str, str] - valid locator used by Selenium to locate element
    """
    return By.XPATH, _attribute_xpath(element, HtmlAttribute.text,
                                      attribute_value, *child_locators,
                                      strict_check=strict_check)


def xpath_by_multiple_attributes(element: HtmlElement,
                                 *attribute_with_value: Tuple[HtmlAttribute, Optional[str]],
                                 strict_check: bool = True) -> Tuple[str, str]:
    """
    Function for creating locator tuple used by Selenium with multiple attributes checking
    in the xpath. All attributes are checked with "and"
    Args:
        element: HtmlElement - Frontend element which should be located
        attribute_with_value: Tuple[HtmlAttribute, Optional[str]] - tuple containing attribute and
                              attribute value which should be looking for
        strict_check: bool - defines if attribute_value should be equal ('=')
                      or should be contained ('contains()') within searched locator
    Example: xpath_by_multiple_attributes(
                  HtmlElement.button,
                  (HtmlAttribute.data_testid, 'basecampSelection.collapsableList'),
                  (HtmlAttribute.text, 'toggle'),
                  strict_check=False)
              )
    Result: ('xpath', "//button[contains(@data-testid, 'basecampSelection.collapsableList')
            and contains(text(), 'toggle')]")

    Returns: Tuple[str, str] - valid locator used by Selenium to locate element
    """
    inner_xpaths = list()
    for attribute, attribute_value in attribute_with_value:
        if strict_check:
            current_inner_xpath = f"{attribute.value}"
            if attribute_value:
                current_inner_xpath += f"='{attribute_value}'"
            inner_xpaths.append(current_inner_xpath)
        else:
            inner_xpaths.append(f"contains({attribute.value}, '{attribute_value}')")

    return By.XPATH, f"//{element.value}[{' and '.join(inner_xpaths)}]"


def xpath_by_multiple_attributes_chained(
        *attribute_with_value: Tuple[HtmlElement, Optional[HtmlAttribute], Optional[str]],
        strict_check: bool = True
) -> Tuple[str, str]:

    chained_xpaths = list()
    for element, attribute, attribute_value in attribute_with_value:
        if attribute is None:
            chained_xpaths.append(element.value)
        elif strict_check:
            chained_xpaths.append(f"{element.value}[{attribute.value}='{attribute_value}']")
        else:
            chained_xpaths.append(f"{element.value}[contains({attribute.value}, '{attribute_value}')]")

    return By.XPATH, f"//{'//'.join(chained_xpaths)}"


def _attribute_xpath(element: HtmlElement, attribute: HtmlAttribute, attribute_value: str,
                     *child_locators: str, strict_check: bool = True, index: Optional[int] = None) -> str:
    """
    Private function for creating locator xpath string
    Args:
        element: HtmlElement - describes to which element xpath should point
        attribute: HtmlAttribute - describes to which attribute xpath should point
        attribute_value: str - describes what value of the attribute
                         should be searched to locate element
        child_locators: str - child locators of the main locator
        strict_check: bool - defines if attribute_value should be equal ('=')
                      or should be contained ('contains()') within searched locator

    Returns: str - valid xpath with provided element, attribute and attribute value
    """
    if strict_check:
        xpath = f"//{element.value}[{attribute.value}='{attribute_value}']"
    else:
        xpath = f"//{element.value}[contains({attribute.value}, '{attribute_value}')]"
    for locator in child_locators:
        xpath += f'/{locator}'
    if index is not None:
        xpath += f"[{index}]"
    return xpath
