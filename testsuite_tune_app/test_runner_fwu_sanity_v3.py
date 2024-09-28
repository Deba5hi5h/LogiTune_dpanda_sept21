"""
IMPORTS NEED TO BE THIS WAY, AS UPDATING SETTINGS FILE
NEEDS TO BE DONE BEFORE IMPORTING IT TO ANY FILE
"""

import argparse
from common import config
from testsuite_tune_app.update_easteregg.tc_111_update_bomberman_mono_easterEggOTA import UpdateBombermanMono
from testsuite_tune_app.update_easteregg.tc_112_update_bomberman_stereo_easterEggOTA import UpdateBombermanStereo
from testsuite_tune_app.update_easteregg.tc_222_update_zone305_easterEggOTA_dongleQuadrun import \
    UpdateZone305QuadrunDongle

"""
Generic test FWU sanity runner.

To add new device to suite, just import it below.
PATTERN: from testsuite_tune_app.tcXXXXX import DeviceForFWU

Test runner will automatically handle creation and execution of FWU tests

-r, --repeats - number of FWU runs for each device
-d, --dock_devices - (Logi Dock only) decide if run FWU of devices connected to Logi Dock
"""

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--installer", help="installer version")
parser.add_argument("-r", "--repeats", type=int, default=3, help="Number of FWU repeats")
parser.add_argument("-d", "--devices", help="What devices do you want to use.", default="all")
args = parser.parse_args()

# Run Configuration
settings = config.CommonConfig.get_instance()
settings.set_value_in_section('JENKINS_FWU_TESTS', 'JENKINS_FWU_CONFIG', 'True')
if args.repeats is not None:
    settings.set_value_in_section('JENKINS_FWU_TESTS', 'JENKINS_REPEATS', args.repeats)
if args.installer is not None:
    settings.set_value_in_section('RUN_CONFIG', 'INSTALLER', args.installer)
settings.set_value_in_section('RUN_CONFIG', 'PROJECT', 'LogiTune')
settings.set_value_in_section('RUN_CONFIG', 'dashboard_publish', 'True')

MAILING_LIST = (
    'ptokarczyk@logitech.com',
    'plesniak@logitech.com',
    'rdrozd@logitech.com',
    'sveerbhadrappa@logitech.com',
    'bchandrashekar@logitech.com',
)

from base import global_variables
from testsuite_tune_app.test_runner import run_tests
from testsuite_tune_app.verify_device_connection import check_devices

global_variables.test_category = 'FW Update Stress'

from testsuite_tune_app.tc00_install import TuneInstall
from testsuite_tune_app.tc20_uninstall import TuneUninstall

from testsuite_tune_app.update_easteregg.tc_109A_update_brio4k_easterEggOTA import UpdateBrio4K
from testsuite_tune_app.update_easteregg.tc_110A_update_c930e_easterEggOTA import UpdateC930e
from testsuite_tune_app.update_easteregg.tc_106A_update_degas_easterEggOTA import UpdateDegasEasterEggOTA
from testsuite_tune_app.update_easteregg.tc_105A_update_gauguin_easterEggOTA import UpdateGauguin
from testsuite_tune_app.update_easteregg.tc_107B_update_matisse_easterEgg import UpdateMatisseViaEasterEgg
from testsuite_tune_app.update_easteregg.tc_102_update_zone_wired_easterEggOTA import UpdateZoneWired
from testsuite_tune_app.update_easteregg.tc_101_update_zone750_easterEggOTA import UpdateZone750
from testsuite_tune_app.update_easteregg.tc_103_update_zonewiredearbuds_easterEggOTA import UpdateZoneWiredEarbuds
from testsuite_tune_app.update_easteregg.tc_204_update_zonewireless_easterEggOTA_dongleBTC import UpdateZoneWirelessDongle
from testsuite_tune_app.update_easteregg.tc_206_update_zonewirelesspluss_easterEggOTA_dongleSUC import UpdateZoneWirelessPlusDongle
from testsuite_tune_app.update_easteregg.tc_202_update_zone900_easterEggOTA_dongleSUC import UpdateZone900Dongle
from testsuite_tune_app.update_easteregg.tc_210_update_zonevibe125_easterEggOTA_dongleBTC import UpdateZoneVibe125Dongle
from testsuite_tune_app.update_easteregg.tc_219_update_zone950_easterEggOTA_dongleQuadrun import UpdateZone950QuadrunDongle
from testsuite_tune_app.update_easteregg.tc_104_update_logidock_easterEgg import UpdateLogiDock
from testsuite_tune_app.update_easteregg.tc_108A_update_litrabeam_easterEggOTA import UpdateLitraBeam

suites = {
    'zone_950': UpdateZone950QuadrunDongle,
    'brio_4k': UpdateBrio4K,
    'c930e': UpdateC930e,
    'brio_30x': UpdateDegasEasterEggOTA,
    'brio_50x': UpdateGauguin,
    'brio_70x': UpdateMatisseViaEasterEgg,
    'zone_wired': UpdateZoneWired,
    'zone_750': UpdateZone750,
    'zone_wired_earbuds': UpdateZoneWiredEarbuds,
    'zone_wireless': UpdateZoneWirelessDongle,
    'zone_wireless_plus': UpdateZoneWirelessPlusDongle,
    'zone_900': UpdateZone900Dongle,
    'zone_vibe_125': UpdateZoneVibe125Dongle,
    'logi_dock': UpdateLogiDock,
    'litra_beam': UpdateLitraBeam,
    'bomberman_mono': UpdateBombermanMono,
    'bomberman_stereo': UpdateBombermanStereo,
    'zone_305': UpdateZone305QuadrunDongle
}




if __name__ == '__main__':
    devices = ['zone_950', 'brio_4k', 'c930e', 'brio_30x', 'brio_50x', 'brio_70x', 'zone_wired', 'zone_750',
               'zone_wired_earbuds', 'zone_wireless', 'zone_wireless_plus', 'zone_900', 'zone_vibe_125', 'logi_dock',
               'litra_beam', 'bomberman_mono', 'bomberman_stereo', 'zone_305']

    if args.devices != "all":
        devices = [device.strip() for device in args.devices.strip().split(",")]


    tc_to_run = []

    for device in devices:
        tc_to_run.append(suites[device])

    tc_to_run.append(TuneUninstall)

    tune_install = TuneInstall()
    tune_install.setUpClass()
    tune_install.test_001_VC_42593_install_logi_tune()

    check_devices(testcases_to_run=tc_to_run, mailing_list=MAILING_LIST,
                  skip_missing_devices_in_test_suite=True)
    run_tests(tc_to_run, send_mail_project_name='LogiTune', test_category='FW Update Stress')
