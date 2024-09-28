
import argparse
import unittest
from base import global_variables
from common import config
from common.email_notification import EmailNotification
from testsuite_tune_app.tc00_install import TuneInstall
from testsuite_tune_app.tc09_headset_zone_wired import ZoneWired
from testsuite_tune_app.tc10_headset_zone_750 import Zone750
from testsuite_tune_app.tc11_headset_zone_wired_earbuds import ZoneWiredEarbuds
from testsuite_tune_app.tc12_headset_zone_wireless_plus import ZoneWirelessPlus
from testsuite_tune_app.tc13_headset_zone_wireless import ZoneWireless
from testsuite_tune_app.tc14_headset_zone_900 import Zone900
from testsuite_tune_app.tc15_headset_zone_vibe_125 import ZoneVibe125
from testsuite_tune_app.tc24_headset_zone_vibe_wireless import ZoneVibeWireless
from testsuite_tune_app.tc36_headset_zone_950 import Zone950

from testsuite_tune_app.tc41_headset_zone_305 import Zone305
from testsuite_tune_app.tc42_headset_bomberman_mono import BombermanMono
from testsuite_tune_app.tc43_headset_bomberman_stereo import BombermanStereo
from testsuite_tune_app.tc20_uninstall import TuneUninstall
from testsuite_tune_app.verify_device_connection import check_devices


# Extracted setup of commandline arguments to a separate function
def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--installer", help="installer version")
    parser.add_argument("-r", "--retry", help="retry count")
    parser.add_argument("-d", "--devices", help="What devices do you want to use.", default="all")
    parser.add_argument("-e", "--email_notification", help="send email notification", default=True,
                        type=lambda x: (str(x).lower() == 'true'))
    return parser.parse_args()

# Extracted settings migration to a separate function
def setup_settings(instance, args):
    settings_dict = {
        ('JENKINS_FWU_TESTS', 'JENKINS_FWU_CONFIG'): 'True',
        ('RUN_CONFIG', 'PROJECT'): 'LogiTune',
        ('RUN_CONFIG', 'dashboard_publish'): 'True',
        ('RUN_CONFIG', 'jira_update'): 'True'
    }
    if args.installer is not None:
        settings_dict[('RUN_CONFIG', 'INSTALLER')] = args.installer
    return apply_settings(instance, settings_dict)

def apply_settings(settings, settings_dict):
    for key, value in settings_dict.items():
        section, key = key
        settings.set_value_in_section(section, key, value)

def load_tests(test_class, test_cases):
    """Function to load a sequence of tests."""
    return [test_class(test_case) for test_case in test_cases]

def main():
    args = setup_parser()
    settings = config.CommonConfig.get_instance()
    setup_settings(settings, args)

    global_variables.test_category = f'Webcams parameters persistency after firmware update'

    MAILING_LIST = (
        'ptokarczyk@logitech.com',
        'plesniak@logitech.com',
        'rdrozd@logitech.com',
        'sveerbhadrappa@logitech.com',
        'bchandrashekar@logitech.com',
    )

    # Load Tests
    tests_install = unittest.TestLoader().loadTestsFromTestCase(TuneInstall)
    tests_uninstall = unittest.TestLoader().loadTestsFromTestCase(TuneUninstall)

    suite_install = unittest.TestSuite(tests_install)
    suite_uninstall = unittest.TestSuite(tests_uninstall)

    device_tests_mapping = {
        'zone_950': Zone950,
        'zone_wired': ZoneWired,
        'zone_750': Zone750,
        'zone_900': Zone900,
        'zone_wired_earbuds': ZoneWiredEarbuds,
        'zone_wireless': ZoneWireless,
        'zone_wireless_plus': ZoneWirelessPlus,
        'zone_vibe_125': ZoneVibe125,
        'zone_vibe_wireless': ZoneVibeWireless,
        'bomberman_mono': BombermanMono,
        'bomberman_stereo': BombermanStereo,
        'zone_305': Zone305
    }

    # Now iterate over each item in the dictionary
    devices = ['zone_wired', 'zone_750', 'zone_900', 'zone_wired_earbuds', 'zone_wireless', 'zone_wireless_plus',
               'zone_vibe_125', 'zone_vibe_wireless', 'zone_950', 'bomberman_mono', 'bomberman_stereo', 'zone_305']
    if args.devices != "all":
        devices = args.devices.strip().split(",")

    testcases_to_run = []
    for device in devices:
        if device in device_tests_mapping:
            testcases_to_run.append(device_tests_mapping[device])

    check_devices(testcases_to_run=testcases_to_run, mailing_list=MAILING_LIST,
                  skip_missing_devices_in_test_suite=True)

    # Load Tests
    load_tests = [unittest.TestLoader().loadTestsFromTestCase(tc_item)
                  for tc_item in testcases_to_run]

    # Setup Suite
    setup_suite = [unittest.TestSuite(loaded_test) for loaded_test in load_tests]

    if args.email_notification:
        global_variables.email_flag = True
        EmailNotification.send_job_email()

    global_variables.teardownFlag = False

    test_runner = unittest.TextTestRunner()
    test_runner.run(suite_install)

    # Iterate only over the suites we are interested in, based on the provided installer
    for suite in setup_suite:
        unittest.TextTestRunner().run(suite)

    global_variables.teardownFlag = True
    test_runner.run(suite_uninstall)
    if args.email_notification:
        global_variables.email_to = ",".join(MAILING_LIST)


if __name__ == "__main__":
    main()


