import argparse
import unittest
from base import global_variables
from common import config
from common.email_notification import EmailNotification
from testsuite_tune_app.tc00_install import TuneInstall
from testsuite_tune_app.tc01_webcam_brio import WebcamBrio
from testsuite_tune_app.tc04_webcam_c930e import WebcamC930e
from testsuite_tune_app.tc16_webcam_brio_30X import WebcamBrio30X
from testsuite_tune_app.tc08_webcam_brio_50X import WebcamBrio50X
from testsuite_tune_app.tc17_webcam_brio_70X import WebcamBrio70X
from testsuite_tune_app.tc20_uninstall import TuneUninstall

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
        'brio': (WebcamBrio, ['test_101_VC_58353_connect_webcam_brio',
                              'test_116_VC_101079_parameters_persistency_after_fw_update_brio']),
        'c930e': (WebcamC930e, ['test_401_VC_58425_connect_webcam_c930e',
                                'test_415_VC_101078_parameters_persistency_after_fw_update_c930e']),
        'brio30x': (WebcamBrio30X, ['test_1601_VC_77175_connect_webcam_brio_30X',
                                    'test_1611_VC_101080_parameters_persistency_after_fw_update_brio_30X']),
        'brio50x': (WebcamBrio50X, ['test_801_VC_69975_connect_webcam_brio_50X',
                                    'test_816_VC_101082_parameters_persistency_after_fw_update_brio_50X']),
        'brio70x': (WebcamBrio70X, ['test_1701_VC_88128_connect_webcam_brio_70X',
                                    'test_1716_VC_101081_parameters_persistency_after_fw_update_brio_70X']),
    }

    # Now iterate over each item in the dictionary
    devices = ['brio', 'c930e', 'brio30x', 'brio50x', 'brio70x']
    if args.devices != "all":
        devices = args.devices.strip().split(",")

    # Create the suite and add the tests
    suites = {name: unittest.TestSuite() for name in devices}
    for device in devices:
        if device in device_tests_mapping:
            test_class, test_cases = device_tests_mapping[device]
            suites[device].addTests(load_tests(test_class, test_cases))

    if args.email_notification:
        global_variables.email_flag = True
        EmailNotification.send_job_email()

    global_variables.teardownFlag = False

    test_runner = unittest.TextTestRunner()
    test_runner.run(suite_install)

    # Iterate only over the suites we are interested in, based on the provided installer
    for suite in devices:
        test_runner.run(suites[suite])

    global_variables.teardownFlag = True
    test_runner.run(suite_uninstall)
    if args.email_notification:
        global_variables.email_to = ",".join(MAILING_LIST)


if __name__ == "__main__":
    main()
