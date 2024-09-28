
import argparse
import unittest
from base import global_variables
from common import config
from common.email_notification import EmailNotification
from testsuite_tune_app.tc00_install import TuneInstall
from testsuite_tune_app.tc01_webcam_brio import WebcamBrio
from testsuite_tune_app.tc02_webcam_c920e import WebcamC920e
from testsuite_tune_app.tc04_webcam_c930e import WebcamC930e
from testsuite_tune_app.tc06_webcam_streamcam import WebcamStreamCam
from testsuite_tune_app.tc34_webcam_brio_10X import WebcamBrio10X
from testsuite_tune_app.tc16_webcam_brio_30X import WebcamBrio30X
from testsuite_tune_app.tc08_webcam_brio_50X import WebcamBrio50X
from testsuite_tune_app.tc17_webcam_brio_70X import WebcamBrio70X

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
        'brio': WebcamBrio,
        'c920e': WebcamC920e,
        'c930e': WebcamC930e,
        'streamcam': WebcamStreamCam,
        'brio10x': WebcamBrio10X,
        'brio30x': WebcamBrio30X,
        'brio50x': WebcamBrio50X,
        'brio70x': WebcamBrio70X,
    }

    # Now iterate over each item in the dictionary
    devices = ['brio', 'c920e', 'c930e', 'streamcam', 'brio10x', 'brio30x', 'brio50x', 'brio70x']
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

