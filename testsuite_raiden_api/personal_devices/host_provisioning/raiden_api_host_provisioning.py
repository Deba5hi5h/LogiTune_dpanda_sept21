import json
import logging
import unittest
import sys
import common.log_helper as log_helper
from apis.raiden_api import raiden_helper, raiden_validation_methods
from base.raiden_base_api import RaidenBaseAPI
from extentreport.report import Report
import random
import math


log = logging.getLogger(__name__)
host_id = ""


class RaidenAPI_Host_Provisioning_Personal_Devices(RaidenBaseAPI):
    """
    Test to verify device APIs for Meetup.
    """

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPI_Host_Provisioning_Personal_Devices, cls).setUpClass()
            raiden_backend_version = raiden_helper.get_raiden_backend_version(cls.config)
            log.info('Sync Portal API version is {}'.format(raiden_backend_version))
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPI_Host_Provisioning_Personal_Devices, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPI_Host_Provisioning_Personal_Devices, self).setUp() #Extent Report
        self.token = raiden_helper.signin_method(self.config, self.role)
        self.org_id = raiden_helper.get_org_id(self.role, self.config, self.token)
        log.info('Token {}'.format(self.token))
        log.info('Starting {}'.format(self._testMethodName))

    def tearDown(self):
        super(RaidenAPI_Host_Provisioning_Personal_Devices, self).tearDown() #Extent Report

    def test_001_VC_53867_Host_Computer_Provisioning(self):
        """Host Computer Provisioning- Personal Devices.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                 1. Initiate Host Provisioning: POST CALL to {{PROTOCOL}}://{{API_SERVER}}/api/org/{{ORG_ID}}/host/prov
                 2. Complete Host Provisioning: POST call to {{PROTOCOL}}://{{API_SERVER}}/api/host/prov/{{PROVISION_ID}}/complete

        """
        try:
            self.banner('Host Computer Provisioning- Personal Devices.')
            base_url = self.config.BASE_URL

            # Step-1: Initiate Host Provisioning

            initiate_host_provisioning_url = base_url + "/api/org/" + self.org_id + "/host/prov"
            data_initiate_prov = json.dumps(
                {
                  "ttl": "3600",
                  "max": "10"
                })

            response = raiden_helper.send_request(
                method='POST', url=initiate_host_provisioning_url, body= data_initiate_prov, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Response for Initiate Host Provisioning')
            Report.logResponse(format(json_formatted_response))
            self.provision_response = response['completion']
            self.provision_id = self.provision_response['provId']

            status_initiate_host_provisioning = raiden_validation_methods.validate_initiate_host_provisioning(response)

            # Step 2: Complete Host Provisioning.
            complete_host_provisioning_url = base_url + "/api/host/prov/" + self.provision_id + "/complete"
            data_complete_prov = json.dumps(
                {
                    "completion":
                        self.provision_response
                    ,
                    "host":
                        {
                            "hostName": "VC-Room" + str(math.floor(random.random()*1000)),
                            "machineId": "0e6812f7-f5c2-42e5-bb4e-4f74e18f7545",
                            "sw": "1.2.3",
                            "model": "Microsoft Corporation Surface",
                            "os": "Microsoft Windows 10 Enterprise",
                            "osv": "10.0.17763",
                            "proc": "Intel(R) Core(TM) i5-7360U CPU @ 2.30GHz",
                            "ram": 16,
                            "tzOffset": 3600000,
                            "tzName": "USA",
                            "ts": 1614292924012,
                            "channel": "default",
                            "serial": "112316609LP001",
                            "clients": [{"type": "Tune", "sw": "1.0.0", "channel": "default"}]
                        }
                })

            response = raiden_helper.send_request(
                method='POST', url=complete_host_provisioning_url, body=data_complete_prov, token=self.token
            )
            global host_id
            host_id = response['hostId']
            json_formatted_response = json.dumps(response, indent=2)
            Report.logInfo(f'Response for Complete Host Provisioning')
            Report.logResponse(format(json_formatted_response))

            status_complete_host_provisioning = raiden_validation_methods.validate_complete_host_provisioning(response)

            status = status_initiate_host_provisioning & status_complete_host_provisioning
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e

    def test_002_VC_53868_Get_Host_Info(self):
        """Get Host Info.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                 Get Host Info: POST call to  {{PROTOCOL}}://{{API_SERVER}}/api/org/{{ORG_ID}}/host/{{HOST_ID}}/info

        """
        try:
            self.banner('Get Host Info.')
            base_url = self.config.BASE_URL

            # Get Host Info.
            get_host_info_url = base_url + "/api/org/" + self.org_id + "/host/" + host_id + "/info"

            response = raiden_helper.send_request(
                method='GET', url=get_host_info_url, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info('Response for Get Host Info- {}'.format(json_formatted_response))

            status = raiden_validation_methods.validate_get_host_info(response)
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e

    def test_003_VC_53869_Update_Host_Info(self):
        """Update Host Info.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                 Update Host Info: PUT call to {{PROTOCOL}}://{{API_SERVER}}/api/org/{{ORG_ID}}/host/{{HOST_ID}}

        """
        try:
            self.banner('Update Host Info providing name of the host as Lenovo Thinkpad')
            base_url = self.config.BASE_URL

            # Update Host Info.
            update_host_info_url = base_url + "/api/org/" + self.org_id + "/host/" + host_id

            payload = json.dumps({"name": "Lenovo Thinkpad"})

            response = raiden_helper.send_request(
                method='PUT', url=update_host_info_url, body=payload, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info('Response for Update Host Info- {}'.format(json_formatted_response))

            status_update_host_info = raiden_validation_methods.validate_empty_response(response)

            get_host_info_url = base_url + "/api/org/" + self.org_id + "/host/" + host_id + "/info"

            response = raiden_helper.send_request(
                method='GET', url=get_host_info_url, token=self.token
            )

            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info('Response for Get Host Info- {}'.format(json_formatted_response))

            status_get_host_info = raiden_validation_methods.validate_get_host_info(response)

            status = status_update_host_info & status_get_host_info

            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e

    def test_004_VC_53870_Move_Host_To_Group(self):
        """Move Host to group.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                 Move Host to group: POST call to {{PROTOCOL}}://{{API_SERVER}}/api/org/{{ORG_ID}}/host/group

        """
        try:
            self.banner('Move host to group.')
            base_url = self.config.BASE_URL

            # Move host to All groups.
            move_host_to_group_url = base_url + "/api/org/" + self.org_id + "/host/group"

            payload = json.dumps({"hostIds": [host_id], "target": "/CA"})

            response = raiden_helper.send_request(
                method='POST', url=move_host_to_group_url, body=payload, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            log.info('Response for Move Host to Group- {}'.format(json_formatted_response))

            status = raiden_validation_methods.validate_empty_response(response)
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e

    def test_005_VC_53871_Delete_Host_Computer(self):
        """Delete Hosts.
            Setup:
                  Sign in to Sync Portal using valid owner credentials.

            Test:
                 Delete Host Computer: POST call to {{PROTOCOL}}://{{API_SERVER}}/api/org/{{ORG_ID}}/host/delete

        """
        try:
            self.banner('Delete host computer- Personal Devices.')
            base_url = self.config.BASE_URL

            # Delete host computer from Personal Devices
            delete_host = base_url + "/api/org/" + self.org_id + "/host/delete"

            payload = json.dumps({"hostIds": [host_id]})

            response = raiden_helper.send_request(
                method='POST', url=delete_host, body=payload, token=self.token
            )
            json_formatted_response = json.dumps(response, indent=2)
            Report.logResponse(format(json_formatted_response))
            Report.logInfo(f'Delete host computer- {json_formatted_response}')

            status = raiden_validation_methods.validate_empty_response(response)
            assert status is True, 'Error in status'

        except AssertionError as e:
            log_helper.test_result_logger(self.id(), False, e)
            raise e


if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RaidenAPI_Host_Provisioning_Personal_Devices)

    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result is None or result.failures or result.errors or result.unexpectedSuccesses:
        sys.exit("Test failures detected.")