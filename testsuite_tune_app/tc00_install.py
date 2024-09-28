import unittest

from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase


class TuneInstall(UIBase):
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()

    def test_001_VC_42593_install_logi_tune(self):
        from common import config
        settings = config.CommonConfig.get_instance()
        version = settings.get_value_from_section('INSTALLER', 'RUN_CONFIG')
        self.tune_methods.tc_install_logitune(version=version)

    def test_002_VC_42594_app_with_no_device(self):
        self.tune_methods.tc_app_with_no_device()


if __name__ == "__main__":
    unittest.main()
