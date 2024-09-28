import time
import unittest

from base import global_variables
from base.base_ui import UIBase

from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.api_parameters import local_api_pc_configuration, quadrun_wo_headset_api
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_commands import \
    CenturionCommands
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.centurion_features.features import \
    Features


class QuadrunDongleWithoutHeadsetApiTests(UIBase):
    """
    Class contains basic API tests for quadrun dongle.
    """

    centurion = None

    @classmethod
    def setUpClass(cls):
        super(QuadrunDongleWithoutHeadsetApiTests, cls).setUpClass()
        cls.centurion = CenturionCommands(device_name=quadrun_wo_headset_api.name,
                                          conn_type=ConnectionType.quadrun,
                                          com_port=local_api_pc_configuration.com_port)
        cls.features = Features(cls.centurion)
        global_variables.firmware_api_device_name = "Zone_Receiver"
        global_variables.firmware_api_device_conn = ConnectionType.dongle

    @classmethod
    def tearDownClass(cls):
        cls.centurion.close_port()
        super(QuadrunDongleWithoutHeadsetApiTests, cls).tearDownClass()

    def test_2000_VC_XXXXX_set_vendor_mode(self) -> None:
        try:
            self.features.quadrun.lock_device()
            response = self.features.quadrun.vendor_mode()
            self.features.quadrun.verify_command_confirmation(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2001_VC_XXXXX_get_firmware_version(self) -> None:
        try:
            response = self.features.quadrun.get_quadrun_fw_version()
            self.features.quadrun.verify_firmware_version(response=response, fw_version=quadrun_wo_headset_api.firmware_version)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2003_VC_XXXXX_set_color_code(self) -> None:
        try:
            colors = {'graphite': [0x00, 0x00],
                      'rose': [0x01, 0x00],
                      'off-white': [0x02, 0x00]}

            for key, value in colors.items():
                self.features.quadrun.set_device_test_mode()
                self.features.quadrun.set_color_code(key, value)
                self.features.quadrun.exit_device_test_mode()
                response = self.features.quadrun.get_color_code()
                self.features.quadrun.verify_get_color_code(response=response,
                                                            color_code=value)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2004_VC_XXXXX_get_product_serial_number(self) -> None:
        try:
            response = self.features.quadrun.get_product_serial_number()
            self.features.quadrun.verify_get_product_serial_number(response=response,
                                                                   serial_number=quadrun_wo_headset_api.serial_number)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2005_VC_XXXXX_set_pairing_mode(self) -> None:
        try:
            response = self.features.quadrun.set_pairing_mode()
            self.features.quadrun.verify_set_pairing_mode(response)
            time.sleep(5)
            response = self.features.quadrun.set_page_scan()
            self.features.quadrun.verify_set_page_scan(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2006_VC_XXXXX_read_bt_address_of_paired_headset(self) -> None:
        try:
            response = self.features.quadrun.read_bt_address_of_paired_headset()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2007_VC_XXXXX_clear_pdl(self) -> None:
        try:
            response = self.features.quadrun.clear_pdl()
            self.features.quadrun.verify_command_confirmation(response)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2008_VC_XXXXX_test_mode(self) -> None:
        try:
            self.features.quadrun.set_device_test_mode()
            time.sleep(1)
            self.features.quadrun.exit_device_test_mode()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2009_VC_XXXXX_unlock_and_lock_quadrun(self) -> None:
        try:
            self.features.quadrun.unlock_device()
            time.sleep(1)
            self.features.quadrun.lock_device()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2010_VC_XXXXX_dfu_mode(self) -> None:
        try:
            self.features.quadrun.enter_dfu_mode()
            self.features.quadrun.get_status_request()

        except Exception as ex:
            Report.logException(str(ex))

    def test_2011_VC_XXXXX_bt_status_indication(self) -> None:
        try:
            for state in [0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
                self.features.quadrun.bt_status_indication(state)
        except Exception as ex:
            Report.logException(str(ex))

    def test_2012_VC_XXXXX_get_led_cycle_duty(self) -> None:
        try:
            self.features.quadrun.get_led_cycle_duty()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2013_VC_XXXXX_connect_device(self) -> None:
        try:
            Report.logSkip("manual")
            self.skipTest("manual")
            self.features.quadrun.connect_device()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2014_VC_XXXXX_clear_page(self) -> None:
        try:
            Report.logSkip("manual")
            self.skipTest("manual")
            self.features.quadrun.clear_page()
        except Exception as ex:
            Report.logException(str(ex))

    def test_2015_VC_XXXXX_disconnect_device(self) -> None:
        try:
            Report.logSkip("manual")
            self.skipTest("manual")
            self.features.quadrun.disconnect_device()
        except Exception as ex:
            Report.logException(str(ex))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(QuadrunDongleWithoutHeadsetApiTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
