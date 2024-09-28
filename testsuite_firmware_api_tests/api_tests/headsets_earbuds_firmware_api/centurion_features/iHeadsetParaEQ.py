from extentreport.report import Report
from testsuite_firmware_api_tests.api_tests.device_api_names import ConnectionType
from testsuite_firmware_api_tests.api_tests.headsets_earbuds_firmware_api.commands_raw import (
    CMD_SET_ANTI_STARTLE,
    CMD_GET_ANTI_STARTLE,
)


class HeadsetParaEQ:
    """
    https://github.com/Logitech/mbg-centpp/blob/master/host/Documentation/Features/0x0504_iHeadsetParaEQ.md
    """

    def __init__(self, centurion):
        self.centurion = centurion
