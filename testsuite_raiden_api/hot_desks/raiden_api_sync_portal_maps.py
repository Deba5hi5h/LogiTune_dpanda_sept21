from datetime import datetime
import logging
import unittest

from base.base_ui import UIBase
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from extentreport.report import Report


log = logging.getLogger(__name__)

class RaidenAPISyncPortalMaps(UIBase):
    '''
        API: Sync Portal- Maps

        Tests:
            1. Add map in an organization
            2.Get map(s) in organization
            3.Get map(s) under unassigned section
            4.Link the map to Site, building and Floor
            5.Get the map associated with the building
            6.Rename map
            7.Re-assign map to another floor
            8.Change the map status from hidden to visible
            9.Delete map
            10.Delete site

    '''

    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    syncportal_methods = SyncPortalTCMethods()

    @classmethod
    def setup(cls):
        try:
            super(RaidenAPISyncPortalMaps, cls).setUp()

        except Exception as e:
            Report.logException(f'Unable to raise the test-suite')
            raise e

    @classmethod
    def tearDownClass(cls):
        super(RaidenAPISyncPortalMaps, cls).tearDownClass()

    def setUp(self):
        super(RaidenAPISyncPortalMaps, self).setUp()

    def tearDown(self):
        super(RaidenAPISyncPortalMaps, self).tearDown()

    def test_1401_VC_123272_organization_maps_scenarios(self):

        role = 'OrgAdmin'
        now = datetime.now()
        map_name = now.strftime("%Y%m%d%H%M%S") + '_map_for_testing'

        Report.logInfo('STEP 1: Add map to organization')
        result_list = self.syncportal_hotdesks_methods.tc_add_maps_to_organization(
            role=role, map_name=map_name)

        map_id = result_list[0]
        floor_path = result_list[1]
        token = result_list[2]
        org_id = result_list[3]
        site = result_list[4]
        site_location_id = result_list[5]
        building_location_id = result_list[6]
        floor_location_id = result_list[7]
        building = result_list[8]
        floor = result_list[9]

        Report.logInfo('STEP 2: Get map(s) in organization')
        self.syncportal_hotdesks_methods.tc_get_maps_in_organization(token, org_id, map_id)

        Report.logInfo('STEP 3: Get map(s) under unassigned section')
        self.syncportal_hotdesks_methods.tc_get_maps_under_unassigned_section(token, org_id)

        Report.logInfo('STEP 4: Link the map to Site, building and Floor')
        self.syncportal_hotdesks_methods.tc_link_map_to_site_building_floor(token, org_id, map_id, site, site_location_id, building, building_location_id, floor, floor_location_id)

        Report.logInfo('STEP 5: Get the map associated with the building')
        self.syncportal_hotdesks_methods.tc_get_maps_associated_with_building(token, org_id, map_id, building_location_id)

        Report.logInfo('STEP 6: Rename Map')
        self.syncportal_hotdesks_methods.tc_rename_map(token, org_id, map_id, map_name)

        Report.logInfo('STEP 7: Re-assign map to another floor')
        self.syncportal_hotdesks_methods.tc_reassign_map_to_another_floor(token, org_id, map_id, site,
                                                                          site_location_id, building_location_id, floor_location_id)
        Report.logInfo('STEP 8: Change the map status from hidden to visible')
        self.syncportal_hotdesks_methods.tc_change_map_status_hidden_to_visible(token, org_id, map_id)

        Report.logInfo(
            'STEP 9 : Delete map.')
        self.syncportal_hotdesks_methods.tc_delete_map(token, org_id, map_id)

        Report.logInfo(
            'STEP 10 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)

if __name__ == "__main__":
    unittest.main()

