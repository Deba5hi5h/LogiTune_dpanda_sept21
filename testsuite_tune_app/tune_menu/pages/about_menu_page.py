from base.base_ui import UIBase
from common.usb_switch import *
from locators.tune_menu.about_menu_page_locators import AboutMenuPageLocators


class AboutMenuPage(UIBase):

    def assert_about_page(self):
        self.assertEqual(self.look_element(AboutMenuPageLocators.PAGE_TITLE).text, 'About')
        self.assertIn(INSTALLER, self.look_element(AboutMenuPageLocators.APP_VERSION).text)
