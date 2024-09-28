import random
from typing import Any, Optional

from selenium.webdriver.common.by import By

from apps.raiden.sync_portal_inventory import SyncPortalInventory
from apps.raiden.sync_portal_methods import SyncPortalMethods
from apps.tune.TuneElectron import TuneElectron
from apps.tune.logi_sync_personal_collab.utils import DEVICE_OFFLINE_STATUS, DEVICE_ONLINE_STATUS, LOGI_TUNE_DEVICES
from base import global_variables
from common.usb_switch import connect_device, disconnect_device, disconnect_all
from config.aws_helper import AWSHelper
from extentreport.report import Report


class TuneSyncPersonalCollab(SyncPortalMethods):
    tune_app = TuneElectron()

    def tc_verify_personal_room_in_sync_portal(self, room_name: str) -> None:
        """
        Method to verify device appears in Room in Sync Portal

        :param room_name:
        :return none
        """
        driver = global_variables.driver
        try:
            config = AWSHelper.get_config('raiden-latest1')
            role = 'Owner'

            inventory = SyncPortalMethods() \
                .login_to_sync_portal_personal_devices(config, role)
            room_status = inventory.verify_room_displayed_in_inventory(room_name, timeunit=30)
            if room_status:
                Report.logPass(f"Room {room_name} is added in Sync Portal Personal Devices Inventory", True)
            else:
                Report.logFail(f"Room {room_name} is not added in Sync Portal Personal Devices Inventory", True)
        except Exception as e:
            Report.logException(str(e))
            raise e
        finally:
            self.browser.close_browser()
            global_variables.driver = driver

    def tc_verify_personal_device_detected_in_tune_and_sync_portal(self,
                                                                   available_devices: list[str],
                                                                   room_name: str) -> None:
        """
        Verify if a personal device is added in the Sync Portal.

        Args:
            available_devices (list[str]): List of available device names.
            room_name (str): Name of the room.

        """
        driver = global_variables.driver
        try:
            if len(available_devices) == 0:
                assert False, Report.logFail(f"No devices available for tests.", True)
            devices_under_test = self._select_devices_under_tests(available_devices)
            Report.logPass(f"Selected devices: {devices_under_test}")
            if len(devices_under_test) == 0:
                assert False, Report.logFail(
                    f"No devices available for tests from LOGI_TUNE_DEVICES.", True)

            self.tune_app.open_tune_app()
            self.tune_app.click_my_devices()

            for device_name in devices_under_test:
                connect_device(device_name=device_name)

                Report.logInfo(f"Check {device_name} status.")
                self.tune_app.verify_device(device_name=device_name, status=True)

            tune_driver = global_variables.driver

            global_variables.driver = driver

            config = AWSHelper.get_config('raiden-latest1')
            role = 'Owner'

            inventory = SyncPortalMethods() \
                .login_to_sync_portal_personal_devices(config, role)

            for device_name in devices_under_test:
                Report.logInfo(f"Check {device_name} status.")
                if self._is_b2b_personal_device(device_name):
                    Report.logInfo(f"{device_name} is a B2B device. "
                                   f"It should be displayed in Sync Portal in Personal Devices Inventory.")

                    sync_display_name = self._get_personal_device_display_name(device_name)
                    self._verify_personal_device_displayed_with_status_on_room_dashboard(sync_display_name,
                                                                                         inventory,
                                                                                         room_name,
                                                                                         status=DEVICE_ONLINE_STATUS)
                    self._click_close_personal_room_dashboard()

                    disconnect_device(device_name=device_name)

                    driver = global_variables.driver
                    global_variables.driver = tune_driver

                    self.tune_app.verify_device(device_name=device_name, status=False)

                    global_variables.driver = driver

                    self._verify_personal_device_displayed_with_status_on_room_dashboard(sync_display_name, inventory,
                                                                                         room_name,
                                                                                         status=DEVICE_OFFLINE_STATUS)
                else:
                    sync_display_name = self._get_personal_device_display_name(device_name)
                    Report.logInfo(f"{device_name} is a Retail device. "
                                   f"It should NOT be displayed in Sync Portal in Personal Devices Inventory.")
                    self._verify_personal_device_not_displayed_on_room_dashboard(sync_display_name, inventory,
                                                                                 room_name)
                self._click_close_personal_room_dashboard()

        except Exception as e:
            Report.logException(str(e))
            raise e
        finally:
            disconnect_all()
        self.browser.close_browser()
        global_variables.driver = driver

    @staticmethod
    def _select_devices_under_tests(available_devices: list[str]) -> list[str]:
        selected_devices = []
        comparison_devices = ["Brio 305", "Zone Wired Earbuds"]
        for category in LOGI_TUNE_DEVICES.keys():
            available_in_category = [device for device in LOGI_TUNE_DEVICES[category] if device in available_devices]

            if available_in_category:
                tmp = []
                for device in available_in_category:
                    if device not in comparison_devices:
                        tmp.append(device)
                if len(tmp) > 0:
                    selected_devices.append(random.choice(tmp))

        return selected_devices

    def _click_close_personal_room_dashboard(self) -> None:
        Report.logInfo('CLose Room inventory dashboard.')
        self.look_element((By.XPATH, "//*[contains(@class, 'TopNav__LargeCloseIcon')]")).click()

    def _verify_personal_device_displayed_with_status_on_room_dashboard(self,
                                                                        device_name: str,
                                                                        inventory: SyncPortalInventory,
                                                                        room_name: str,
                                                                        status: bool) -> None:
        if inventory.click_on_inventory_room(room_name=room_name, timeunit=10) \
                .verify_personal_device_availability_in_personal_device_room(device_name=device_name,
                                                                             is_online=status):
            Report.logPass(
                f"{device_name} is displayed in Sync Portal Personal Room with correct status.",
                True)
        else:
            Report.logFail(f"{device_name} is not displayed or not showing the correct status.")

    def _verify_personal_device_not_displayed_on_room_dashboard(self, device_name, inventory, room_name):
        if not inventory.click_on_inventory_room(room_name=room_name, timeunit=10) \
                .verify_personal_device_availability_in_personal_device_room(device_name=device_name):
            Report.logPass(
                f"{device_name} is not displayed in Sync Portal Personal Room as expected. It is a Retail device.",
                True)
        else:
            Report.logFail(f"{device_name} is displayed one the Personal Devices Room which is wrong.")

    @staticmethod
    def _is_b2b_personal_device(device_name: str) -> bool:
        for category in LOGI_TUNE_DEVICES:
            if device_name in LOGI_TUNE_DEVICES[category] and LOGI_TUNE_DEVICES[category][device_name]['product_type'] == "B2B":
                return True
        return False

    @staticmethod
    def _get_personal_device_display_name(device_name: str) -> Optional[str]:
        for category in LOGI_TUNE_DEVICES:
            if device_name in LOGI_TUNE_DEVICES[category]:
                return LOGI_TUNE_DEVICES[category][device_name]['sync_display_name']
        return None
