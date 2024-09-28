import logging
from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RaidenAPICloudAPI(UIBase):
    """
        Test to verify cloud api.
    """
    syncportal_methods = SyncPortalTCMethods()
    data = {}
    role = "OrgAdmin"

    @classmethod
    def setUpClass(cls):
        try:
            super(RaidenAPICloudAPI, cls).setUpClass()
            cls.role = 'OrgAdmin'

        except Exception as e:
            log.error('Unable to setup the logisync test suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPICloudAPI, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPICloudAPI, self).setUp()

    def tearDown(self):
        super(RaidenAPICloudAPI, self).tearDown()

    def test_0001_VC_142579_Get_Org_Details_For_Premium_Licensed_Users(self):
        '''
            Test: To get organization details for customers with select, sync plus and essential licenses
            Pre-Setup:
                1. Sign in to Sync Portal using valid owner credentials.
                2. Generate client certificate
                3. Save certificate in project directory

            Test:
                1) Get cloud api response using above client certificate for small premium licensed orgs, when limit is set to smaller values and without continuation string
                2) Get cloud api response with continuation string
                3) Delete the certificate
        '''

        Report.logInfo('STEP 1: To get all room, desk, devices details for organization with select, sync plus and essential licenses without continuation string')
        response_cloud_api, client_certificate_id = self.syncportal_methods.tc_get_org_details_without_continuation_with_limit_parameter(self.role)

        Report.logInfo('STEP 2: To get all room, desk, devices details for organization with select, sync plus and essential licenses with continuation')
        response_cloud_api_with_continuation = self.syncportal_methods.tc_get_org_details_with_continuation_parameter(self.role, response_cloud_api)

        Report.logInfo('STEP 3: Delete the client certificate')
        self.syncportal_methods.tc_delete_client_certificate(self.role, client_certificate_id)

    def test_0002_VC_142579_Cloud_API_Testing_For_Forbideen_Status(self):
        '''
             Test:  To test cloud api with org having de-activated client certificate

              Pre-Setup:
                 1. Sign in to Sync Portal using valid owner credentials.
                 2. Generate client certificate for Org with Select license
                 3. Save certificate in project directory
                 4. De-activate the above client certificate
                 5. Make GET /org/{orgId}/place request with deactivated certificate
                 6. Validate the response
                 7. Delete the client certificate

            Test:
                1) Make GET /org/{orgId}/place request with deactivated certificate and validate for status code = 403

        '''

        Report.logInfo('STEP 1: To test cloud api for org with deactivated client certificate')
        client_certificate_id, response_cloud_api = self.syncportal_methods.tc_test_cloud_api_with_deactivated_certificate(self.role)

        Report.logInfo('STEP 2: Delete the client certificate')
        self.syncportal_methods.tc_delete_client_certificate(self.role, client_certificate_id)

    def test_0003_VC_142579_Cloud_API_Testing_For_Too_Many_Requests(self):
        '''
             Test:  To test cloud api by making more than 10 GET /org/{orgId}/place requests in a minute
            Setup:
                 1. Sign in to Sync Portal using valid owner credentials.
                 2. Generate client certificate for Org with Select license
                 3. Save certificate in project directory

            Test:
                1) Validate cloud api by making more than 10 GET /org/{orgId}/place requests in a minute
                2) Delete the certificate

        '''

        Report.logInfo('STEP 1: Validate cloud api by making more than 10 requests in a minute')
        client_certificate_id, response_status_code = self.syncportal_methods.tc_cloud_api_send_too_many_requests(self.role)

        Report.logInfo('STEP 2: Delete the client certificate')
        self.syncportal_methods.tc_delete_client_certificate(self.role, client_certificate_id)
