import unittest

from common import config
# Command Line arguments
import argparse

from common.email_notification import EmailNotification

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'SyncApp')

from base import global_variables
from testsuite_sync_app.tc00_install import Install
from testsuite_sync_app.tc04_kong import Kong
from testsuite_sync_app.tc25_uninstall import Uninstall

# Load Tests
tests_Install = unittest.TestLoader().loadTestsFromTestCase(Install)

# Setup Suite
suite_Install = unittest.TestSuite(tests_Install)  # All test cases
suite_Kong = unittest.TestSuite()
suite_Uninstall = unittest.TestSuite()

# Add CollabOS compatibility test cases to suite

suite_Kong.addTests([Kong('test_401_VC_39951_rallybar_add_device'),
                     Kong('test_405_VC_58626_rallybar_rightsight2'),
                     Kong('test_409_VC_XXXX_rallybar_groupview_speakerview_persistence'),
                     Kong('test_412_VC_40029_rallybar_antiflicker_settings'),
                     Kong('test_415_VC_40035_rallybar_audio_speaker_boost'),
                     Kong('test_417_VC_40037_rallybar_audio_ai_noise_suppression'),
                     Kong('test_420_VC_72050_rallybar_audio_reverb_control_device'),
                     Kong('test_422_VC_53060_rallybar_audio_microphone_eq_device'),
                     Kong('test_424_VC_53062_rallybar_audio_speaker_eq_device'),
                     Kong('test_425_VC_69201_rallybar_manual_color_settings_in_sync'),
                     Kong('test_429_VC_69205_rallybar_camera_settings_floating_window'),
                     Kong('test_431_VC_69200_rallybar_camera_settings_adjustments'),
                     Kong('test_432_VC_39957_rallybar_forget_device')
                     ])
suite_Uninstall.addTests([Uninstall('test_251_VC_39960_disconnect_from_sync_app'),
                          Uninstall('test_258_VC_39961_uninstall_sync_app')
                          ])

# Run Suite
global_variables.retry_count = 1
global_variables.test_category = 'CollabOS-Compatibility'
global_variables.teardownFlag = False
unittest.TextTestRunner().run(suite_Install)
unittest.TextTestRunner().run(suite_Kong)
global_variables.teardownFlag = True
unittest.TextTestRunner().run(suite_Uninstall)
