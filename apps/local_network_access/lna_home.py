import time

from apps.local_network_access.lna_camera import LNACamera
from apps.local_network_access.lna_connectivity import LNAConnectivity
from apps.local_network_access.lna_display_and_audio import LNADisplayAndAudio
from apps.local_network_access.lna_sync import LNASync
from base.base_ui import UIBase
from locators.local_network_access.lna_home_locators import LNAHomeLocators


class LNAHome(UIBase):
    """
    LNA Home page methods
    """

    def click_sync(self) -> LNASync:
        """
        Method to click Sync from side Navigation
        :param :
        :return : LNASync
        """
        self.look_element(LNAHomeLocators.SYNC).click()
        return LNASync()

    def click_display_and_audio(self) -> LNADisplayAndAudio:
        """
        Method to click Display and Audio from side Navigation
        :param :
        :return : LNADisplayAndAudio
        """
        self.look_element(LNAHomeLocators.DISPLAY_AUDIO).click()
        return LNADisplayAndAudio()

    def click_camera(self) -> LNACamera:
        """
        Method to click Camera from side Navigation
        :param :
        :return : LNACamera
        """
        self.look_element(LNAHomeLocators.CAMERA).click()
        return LNACamera()

    def click_connectivity(self) -> LNAConnectivity:
        """
        Method to click Connectivity from side Navigation
        :param :
        :return : LNAConnectivity
        """
        self.look_element(LNAHomeLocators.CONNECTIVITY).click()
        return LNAConnectivity()

    def click_peripherals(self):
        """
        Method to click Peripherals from side Navigation
        :param :
        :return :
        """
        self.look_element(LNAHomeLocators.PERIPHERALS).click()

    def click_system(self):
        """
        Method to click System from side Navigation
        :param :
        :return :
        """
        self.look_element(LNAHomeLocators.SYSTEM).click()

    def click_about(self):
        """
        Method to click About from side Navigation
        :param :
        :return :
        """
        self.look_element(LNAHomeLocators.ABOUT).click()

