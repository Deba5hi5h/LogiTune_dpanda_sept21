import logging
import os
import time
import unittest

from base.base_ui import UIBase
from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_tune_app.update_easteregg.device_parameters_jenkins import bomberman_stereo

from apps.tune.TuneElectron import TuneElectron, disconnect_device, connect_device, disconnect_all

log = logging.getLogger(__name__)
directory = os.path.dirname(os.path.dirname(__file__))


class DetectBombermanStereo(UIBase):
    tune_app = TuneElectron()
    device_name = bomberman_stereo.device_name
    conn_type = ConnectionType.dongle

    def test_001_VC_143762_detect_bomberman_stereo(self):
        try:
            disconnect_all()
            self.tune_app.open_tune_app()
            self.tune_app.open_my_devices_tab()
            for i in range(1, 5):
                Report.logInfo(f"{self.device_name} detection. Try {i}")
                time.sleep(5)
                connect_device(self.device_name)
                time.sleep(10)
                self.tune_app.is_device_label_displayed(self.device_name)
                disconnect_device(self.device_name)
                time.sleep(5)

        except Exception as e:
            Report.logException(str(e))
        finally:
            if self.tune_app:
                self.tune_app.close_tune_app()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DetectBombermanStereo)
    unittest.main(warnings='ignore')
    unittest.TextTestRunner(verbosity=2).run(suite)




