"""
This class is used to represent a execution path in Zephyr
Anyone who wants to use this class should inherit ExecutionPath class and implement the required properties
"""

import os
import platform
import re
import sys

from functools import lru_cache
from typing import Callable

from base import global_variables
from base.base_settings import TUNES_APP_PATH_MAC, TUNES_APP_PATH_MAC_NEW, TUNES_APP_PATH_WIN, TUNES_APP_PATH_WIN_NEW
from common.framework_params import INSTALLER
from common.platform_helper import get_current_system_version
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType, DeviceName

class ExecutionPath(dict):
    """
    A class to represent a execution path of a test case

    Attributes
    ----------
    version_name : str
        the name of the version
    clone_cycle_id : str
        the id of the cloned cycle
    cycle_name : str
        the name of the cycle
    folder_name : str
        the name of the folder, optional
    is_target_version : Callable[[dict], bool]
        the function to find the target version
    is_target_cloned_cycle : Callable[[dict], bool]
        the function to find the target cycle
    """

    @property
    def version_name(self) -> str:
        """
        Required

        Returns
        -------
        str
            the name of the version

        Raises
        ------
        NotImplementedError
        """
        raise NotImplemented

    @property
    def clone_cycle_id(self) -> str:
        """
        Required

        Returns
        -------
        str
            the id of the cloned cycle

        Raises
        ------
        NotImplementedError
        """
        raise NotImplemented

    @property
    def cycle_name(self) -> str:
        """
        Required

        Returns
        -------
        str
            the name of the cycle

        Raises
        ------
        NotImplementedError
        """
        raise NotImplemented

    @property
    def folder_name(self) -> str:
        """
        Optional

        Returns
        -------
        str
            the name of the folder
        """
        return None

    @property
    def is_target_version(self) -> Callable[[dict], bool]:
        """
        Required

        Returns
        -------
        Callable[[dict], bool]
            the function to find the target version
        """

        def fn(version):
            return version['label'] == self.version_name

        return fn

    @property
    def is_target_cloned_cycle(self) -> Callable[[dict], bool]:
        """
        Required

        Returns
        -------
        Callable[[dict], bool]
            the function to find the target cycle
        """

        def fn(cycle):
            return cycle['name'] == self.cycle_name

        return fn

    @property
    def is_target_cloned_folder(self) -> Callable[[dict], bool]:
        """
        Required

        Returns
        -------
        Callable[[dict], bool]
            the function to find the target folder
        """

        folder_name = self.folder_name
        if folder_name is None:
            return None

        def fn(folder):
            return folder['folderName'] == folder_name

        return fn

    def build(self) -> tuple:
        """
        automatic creation of cycle and folder if not exist

        Returns
        -------
        Callable[[dict], tuple]
            a function to build the execution path
        """
        version_id = global_variables.jira.get_version_by_fn(self.is_target_version)
        if version_id is None:
            raise Exception(f"version name {self.version_name} not found")

        # clone cycle
        cycle_id = global_variables.jira.create_or_update_cycle(
            clonedCycleId=self.clone_cycle_id,
            cycleName=self.cycle_name,
            versionId=version_id,
            is_target_cloned_cycle=self.is_target_cloned_cycle
        )

        # clone and rename folder
        folder_id = global_variables.jira.create_or_update_folder(
            folderName=self.folder_name,
            cycleId=cycle_id,
            versionId=version_id,
            is_target_cloned_folder=self.is_target_cloned_folder
        )

        return version_id, cycle_id, folder_id

    def __hash__(self):
        return hash(self.__module__)

