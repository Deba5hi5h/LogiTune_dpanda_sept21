import logging
import unittest

from base.base_ui import UIBase
from testsuite_jasmine_api.tc_methods_jasmine_meeting_room_booking import SyncPortalJasmineRoomBookingTCMethods
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from testsuite_raiden_api.tc_methods_hot_desks import SyncPortalTCMethodsHotDesks
from datetime import datetime
from common import jasmine_config
from extentreport.report import Report

log = logging.getLogger(__name__)

class JasmineMapsApi(UIBase):
    """
        Test to verify jasmine maps APIs for Tap.
    """
    syncportal_methods = SyncPortalTCMethods()
    syncportal_jasmine_roombooking_methods = SyncPortalJasmineRoomBookingTCMethods()
    syncportal_hotdesks_methods = SyncPortalTCMethodsHotDesks()
    device_name = "Nintendo"
    flexdesk_device_name = "Coily"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    map_name = now.strftime("%Y%m%d%H%M%S") + '_map_for_testing'
    desk_name = now.strftime("%Y%m%d%H%M%S") + " Auto-Desk"
    data = {}
    role = "OrgAdmin"
    timezone = 'Asia/Calcutta'

    def test_1201_vc_145304_get_jasmine_maps_list(self):
        '''
                     Test: To Get list of maps visible to the room
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Choose room resource, M365 Logi QA Room 11
                        3. Login as serviceuser2@logivcqa1.onmicrosoft.com and create meeting with room M365 Logi QA Room 11

                    Test:
                        1.Add room to group
                        2.Initiate and complete provisioning of Tap Scheduler to existing room created
                        3.Link to bookable resource
                        4.Add map
                        5.Assign map to group location
                        6.Publish the map
                        7.Add room to the map
                        8.Get the map list
                        9.Unlink room
                        10.Delete map
                        11.Delete room
                        12.Delete desk
                        13.Delete certificate
                        14.Delete Site

                '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Add room to group')
        site_name = self.syncportal_methods.tc_add_room_to_group(
            role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 2: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(self.role, self.room_name)

        Report.logInfo(
            'STEP 3: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo('STEP 4: Add map to organization')
        result_list = self.syncportal_hotdesks_methods.tc_add_maps_to_organization(
            role=self.role, map_name=self.map_name)

        map_id = result_list[0]
        location_path = result_list[1]
        token = result_list[2]
        org_id = result_list[3]
        site = result_list[4]
        site_location_id = result_list[5]
        building_location_id = result_list[6]
        floor_location_id = result_list[7]
        building = result_list[8]
        floor = result_list[9]
        org_identifier = result_list[10]

        Report.logInfo('STEP 5: Assign map to Site, building and Floor')
        self.syncportal_hotdesks_methods.tc_link_map_to_site_building_floor(token, org_id, map_id, site,
                                                                            site_location_id, building,
                                                                            building_location_id, floor,
                                                                            floor_location_id)

        Report.logInfo('STEP 6: Publish map - change the map status from hidden to visible')
        published_at_time = self.syncportal_hotdesks_methods.tc_change_map_status_hidden_to_visible(token, org_id, map_id)

        Report.logInfo('STEP 7: Assign room to map created')
        self.syncportal_hotdesks_methods.tc_assign_room_to_map(token, org_id, self.map_name, map_id, org_identifier, site, site_location_id, building_location_id,
                                         floor_location_id, self.room_name, room_id, published_at_time, location_path)

        Report.logInfo(
            'STEP 8: Get the room agenda and validate that meeting shows up there for current day')
        self.syncportal_jasmine_roombooking_methods.tc_get_jasmine_maps_list(self.role, jasmine_cert_path, jasmine_privatekey_path, room_id, map_id)

        Report.logInfo(
            'STEP 9: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 10: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 11 : Delete map.')
        self.syncportal_hotdesks_methods.tc_delete_map(token, org_id, map_id)

        Report.logInfo(
            'STEP 12: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path, jasmine_privatekey_path)

        Report.logInfo(
            'STEP 13 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)


    def test_1202_vc_145304_get_jasmine_map_content_by_id(self):
        '''
                     Test: To get the jasmine map content by map id
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Choose room resource, M365 Logi QA Room 11
                        3. Login as serviceuser2@logivcqa1.onmicrosoft.com and create meeting with room M365 Logi QA Room 11

                    Test:
                        1.Add room to group
                        2.Initiate and complete provisioning of Tap Scheduler to existing room created
                        3.Link to bookable resource
                        4.Add map
                        5.Assign map to group location
                        6.Publish the map
                        7.Add room to the map
                        8.Get the map list
                        9.Unlink room
                        10.Delete map
                        11.Delete room
                        12.Delete certificate
                        13.Delete Site

                '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Add room to group')
        site_name = self.syncportal_methods.tc_add_room_to_group(
            role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 2: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(self.role, self.room_name)

        Report.logInfo(
            'STEP 3: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo('STEP 4: Add map to organization')
        result_list = self.syncportal_hotdesks_methods.tc_add_maps_to_organization(
            role=self.role, map_name=self.map_name)

        map_id = result_list[0]
        location_path = result_list[1]
        token = result_list[2]
        org_id = result_list[3]
        site = result_list[4]
        site_location_id = result_list[5]
        building_location_id = result_list[6]
        floor_location_id = result_list[7]
        building = result_list[8]
        floor = result_list[9]
        org_identifier = result_list[10]

        Report.logInfo('STEP 5: Assign map to Site, building and Floor')
        self.syncportal_hotdesks_methods.tc_link_map_to_site_building_floor(token, org_id, map_id, site,
                                                                            site_location_id, building,
                                                                            building_location_id, floor,
                                                                            floor_location_id)

        Report.logInfo('STEP 6: Publish map - change the map status from hidden to visible')
        published_at_time = self.syncportal_hotdesks_methods.tc_change_map_status_hidden_to_visible(token, org_id, map_id)

        Report.logInfo('STEP 7: Assign room to map created')
        self.syncportal_hotdesks_methods.tc_assign_room_to_map(token, org_id, self.map_name, map_id, org_identifier, site, site_location_id, building_location_id,
                                         floor_location_id, self.room_name, room_id, published_at_time, location_path)

        Report.logInfo(
            'STEP 8: Get the room agenda and validate that meeting shows up there for current day')
        self.syncportal_jasmine_roombooking_methods.tc_get_map_content_by_id(self.role, jasmine_cert_path, jasmine_privatekey_path, room_id, map_id)

        Report.logInfo(
            'STEP 9: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 10: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 11 : Delete map.')
        self.syncportal_hotdesks_methods.tc_delete_map(token, org_id, map_id)

        Report.logInfo(
            'STEP 12: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path, jasmine_privatekey_path)

        Report.logInfo(
            'STEP 13 : Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)


    def test_1203_vc_145304_get_jasmine_map_desk_status_by_floorid(self):
        '''
                     Test: Fetch booking status of desks by floorId for hydrating map in Jasmine App
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Choose room resource, M365 Logi QA Room 21
                        3. Login as serviceuser2@logivcqa1.onmicrosoft.com and create meeting with room M365 Logi QA Room 21

                    Test:
                        1.Add the end users to the organization
                        2.Book a session for a desk
                        3.Add room to group
                        4.Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key
                        5.Link created room to bookable
                        6.Add map to organization
                        7.Assign map to Site, building and Floor
                        8.Publish map - change the map status from hidden to visible
                        9.Assign room to map created
                        10.Assign desk to map created
                        11.Get booking status of desks by floorId
                        12.UnLink rooms from bookables
                        13.Delete map
                        14.Delete room
                        15.Delete desk
                        16.Delete certificate
                        17.Delete Site

        '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Add the end users to the organization.')
        user_id, email = self.syncportal_methods.tc_add_end_user(role=self.role)

        Report.logInfo('STEP 2: Book a session for desk')
        site, building, floor, self.desk_id, site_location_id, building_location_id, floor_location_id, area_location_id, reservation_id = self.syncportal_jasmine_roombooking_methods.tc_flex_desk_session_booking_jasmine(
            role=self.role, desk_name=self.desk_name, user_id=user_id, email_id=email,
            desk_device_name=self.flexdesk_device_name, building_timezone=self.timezone)

        Report.logInfo(
            'STEP 3: Add room to group')
        site_name = self.syncportal_methods.tc_add_room_to_group(
            role=self.role, room_name=self.room_name)

        Report.logInfo(
            'STEP 4: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(
            self.role, self.room_name)

        Report.logInfo(
            'STEP 5: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo('STEP 6: Add map to organization')
        result_list = self.syncportal_jasmine_roombooking_methods.tc_add_map_to_organization(
            role=self.role, map_name=self.map_name)

        map_id = result_list[0]
        location_path = result_list[1]
        token = result_list[2]
        org_id = result_list[3]
        org_identifier = result_list[4]

        Report.logInfo('STEP 7: Assign map to Site, building and Floor')
        self.syncportal_hotdesks_methods.tc_link_map_to_site_building_floor(token, org_id, map_id, site,
                                                                            site_location_id, building,
                                                                            building_location_id, floor,
                                                                            floor_location_id)

        Report.logInfo('STEP 8: Publish map - change the map status from hidden to visible')
        published_at_time = self.syncportal_hotdesks_methods.tc_change_map_status_hidden_to_visible(token, org_id,
                                                                                                    map_id)

        Report.logInfo('STEP 9: Assign room to map created')
        self.syncportal_hotdesks_methods.tc_assign_room_to_map(token, org_id, self.map_name, map_id, org_identifier,
                                                               site, site_location_id, building_location_id,
                                                               floor_location_id, self.room_name, room_id,
                                                               published_at_time, location_path)

        Report.logInfo('STEP 10: Assign desk to map created')
        self.syncportal_hotdesks_methods.tc_assign_desk_to_map(token, org_id, self.map_name, map_id,
                                                               org_identifier,
                                                               site_location_id, building_location_id,
                                                               floor_location_id, self.desk_name, self.desk_id,
                                                               published_at_time, location_path, area_location_id)

        Report.logInfo(
            'STEP 11: Get booking status of desks by floorId')
        self.syncportal_jasmine_roombooking_methods.tc_get_booking_status_of_desk_by_floorid(self.role,
                                                                                             jasmine_cert_path,
                                                                                             jasmine_privatekey_path,
                                                                                             self.desk_id,
                                                                                             floor_location_id)

        Report.logInfo(
            'STEP 12: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 13: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 14: Delete the desk')
        self.syncportal_hotdesks_methods.tc_delete_desk(role=self.role, desk_id=self.desk_id)

        Report.logInfo(
            'STEP 15: Delete map.')
        self.syncportal_hotdesks_methods.tc_delete_map(token, org_id, map_id)

        Report.logInfo(
            'STEP 16: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path,
                                                                                  jasmine_privatekey_path)

        Report.logInfo(
            'STEP 17: Delete the site.')
        self.syncportal_hotdesks_methods.tc_delete_site(self.role, site)


    if __name__ == "__main__":
        unittest.main()