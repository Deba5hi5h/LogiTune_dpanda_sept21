import logging
import unittest

from base.base_ui import UIBase
from testsuite_jasmine_api.tc_methods_jasmine_meeting_room_booking import SyncPortalJasmineRoomBookingTCMethods
from testsuite_raiden_api.tc_methods_meeting_rooms import SyncPortalTCMethods
from datetime import datetime
from extentreport.report import Report
from common import jasmine_config

log = logging.getLogger(__name__)

class JasmineAgendaAPI(UIBase):
    """
        Test to verify jasmine agenda APIs.
    """
    syncportal_methods = SyncPortalTCMethods()
    syncportal_jasmine_roombooking_methods = SyncPortalJasmineRoomBookingTCMethods()
    device_name = "Nintendo"
    now = datetime.now()
    room_name = now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom"
    data = {}
    role = "OrgAdmin"
    room_name_list = list()
    room_id_list = list()

    def test_1101_VC_139122_Get_Jasmine_Room_Agenda(self):
        '''
                     Test: To get the jasmine app room agenda details
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Choose room resource, M365 Logi QA Room 11
                        3. Login as serviceuser2@logivcqa1.onmicrosoft.com and create meeting with room M365 Logi QA Room 11

                    Test:
                        1) Initiate and complete provisioning of Tap Scheduler to existing room created
                        2) Link above created room to bookable/room resource (M365 Logi QA Room 11)
                        3) Get the Jasmine room agenda
                        4) Unlink the room from resource
                        5) Delete the room
                        6) Delete the certificate generated
                '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(self.role, self.room_name)

        Report.logInfo(
            'STEP 2: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo(
            'STEP 3: Get the room agenda and validate that meeting shows up there for current day')
        self.syncportal_jasmine_roombooking_methods.tc_get_jasmine_room_agenda(self.role, jasmine_cert_path, jasmine_privatekey_path, room_id)

        Report.logInfo(
            'STEP 4: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 5: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 6: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path, jasmine_privatekey_path)

    def test_1102_VC_139122_Book_Room_Adhoc(self):
        '''
                             Test: To perform adhoc booking
                            Setup:
                                1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                1) Initiate and complete provisioning of Tap Scheduler to existing room created
                                2) Choose room resource, M365 Logi QA Room 11 and link room to room resource
                                3) Perform Adhoc booking and validate the response
                                4) Unlink the room from resource
                                5) Delete the room
                                6) Delete the certificate generated
        '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(
            self.role, self.room_name)

        Report.logInfo(
            'STEP 2: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo(
            'STEP 3: Perform adhoc room booking')
        bookingId = self.syncportal_jasmine_roombooking_methods.tc_jasmine_perform_adhoc_room_booking(self.role, jasmine_cert_path, jasmine_privatekey_path,
                                                           room_id)
        Report.logInfo(
            'STEP 4: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 5: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 6: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path,
                                                                                  jasmine_privatekey_path)

    def test_1103_VC_139122_Book_Room_Adhoc_Cancel_Adhoc_Booking(self):
        '''
                             Test: To perform adhoc booking and cancel the booking
                            Setup:
                                1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                1) Initiate and complete provisioning of Tap Scheduler to existing room created
                                2) Choose room resource, M365 Logi QA Room 11 and link room to room resource
                                3) Perform Adhoc booking and validate the response
                                4) Cancel Adhoc booking and validate the response
                                5) Unlink the room from resource
                                6) Delete the room
                                7) Delete the certificate generated
        '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(
            self.role, self.room_name)

        Report.logInfo(
            'STEP 2: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo(
            'STEP 3: Perform adhoc room booking')
        bookingId = self.syncportal_jasmine_roombooking_methods.tc_jasmine_perform_adhoc_room_booking(self.role, jasmine_cert_path, jasmine_privatekey_path,
                                                           room_id)
        Report.logInfo(
            'STEP 5: Cancel adhoc room booking')
        self.syncportal_jasmine_roombooking_methods.tc_jasmine_cancel_adhoc_room_booking(self.role, jasmine_cert_path, jasmine_privatekey_path,
                                                           room_id, bookingId)

        Report.logInfo(
            'STEP 5: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 6: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 7: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path,
                                                                                  jasmine_privatekey_path)

    def test_1104_VC_139122_Book_Room_Adhoc_Update_Adhoc_Booking(self):
        '''
                             Test: To perform adhoc booking and update the booking details
                            Setup:
                                1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                1) Initiate and complete provisioning of Tap Scheduler to existing room created
                                2) Choose room resource, M365 Logi QA Room 11 and link room to room resource
                                3) Perform Adhoc booking and validate the response
                                4) Update Adhoc booking and validate the response
                                5) Unlink the room from resource
                                6) Delete the room
                                7) Delete the certificate generated
        '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(
            self.role, self.room_name)

        Report.logInfo(
            'STEP 2: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo(
            'STEP 3: Perform adhoc room booking')
        booking_id = self.syncportal_jasmine_roombooking_methods.tc_jasmine_perform_adhoc_room_booking(self.role,
                                                                                                 jasmine_cert_path,
                                                                                                 jasmine_privatekey_path,
                                                                                                 room_id)
        Report.logInfo(
            'STEP 5: Update the adhoc room booking')
        self.syncportal_jasmine_roombooking_methods.tc_jasmine_update_adhoc_room_booking(self.role, jasmine_cert_path,
                                                                                         jasmine_privatekey_path,
                                                                                         room_id, booking_id)

        Report.logInfo(
            'STEP 5: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 6: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 7: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path,
                                                                                  jasmine_privatekey_path)

    def test_1106_VC_139122_Get_Booking_Settings(self):
        '''
                     Test: To get booking settings for the room
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.
                        2. Choose room resource, M365 Logi QA Room 11
                        3. Login as serviceuser2@logivcqa1.onmicrosoft.com and create meeting with room M365 Logi QA Room 11

                    Test:
                        1) Initiate and complete provisioning of Tap Scheduler to existing room created
                        2) Link above created room to bookable/room resource (M365 Logi QA Room 11)
                        3) Get the room booking settings
                        4) Unlink the room from resource
                        5) Delete the room
                        6) Delete the certificate generated
                '''

        bookable_id = jasmine_config.bookable_id

        Report.logInfo(
            'STEP 1: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
        room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(self.role, self.room_name)

        Report.logInfo(
            'STEP 2: Link created room to bookable')
        self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo(
            'STEP 3: Get the room agenda and validate that meeting shows up there for current day')
        self.syncportal_jasmine_roombooking_methods.tc_get_room_booking_settings(self.role, jasmine_cert_path, jasmine_privatekey_path, room_id)

        Report.logInfo(
            'STEP 4: UnLink rooms from bookables.')
        self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        Report.logInfo(
            'STEP 5: Delete the room')
        self.syncportal_methods.tc_delete_room(self.role, self.room_name)

        Report.logInfo(
            'STEP 6: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path, jasmine_privatekey_path)

    def test_1105_VC_139122_Get_Room_Agenda_Snapshot(self):
        '''
                            Test: To get room agenda snapshot
                            Setup:
                                1. Sign in to Sync Portal using valid owner credentials.

                            Test:
                                1) Initiate and complete provisioning of Tap Scheduler to rooms created
                                2) Choose room resource, M365 Logi QA Room 7, M365 Logi QA Room 11, M365 Logi QA Room 21 and link all room to room resource
                                3) Get room agenda snapshot and validate the response
                                4) Unlink all the rooms from resource
                                5) Delete all the created rooms
                                6) Delete the certificate generated
        '''

        # List of bookable id
        bookable_id_list = jasmine_config.bookable_id_list

        i = 0

        for bookable_id in bookable_id_list:
            i = i + 1
            room_name = self.now.strftime("%Y%m%d%H%M%S") + " Auto-EmptyRoom" + str(i)
            self.room_name_list.append(room_name)

            Report.logInfo(
                'STEP 1: Initiate and complete room provisioning of Tap Scheduler and get room id, certificate, private key')
            room_id, jasmine_cert_path, jasmine_privatekey_path = self.syncportal_jasmine_roombooking_methods.tc_appliance_provisioning_nintendo_get_certificate_privatekey(
            self.role, room_name)

            self.room_id_list.append(room_id)

            Report.logInfo(
                'STEP 2: Link created room to bookable')
            self.syncportal_methods.tc_link_room_to_bookable(self.role, room_id, bookable_id)

        Report.logInfo(
            'STEP 3: Get room agenda snapshot and validate that meeting shows up there for current day')

        self.syncportal_jasmine_roombooking_methods.tc_get_jasmine_room_agenda_snapshot(self.role, jasmine_cert_path,
                                                                           jasmine_privatekey_path, self.room_id_list)

        for bookable_id in bookable_id_list:
            Report.logInfo(
                'STEP 4: UnLink rooms from bookables.')
            self.syncportal_methods.tc_unlink_rooms_from_bookables(self.role, bookable_id)

        for room_name in self.room_name_list:
            Report.logInfo(
                'STEP 5: Delete the room')
            self.syncportal_methods.tc_delete_room(self.role, room_name)

        Report.logInfo(
            'STEP 6: Delete the certificate created')
        self.syncportal_jasmine_roombooking_methods.tc_delete_jasmine_certificate(jasmine_cert_path,
                                                                                  jasmine_privatekey_path)


    if __name__ == "__main__":
        unittest.main()

