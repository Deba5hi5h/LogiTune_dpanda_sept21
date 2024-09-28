import time
from typing import Type, Union

from apps.tune.TuneElectron import TuneElectron
from base import global_variables
from base.base_ui import UIBase
from common.email_notification import EmailNotification
from common.JiraLibrary import JiraAPI
from common.usb_switch import connect_device, disconnect_all, disconnect_device


class VerifyDevices:
    def __init__(self):
        disconnect_all()
        self.tune_app = TuneElectron()
        self.tune_app.open_tune_app()
        self.tune_app.open_my_devices_tab()

    def _check_device_visibility(self, device_name: str, is_svc_lab=True) -> bool:
        strict_check_devices = [
            'Zone 900',
            'Zone Vibe 125',
            'Zone Wireless',
            'Zone Wireless Plus',
        ]
        try:
            connect_device(device_name)
            time.sleep(5)
            if device_name in strict_check_devices:
                result = self.tune_app.verify_device_name_displayed(device_name, exact_name=True)
            else:
                result = self.tune_app.verify_device_name_displayed(device_name)
            if device_name == "Zone 950":
                if not result:
                    self.tune_app.power_on_zone950(is_svc_lab)
                    result = self.tune_app.verify_device_name_displayed(device_name)
                self.tune_app.click_device(device_name)
                charging_status = self.tune_app.check_charging_status(device_name)
                if not charging_status and is_svc_lab:
                    connect_device('zone_950_charge')
                    time.sleep(10)
                    charging_status = self.tune_app.check_charging_status(device_name)
                battery_level = self.tune_app.check_battery_level(device_name)
                if battery_level < 50:
                    if charging_status:
                        self.tune_app.wait_until_battery_level(device_name, 45)
                    else:
                        result = False

            disconnect_device(device_name)
            return result
        except Exception as e:
            print(repr(e))
            return False

    def get_not_available_devices(self, devices_names: list, is_svc_lab=True) -> list:
        not_available = list()
        for device_name in devices_names:
            print(f'Checking if device available: {device_name}')
            if not self._check_device_visibility(device_name, is_svc_lab):
                print(f'{device_name} is not detected in LogiTune')
                not_available.append(device_name)
            else:
                print(f'{device_name} was successfully shown in LogiTune')
        return not_available


def check_devices(testcases_to_run: list, mailing_list: Union[tuple, list],
                  skip_missing_devices_in_test_suite: bool = True,
                  is_svc_lab: bool = True) -> None:
    try:
        verify_devices = VerifyDevices()
        available_devices = _get_available_devices_list(testcases_to_run)
        missing_devices = verify_devices.get_not_available_devices(available_devices, is_svc_lab=is_svc_lab)
        if missing_devices:
            print(f'Sending email with missing devices: {missing_devices}')
            global_variables.email_to = ",".join(mailing_list)
            global_variables.email_flag = True
            EmailNotification.send_missing_devices(missing_devices)
        print(f'Missing devices: {missing_devices}')
        if skip_missing_devices_in_test_suite:
            _pop_missing_devices_from_execution(testcases_to_run, missing_devices)
        global_variables.tune_available_devices = [item for item in available_devices if item not in missing_devices]
        print(f'ALL DEVICES UNDER TESTS: {global_variables.tune_available_devices}')
    except Exception as e:
        print(f'EXCEPTION in check_devices: {repr(e)}')


def _get_available_devices_list(testcases_to_run: list) -> list:
    available_devices = list()
    for device in testcases_to_run:
        try:
            name = device().device_name
            if name:
                available_devices.append(name)
        except AttributeError:
            pass
    return available_devices


def _pop_missing_devices_from_execution(testcases_to_run: list, missing_devices: list) -> None:
    print(f'Before removing devices: {len(testcases_to_run)}')
    devices_to_remove = list()
    for missing_device in missing_devices:
        for device in testcases_to_run:
            try:
                name = device().device_name
                if name and missing_device == name:
                    devices_to_remove.append(device)
            except AttributeError:
                pass
    for device in devices_to_remove:
        testcases_to_run.remove(device)
        _set_all_test_cases_as_skipped(device)
    print(f'After removing devices: {len(testcases_to_run)}')


def _check_skipped_suite_as_skipped_in_jira(testcase_name: str) -> None:
    try:
        jira = JiraAPI()
        split_test_case_name = testcase_name.split("_")
        jira_id = split_test_case_name[2] + "-" + split_test_case_name[3]
        comment = 'Skipped due to device not detected on test bench'
        jira.execute_test(jira_id, 'SKIPPED', comment)
    except Exception as e:
        print(f'EXCEPTION in _check_skipped_suite_as_skipped_in_jira: {repr(e)}')


def _set_all_test_cases_as_skipped(suite_class: Type[UIBase]) -> None:
    class_methods = dir(suite_class)
    test_methods = [method for method in class_methods if 'VC' in method and 'test' in method]
    print(f'Skipping these tests in JIRA: {test_methods}')
    for method in test_methods:
        _check_skipped_suite_as_skipped_in_jira(method)
