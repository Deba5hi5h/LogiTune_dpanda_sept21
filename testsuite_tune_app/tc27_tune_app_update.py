import unittest

from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneElectron import TuneElectron
from base.base_ui import UIBase
from common.framework_params import INSTALLER, MAC_SLAVE_PASS


class TuneAppUpdate(UIBase):
    """
    Test class containing LogiTune App Update tests.
    """
    # used in tearDown to update test status on zephyr
    cycle_name = "UI"

    tune_app = TuneElectron()
    tune_methods = TuneUIMethods()

    def test_2701_VC_99961_tune_app_update_from_production(self) -> None:
        """
        Test method to Update App from production version to the latest release on QA channel
        """
        # Get production version as baseline version
        production_version = self.tune_methods.tc_get_tune_production_ver()
        latest_version = INSTALLER

        # Skip if the latest release is the same as production version
        if production_version in latest_version:
            self.skipTest("Production version is the same as latest release. Skip this test.")

        # Install production version and then update to the latest release
        self.tune_methods.tc_install_logitune(version=production_version)
        self.tune_methods.tc_update_logitune()

        # Verify if updated version is equal to INSTALLER
        self.tune_methods.tc_verify_tune_updated(latest_version, MAC_SLAVE_PASS)


if __name__ == "__main__":
    unittest.main()
