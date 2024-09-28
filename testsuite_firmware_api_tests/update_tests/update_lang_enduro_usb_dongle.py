import logging
import os
import subprocess
import time
import unittest

from parameterized import parameterized
from common.platform_helper import get_custom_platform

from base.base_ui import UIBase
from extentreport.report import Report

from apps.tune.TuneElectron import TuneElectron
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import Features

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
firmware_directory = os.path.join(directory, "firmware_tunes", "Logitech_Enduro")
DIR_PATH = os.path.join(firmware_directory, "Voice_prompt")

# file_name, file_path, cent++ value
lang_de = ("DE_GERMAN", os.path.join(DIR_PATH, f"DE_GERMAN.img"), 3)
lang_en = ("EN_English", os.path.join(DIR_PATH, f"EN_English.img"), 0)
lang_es = ("ES_Spanish", os.path.join(DIR_PATH, f"ES_Spanish.img"), 2)
lang_fr = ("FR_French", os.path.join(DIR_PATH, f"FR_French.img"), 1)
lang_it = ("IT_Italian", os.path.join(DIR_PATH, f"IT_Italian.img"), 6)
lang_pt = ("PT_Portuguese", os.path.join(DIR_PATH, f"PT_Portuguese.img"), 10)

LANGS = [lang_de, lang_en, lang_es, lang_fr, lang_it, lang_pt]
# LANGS = [lang_pt]

enduro_BT = "046D_0AEE_2129ML000028"
enduro_new_MFI_BT = "046D_0AEE_2140ML000EQ8"
enduro_new_not_MFI_BT = "046D_0AEE_2140ML000DJ8"

PLATFORM = get_custom_platform()


class UpdateLanguageEnduroDongleConnection(UIBase):

    @classmethod
    def setUpClass(cls) -> None:
        super(UpdateLanguageEnduroDongleConnection, cls).setUpClass()
        cls.tunesApp = TuneElectron()

    @parameterized.expand([(loop, ver) for loop in range(1, 2) for ver in LANGS])
    def test_XXX_VC_YYYYY_upgrade_language_enduro_directBT_connection(self, loop_no, ver):

        Report.logInfo(f"Loop no: {loop_no}")
        Report.logInfo(f"Update to: {ver[0]}")
        device_mac = enduro_new_not_MFI_BT
        timeout = 20


        try:
            Report.logInfo(f"Start {ver[0]} language installation")
            self.start_performance_test()
            self.__install_enduro_lang(device_mac, ver)
            self.end_performance_test(f"Enduro language {ver[0]} installation finished!")
            time.sleep(timeout)

        except Exception as e:
            Report.get_screenshot()
            Report.logException(str(e))

    def __install_enduro_lang(self, device_mac, ver):
        Report.logInfo(f"Installing Enduro language: {ver[0]}")
        if PLATFORM == 'windows':
            cmd = f"{firmware_directory}\\updater\\FWU_Sample.exe hid_audio_data {device_mac} {ver[1]}"
        else:
            cmd = f"{firmware_directory}/updater/LGT_HID_E_FW_Update_CLT hid_audio_data {device_mac} {ver[1]}"

        Report.logInfo(f"Command: {cmd}")

        try:
            t_res = subprocess.check_output(cmd, shell=True, stdin=subprocess.PIPE)

            Report.logInfo(f" OUTPUT: {t_res}")

            assert "update_successfully" in t_res.decode('utf-8')

            time.sleep(20)

            if PLATFORM == 'windows':
                Report.logInfo(f"Check FW version...")
                self.__verify_fw_lang(ver)

            Report.logInfo(f"Enduro {ver[0]} language installation finished with success!!!!")

        except Exception as e3:
            Report.logException(f"EXCEPTION FOUND + {e3}")

    def __verify_fw_lang(self, ver):
        centurion = CenturionCommands()
        features = Features(centurion)

        response = features.earcon_feature.get_language()
        features.earcon_feature.verify_get_language(response, ver[2])
        centurion.close_port()

        Report.logInfo(f"Current Enduro version is: {ver[0]}")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(UpdateLanguageEnduroDongleConnection)
    unittest.TextTestRunner(verbosity=2).run(suite)
