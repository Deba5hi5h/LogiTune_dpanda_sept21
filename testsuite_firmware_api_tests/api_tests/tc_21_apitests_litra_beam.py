import random
import time
import unittest

from base import global_variables
from base.base_ui import UIBase

from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features


class LitraBeamApiTests(UIBase):
    """
    Class contains basic API tests for Litra Beam dongle.
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(LitraBeamApiTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name="Litra Beam",
                                          conn_type=ConnectionType.litra_beam,
                                          com_port="")
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "Litra_Beam"
        global_variables.firmware_api_device_conn = ConnectionType.litra_beam

    @classmethod
    def tearDownClass(cls):
        cls.centurion.close_port()
        super(LitraBeamApiTests, cls).tearDownClass()

    def test_2100_VC_XXXXX_set_power_on(self) -> None:
        try:
            self.features.litra_beam.set_power_on()
            response = self.features.litra_beam.get_power_state()
            self.features.litra_beam.verify_power_state(response, 1)

        except Exception as ex:
            Report.logException(str(ex))

    def test_2101_VC_XXXXX_set_get_brightness(self) -> None:
        try:
            min_value, max_value = self.features.litra_beam.get_brightness_info()
            Report.logInfo(f"Min Brightness: {min_value}")
            Report.logInfo(f"Max Brightness: {max_value}")

            value = random.randint(min_value, max_value)

            for x in [min_value, value, max_value]:
                self.features.litra_beam.set_brightness(x)

                time.sleep(1)
                response = self.features.litra_beam.get_brightness()
                self.features.litra_beam.verify_brightness(response, x)

        except Exception as ex:
            Report.logException(str(ex))

    def test_2102_VC_XXXXX_set_get_color_temperature(self) -> None:
        try:
            min_value, max_value = self.features.litra_beam.get_color_temperature_info()
            Report.logInfo(f"Min Temperature: {min_value}")
            Report.logInfo(f"Max Temperature: {max_value}")

            value = random.randrange(min_value, max_value, 100)

            for x in [min_value, value, max_value]:
                self.features.litra_beam.set_color_temperature(x)

                time.sleep(1)
                response = self.features.litra_beam.get_color_temperature()
                self.features.litra_beam.verify_color_temperature(response, x)

        except Exception as ex:
            Report.logException(str(ex))

    def test_2103_VC_XXXXX_set_power_off(self) -> None:
        try:
            self.features.litra_beam.set_power_off()
            response = self.features.litra_beam.get_power_state()
            self.features.litra_beam.verify_power_state(response, 0)

        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LitraBeamApiTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
