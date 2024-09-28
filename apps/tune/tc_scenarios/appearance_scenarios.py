
from apps.tune.tc_scenarios.base_scenarios import BaseScenarios
from apps.tune.tune_ui_methods import TuneUIMethods
from apps.tune.TuneAppSettings import TuneAppSettings
from apps.tune.TuneElectron import TuneElectron
from common.comparators import Comparator
from common.framework_params import INSTALLER
from common.platform_helper import get_dark_mode_value, set_dark_mode
from extentreport.report import Report


class AppearanceScenarios(BaseScenarios):

    def appearance_assert(self, condition, log_pass, log_fail, screenshot_on_pass=True):
        self._assert(condition, log_pass, log_fail, screenshot_on_pass, wait_before_assert=1)

    def tc_check_apperance_mode_after_change_with_button(self) -> None:
        try:
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_appearance_button()

            Report.logInfo("Checking if appearance popup is visible")
            self.appearance_assert(
                condition=self.tune_pages.settings.verify_appearance_label_visible(),
                log_pass="Appearance Popup is visible",
                log_fail="Appearance Popup is not visible",
                screenshot_on_pass=True
            )

            Report.logInfo("Clicking light mode and checking if light mode is present")
            self.tune_pages.settings.click_light_mode_button()
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == 'light',
                log_pass="Light mode is present as intended",
                log_fail="Light mode is not present"
            )

            Report.logInfo("Clicking dark mode and checking if dark mode is present")
            self.tune_pages.settings.click_dark_mode_button()
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == 'dark',
                log_pass="Dark mode is present as intended",
                log_fail="Dark mode is not present"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

        finally:
            self.tune_pages.settings.click_close_appearance_button()
            self.tune_pages.settings.click_close_button()

    def tc_check_appearance_mode_applied_after_system_mode_changes(self) -> None:
        try:
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_appearance_button()

            Report.logInfo("Checking if appearance popup is visible")
            self.appearance_assert(
                condition=self.tune_pages.settings.verify_appearance_label_visible(),
                log_pass="Appearance Popup is visible",
                log_fail="Appearance Popup is not visible",
                screenshot_on_pass=True
            )

            current_dark_mode: bool = get_dark_mode_value()
            Report.logInfo(f"Current dark mode status on system is: {current_dark_mode}")

            Report.logInfo(f"Clicking system mode and checking if {current_dark_mode} mode is present")
            self.tune_pages.settings.click_system_mode_button()

            expected_mode = 'dark' if current_dark_mode else 'light'

            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == expected_mode,
                log_pass=f"{expected_mode} mode is present as set in the system",
                log_fail=f"{expected_mode} mode is not present"
            )

            Report.logInfo(f"Toggling dark mode on system to {not current_dark_mode}")
            set_dark_mode(not current_dark_mode)

            toggled_dark_mode: bool = get_dark_mode_value()

            self.appearance_assert(
                condition=toggled_dark_mode is not current_dark_mode,
                log_pass="Dark mode toggled on system with success",
                log_fail="Dark mode toggling on system failed"
            )

            expected_mode = 'dark' if toggled_dark_mode else 'light'

            Report.logInfo("Checking if system dark mode toggle is affecting tune")
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == expected_mode,
                log_pass=f"{expected_mode} mode is present as set in the system",
                log_fail=f"{expected_mode} mode is not present"
            )

            Report.logInfo("Toggling dark mode to its starting value")
            set_dark_mode(current_dark_mode)

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

        finally:
            self.tune_pages.settings.click_close_appearance_button()
            self.tune_pages.settings.click_close_button()

    def tc_check_appearance_mode_persistency_after_relaunch(self) -> None:
        try:
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_appearance_button()

            Report.logInfo("Checking if appearance popup is visible")
            self.appearance_assert(
                condition=self.tune_pages.settings.verify_appearance_label_visible(),
                log_pass="Appearance Popup is visible",
                log_fail="Appearance Popup is not visible",
                screenshot_on_pass=True
            )

            current_dark_mode: bool = get_dark_mode_value()
            Report.logInfo(f"Current dark mode status on system is: {current_dark_mode}")

            Report.logInfo(f"Clicking system mode and checking if {current_dark_mode} mode is present")
            self.tune_pages.settings.click_system_mode_button()

            expected_mode = 'dark' if current_dark_mode else 'light'

            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == expected_mode,
                log_pass=f"{expected_mode} mode is present as set in the system",
                log_fail=f"{expected_mode} mode is not present"
            )

            destination_mode = not current_dark_mode
            destination_mode_str = 'dark' if destination_mode else 'light'
            Report.logInfo(f"Changing mode to opposite that currently set on system - {destination_mode_str}")

            if destination_mode:
                self.tune_pages.settings.click_dark_mode_button()
            else:
                self.tune_pages.settings.click_light_mode_button()

            Report.logInfo(f"Checking if mode was successfully set to: {destination_mode_str}")
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == destination_mode_str,
                log_pass=f"{destination_mode_str} mode is present",
                log_fail=f"{destination_mode_str} mode is not present"
            )
            Report.logInfo("Restarting tune App")
            tune_app: TuneElectron = TuneElectron()
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_quit()
            tune_app.open_tune_app()
            Report.logInfo("Entering appearance options")
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_appearance_button()

            Report.logInfo("Checking if previously set mode persisted relaunching")
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == destination_mode_str,
                log_pass=f"Previously set mode: {destination_mode_str} persisted tune relaunching",
                log_fail=f"Previously set mode: {destination_mode_str} did not persist relaunching"
            )

            Report.logInfo("Setting appearance mode to system")
            self.tune_pages.settings.click_system_mode_button()

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

        finally:
            self.tune_pages.settings.click_close_appearance_button()
            self.tune_pages.settings.click_close_button()

    def tc_check_appearance_mode_persistency_after_update(self) -> None:
        tune_app = TuneElectron()
        tune_methods = TuneUIMethods()
        tune_settings = TuneAppSettings()
        try:
            Report.logInfo(f"Installing Tune Version {INSTALLER}")
            tune_methods.tc_install_logitune(INSTALLER)
            tune_app.open_tune_app()

            Report.logInfo("Entering about page")
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_about()

            tune_version = self.tune_pages.about_page.get_tune_version()

            self._assert(
                condition=tune_version == INSTALLER,
                log_pass="Currently installed version matches INSTALLER version",
                log_fail="Currently installed version is not matching INSTALLER version"
            )

            Report.logInfo("Clicking close button to exit about page")
            self.tune_pages.about_page.click_close_button()

            Report.logInfo("Entering appearance options")

            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_appearance_button()

            Report.logInfo("Checking if appearance popup is visible")
            self.appearance_assert(
                condition=self.tune_pages.settings.verify_appearance_label_visible(),
                log_pass="Appearance Popup is visible",
                log_fail="Appearance Popup is not visible",
                screenshot_on_pass=True
            )

            current_dark_mode: bool = get_dark_mode_value()
            Report.logInfo(f"Current dark mode status on system is: {current_dark_mode}")

            Report.logInfo(f"Clicking system mode and checking if {current_dark_mode} mode is present")
            self.tune_pages.settings.click_system_mode_button()

            expected_mode = 'dark' if current_dark_mode else 'light'

            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == expected_mode,
                log_pass=f"{expected_mode} mode is present as set in the system",
                log_fail=f"{expected_mode} mode is not present"
            )

            destination_mode = not current_dark_mode
            destination_mode_str = 'dark' if destination_mode else 'light'
            Report.logInfo(f"Changing mode to opposite that currently set on system - {destination_mode_str}")

            if destination_mode:
                self.tune_pages.settings.click_dark_mode_button()
            else:
                self.tune_pages.settings.click_light_mode_button()

            Report.logInfo(f"Checking if mode was successfully set to: {destination_mode_str}")
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == destination_mode_str,
                log_pass=f"{destination_mode_str} mode is present",
                log_fail=f"{destination_mode_str} mode is not present"
            )
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_quit()

            Report.logInfo("Updating Tune App")
            tune_settings.adjust_logitune_settings_file(app_update='dev2')
            tune_app.open_tune_app(update=True)
            tune_app.click_update_logitune_now()
            Report.logInfo("Wait for Tune Update Finish")
            self._assert(
                condition=tune_app.wait_for_tune_restart(),
                log_pass="Logi Tune Update Process finished",
                log_fail="Logi Tune Update process not finished correctly"
            )
            tune_app.reopen_tune_app()

            self.tune_pages.home.click_update_finished_ok_if_visible()

            Report.logInfo("Entering about page")
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_about()

            tune_version_updated = self.tune_pages.about_page.get_tune_version()

            self._assert(
                condition=Comparator.compare_versions(tune_version_updated, tune_version) == 1,
                log_pass="Tune version after update is higher than base version",
                log_fail="Tune version after update is not higher than base version"
            )

            Report.logInfo("Clicking close button to exit about page")
            self.tune_pages.about_page.click_close_button()

            Report.logInfo("Entering appearance options")
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_settings()
            self.tune_pages.settings.click_appearance_button()

            Report.logInfo("Checking if previously set mode persisted relaunching")
            self.appearance_assert(
                condition=self.tune_pages.settings.get_appearance_mode() == destination_mode_str,
                log_pass=f"Previously set mode: {destination_mode_str} persisted tune app update",
                log_fail=f"Previously set mode: {destination_mode_str} did not persist app update"
            )

        except Exception as e:
            Report.logException(f"During test exception occurred: {repr(e)}")

        finally:
            self.tune_pages.settings.click_close_appearance_button()
            self.tune_pages.settings.click_close_button()
            Report.logInfo(f"Installing Tune Version {INSTALLER} after tests")
            tune_methods.tc_install_logitune(INSTALLER)
            tune_app.open_tune_app()

            Report.logInfo("Entering about page")
            self.tune_pages.home.click_more_options()
            self.tune_pages.home.click_about()

            tune_version = self.tune_pages.about_page.get_tune_version()

            self._assert(
                condition=tune_version == INSTALLER,
                log_pass="Currently installed version matches INSTALLER version",
                log_fail="Currently installed version is not matching INSTALLER version"
            )
