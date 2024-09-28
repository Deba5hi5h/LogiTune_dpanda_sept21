import time

from selenium.webdriver import ActionChains

from apis.sync_helper import SyncHelper
from apps.sync import sync_config
from apps.sync.sync_config import SYNC_TIMEOUT, SyncConfig
from base import global_variables
from base.base_ui import UIBase
from extentreport.report import Report
from locators.sync_app.sync_app_device_camera_locators import SyncAppDeviceCameraLocators


class SyncDeviceCamera(UIBase):

    def click_refer_to_faq(self):
        """
        Method to click on Refer to our FAQ link

        :param :
        :return SyncDeviceCamera:
        """
        self.look_element(SyncAppDeviceCameraLocators.REFER_TO_FAQ).click()
        return SyncDeviceCamera()

    def click_learn_more(self):
        """
        Method to click on Learn More link

        :param :
        :return SyncDeviceCamera:
        """
        self.look_element(SyncAppDeviceCameraLocators.LEARN_MORE).click()
        return SyncDeviceCamera()

    def click_on_call_start(self):
        """
        Method to click on On-Call Start Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "On Call start"
        e = self.look_element(SyncAppDeviceCameraLocators.ON_CALL_START_RADIO)
        e.click()
        time.sleep(2)
        UIBase.report_flag = False
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_dynamic(self):
        """
        Method to click on Dynamic Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Dynamic"
        e = self.look_element(SyncAppDeviceCameraLocators.DYNAMIC_RADIO)
        e.click()
        time.sleep(2)
        UIBase.report_flag = False
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_group_view(self):
        """
        Method to click on Group View

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Group View"
        # sync_version = self.get_sync_minor_version()
        if self.verify_element(SyncAppDeviceCameraLocators.GROUP_VIEW_NEW, timeunit=10):
            e = self.look_element(SyncAppDeviceCameraLocators.GROUP_VIEW_NEW)
            time.sleep(2)
            UIBase.report_flag = False
            self.click_by_script(e)
            self.verify_group_view_selected(timeout=15)
        else:
            e = self.look_element(SyncAppDeviceCameraLocators.GROUP_VIEW)
            self.click_by_script(e)
            SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_speaker_view(self):
        """
        Method to click on Speaker View

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker View"
        # sync_version = self.get_sync_minor_version()
        if self.verify_element(SyncAppDeviceCameraLocators.SPEAKER_VIEW_NEW, timeunit=10):
            e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_VIEW_NEW)
            time.sleep(2)
            UIBase.report_flag = False
            self.click_by_script(e)
            self.verify_speaker_view_selected(timeout=15)
        else:
            e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_VIEW)
            self.click_by_script(e)
            SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_speaker_detection_slower(self):
        """
        Method to click on Speaker Detection Slower Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker Detection Slower"
        e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_DETECTION_SLOW)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_speaker_detection_default(self):
        """
        Method to click on Speaker Detection Default Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker Detection Default"
        e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_DETECTION_DEFAULT)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_speaker_detection_faster(self):
        """
        Method to click on Speaker Detection Faster Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Speaker Detection Faster"
        e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_DETECTION_FAST)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_framing_speed_slower(self):
        """
        Method to click on Framing Speed Slower Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Framing Speed Slower"
        e = self.look_element(SyncAppDeviceCameraLocators.FRAMING_SPEED_SLOW)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_framing_speed_default(self):
        """
        Method to click on Framing Speed Default Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Framing Speed Default"
        e = self.look_element(SyncAppDeviceCameraLocators.FRAMING_SPEED_DEFAULT)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_framing_speed_faster(self):
        """
        Method to click on Framing Speed Faster Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Framing Speed Faster"
        e = self.look_element(SyncAppDeviceCameraLocators.FRAMING_SPEED_FAST)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_pal(self):
        """
        Method to click on PAL 50Hz Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "PAL 50 Hz"
        e = self.look_element(SyncAppDeviceCameraLocators.PAL_50HZ)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_ntsc(self):
        """
        Method to click on NTSC 60Hz Radio button

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "NTSC 60 Hz"
        e = self.look_element(SyncAppDeviceCameraLocators.NTSC_60HZ)
        self.click_by_script(e)
        SyncConfig.is_selected(e)
        return SyncDeviceCamera()

    def click_reset_manual_color_settings(self):
        """
        Method to reset manual color settings

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Reset Manual Color Settings"
        if self.verify_element(SyncAppDeviceCameraLocators.RESET_MANUAL_COLOR_SETTINGS, timeunit=5):
            self.look_element(SyncAppDeviceCameraLocators.RESET_MANUAL_COLOR_SETTINGS).click()
        else:
            self.look_element(SyncAppDeviceCameraLocators.RESET_MANUAL_COLOR_SETTINGS_OLD).click()
        time.sleep(2)
        return SyncDeviceCamera()

    def click_reset_camera_adjustments(self):
        """
        Method to reset Camera Adjustments

        :param :
        :return SyncDeviceCamera:
        """
        UIBase.elementName = "Reset Camera Adjustments"
        if self.verify_element(SyncAppDeviceCameraLocators.RESET_CAMERA_ADJUSTMENTS, timeunit=5):
            self.look_element(SyncAppDeviceCameraLocators.RESET_CAMERA_ADJUSTMENTS).click()
        else:
            self.look_element(SyncAppDeviceCameraLocators.RESET_CAMERA_ADJUSTMENTS_OLD).click()
        time.sleep(2)
        return SyncDeviceCamera()

    def click_edit_boundaries(self):
        """
        Method to click Edit Boundaries button

        :param :
        :return SyncDeviceCamera
        """
        self.look_element(SyncAppDeviceCameraLocators.EDIT_BOUNDARIES).click()
        time.sleep(3)
        return SyncDeviceCamera()

    def click_auto_calibrate(self):
        """
        Method to click Auto Calibrate button

        :param :
        :return SyncDeviceCamera
        """
        self.look_element(SyncAppDeviceCameraLocators.AUTO_CALIBRATE).click()
        time.sleep(3)
        return SyncDeviceCamera()

    def enable_right_sight(self):
        """
        Method to enable RightSight

        :param :
        :return SyncDeviceCamera:
        """
        if self.verify_right_sight_enabled(timeout=1, enabled=False):
            Report.logInfo("Enabling Right Sight")
            self.look_element(SyncAppDeviceCameraLocators.RIGHT_SIGHT_TOGGLE).click()
            self.verify_right_sight_enabled()
        return SyncDeviceCamera()

    def disable_right_sight(self):
        """
        Method to disable RightSight

        :param :
        :return SyncDeviceCamera:
        """
        if self.verify_right_sight_enabled(timeout=1, enabled=True):
            Report.logInfo("Disabling Right Sight")
            self.look_element(SyncAppDeviceCameraLocators.RIGHT_SIGHT_TOGGLE_OFF).click()
            self.verify_right_sight_enabled(enabled=False)
        return SyncDeviceCamera()

    def enable_picture_in_picture(self):
        """
        Method to enable Picture in Picture

        :param :
        :return SyncDeviceCamera:
        """
        if self.verify_picture_in_picture_enabled(timeout=1, enabled=False):
            Report.logInfo("Enabling Picture in Picture")
            self.look_element(SyncAppDeviceCameraLocators.PICTURE_IN_PICTURE_TOGGLE).click()
            self.verify_picture_in_picture_enabled()
        return SyncDeviceCamera()

    def disable_picture_in_picture(self):
        """
        Method to disable Picture in Picture

        :param :
        :return SyncDeviceCamera:
        """
        if self.verify_picture_in_picture_enabled(timeout=1, enabled=True):
            Report.logInfo("Disabling Picture in Picture")
            self.look_element(SyncAppDeviceCameraLocators.PICTURE_IN_PICTURE_TOGGLE).click()
            self.verify_picture_in_picture_enabled(enabled=False)
        return SyncDeviceCamera()

    def turn_on_grid_video_preview(self):
        """ Method to turn ON grid lines in Video preview

        :param None
        :param percentage: target value of the slider
        @return: SyncDeviceCamera
        """
        if not self.verify_grid_in_preview():
            Report.logInfo("Turning ON Grid Lines")
            UIBase.elementName = 'Grid Button'
            self.look_element(SyncAppDeviceCameraLocators.GRID_BUTTON).click()
        return SyncDeviceCamera()

    def turn_off_grid_video_preview(self):
        """ Method to turn OFF grid lines in Video preview

        :param :
        @return: SyncDeviceCamera
        """
        if self.verify_grid_in_preview():
            Report.logInfo("Turning OFF Grid Lines")
            UIBase.elementName = 'Grid Button'
            self.look_element(SyncAppDeviceCameraLocators.GRID_BUTTON).click()
        return SyncDeviceCamera()

    def collapse_video_preview(self):
        """ Method to Collapse Video preview

        :param :
        @return: SyncDeviceCamera
        """
        if not self.verify_video_preview_collapsed():
            Report.logInfo("Collapsing Video Preview")
            UIBase.elementName = 'Video Preview Collapse'
            self.look_element(SyncAppDeviceCameraLocators.VIDEO_PREVIEW_COLLAPSE).click()
        return SyncDeviceCamera()

    def restore_video_preview(self):
        """ Method to Restore Video preview

        :param :
        @return: SyncDeviceCamera
        """
        if self.verify_video_preview_collapsed():
            Report.logInfo("Restoring Video Preview")
            UIBase.elementName = 'Video Preview Restore'
            self.look_element(SyncAppDeviceCameraLocators.VIDEO_PREVIEW_RESTORE).click()
        return SyncDeviceCamera()

    def expand_manual_color_settings(self):
        """
        Method to expand manual color settings

        :param :
        :return SyncDeviceCamera:
        """
        element = self.look_element(SyncAppDeviceCameraLocators.MANUAL_COLOR_SETTINGS)
        if SyncConfig.is_attribute_present(element, 'class', 'expanded', timeout=1, present=False):
            Report.logInfo("Expanding Manual Color Settings")
            element.click()
        return SyncDeviceCamera()

    def expand_camera_adjustments(self):
        """
        Method to expand Camera Adjustments

        :param :
        :return SyncDeviceCamera:
        """
        element = self.look_element(SyncAppDeviceCameraLocators.CAMERA_ADJUSTMENTS)
        if SyncConfig.is_attribute_present(element, 'class', 'expanded', timeout=1, present=False):
            Report.logInfo("Expanding Camera Adjustments")
            element.click()
        return SyncDeviceCamera()

    def get_color_value(self, color_setting: str) -> int:
        """
        Method to get manual color setting value

        :param color_setting: eg: brightness, contrast, saturation, sharpness
        :return percentage int value
        """
        value = self.look_element(eval(f"SyncAppDeviceCameraLocators.{color_setting.upper()}_PERCENTAGE")).text
        return int(value.strip('%'))

    def get_screenshot_from_video_stream(self, name=None):
        """
        Method to capture a screenshot of the video stream and name it.

        :name : filename
        :return none
        """
        time.sleep(5)
        element = self.look_element(SyncAppDeviceCameraLocators.VIDEO_STREAM)
        return Report.get_element_screenshot(element, name)

    def set_color_value(self, color_setting: str, percentage: int) -> int:
        """
        Method to adjust manual color setting and get the resultant value of the slider

        :param color_setting: Manual color setting value eg: brightness, contrast, saturation, sharpness
        :param percentage : target value of the slider
        :return resultant value of the slider adjustment
        """
        self.drag_slider(color_setting, percentage)
        time.sleep(2)
        color_value = self.get_color_value(color_setting)
        if color_value == percentage:
            Report.logPass(f"{color_setting.title()} has been adjusted to {percentage}%", True)
        else:
            Report.logInfo(f"Failed to adjust {color_setting.title()} to {percentage}%. "
                           f"{color_setting.title()} value is at: {color_value}%")
        return color_value

    def set_camera_adjustments(self, camera_adjustment: str, percentage: int):
        """ Method to set manual camera adjustment for Focus, Exposure or White Balance based on percentage

        :param camera_adjustment:
        :param percentage:
        @return: SyncDeviceCamera:
        """
        driver = global_variables.driver
        try:
            camera_adjustment = camera_adjustment.replace(' ', '_').upper()
            if camera_adjustment == 'MANUAL_FOCUS':
                self.disable_auto_focus()
            elif camera_adjustment == 'MANUAL_EXPOSURE':
                self.disable_auto_exposure()
            elif camera_adjustment == 'MANUAL_WHITE_BALANCE':
                self.disable_auto_white_balanace()
            global_variables.driver = sync_config.base_driver
            knob = self.look_element(eval(f"SyncAppDeviceCameraLocators.{camera_adjustment}_SLIDER_KNOB"))
            current_value = self._get_slider_value(knob)
            move = ActionChains(global_variables.driver)
            move.click_and_hold(knob).move_by_offset((percentage - current_value) * 2, 0).release().perform()
            Report.logInfo(f"Setting {camera_adjustment} to {percentage}")
        except Exception as e:
            Report.logException(str(e))
        global_variables.driver = driver
        return SyncDeviceCamera()

    def disable_auto_focus(self):
        """ Method to disable Auto Focus

        :param :
        @return: SyncDeviceCamera:
        """
        if self.verify_auto_focus_enabled():
            Report.logInfo("Disabling Auto Focus")
            self.look_element(SyncAppDeviceCameraLocators.AUTO_FOCUS).click()
            time.sleep(1)
        else:
            Report.logInfo("Auto Focus is already disabled")
        return SyncDeviceCamera()

    def enable_auto_focus(self):
        """ Method to enable Auto Focus

        :param :
        @return: SyncDeviceCamera:
        """
        if not self.verify_auto_focus_enabled():
            Report.logInfo("Enabling Auto Focus")
            self.look_element(SyncAppDeviceCameraLocators.AUTO_FOCUS).click()
            time.sleep(1)
        else:
            Report.logInfo("Auto Focus is already enabled")
        return SyncDeviceCamera()

    def verify_auto_focus_enabled(self) -> bool:
        """ Method to verify Auto Focus is enabled

        :param :
        @return: bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.AUTO_FOCUS)
        return e.is_selected()

    def disable_auto_exposure(self):
        """ Method to disable Auto Exposure

        :param :
        @return: SyncDeviceCamera
        """
        if self.verify_auto_exposure_enabled():
            Report.logInfo("Disabling Auto Exposure")
            self.look_element(SyncAppDeviceCameraLocators.AUTO_EXPOSURE).click()
            time.sleep(1)
        else:
            Report.logInfo("Auto Exposure is already disabled")
        return SyncDeviceCamera()

    def enable_auto_exposure(self):
        """ Method to enable Auto Exposure

        :param :
        @return: SyncDeviceCamera:
        """
        if not self.verify_auto_exposure_enabled():
            Report.logInfo("Enabling Auto Focus")
            self.look_element(SyncAppDeviceCameraLocators.AUTO_EXPOSURE).click()
            time.sleep(1)
        else:
            Report.logInfo("Auto Exposure is already enabled")
        return SyncDeviceCamera()

    def verify_auto_exposure_enabled(self) -> bool:
        """ Method to verify Auto Exposure is enabled

        :param :
        @return: bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.AUTO_EXPOSURE)
        return e.is_selected()

    def disable_auto_white_balanace(self):
        """ Method to disable Auto White Balance

        :param :
        @return: SyncDeviceCamera:
        """
        if self.verify_auto_white_balanace_enabled():
            Report.logInfo("Disabling Auto White Balance")
            self.look_element(SyncAppDeviceCameraLocators.AUTO_WHITE_BALANCE).click()
            time.sleep(1)
        else:
            Report.logInfo("Auto White Balance is already disabled")
        return SyncDeviceCamera()

    def enable_auto_white_balanace(self):
        """ Method to enable Auto White Balance

        :param :
        @return: SyncDeviceCamera:
        """
        if not self.verify_auto_white_balanace_enabled():
            Report.logInfo("Enabling Auto White Balance")
            self.look_element(SyncAppDeviceCameraLocators.AUTO_WHITE_BALANCE).click()
            time.sleep(1)
        else:
            Report.logInfo("Auto White Balance is already enabled")
        return SyncDeviceCamera()

    def verify_auto_white_balanace_enabled(self) -> bool:
        """ Method to verify Auto White Balance is enabled

        :param :
        @return: bool
        """
        e = self.look_element(SyncAppDeviceCameraLocators.AUTO_WHITE_BALANCE)
        return e.is_selected()

    def drag_slider(self, color_setting: str, percentage: int):
        """ Method to drag the slider to specific value

        :param color_setting Manual color setting value eg: brightness, contrast, saturation, sharpness
        :param percentage: target value of the slider
        @return: None
        """
        driver = global_variables.driver
        try:
            global_variables.driver = sync_config.base_driver
            knob = self.look_element(eval(f"SyncAppDeviceCameraLocators.{color_setting.upper()}_SLIDER_KNOB"))
            current_value = self._get_slider_value(knob)
            move = ActionChains(global_variables.driver)
            move.click_and_hold(knob).move_by_offset((percentage - current_value) * 2, 0).release().perform()
            Report.logInfo(f"Setting {color_setting} to {percentage}")
        except Exception as e:
            Report.logException(str(e))
        global_variables.driver = driver

    @staticmethod
    def _get_slider_value(knob_element):
        max = int(knob_element.get_attribute('aria-valuemax'))
        min = int(knob_element.get_attribute('aria-valuemin'))
        current = int(knob_element.get_attribute('aria-valuenow'))
        return round((current - min) * 100 / (max - min))

    def verify_right_sight_enabled(self, timeout: int = None, enabled: bool = True) -> bool:
        """
        Method to verify RightSight is enabled

        :param timeout:
        :param enabled:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.RIGHT_SIGHT_TOGGLE)
        return SyncConfig.is_selected(e, timeout=timeout, selected=enabled)

    def verify_on_call_start_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify RightSight On-Call start radio is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.ON_CALL_START_RADIO)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_dynamic_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify RightSight Dynamic radio is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.DYNAMIC_RADIO)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_group_view_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Group View is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        if self.verify_element(SyncAppDeviceCameraLocators.GROUP_VIEW_NEW, timeunit=10):
            e = self.look_element(SyncAppDeviceCameraLocators.GROUP_VIEW_NEW)
            return SyncConfig.is_attribute_present(e, 'class', 'tMIvo', timeout=timeout, present=selected)
        else:
            e = self.look_element(SyncAppDeviceCameraLocators.GROUP_VIEW)
            return SyncConfig.is_selected(e, selected=selected)

    def verify_speaker_view_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Group View is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        if self.verify_element(SyncAppDeviceCameraLocators.SPEAKER_VIEW_NEW, timeunit=10):
            e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_VIEW_NEW)
            return SyncConfig.is_attribute_present(e, 'class', 'tMIvo', timeout=timeout, present=selected)
        else:
            e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_VIEW)
            return SyncConfig.is_selected(e, selected=selected)

    def verify_picture_in_picture_enabled(self, timeout: int = None, enabled: bool = True):
        """
        Method to verify picture in picture is enabled

        :param timeout:
        :param enabled:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.PICTURE_IN_PICTURE_TOGGLE)
        return SyncConfig.is_selected(e, timeout=timeout, selected=enabled)

    def verify_speaker_detection_slower_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Speaker Detection Slower is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_DETECTION_SLOW)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_speaker_detection_default_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Speaker Detection Default is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_DETECTION_DEFAULT)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_speaker_detection_faster_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Speaker Detection Faster is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.SPEAKER_DETECTION_FAST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_framing_speed_slower_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Framing Speed Slower is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.FRAMING_SPEED_SLOW)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_framing_speed_default_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Framing Speed Default is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.FRAMING_SPEED_DEFAULT)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_framing_speed_faster_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify Framing Speed Faster is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.FRAMING_SPEED_FAST)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_pal_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify PAL 50 Hz is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.PAL_50HZ)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_ntsc_selected(self, timeout: int = None, selected: bool = True) -> bool:
        """
        Method to verify NTSC 60 Hz is selected

        :param timeout:
        :param selected:
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.NTSC_60HZ)
        return SyncConfig.is_selected(e, timeout=timeout, selected=selected)

    def verify_grid_in_preview(self) -> bool:
        """
        Method to verify if grid view is enabled in preview

        :param :
        :return bool:
        """
        e = self.look_element(SyncAppDeviceCameraLocators.GRID_BUTTON_PROPERTY)
        return SyncConfig.is_attribute_present(e, 'id', 'off', timeout=1)

    def verify_grid_lines_video_preview(self) -> bool:
        """ Method to verify if Grid Lines are present

        :param :
        @return: bool:
        """
        if self.verify_grid_in_preview():
            horizonal = self.look_element(SyncAppDeviceCameraLocators.GRID_LINES_HORIZONTAL)
            vertical = self.look_element(SyncAppDeviceCameraLocators.GRID_LINES_VERTICAL)
            if horizonal.rect['height'] == 1 and vertical.rect['width'] == 1:
                return True
        return False

    def verify_video_preview_collapsed(self) -> bool:
        """ Method to verify Video preview is collapsed

        :param :
        @return: bool
        """
        e = self.look_element(SyncAppDeviceCameraLocators.VIDEO_PREVIEW_COLLAPSE)
        return SyncConfig.is_attribute_present(e, 'aria-expanded', 'false', timeout=1)

    def verify_auto_calibrate_enabled(self) -> bool:
        """ Method to verify Auto Calibrate button is enabled

        :param :
        @return: bool
        """
        e = self.look_element(SyncAppDeviceCameraLocators.AUTO_CALIBRATE)
        return SyncConfig.is_attribute_present(e, 'class', 'disabled', timeout=1, present=False)

    def verify_confirm_enabled(self) -> bool:
        """ Method to verify Edit Boundaries Confirm button is enabled

        :param :
        @return: bool
        """
        e = self.look_element(SyncAppDeviceCameraLocators.EDIT_BOUNDARIES_CONFIRM)
        return SyncConfig.is_attribute_present(e, 'class', 'disabled', timeout=1, present=False)

    def verify_cancel_enabled(self) -> bool:
        """ Method to verify Edit Boundaries Cancel button is enabled

        :param :
        @return: bool
        """
        e = self.look_element(SyncAppDeviceCameraLocators.EDIT_BOUNDARIES_CANCEL)
        return SyncConfig.is_attribute_present(e, 'class', 'disabled', timeout=1, present=False)

    @staticmethod
    def get_sync_minor_version():
        try:
            sync_version = SyncHelper.get_logisync_version()
            version_list = sync_version.split('.')
            sync_version = int(version_list[len(version_list) - 1])
        except Exception as e:
            sync_version = 0
        return sync_version
