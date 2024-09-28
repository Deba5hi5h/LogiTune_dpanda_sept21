import logging
import os
import unittest
import time

from extentreport.report import Report
from parameterized import parameterized
from testsuite_firmware_api_tests.update_tests.base.quadrun_receiver_fwu_base import (
    UpdateQuadrunReceiver)
from testsuite_tune_app.update_easteregg.device_parameters import zone_vibe_130


log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
firmware_directory = os.path.join(directory, "firmware_tunes", "easterEgg")

DEVICE = zone_vibe_130


class QuadrunUpdateForZoneVibe130(UpdateQuadrunReceiver):

    @classmethod
    def setUpClass(cls):
        baseline_file = os.path.join(
            firmware_directory,
            f"Quadrun_PB1_Release_Version_{DEVICE.baseline_dongle_version}_DFU_image.bin",
        )
        target_file = os.path.join(
            firmware_directory,
            f"Quadrun_PB1_Release_Version_{DEVICE.target_dongle_version}_DFU_image.bin",
        )

        cls.device_address = DEVICE.dongle_address
        cls.device_name = DEVICE.device_name
        cls.timeout = 20
        cls.firmware_downgrade = {"fw_version": DEVICE.baseline_dongle_version,
                                  "binary_path": baseline_file}
        cls.firmware_update = {"fw_version": DEVICE.target_dongle_version,
                               "binary_path": target_file}

        super(QuadrunUpdateForZoneVibe130, cls).setUpClass()

    @parameterized.expand([(x,) for x in range(1, DEVICE.repeats + 1)])
    def test_01_VC_YYYYY_update_quadrun_for_zone_vibe_130(self, retry):
        Report.logInfo(f"Try number: {retry}")
        try:
            for step in (self.firmware_downgrade, self.firmware_update):
                self.flash_firmware(**step, timeout=self.timeout)
        except Exception as e:
            Report.logException(repr(e))
            time.sleep(self.timeout)
            raise e

    @classmethod
    def tearDownClass(cls):
        super(QuadrunUpdateForZoneVibe130, cls).tearDownClass()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(QuadrunUpdateForZoneVibe130)
    unittest.TextTestRunner(verbosity=2).run(suite)
