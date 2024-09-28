import logging
import os
import subprocess
import unittest
import time

from base.base_ui import UIBase
from common.platform_helper import get_custom_platform
from extentreport.report import Report
from parameterized import parameterized

from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import CenturionCommands

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
firmware_directory = os.path.join(directory, "firmware_tunes", "Logitech_Zaxxon")
PLATFORM = get_custom_platform()

pink_dongle = '46D:AEA:2041ML0018S8'


class InstallZaxxonFwUsbDongle(UIBase):

    @classmethod
    def setUpClass(cls):
        super(InstallZaxxonFwUsbDongle, cls).setUpClass()
        cls.stats_file = os.path.join(directory, "firmware_tunes", "Logitech_Zaxxon", f"stats_{round(time.time())}.txt")
        print(f"stats file {cls.stats_file}")
        open(cls.stats_file, 'w').close()  # clear txt file

    @classmethod
    def tearDownClass(cls):
        # cls.__calculate_average_time(cls.stats_file)
        super(InstallZaxxonFwUsbDongle, cls).tearDownClass()


    @parameterized.expand([(x,) for x in range(1, 16)])
    def test_XXX_VC_YYYYY_install_Zaxxon_FW(self, retry):
        Report.logInfo(f"Try number: {retry}")
        timeout = 30

        try:
            versions = ["03.19"]
            for version in versions:
                fw_version = f"03.20"
                Report.logInfo(f"Start FW {fw_version} FW installation.")
                self.start_performance_test()
                self.__install_zaxxon_fw_via_dongle(fw_version)
                elapsed_time = self.end_performance_test(f"Zaxxon FW installation {fw_version} finished!")
                self.__save_elapsed_time_to_file(f"{fw_version}: {round(elapsed_time)} sec")
                time.sleep(timeout)

                fw_version = f"{version}"
                Report.logInfo(f"Start FW {fw_version} FW installation.")
                self.start_performance_test()
                self.__install_zaxxon_fw_via_dongle(fw_version)
                elapsed_time = self.end_performance_test(f"Zaxxon FW installation {fw_version} finished!")
                self.__save_elapsed_time_to_file(f"{fw_version}: {round(elapsed_time)} sec")
                time.sleep(timeout)

        except Exception as e:
            Report.logException(str(e))

    def __save_elapsed_time_to_file(self, elapsed_time):
        with open(self.stats_file, 'a') as file:
            file.write(str(elapsed_time) + '\n')

    @staticmethod
    def __calculate_average_time(stats_file):

        with open(stats_file, 'r') as s_file:
            lines = s_file.readlines()

        values = []
        for str_value in lines:
            values.append(int(str_value))

        with open(stats_file, 'a') as f_file:
            f_file.write(f"average time in second: {round(sum(values)/len(values),1)}")


    def __install_zaxxon_fw_via_dongle(self, fw_version):
        Report.logInfo(f"Installing Zaxxon FW: {fw_version}")
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater\\OTAUpdater.exe -t Dongle -f {firmware_directory}\\files\\Zaxxon_v00.00.{fw_version}_encrypted_ota.bin"
        else:
            cmd = f"{firmware_directory}/updater/Application -t Dongle -f {firmware_directory}/files/Zaxxon_v00.00.{fw_version}_encrypted_ota.bin"
        Report.logInfo(f"Command: {cmd}")

        os.system(cmd)

        # try:
        #     t_res = subprocess.run(cmd, shell=True, timeout=1000, stdout=subprocess.PIPE)
        #
        #     res = t_res.stdout
        #
        #     Report.logInfo("RESPONSE: " + res.decode('utf-8'))
        #
        #     if f"Update Successfully Finished" not in res.decode('utf-8'):
        #         Report.logFail("Zaxxon firmware installation failed")
        #         assert False, "Zaxxon firmware installation failed"
        #
        #     if f"Right Earbud :: v00.00.{fw_version}" not in res.decode('utf-8'):
        #         Report.logFail("Wrong Right Earbud version")
        #         assert False, "Wrong Right Earbud version"
        #
        #     if f"Left  Earbud :: v00.00.{fw_version}" not in res.decode('utf-8'):
        #         Report.logFail("Wrong Left Earbud version")
        #         assert False, "Wrong left Earbud version"
        #
        #     Report.logInfo(f"Zaxxon Firmware installation to {fw_version} finished with success!!!!")
        # except subprocess.TimeoutExpired as tex:
        #     Report.logException(f"TimeoutExpired ERROR FOUND + {tex.stdout.decode('utf-8')}")
        # except subprocess.SubprocessError as e2:
        #     Report.logException(f"SUBPROCESS ERROR FOUND + {e2}")
        # except Exception as e3:
        #     Report.logException(f"EXCEPTION FOUND + {e3}")

    def __verify_fw_version_via_dongle(self, fw_version):
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater\\OTAUpdater.exe -t Dongle -v"
        else:
            cmd = f"{firmware_directory}/updater/Application -t Dongle -v"
        print(f'cmd: {cmd}')

        res = subprocess.check_output(cmd, shell=True)
        print(res.decode('utf-8'))

        assert f"Right Earbud :: v00.00.{fw_version}" in res.decode('utf-8'), "Wrong Right Earbud version"
        assert f"Left  Earbud :: v00.00.{fw_version}" in res.decode('utf-8'), "Wrong Left Earbud version"
        Report.logInfo(f"Current Zaxxon Firmware version: {fw_version}")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(InstallZaxxonFwUsbDongle)
    unittest.TextTestRunner(verbosity=2).run(suite)




