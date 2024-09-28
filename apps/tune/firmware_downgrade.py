import os
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

from base.base_ui import UIBase
from common.usb_switch import *

class Firmware():

    def __init__(self, device_name):
        self.device_name = device_name
        self.implicitWait = 30
        self.explicitWait = 20
        self.desired_cap = {}
        rootPath = str(UIBase.rootPath)
        if str(device_name).upper() == "BRIO":
            filePath = rootPath + "/firmware_tunes/Logitech_Brio/FWUpdateBRIO-Dev-2.0.30.exe"
        elif str(device_name).upper() == "ZONE":
            filePath = rootPath + "/firmware_tunes/Logitech_Zone750_V36/FWUpdate.exe"

        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, filePath)
        self.desired_cap["app"] = destinationFile

    def openFirmwareUpdate(self):
        self.driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", desired_capabilities=self.desired_cap)
        self.driver.implicitly_wait(self.implicitWait)
        self.wait = WebDriverWait(self.driver, self.explicitWait)
        self.wait.until(expected_conditions.visibility_of(self.driver.find_element(By.NAME, "More Details...")))
        return self.driver

    def closeFirmwareUpdate(self):
        self.driver.quit()

    def updateFirmware(self):
        elements = self.driver.find_elements(By.XPATH, "//CheckBox[@ClassName='Button'][contains(@Name,'Update')]")
        for element in elements:
            element.click()
        self.driver.find_element(By.XPATH, "//Button[@ClassName='Button'][@Name='Update Device']").click()
        self.driver.find_element(By.XPATH, "//Button[@ClassName='Button'][@Name='Yes']").click()
        self.driver.implicitly_wait(1)
        i = 600
        while i > 0:
            time.sleep(1)
            try:
                self.driver.find_element(By.XPATH, "//Button[@ClassName ='Button'][@Name='OK']")
                break
            except Exception:
                i = i - 1
        self.driver.implicitly_wait(self.implicitWait)
        self.driver.find_element(By.XPATH, "//Button[@ClassName ='Button'][@Name='OK']").click()
        self.driver.find_element(By.XPATH, "//Button[@ClassName='Button'][@Name='Close']").click()

    def downgrade_firmware(self):
        Report.logInfo("Downgrading {} Firmware".format(self.device_name))
        self.openFirmwareUpdate()
        self.updateFirmware()
        self.closeFirmwareUpdate()
        Report.logInfo("{} Firmware downgrade complete".format(self.device_name))
        time.sleep(5)
        disconnect_device(self.device_name)
        time.sleep(5)
        connect_device(self.device_name)
        time.sleep(5)