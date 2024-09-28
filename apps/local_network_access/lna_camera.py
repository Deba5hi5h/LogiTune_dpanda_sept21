import time

from base.base_ui import UIBase
from extentreport.report import Report
from locators.local_network_access.lna_camera_locators import LNACameraLocators


class LNACamera(UIBase):
    """
    LNA Camera page methods
    """

    def expand_rightsight_section(self):
        """
        Method to expand RightSight section
        :param :
        :return :
        """
        e = self.look_element(LNACameraLocators.RIGHTSIGHT_EXPAND)
        if "open" not in e.get_attribute('className'):
            Report.logInfo("Expanding RightSight section")
            self.look_element(LNACameraLocators.RIGHTSIGHT).click()
        return LNACamera()

    def expand_room_occupancy(self):
        """
        Method to expand Room Occupancy section
        :param :
        :return :
        """
        e = self.look_element(LNACameraLocators.ROOM_OCCUPANCY_EXPAND)
        if "open" not in e.get_attribute('className'):
            Report.logInfo("Expanding Room Occupancy section")
            self.look_element(LNACameraLocators.ROOM_OCCUPANCY).click()
        return LNACamera()

    def verify_rightsight_enabled(self) -> bool:
        """
        Method to verify if RightSight is enabled
        :param :
        :return :bool
        """
        e = self.look_element(LNACameraLocators.RIGHTSIGHT_CHECKBOX)
        return True if e.get_attribute('checked') == "true" else False

    def enable_rightsight(self):
        """
        Method to enable RightSight
        :param :
        :return :LNACamera
        """
        if not self.verify_rightsight_enabled():
            Report.logInfo("Enabling RightSight")
            self.look_element(LNACameraLocators.RIGHTSIGHT_TOGGLE).click()
        return LNACamera()

    def disable_rightsight(self):
        """
        Method to disable RightSight
        :param :
        :return :LNACamera
        """
        if self.verify_rightsight_enabled():
            Report.logInfo("Disabling RightSight")
            self.look_element(LNACameraLocators.RIGHTSIGHT_TOGGLE).click()
        return LNACamera()

    def verify_group_view_selected(self) -> bool:
        """
        Method to verify Group View is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNACameraLocators.GROUP_VIEW)
        return e.is_selected()

    def verify_speaker_view_selected(self) -> bool:
        """
        Method to verify Speaker View is selected
        :param :
        :return :bool
        """
        e = self.look_element(LNACameraLocators.SPEAKER_VIEW)
        return e.is_selected()

    def set_group_view(self):
        """
        Method to Set Group View

        :param :
        :return :
        """
        Report.logInfo("Setting Group view in device settings")
        self.look_element(LNACameraLocators.GROUP_VIEW).click()
        time.sleep(2)
        return LNACamera()

    def set_speaker_view(self):
        """
        Method to Set Group View

        :param :
        :return :
        """
        Report.logInfo("Setting Speaker view in device settings")
        self.look_element(LNACameraLocators.SPEAKER_VIEW).click()
        time.sleep(2)
        return LNACamera()

    def verify_picture_in_picture_enabled(self) -> bool:
        """
        Method to verify Picture in picture is enabled
        :param :
        :return :bool
        """
        e = self.look_element(LNACameraLocators.PICTURE_IN_PICTURE)
        return e.is_selected()

    def enable_picture_in_picture(self):
        """
        Method to Enable Picture in Picture - #Sync App Additions

        :param :
        :return :LNACamera
        """
        if not self.verify_picture_in_picture_enabled():
            Report.logInfo("Enabling Picture in picture in Device")
            self.look_element(LNACameraLocators.PICTURE_IN_PICTURE).click()
        else:
            Report.logInfo("Picture in picture is already enabled in Device")
        time.sleep(5)
        return LNACamera()

