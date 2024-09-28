import logging
import unittest
import re

from parameterized import parameterized

from extentreport.report import Report
from apps.tune.TuneElectron import TuneElectron
from base.fwu_stress_base import FwuStressBase
from testsuite_tune_app.update_easteregg.device_parameters import language_update
from common.recorder import initialize_recorder
from common.framework_params import TUNE_RECORDER


log = logging.getLogger(__name__)


class LanguageDownload(FwuStressBase):
    """
    Suite class for Language Download tests via EasterEgg and OTA.
    """
    recorder = None

    def _start_recording(self, tune_app: TuneElectron, test_name: str):
        if TUNE_RECORDER:
            window_coordinates = tune_app.get_window_position_and_size()
            self.recorder = initialize_recorder(self.logdirectory, test_name, **window_coordinates)
            self.recorder.start_recording()

    def _stop_recording(self, save_record: bool = False):
        if TUNE_RECORDER:
            self.recorder.stop_recording_and_save()
            if not save_record:
                self.recorder.delete()

    @parameterized.expand([(x, language) for x in range(1, language_update.repeats + 1) for
                           language in language_update.languages])
    def test_language_download(self, retry, language):
        """
        Scenario:
        1. Downgrade Headset via Easter Egg.
        2. Update Headset via OTA.
        """
        language_name = re.search(r"LANGUAGE_(.*)\'", language.radio_locator[1]).group(1)
        Report.logInfo(f"Try number: {retry} for language {language_name}")

        tune_app = TuneElectron()
        test_name = unittest.TestCase.id(self).split('.')[-1]
        try:
            tune_app.open_tune_app(clean_logs=True)
            self._start_recording(tune_app, test_name)
            tune_app.open_device_in_my_devices_tab(language_update.device_name)
            tune_app.open_languages_tab()
            tune_app.start_language_update(language.button_locator)
            tune_app.open_device_in_my_devices_tab(language_update.device_name, skip_exception=True)
            tune_app.open_languages_tab()
            tune_app.verify_language_update_success(language.radio_locator)
            self._stop_recording()
        except Exception as ex:
            self._stop_recording(save_record=True)
            tune_app.save_logitune_logs_in_testlogs(
                testlogs_path=self.logdirectory, test_name=unittest.TestCase.id(self)
            )
            Report.logException(str(ex))
        finally:
            if tune_app:
                tune_app.close_tune_app()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LanguageDownload)
    unittest.TextTestRunner(verbosity=2).run(suite)
