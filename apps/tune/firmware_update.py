import json
import time
import unittest
from typing import Optional

from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from base.fwu_stress_base import FwuStressBase
from common.usb_switch import connect_device, disconnect_device
from extentreport.report import Report
from common.recorder import initialize_recorder
from common.framework_params import JENKINS_FWU_CONFIG, TUNE_RECORDER
from common.ota_versions import DeviceFirmwareVersionGetter


class FirmwareUpdate(UIBase):
    """Updates provided device with given firmware

    Class which updates provided device (could be headset, camera or dock) with given firmwares
    (depending if receiver is available). It creates whole downgrade/update loop (downgrade
    only if needed). Inherits from UIBase.

    Attributes:
        retry: An integer count of ran tests
        test_entity: A FwuStressBase instance of test module
        device_name: A string providing device name
        baseline_version_device: A string providing needed FW version of device before update
        target_version_device: A string providing FW version of device after update
        file_path_device: A string with file path of the binary to flash device with Easter Egg
          on downgrade
        timeout: An integer with default time after which update should time out in seconds
          (default 600)
        easter_egg_on_second_update: A boolean flag to decide if second update will be done via
          Easter Egg or OTA (default False)
        file_path_target: An optional string with file path of the binary to flash device with
          Easter Egg on the update (default None)
        baseline_version_receiver: An optional string providing needed FW version of receiver
          before update (default None)
        target_version_receiver: An optional string providing FW version of receiver after update
           (default None)
        file_path_receiver: An optional string with file path of the binary to flash receiver
          with Easter Egg on downgrade (default None)
        tune_env: An optional string which provides tune environment which should be used,
          valid values - prod, qa, dev (default None). If not provided, it will be taken from
          properties.LOCAL file
    """

    def __init__(
        self,
        retry: int,
        test_entity: FwuStressBase,
        device_name: str,
        baseline_version_device: str,
        target_version_device: str,
        file_path_device: str,
        timeout: int = 600,
        easter_egg_on_second_update: bool = False,
        file_path_target: Optional[str] = None,
        baseline_version_receiver: Optional[str] = None,
        target_version_receiver: Optional[str] = None,
        file_path_receiver: Optional[str] = None,
        tune_env: Optional[str] = None,
        save_pass_logs: bool = False,
        ota_api_product_name: Optional[str] = None,
        auto_env_pick: bool = True,
        baseline_version_eeprom: Optional[str] = None,
        target_version_eeprom: Optional[str] = None,
        file_path_eeprom: Optional[str] = None,
        baseline_version_tahiti: Optional[str] = None,
        target_version_tahiti: Optional[str] = None,
        file_path_tahiti: Optional[str] = None,
        jenkins_configuration: bool = False,
        reconnect_after_fwu_failure: bool = True
    ):
        super().__init__()
        self.retry = retry
        self.test_entity = test_entity
        self.device_name = device_name
        self.baseline_version_device = baseline_version_device
        self.target_version_device = target_version_device
        self.file_path_device = file_path_device
        self.timeout = timeout
        self.easter_egg_on_second_update = easter_egg_on_second_update
        self.file_path_target = file_path_target
        self.baseline_version_receiver = baseline_version_receiver
        self.target_version_receiver = target_version_receiver
        self.file_path_receiver = file_path_receiver
        self.tune_env = tune_env
        self.save_pass_logs = save_pass_logs
        self.auto_env_pick = auto_env_pick
        self.ota_api_product_name = ota_api_product_name
        self.baseline_version_eeprom = baseline_version_eeprom
        self.target_version_eeprom = target_version_eeprom
        self.file_path_eeprom = file_path_eeprom
        self.baseline_version_tahiti = baseline_version_tahiti
        self.target_version_tahiti = target_version_tahiti
        self.file_path_tahiti = file_path_tahiti
        self.jenkins_configuration = jenkins_configuration
        self.recorder = None
        if not self.easter_egg_on_second_update:
            self._check_firmwares_within_environments()
        self.reconnect_after_fwu_failure = reconnect_after_fwu_failure

    def _check_firmwares_within_environments(self):
        valid = False
        data = dict()
        vg = DeviceFirmwareVersionGetter(self.jenkins_configuration)
        for i in range(3):
            if i != 0:
                time.sleep(3)
                Report.logInfo(f"Retrying for {i} time, because not valid environment found")
            if self.ota_api_product_name:
                data = vg.get_device_version_all_branches(
                    self.ota_api_product_name, endpoint_provided=True
                )
            else:
                data = vg.get_device_version_all_branches(self.device_name)
            env = vg.check_availability(
                data, self.target_version_device, self.target_version_receiver
            )

            if env:
                if self.auto_env_pick:
                    self.tune_env = env[0]
                if self.tune_env in env:
                    valid = True
                    break

        if valid:
            Report.logInfo(f"{self.tune_env.upper()} branch contains valid firmwares")
        else:
            Report.logFail(
                f"Invalid FW/ENV branch provided. Firmwares available within branches:\n"
                f"{json.dumps(data, indent=2)}"
            )
            receiver_ver = self.target_version_receiver
            raise InterruptedError(
                f"{self.tune_env.upper()} doesn't contain FW: Device - {self.target_version_device}"
                f"{', Dongle - ' + receiver_ver if receiver_ver is not None else ''}"
            )

    def _open_tune(self):
        self.tune_app = TuneElectron()
        modify_flag = True if self.retry == 1 else False
        self.tune_app.open_tune_app(
            modify_json=modify_flag, clean_logs=True, tune_env=self.tune_env
        )

    def _start_recording(self, test_name: str):
        if TUNE_RECORDER:
            window_coordinates = self.tune_app.get_window_position_and_size()
            self.recorder = initialize_recorder(
                self.logdirectory, test_name, **window_coordinates
            )
            self.recorder.start_recording()
            time.sleep(5)

    def _stop_recording(self, save_record: bool = False):
        if TUNE_RECORDER and self.recorder is not None:
            self.recorder.stop_recording_and_save()
            if not save_record:
                self.recorder.delete()

    def update(self):
        """Runs full loop of firmware downgrade/update of given device

        Executes downgrade (if needed) and update of the given device with provided firmwares.

        Returns: None
        """
        test_name = unittest.TestCase.id(self.test_entity).split(".")[-1]
        test_run = test_name.split("_")[-1]
        test_name = test_name[: -(1 + len(test_run))]
        try:
            baseline = "/".join(
                [
                    ver
                    for ver in (
                        self.baseline_version_device,
                        self.baseline_version_receiver,
                    )
                    if ver is not None
                ]
            )
            target = "/".join(
                [
                    ver
                    for ver in (
                        self.target_version_device,
                        self.target_version_receiver,
                    )
                    if ver is not None
                ]
            )
            is_receiver = (
                "" if self.baseline_version_receiver is None else " with receiver"
            )
            Report.logInfo(
                f"Start {self.device_name} update{is_receiver}: {baseline} -> {target}", color="Navy"
            )
            self._open_tune()
            self._start_recording(f"{test_run}_{test_name}")
            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.open_about_the_device(device_name=self.device_name)
            is_same_version = self.tune_app.is_same_version(
                device_name=self.device_name,
                device_expected_version=self.baseline_version_device,
                receiver_expected_version=self.baseline_version_receiver,
            )
            # Checking if device or receiver hasn't got needed FW version already
            if not all(is_same_version.values()):

                if is_same_version.get("device"):
                    Report.logPass(
                        f"{self.device_name} already has correct version: "
                        f"{self.baseline_version_device}"
                    )
                else:
                    Report.logInfo(
                        f"Start {self.device_name} downgrade via easterEgg to: "
                        f"{self.baseline_version_device}", color="Blue"
                    )
                    device_version = self.tune_app.update_firmware_with_easter_egg(
                        device_file_path=self.file_path_device,
                        device_name=self.device_name,
                        timeout=self.timeout,
                    ).split("\n")[0]
                    Report.logInfo(
                        f"{self.device_name} version after easterEgg downgrade: {device_version}",
                        screenshot=True,
                    )
                    assert self.tune_app.validate_versions(
                        self.baseline_version_device, device_version
                    ), Report.logFail(
                        f"{self.baseline_version_device} not in {device_version}"
                    )

                if self.baseline_version_receiver:
                    if is_same_version.get("receiver"):
                        Report.logPass(
                            f"Receiver already has correct version: "
                            f"{self.baseline_version_receiver}"
                        )
                    else:
                        Report.logInfo(
                            f"Start {self.device_name} receiver downgrade via easterEgg to: "
                            f"{self.baseline_version_receiver}", color="Blue"
                        )
                        receiver_version = (
                            self.tune_app.update_firmware_with_easter_egg(
                                device_file_path=self.file_path_receiver,
                                device_name=self.device_name,
                                is_receiver=True,
                                timeout=self.timeout,
                            ).split("\n")[1]
                        )
                        Report.logInfo(
                            f"Receiver version after easterEgg downgrade: {receiver_version}",
                            screenshot=True,
                        )
                        assert self.tune_app.validate_versions(
                            self.baseline_version_receiver, receiver_version
                        ), Report.logFail(
                            f"{self.baseline_version_receiver} not in {receiver_version}"
                        )

                Report.logPass("Downgrade via Easter Egg finished with success.")
                self.tune_app.close_tune_app()

                time.sleep(5)
                if self.save_pass_logs:
                    self.tune_app.open_tune_app()
                else:
                    self.tune_app.open_tune_app(clean_logs=True)
                self.tune_app.open_device_in_my_devices_tab(self.device_name)
                self.tune_app.open_about_the_device(device_name=self.device_name)

            else:
                Report.logPass(
                    f"{self.device_name} already has correct version: "
                    f"{self.baseline_version_device}"
                )
                if self.baseline_version_receiver:
                    Report.logPass(
                        f"Receiver already has correct version: {self.baseline_version_receiver}"
                    )
            if self.easter_egg_on_second_update:
                Report.logInfo(
                    f"Start {self.device_name} update via Easter Egg to: "
                    f"{self.target_version_device}",
                    screenshot=True, color="Navy"
                )
                updated_device_version = self.tune_app.update_firmware_with_easter_egg(
                    device_file_path=self.file_path_target,
                    device_name=self.device_name,
                    timeout=self.timeout,
                ).split("\n")[0]
                Report.logInfo(
                    f"Headset version after easterEgg: {updated_device_version}",
                    screenshot=True,
                )
                assert self.tune_app.validate_versions(
                    self.target_version_device, updated_device_version
                ), Report.logFail(
                    f"{self.target_version_device} not in {updated_device_version}"
                )
                Report.logPass("Update via Easter Egg finished with success.")

            else:
                Report.logInfo(
                    f"Start {self.device_name} update via OTA to: {self.target_version_device}",
                    screenshot=True, color="Navy"
                )
                updated_version = self.tune_app.start_update_from_device_tab(
                    device_name=self.device_name,
                    timeout=self.timeout,
                )
                if len(updated_version) > 1:
                    updated_device_version, updated_receiver_version = updated_version
                else:
                    updated_device_version = updated_version[0]
                    updated_receiver_version = None

                Report.logInfo(
                    f"{self.device_name} version after OTA: {updated_device_version}",
                    screenshot=True,
                )
                assert self.tune_app.validate_versions(
                    self.target_version_device, updated_device_version
                ), Report.logFail(
                    f"{self.target_version_device} not in {updated_device_version}"
                )
                if updated_receiver_version is not None:
                    Report.logInfo(
                        f"Receiver version after OTA: {updated_receiver_version}",
                        screenshot=True,
                    )
                    assert self.tune_app.validate_versions(
                        self.target_version_receiver, updated_receiver_version
                    ), Report.logFail(
                        f"{self.target_version_receiver} not in {updated_receiver_version}"
                    )
                Report.logPass("Update via OTA finished with success.")

            if self.save_pass_logs:
                test_name = f"{test_run}_PASS_{test_name}"
                self._stop_recording(save_record=True)
                self.tune_app.save_logitune_logs_in_testlogs(
                    testlogs_path=self.logdirectory, test_name=test_name
                )
            else:
                self._stop_recording()
        except Exception as ex:
            test_name = f"{test_run}_FAIL_{test_name}"
            self._stop_recording(save_record=True)
            self.tune_app.save_logitune_logs_in_testlogs(
                testlogs_path=self.logdirectory, test_name=test_name
            )

            if JENKINS_FWU_CONFIG and self.reconnect_after_fwu_failure:
                disconnect_device(device_name=self.device_name)
                time.sleep(5)
                connect_device(device_name=self.device_name)
                time.sleep(3)
            Report.logException(str(ex))
            raise InterruptedError
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def update_camera_components(self, force_eeprom_update: bool = True) -> None:
        """Runs full loop of firmware (and EEPROM if available) downgrade/update of given camera

        Executes downgrade (if needed) and update of the given camera with provided firmware and EEPROM versions.

        Param force_eeprom_update: True if you want to flash EEPROM during downgrade even if it already has proper version

        Returns: None
        """

        test_name = unittest.TestCase.id(self.test_entity).split(".")[-1]
        test_run = test_name.split("_")[-1]
        test_name = test_name[: -(1 + len(test_run))]

        try:
            self._open_tune()
            self._start_recording(f"{test_run}_{test_name}")
            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.open_about_the_device(device_name=self.device_name)
            self.tune_app.click_more_details()
            (
                current_firmware,
                current_eeprom,
            ) = self.tune_app.get_camera_fw_versions_from_more_details(
                ["Firmware", "EEPROM Version"]
            )

            self.tune_app.close_more_details()

            ### DOWNGRADE
            Report.logInfo("Starting downgrade process...")
            # Compare current and baseline firmware version to determine whether downgrade is necessary
            if not self.tune_app.validate_versions(
                current_firmware, self.baseline_version_device
            ):
                Report.logInfo(
                    f"Current firmware version ({current_firmware}) is different from desired baseline "
                    f"version ({self.baseline_version_device}). Staring firmware downgrade via EasterEgg..."
                )

                updated_device_version = self.tune_app.update_firmware_with_easter_egg(
                    device_file_path=self.file_path_device,
                    device_name=self.device_name,
                    timeout=self.timeout,
                ).split("\n")[0]

                Report.logInfo(
                    f"{self.device_name} firmware version after EasterEgg: {updated_device_version}",
                    screenshot=True,
                )
            else:
                Report.logInfo(
                    f"{self.device_name} already has correct firmware version: {self.baseline_version_device}"
                )

            # If EEPROM update is desired: force EEPROM update or compare current and baseline firmware version to determine whether downgrade is necessary
            if (
                current_eeprom and self.baseline_version_eeprom and self.target_version_eeprom
            ):
                if force_eeprom_update or not self.tune_app.validate_versions(
                    current_eeprom, self.baseline_version_eeprom, eeprom_validation=True
                ):
                    Report.logInfo(
                        f"Current EEPROM version: {current_eeprom}. Updating to desired baseline version: {self.baseline_version_eeprom}..."
                    )

                    self.tune_app.update_firmware_with_easter_egg(
                        device_file_path=self.file_path_eeprom,
                        device_name=self.device_name,
                        timeout=self.timeout,
                    ).split("\n")[0]

                    self.tune_app.click_more_details()
                    updated_eeprom_version = "".join(
                        self.tune_app.get_camera_fw_versions_from_more_details(
                            ["EEPROM Version"]
                        )
                    )
                    self.tune_app.close_more_details()

                    Report.logInfo(
                        f"{self.device_name} EEPROM version after EasterEgg: {updated_eeprom_version}"
                    )
                else:
                    Report.logInfo(
                        f"{self.device_name} already has correct EEPROM version: {self.baseline_version_eeprom}"
                    )
            else:
                Report.logInfo(
                    "No EEPROM Version available in Tune or update is not desired"
                )

            ### UPDATE
            # Updating via OTA
            Report.logInfo(
                f"Start {self.device_name} update via OTA to: {self.target_version_device}",
                screenshot=True,
            )

            updated_camera_version = self.tune_app.start_update_from_device_tab(
                device_name=self.device_name,
                timeout=self.timeout,
            )

            Report.logInfo(
                f"{self.device_name} version after OTA: {updated_camera_version}",
                screenshot=True,
            )

            assert self.tune_app.validate_versions(
                self.target_version_device, updated_camera_version[0]
            ), Report.logFail(
                f"{self.target_version_device} not in {updated_camera_version}"
            )

            Report.logPass("Update via OTA finished with success")

            if self.save_pass_logs:
                test_name = f"{test_run}_PASS_{test_name}"
                self._stop_recording(save_record=True)
                self.tune_app.save_logitune_logs_in_testlogs(
                    testlogs_path=self.logdirectory, test_name=test_name
                )
            else:
                self._stop_recording()
        except Exception as ex:
            test_name = f"{test_run}_FAIL_{test_name}"
            self._stop_recording(save_record=True)
            self.tune_app.save_logitune_logs_in_testlogs(
                testlogs_path=self.logdirectory, test_name=test_name
            )
            if JENKINS_FWU_CONFIG:
                disconnect_device(device_name=self.device_name)
                time.sleep(5)
                connect_device(device_name=self.device_name)
                time.sleep(3)
            Report.logException(str(ex))
            raise InterruptedError
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()

    def update_cybermorph_components(self) -> None:
        """Runs full loop of firmware downgrade/update for Cybermorph's headsets components.

        Executes downgrade (if needed) and update of the given device with provided firmwares.

        Returns: None

        The following easter egg updates possible:

            tahiti<whatever>.bin for Tahiti
            tahiti<whatever>force.bin for forced Tahiti
            qcom<whatever>.bin for Qualcomm
            <whatever>.bin for Qualcomm followed by Tahiti
            <whatever>force.bin for Qualcomm followed by forced Tahiti
        The names are case-insensitive.

        """

        test_name = unittest.TestCase.id(self.test_entity).split(".")[-1]
        test_run = test_name.split("_")[-1]
        test_name = test_name[: -(1 + len(test_run))]

        try:
            baseline = "/".join(
                [ver for ver in (
                    self.baseline_version_device,
                    self.baseline_version_tahiti,
                    self.baseline_version_receiver,
                )
                    if ver is not None
                ]
            )
            target = "/".join(
                [ver for ver in (
                    self.target_version_device,
                    self.target_version_tahiti,
                    self.target_version_receiver,
                )
                    if ver is not None
                ]
            )
            is_receiver = ("" if self.baseline_version_receiver is None else " with receiver")
            Report.logInfo(
                f"Start {self.device_name} update{is_receiver}: {baseline} -> {target}"
            )
            self._open_tune()
            self._start_recording(f"{test_run}_{test_name}")
            self.tune_app.open_device_in_my_devices_tab(self.device_name)
            self.tune_app.open_about_the_device(device_name=self.device_name)

            # Get headset and receiver versions
            is_same_core_version = self.tune_app.is_same_version(
                device_name=self.device_name,
                device_expected_version=self.baseline_version_device,
                receiver_expected_version=self.baseline_version_receiver,
            )

            # Get Tahiti Audio version
            self.tune_app.click_more_details()
            (current_tahiti) = self.tune_app.get_camera_fw_versions_from_more_details(["Audio version"])
            self.tune_app.close_more_details()

            ### DOWNGRADE
            Report.logInfo("Starting downgrade process...")
            if not all(is_same_core_version.values()) or not self.tune_app.validate_versions(current_tahiti[0], self.baseline_version_tahiti):
                Report.logInfo(
                    f"Start {self.device_name} downgrade via easterEgg to: "
                    f"{self.baseline_version_device}"
                )

                if is_same_core_version.get("device"):
                    skip_qcom_downgrade = True
                    Report.logInfo(
                        f"{self.device_name} already has correct version: "
                        f"{self.baseline_version_device}"
                    )
                else:
                    skip_qcom_downgrade = False
                    Report.logInfo(f"Start headset downgrade to: {self.baseline_version_device}")
                    device_version = self.tune_app.update_firmware_with_easter_egg(
                        device_file_path=self.file_path_device,
                        device_name=self.device_name,
                        timeout=self.timeout,
                    ).split("\n")[0]
                    Report.logInfo(
                        f"{self.device_name} version after easterEgg: {device_version}",
                        screenshot=True,
                    )
                    assert self.tune_app.validate_versions(
                        self.baseline_version_device, device_version
                    ), Report.logFail(
                        f"{self.baseline_version_device} not in {device_version}"
                    )

                if not skip_qcom_downgrade:
                    # Get Tahiti Audio version
                    self.tune_app.click_more_details()
                    (current_tahiti) = self.tune_app.get_camera_fw_versions_from_more_details(["Audio version"])
                    self.tune_app.close_more_details()

                if self.tune_app.validate_versions(current_tahiti[0], self.baseline_version_tahiti):
                    Report.logInfo(
                        f"{self.device_name} already has correct Tahiti version: "
                        f"{self.baseline_version_tahiti[0]}"
                    )
                else:
                    Report.logInfo(f"Start Tahiti downgrade to: {self.baseline_version_tahiti}")
                    device_version = self.tune_app.update_firmware_with_easter_egg(
                        device_file_path=self.file_path_tahiti,
                        device_name=self.device_name,
                        timeout=self.timeout,
                    ).split("\n")[0]
                    self.tune_app.click_more_details()
                    (tahiti_version_after_downgrade) = self.tune_app.get_camera_fw_versions_from_more_details(["Audio version"])
                    Report.logInfo(
                        f"{self.device_name} Tahiti version after easterEgg: {tahiti_version_after_downgrade[0]}",
                        screenshot=True,
                    )
                    self.tune_app.close_more_details()

                    assert self.tune_app.validate_versions(
                        self.baseline_version_tahiti, tahiti_version_after_downgrade[0]
                    ), Report.logFail(
                        f"{self.baseline_version_tahiti} not in {tahiti_version_after_downgrade[0]}"
                    )

                if self.baseline_version_receiver:
                    if is_same_core_version.get("receiver"):
                        Report.logInfo(
                            f"Receiver already has correct version: "
                            f"{self.baseline_version_receiver}"
                        )
                    else:
                        Report.logInfo(f"Start Receiver downgrade to: {self.baseline_version_receiver}")
                        receiver_version = (
                            self.tune_app.update_firmware_with_easter_egg(
                                device_file_path=self.file_path_receiver,
                                device_name=self.device_name,
                                is_receiver=True,
                                timeout=self.timeout,
                            ).split("\n")[1]
                        )
                        Report.logInfo(
                            f"Receiver version after easterEgg: {receiver_version}",
                            screenshot=True,
                        )
                        assert self.tune_app.validate_versions(
                            self.baseline_version_receiver, receiver_version
                        ), Report.logFail(
                            f"{self.baseline_version_receiver} not in {receiver_version}"
                        )

                Report.logPass("Downgrade via Easter Egg finished with success.")
                self.tune_app.close_tune_app()

                time.sleep(5)
                if self.save_pass_logs:
                    self.tune_app.open_tune_app()
                else:
                    self.tune_app.open_tune_app(clean_logs=True)
                self.tune_app.open_device_in_my_devices_tab(self.device_name)
                self.tune_app.open_about_the_device(device_name=self.device_name)
            else:
                Report.logInfo(
                    f"{self.device_name} already has correct version: "
                    f"{self.baseline_version_device}"
                )
                Report.logInfo(
                    f"{self.device_name} already has correct Tahiti version: "
                    f"{self.baseline_version_tahiti}"
                )
                if self.baseline_version_receiver:
                    Report.logInfo(
                        f"Receiver already has correct version: {self.baseline_version_receiver}"
                    )


            ### UPDATE
            # Updating via OTA
            Report.logInfo(
                f"Start {self.device_name} update via OTA to: {self.target_version_device}",
                screenshot=True,
            )
            updated_version = self.tune_app.start_update_from_device_tab(
                device_name=self.device_name,
                timeout=self.timeout,
            )
            if len(updated_version) > 1:
                updated_device_version, updated_receiver_version = updated_version
            else:
                updated_device_version = updated_version[0]
                updated_receiver_version = None

            Report.logInfo(
                f"{self.device_name} version after OTA: {updated_device_version}",
                screenshot=True,
            )
            self.tune_app.click_more_details()
            (tahiti_version_after_ota) = self.tune_app.get_camera_fw_versions_from_more_details(["Audio version"])
            Report.logInfo(
                f"{self.device_name} Tahiti version after OTA: {tahiti_version_after_ota[0]}",
                screenshot=True,
            )
            self.tune_app.close_more_details()

            assert self.tune_app.validate_versions(
                self.target_version_device, updated_device_version
            ), Report.logFail(
                f"{self.target_version_device} not in {updated_device_version}"
            )
            assert self.tune_app.validate_versions(
                self.target_version_tahiti, tahiti_version_after_ota[0]
            ), Report.logFail(
                f"{self.target_version_tahiti} not in {tahiti_version_after_ota[0]}"
            )
            if updated_receiver_version is not None:
                Report.logInfo(
                    f"Receiver version after OTA: {updated_receiver_version}",
                    screenshot=True,
                )
                assert self.tune_app.validate_versions(
                    self.target_version_receiver, updated_receiver_version
                ), Report.logFail(
                    f"{self.target_version_receiver} not in {updated_receiver_version}"
                )
            Report.logPass("Update via OTA finished with success.")

            if self.save_pass_logs:
                test_name = f"{test_run}_PASS_{test_name}"
                self._stop_recording(save_record=True)
                time.sleep(10)
                self.tune_app.save_logitune_logs_in_testlogs(
                    testlogs_path=self.logdirectory, test_name=test_name
                )
            else:
                self._stop_recording()
        except Exception as e:
            test_name = f"{test_run}_FAIL_{test_name}"
            self._stop_recording(save_record=True)
            time.sleep(10)
            self.tune_app.save_logitune_logs_in_testlogs(
                testlogs_path=self.logdirectory, test_name=test_name
            )
            if JENKINS_FWU_CONFIG:
                disconnect_device(device_name=self.device_name)
                time.sleep(5)
                connect_device(device_name=self.device_name)
                time.sleep(3)
            Report.logException(str(e))
            raise InterruptedError
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()
