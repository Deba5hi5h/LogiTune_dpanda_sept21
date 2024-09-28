import logging
import unittest

from base.base_ui import UIBase
from testsuite_jasmine_api.tc_methods_jasmine_meeting_room_booking import SyncPortalJasmineRoomBookingTCMethods
from extentreport.report import Report

log = logging.getLogger(__name__)

class RoomBookingImageAPI(UIBase):
    """
        Test to verify room booking image APIs.
    """
    syncportal_jasmine_roombooking_methods = SyncPortalJasmineRoomBookingTCMethods()
    role = "OrgAdmin"

    def test_1501_vc_148972_room_booking_image_apis(self):
        '''
                     Test: Jasmine room booking image apis
                    Setup:
                        1. Sign in to Sync Portal using valid owner credentials.

                    Steps:
                        1. Upload room booking image
                        2. Get room booking image details
                        3. Delete uploaded room booking image
                        4. Get room booking images

                '''

        Report.logInfo(
            'STEP 1: Upload room booking image')
        image_id = self.syncportal_jasmine_roombooking_methods.tc_upload_room_booking_image(self.role)

        Report.logInfo(
            'STEP 2: Get room booking image details')
        self.syncportal_jasmine_roombooking_methods.tc_get_room_booking_image_details(self.role, image_id)

        Report.logInfo(
            'STEP 3: Delete uploaded room booking image')
        self.syncportal_jasmine_roombooking_methods.tc_delete_room_booking_uploaded_image(self.role, image_id)

        Report.logInfo(
            'STEP 4: Get room booking images')
        self.syncportal_jasmine_roombooking_methods.tc_get_room_booking_images(self.role)

    if __name__ == "__main__":
        unittest.main()

