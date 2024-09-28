import os
import time

from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from apps.tune_mobile.config import tune_mobile_config
from base import global_variables
from base.base_mobile import MobileBase
from base.listener import CustomListener
from extentreport.report import Report
from appium import webdriver

from locators.tune_mobile.phone_settings_locators import PhoneSettingsLocators


class PhoneSettings(MobileBase):

    def open(self):
        """
        Method to open Phone Settings

        :param :
        :return PhoneSettings:
        """
        self.desired_caps = {}
        self.desired_caps['platformName'] = self.get_platform_name()
        self.desired_caps['deviceName'] = tune_mobile_config.phone
        self.desired_caps['platformVersion'] = self.get_platform_version()
        if self.is_ios_device():
            self.desired_caps['udid'] = self.get_udid()
            self.desired_caps['bundleId'] = "com.apple.Preferences"
        else:
            self.desired_caps['appPackage'] = "com.android.settings"
            self.desired_caps['appActivity'] = "com.android.settings.Settings"
            self.desired_caps['language'] = "en"
            self.desired_caps['locale'] = "en"
        Report.logInfo("Launching Phone Settings")
        driverRaw = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        driverRaw.implicitly_wait(tune_mobile_config.implicit_wait)
        MobileBase.driver = driverRaw
        driver = EventFiringWebDriver(driverRaw, CustomListener())
        global_variables.driver = driver
        return PhoneSettings()

    def close(self):
        """
        Method to close Phone Settings

        :param :
        :return :
        """
        global_variables.driver.quit()
        global_variables.driver = None

    def click_bluetooth(self):
        """
        Method to click Bluetooth

        :param :
        :return PhoneSettings:
        """
        if self.verify_element(PhoneSettingsLocators.BLUETOOTH, timeout=2):
            self.find_element(PhoneSettingsLocators.BLUETOOTH).click()
        return PhoneSettings()

    def click_back_to_bluetooth(self):
        """
        Method to click Back button

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.BACK_TO_BLUETOOTH).click()
        return PhoneSettings()

    def get_device_status(self, device_name: str) -> str:
        """
        Method to click Bluetooth device status

        :param device_name:
        :return str:
        """
        value = 'value' if self.is_ios_device() else 'text'
        if self.verify_element(PhoneSettingsLocators.DEVICE_STATUS, param=device_name, timeout=1):
            return self.find_element(PhoneSettingsLocators.DEVICE_STATUS, param=device_name).get_attribute(value)
        return ""

    def click_device(self, device_name: str):
        """
        Method to click Bluetooth Device

        :param device_name:
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.DEVICE, param=device_name).click()
        return PhoneSettings()

    def click_device_info(self, device_name: str):
        """
        Method to click Bluetooth Device Info icon

        :param device_name:
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.DEVICE_INFO, param=device_name).click()
        return PhoneSettings()

    def click_device_disconnect(self):
        """
        Method to click Bluetooth Device Disconnect button

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.DEVICE_DISCONNECT).click()
        return PhoneSettings()

    def type_search(self, search_text: str):
        """
        Method to type text in search textfield

        :param :
        :return PhoneSettings:
        """
        self.swipe("down")
        self.find_element(PhoneSettingsLocators.SEARCH).send_keys(search_text)
        return PhoneSettings()

    def click_search(self):
        """
        Method to click on search textfield

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.SEARCH_BAR).click()
        return PhoneSettings()

    def click_logitune(self):
        """
        Method to click LogiTune app from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.LOGITUNE).click()
        return PhoneSettings()

    def click_apps(self):
        """
        Method to click Apps from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.APPS).click()
        return PhoneSettings()

    def click_language(self):
        """
        Method to click Language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.LANGUAGE).click()
        return PhoneSettings()

    def click_English(self):
        """
        Method to click English language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.ENGLISH).click()
        return PhoneSettings()

    def click_spanish(self):
        """
        Method to click Spanish language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.SPANISH).click()
        return PhoneSettings()

    def click_italian(self):
        """
        Method to click Italian language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.ITALIAN).click()
        return PhoneSettings()

    def click_french(self):
        """
        Method to click French language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.FRENCH).click()
        return PhoneSettings()

    def click_german(self):
        """
        Method to click German language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.GERMAN).click()
        return PhoneSettings()

    def click_portuguese(self):
        """
        Method to click Portuguese language from Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.PORTUGUESE).click()
        return PhoneSettings()

    def click_notifications(self):
        """
        Method to click Notifications from Tune Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.NOTIFICATIONS).click()
        return PhoneSettings()

    def verify_booking_changes_on(self) -> bool:
        """
        Method to verify Booking Changes is turned on

        :param :
        :return bool:
        """
        el = self.find_element(PhoneSettingsLocators.BOOKING_CHANGES)
        return el.get_attribute('checked') == 'true'

    def verify_booking_reminders_on(self) -> bool:
        """
        Method to verify Booking Reminders is turned on

        :param :
        :return bool:
        """
        el = self.find_element(PhoneSettingsLocators.BOOKING_REMINDERS)
        return el.get_attribute('checked') == 'true'

    def verify_checkin_request_on(self) -> bool:
        """
        Method to verify Check-in Request is turned on

        :param :
        :return bool:
        """
        el = self.find_element(PhoneSettingsLocators.CHECKIN_REQUEST)
        return el.get_attribute('checked') == 'true'

    def verify_teammate_bookings_on(self) -> bool:
        """
        Method to verify Teammate Bookings is turned on

        :param :
        :return bool:
        """
        el = self.find_element(PhoneSettingsLocators.TEAMMATE_BOOKINGS)
        return el.get_attribute('checked') == 'true'

    def disable_booking_changes(self):
        """
        Method to disable Booking Changes notification

        :param :
        :return PhoneSettings:
        """
        if self.verify_booking_changes_on():
            self.find_element(PhoneSettingsLocators.BOOKING_CHANGES).click()
        return PhoneSettings()

    def disable_booking_reminders(self):
        """
        Method to disable Booking Reminders notification

        :param :
        :return PhoneSettings:
        """
        if self.verify_booking_reminders_on():
            self.find_element(PhoneSettingsLocators.BOOKING_REMINDERS).click()
        return PhoneSettings()

    def disable_checkin_request(self):
        """
        Method to disable Check-in Request notification

        :param :
        :return PhoneSettings:
        """
        if self.verify_checkin_request_on():
            self.find_element(PhoneSettingsLocators.CHECKIN_REQUEST).click()
        return PhoneSettings()

    def disable_teammate_bookings(self):
        """
        Method to disable Teammate Bookings notification

        :param :
        :return PhoneSettings:
        """
        if self.verify_teammate_bookings_on():
            self.find_element(PhoneSettingsLocators.TEAMMATE_BOOKINGS).click()
        return PhoneSettings()

    def click_silent_notifications(self):
        """
        Method to click Silent Notifications from Tune Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.NOTIFICATION_SILENT).click()
        return PhoneSettings()

    def verify_silent_notifications(self) -> bool:
        """
        Method to verify Silent Notifications option displayed

        :param :
        :return bool:
        """
        return self.verify_element(PhoneSettingsLocators.NOTIFICATION_SILENT, timeout=3)

    def disable_lock_screen_notification(self):
        """
        Method to disable Lock Screen notification

        :param :
        :return PhoneSettings:
        """
        el = self.find_element(PhoneSettingsLocators.LOCK_SCREEN)
        if self.is_ios_device():
            if el.get_attribute('value') is not None:
                self.find_element(PhoneSettingsLocators.LOCK_SCREEN).click()
        else:
            if el.get_attribute('checked') == 'true':
                el.click()
        return PhoneSettings()

    def disable_notification_center(self):
        """
        Method to disable Notification Center

        :param :
        :return PhoneSettings:
        """
        el = self.find_element(PhoneSettingsLocators.NOTIFICATION_CENTER)
        if el.get_attribute('value') is not None:
            self.find_element(PhoneSettingsLocators.NOTIFICATION_CENTER).click()
        return PhoneSettings()

    def disable_banners_notification(self):
        """
        Method to disable Banners Notifications

        :param :
        :return PhoneSettings:
        """
        el = self.find_element(PhoneSettingsLocators.BANNERS)
        if self.is_ios_device():
            if el.get_attribute('value') is not None:
                self.find_element(PhoneSettingsLocators.BANNERS).click()
        else:
            if el.get_attribute('checked') == 'true':
                el.click()
        return PhoneSettings()

    def click_headset_settings(self, headset: str):
        """
        Method to click Headset Settings Gear button

        :param headset:
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.HEADSET_SETTINGS, param=headset).click()
        return PhoneSettings()

    def click_headset_disconnect(self):
        """
        Method to click Disconnect from Headset Settings

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.HEADSET_DISCONNECT).click()
        return PhoneSettings()

    def click_back(self):
        """
        Method to click Back arrow

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.BACK).click()
        return PhoneSettings()

    def verify_headset_connect(self) -> bool:
        """
        Method to verify connect option displayed

        :param :
        :return bool:
        """
        return self.verify_element(PhoneSettingsLocators.HEADSET_CONNECT)

    def click_see_all(self):
        """
        Method to click See All link for Pixel devices

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.SEE_ALL).click()
        return PhoneSettings()

    def verify_later_button(self) -> bool:
        """
        Method to verify Software update pop shown and later button displayed

        :param :
        :return bool:
        """
        return self.verify_element(PhoneSettingsLocators.LATER, timeout=2)

    def click_later(self):
        """
        Method to click Later button on Software update pop up

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.LATER).click()
        return PhoneSettings()

    def click_remind_me_later(self):
        """
        Method to click Remind me Later button on Software update pop up

        :param :
        :return PhoneSettings:
        """
        self.find_element(PhoneSettingsLocators.REMIND_ME_LATER).click()
        return PhoneSettings()

    def dismiss_software_update(self):
        """
        Method to Dismiss Software update notification

        :param :
        :return :
        """
        if self.verify_later_button():
            self.click_later()
            self.click_remind_me_later()

    def connect_bluetooth_device(self, device_name: str):
        """
        Method to connect Bluetooth device

        :param device_name:
        :return :
        """
        if self.is_ios_device():
            self.click_bluetooth()
            time.sleep(2)
        else:
            os.system(f"adb -s model:{self.get_model()} shell am start -a android.settings.BLUETOOTH_SETTINGS")
        status = self.get_device_status(device_name)
        if status.lower() == "not connected" or status == "":
            if "pixel" in tune_mobile_config.phone.lower():
                self.click_see_all()
                time.sleep(1)
                self.click_device(device_name=device_name)
                self.click_back()
            else:
                self.click_device(device_name=device_name)
            for _ in range(4):
                status = self.get_device_status(device_name)
                if "connected" in status.lower() or "active" in status.lower():
                    break
                time.sleep(1)
        status = self.get_device_status(device_name)
        return True if "connected" in status.lower() or "active" in status.lower() else False

    def disconnect_bluetooth_device(self, device_name: str):
        """
        Method to disconnect Bluetooth device

        :param device_name:
        :return :
        """
        try:
            if self.is_ios_device():
                self.click_bluetooth()
                status = self.get_device_status(device_name)
                if status.lower() == "connected":
                    self.click_device_info(device_name=device_name).click_device_disconnect()
                    time.sleep(2)
            else:
                os.system(f"adb -s model:{self.get_model()} shell am start -a android.settings.BLUETOOTH_SETTINGS")
                status = self.get_device_status(device_name)
                if "connected" in status.lower():
                    self.click_device(device_name=device_name)
                    time.sleep(2)
        except Exception as e:
            Report.logException(str(e))

    def disconnect_all_bluetooth_devices(self):
        """
        Method to disconnect all Bluetooth devices

        :param :
        :return :
        """
        try:
            if self.is_ios_device():
                self.click_bluetooth()
                connected_devices = self.find_elements(PhoneSettingsLocators.CONNECTED_DEVICES)
                for device in connected_devices:
                    device_name = device.get_attribute("label")
                    try:
                        self.click_device_info(device_name=device_name).click_device_disconnect()
                        time.sleep(1)
                    except:
                        print("Unable to disconnect")
                    self.click_back_to_bluetooth()
                    time.sleep(1)
            else:
                os.system(f"adb -s model:{self.get_model()} shell am start -a android.settings.BLUETOOTH_SETTINGS")
                time.sleep(2)
                connected_devices = self.find_elements(PhoneSettingsLocators.CONNECTED_DEVICES)
                while len(connected_devices) > 0:
                    device_name = connected_devices[0].get_attribute("text")
                    if "pixel" in tune_mobile_config.phone.lower():
                        self.click_headset_settings(headset=device_name)
                        self.click_headset_disconnect()
                        self.verify_headset_connect()
                        self.click_back()
                    else:
                        self.click_device(device_name=device_name)
                    connected_devices = self.find_elements(PhoneSettingsLocators.CONNECTED_DEVICES)
        except Exception as e:
            print(str(e))

    def change_language_ios(self, language: str):
        """
        Method to change language

        :param language:
        :return :
        """
        self.open().type_search("Tune").click_logitune().click_language()
        if language.lower() == "english":
            self.click_English()
        elif language.lower() == "italian":
            self.click_italian()
        elif language.lower() == "french":
            self.click_french()
        elif language.lower() == "german":
            self.click_german()
        elif language.lower() == "spanish":
            self.click_spanish()
        elif language.lower() == "portuguese":
            self.click_portuguese()
        time.sleep(1)
        self.close()

    def disable_tune_notifications(self):
        """
        Method to make Tune notifications silent to avoid pop up

        :param :
        :return :
        """
        self.open()
        if self.is_android_device():
            os.system(f"adb -s model:{self.get_model()} shell am start -a android.settings.APP_NOTIFICATION_SETTINGS --es android.provider.extra.APP_PACKAGE com.logitech.logue")
            if self.verify_silent_notifications():
                self.click_silent_notifications()
            elif tune_mobile_config.phone == "OnePlus":
                self.disable_lock_screen_notification().disable_banners_notification()
            else:
                self.disable_booking_reminders().disable_booking_changes().disable_checkin_request().disable_teammate_bookings()
        else:
            self.type_search("Tune").click_logitune().click_notifications()
            self.disable_lock_screen_notification().disable_notification_center().disable_banners_notification()
        self.close()

    def unlock_phone(self):
        """
        Method to unlock phone if it is locked

        :param :
        :return :
        """
        if self.is_android_device():
            if global_variables.driver.is_locked():
                Report.logInfo("Phone is locked, unlocking")
                os.system(f"adb -s model:{self.get_model()} shell input text "
                          f"{self.get_passcode()} && "
                          f"adb -s model:{self.get_model()} shell input keyevent 66")
                time.sleep(2)
                if global_variables.driver.is_locked():
                    driver = global_variables.driver
                    self.open()
                    os.system(f"adb -s model:{self.get_model()} shell input text "
                              f"{self.get_passcode()} && "
                              f"adb -s model:{self.get_model()} shell input keyevent 66")
                    self.close()
                return False
        return True