class Hsinchu(ExecutionPath):
    """
    Customized execution path for Hsinchu
    """
    CYCLE_TEMPLATE_ID = {
        "UI": '10840',
        DeviceName.zone_wired: '11134',
        DeviceName.zone_750: '11135',
        DeviceName.zone_wired_earbuds: '11136',
        DeviceName.zone_wireless: '11137',
        DeviceName.zone_900: '11138',
        DeviceName.zone_vibe_125: '11139',
        DeviceName.zone_vibe_130: '11140',
        DeviceName.zone_vibe_wireless: '11141',
        DeviceName.zone_wireless_2: '11142',
        DeviceName.zone_true_wireless: '11143',
    }

    def __init__(self, cycle, conn_type=None, tune_app=None) -> None:
        self.conn_type = conn_type
        self.tune_app = tune_app

        self.cycle = cycle
        self.folder = {
            ConnectionType.bt: "BT",
            ConnectionType.bt_ui: "BT",
            ConnectionType.dongle: "USB",
            ConnectionType.usb_dock: "USB",
        }.get(conn_type, None)

    @property
    def version_name(self):
        version_name = 'Tune-' + '.'.join(INSTALLER.split('.')[:2]) + '.x-Headset'
        return version_name

    @property
    def clone_cycle_id(self):
        cloneCycleId = Hsinchu.CYCLE_TEMPLATE_ID.get(self.cycle, None)
        if cloneCycleId is None:
            Report.logWarning('cycle: {} not found in CYCLE_TEMPLATE_ID'.format(self.cycle))

        return cloneCycleId

    @property
    @lru_cache(maxsize=None)
    def _firmware_version(self):
        try:
            if not (os.path.exists(TUNES_APP_PATH_WIN) or os.path.exists(TUNES_APP_PATH_WIN_NEW)
                    or os.path.exists(TUNES_APP_PATH_MAC) or os.path.exists(TUNES_APP_PATH_MAC_NEW)):
                raise Exception("Logi Tune not installed")

            self.tune_app.connect_tune_app()
            is_device_connected = self.tune_app.check_is_device_connected(self.cycle)
            if not is_device_connected:
                raise Exception("Device is not connected")

            self.tune_app.open_device_in_my_devices_tab(self.cycle)
            self.tune_app.open_about_the_device(self.cycle)
            version_info = self.tune_app.check_firmware_version(self.cycle, skip_exception=True)
            firmware_version = re.search(r"\d+\.\d+\.\d+", version_info)[0]
            if firmware_version:
                 return firmware_version
        except Exception as e:
            Report.logWarning(f"Failed to get firmware version. Please ensure that tearDown is executed before disconnecting the BT/Dongle: {e}")

        return None

    @property
    def cycle_name(self):
        cycle_name = '{} Tune {}'.format(self.cycle, INSTALLER)
        if self.folder is None:
            return cycle_name

        cycle_name += ' FW ' + self._firmware_version

        return cycle_name

    @property
    def folder_name(self):
        os_name = ' '.join(platform.platform(terse=True).split('-'))

        # workaround for python platform issue, please refer to https://stackoverflow.com/a/69325836
        if os_name == "Windows 10" and sys.getwindowsversion().build > 22000:
            os_name = "Windows 11"

        if os_name.startswith('macOS'):
            mac_os_version = get_current_system_version()
            mac_chip = ('ARM' if platform.processor() == 'arm' else 'Intel')
            os_name = f"macOS {mac_os_version} {mac_chip}"
            # os_name += f" {mac_chip}"

        if self.folder is None:
            return f"{os_name} Automation"

        folder_name = f"{os_name} {self.folder} Automation"
        return folder_name

    @property
    def is_target_cloned_cycle(self):
        """Required

        Raises
        ------
        NotImplementedError
        """

        def fn(cycle):
            return re.sub(' FW .*', '', cycle['name']) == re.sub(' FW .*', '', self.cycle_name)

        return fn

    @property
    def is_target_cloned_folder(self):
        def fn(target_folder):
            # Cloning UI type cycle
            if self.folder is None:
                return True

            # Cloning Device type cycle
            return self.folder_name.split()[-2] in target_folder['folderName'].split()
        return fn

    def build(self, jira_id) -> str:
        """
        Hsinchu not only automatic creation of cycle / folder but also append firmware version to execution's comment

        Parameters
        ----------
        jira_id : str
            Jira ID

        Returns
        -------
        str
            the comment of execution
        """

        # execute_test will get the execution path from global_variables, so we need to set it before calling it
        global_variables.ZEPHYR_EXECUTION_PATH = self

        # to solve the execution won't be updated if its status is same as the previous one
        global_variables.jira.execute_test(jira_id, "WIP")
        Report.logInfo("[Jira Zephyr] Change test status to WIP for rewriting the other test status")
        version_id, cycle_id, folder_id = super().build()

        # update cycle name to latest firmware version that is executed
        execution = global_variables.jira.get_execution_by_issue_key(jira_id, cycle_id, folder_id, version_id)
        if self.cycle_name != execution['cycleName']:
            global_variables.jira.update_cycle(
                cycleId=execution['cycleId'],
                cycleName=self.cycle_name,
                versionId=version_id
            )

            Report.logInfo(f"[Jira Zephyr] firmware version of cycle name updated: {execution['cycleName']} -> {self.cycle_name}")

        # add firmware version to the comment column of execution
        comment = execution['comment']
        if self._firmware_version:
            firmware_version_history = dict(re.findall('(.*) - (.*)', execution['comment']))
            firmware_version_history[f'FW {self._firmware_version}'] = global_variables.testStatus
            comment = '\n'.join(f'{version} - {status}' for version, status in firmware_version_history.items())

        return comment
