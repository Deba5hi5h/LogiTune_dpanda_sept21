import json
import logging
import unittest
import sys
import common.log_helper as log_helper
from apis.raiden_api import raiden_helper, raiden_validation_methods
from base.raiden_base_api import RaidenBaseAPI
from common import framework_params as fp
from common import raiden_config
from extentreport.report import Report

log = logging.getLogger(__name__)


class RaidenAPIBrioDevice(RaidenBaseAPI):
    """
    Test to verify device APIs for Brio.
    """

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPIBrioDevice, cls).setUpClass()
            raiden_backend_version = raiden_helper.get_raiden_backend_version(cls.config)
            log.info(f'Sync Portal API version is {raiden_backend_version}')
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPIBrioDevice, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPIBrioDevice, self).setUp() #Extent Report
        self.token = raiden_helper.signin_method(self.config, self.role)
        self.org_id = raiden_helper.get_org_id(self.role, self.config, self.token)
        log.info('Token {}'.format(self.token))
        log.info('Starting {}'.format(self._testMethodName))

    def tearDown(self):
        super(RaidenAPIBrioDevice, self).tearDown() #Extent Report

    def test_001_VC_79963_Get_Device_Info_Brio(self):
        """Get Device Information in Personal Devices: Brio.
            Setup:
                  1. Sign in to Sync Portal using valid owner credentials.
                  2. Make sure that Brio is connected to the organization.

            Test:
                 1. Query the API: Get Call to
                 GET ~/org/{org-id}/host/Host-{host-id}/info
                 2. Search for accessory Brio and get the device information.

        """
        try:
            self.banner('Get Device Info: Brio')

            get_url = self.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/host/Host-" + \
                             fp.HOST_PC_ID + '/info'

            response = raiden_helper.send_request(
                method='GET', url=get_url, token=self.token
            )
            output = None
            for accessory, object in response['accessories'].items():
                if object['name'] == 'Brio':
                    output = object
                    break

            json_formatted_response = json.dumps(output, indent=2)
            Report.logInfo('Response for GET info of Brio device')
            Report.logResponse(format(json_formatted_response))
            eeprom_version = output['eeprom']
            fw_version = output['fw']
            Report.logInfo('Video Firmware - {}'.format(fw_version))
            Report.logInfo('EEPROM Firmware - {}'.format(eeprom_version))
            status = True if output else False
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPIBrioDevice)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")