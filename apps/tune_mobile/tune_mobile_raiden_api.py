import json
import logging
import unittest
import sys

from apis.raiden_api import raiden_helper, raiden_api_user_helper
from apis.raiden_api.raiden_api_hot_desks_helper import SyncPortalHotDesksMethods
from base import global_variables
from base.base_mobile import MobileBase
from common import raiden_config
from extentreport.report import Report

log = logging.getLogger(__name__)


class TuneMobileRaidenApi(MobileBase):
    """
     Methods to access Raiden API End Users.
     """
    # syncportal_methods = SyncPortalTCMethods()
    # users_email = ""
    # users_userid = ""
    role = 'AladdinOwner'
    sync_portal_hot_desks = SyncPortalHotDesksMethods()

    def add_end_user(self, user_email: str):
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            adduser_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate'
            user_id, email = raiden_api_user_helper.add_enduser(role=self.role,
                                                                adduser_url=adduser_url,
                                                                token=self.token,
                                                                emails=[user_email])
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def delete_end_user(self, user_email: str):
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            get_users_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate'

            delete_user_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(self.org_id) + "/associate"
            user_id = raiden_api_user_helper.get_end_user_id_from_email(user_email,
                                                                        get_users_url,
                                                                        self.token)
            response_delete_user = raiden_api_user_helper.delete_enduser_role(user_id, delete_user_url, self.token)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def get_end_user_group(self, user_email: str) -> list:
        sync_env = global_variables.SYNC_ENV
        user_groups = []
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            user_groups = raiden_api_user_helper.get_groups_associated_with_end_user(global_variables.config, self.role,
                                                                                     self.org_id, self.token, user_email)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env
        return user_groups

    def update_end_user_group(self, user_email: str, group_name: str):
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)

            end_users_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate"

            user_id = raiden_api_user_helper.get_end_user_id_from_email(user_email,
                                                                        end_users_url,
                                                                        self.token)
            current_user_group = str(self.get_end_user_group(user_email=user_email))
            cohort_id = raiden_api_user_helper.get_end_user_group_id_by_group_name(global_variables.config, self.org_id,
                                                                                   self.token, group_name)

            status_update_endusergrp = raiden_api_user_helper.update_withnewgroupname_for_enduser(current_user_group,
                                                                                                  cohort_id,
                                                                                                  end_users_url,
                                                                                                  user_id, self.token)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def get_all_end_user_names(self) -> list:
        sync_env = global_variables.SYNC_ENV
        end_users = []
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            get_users_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate'

            end_users = raiden_api_user_helper.get_all_end_user_names(get_users_url=get_users_url, token=self.token)
            global_variables.SYNC_ENV = sync_env
        except Exception as e:
            Report.logException(str(e))
        return end_users

    def create_booking(self, email_id: str, site: str, building: str, floor: str, area: str, desk_name: str,
                       start: str, end: str, day=0) -> str:
        """
        Method to book a session for an existing desk

        :param email_id:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :param day: 0 for current date, 1 for next day and so on
        """
        sync_env = global_variables.SYNC_ENV
        reservation_id = ""
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)

            reservation_id = self.sync_portal_hot_desks.session_booking_for_existing_desk(self.token, self.org_id,
                                                                                          email_id, site, building,
                                                                                          floor, area, desk_name,
                                                                                          start, end, day)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env
        return reservation_id

    def delete_booking(self, site: str, building: str, floor: str, area: str, desk_name: str, reservation_id: str):
        """
        Method to book a session for an existing desk

        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param reservation_id:
        """
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)

            desk_id = self.sync_portal_hot_desks.get_desk_id_by_desk_name_in_organization(self.token, self.org_id, site,
                                                                                          building, floor, area, desk_name)
            self.sync_portal_hot_desks.flex_desk_delete_reserved_desk(self.token, self.org_id, desk_id, reservation_id)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def update_booking(self, site: str, building: str, floor: str, area: str, desk_name: str,
                       reservation_id: str, start: str, end: str, day=0):
        """
        Method to update session for an existing desk

        :param email_id:email id of user for whom the desk will be booked
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :param start: Start time of booking - Examples "9:00 AM", "3:30 PM" Local time
        :param end: End time of booking - Examples "10:00 AM", "4:30 PM" Local time
        :param day: 0 for current date, 1 for next day and so on
        """
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)

            desk_id = self.sync_portal_hot_desks.get_desk_id_by_desk_name_in_organization(self.token, self.org_id, site,
                                                                    building, floor, area, desk_name)
            self.sync_portal_hot_desks.update_booking_session(token=self.token, org_id=self.org_id, desk_id=desk_id,
                                                              reservation_id=reservation_id, start=start, end=end, day=day)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def get_user_name_by_email(self, email: str) -> str:
        """
        Method to book a session for an existing desk

        :param email: email id
        :return user name:
        """
        sync_env = global_variables.SYNC_ENV
        user_name = ""
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            get_users_url = f'{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate'
            user_name = raiden_api_user_helper.get_end_user_name_from_email(email, get_users_url, self.token)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env
        return user_name

    def delete_bookings_for_user(self, email: str):
        """
        Method to delete all active booking sessions for user

        :param email: email id
        :return user name:
        """
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            self.sync_portal_hot_desks.delete_all_sessions_for_user(token=self.token, org_id=self.org_id, email_id=email)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def delete_bookings_for_desk(self, site: str, building: str, floor: str, area: str, desk_name: str):
        """
        Method to delete all active booking sessions for user

        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :return:
        """
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            token = raiden_helper.signin_method(global_variables.config, "AladdinOwner")
            org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, token)
            sync_portal_hot_desks = SyncPortalHotDesksMethods()
            sync_portal_hot_desks.delete_all_bookings_for_desk(token, org_id, site, building, floor, area, desk_name)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env

    def get_active_user_groups(self) -> list:
        """
        Method to Get active End User groups - User group associated with at least one user

        :param :
        :return list: List of end user groups
        """
        sync_env = global_variables.SYNC_ENV
        end_user_groups = []
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            end_user_groups = raiden_api_user_helper.get_active_end_user_groups(self.org_id, self.token)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env
        return end_user_groups

    def update_desk_policy_settings(self, group_path: str,
                                    reserve_remotely: bool = True,
                                    max_days_in_advance: int = 30,
                                    check_in_time_limit: int = 600,
                                    walk_in_session_duration: int = 1,
                                    walk_in_notify_duration: int = 300,
                                    session_time_limit: int = None,
                                    hardstop_from_reusing: int = None,
                                    reserved_spot_visible: bool = True,
                                    show_qr_code: bool = True):
        """
        Method to update desk policy settings and validate correct values are set

        :param show_qr_code: bool
        :param reserved_spot_visible: bool
        :param hardstop_from_reusing: Time in Seconds. If passed None, Auto extend session will be turned ON
        :param session_time_limit: Time in Hours. If passed None, Session time limit will be turned off
        :param walk_in_notify_duration: Time in seconds
        :param walk_in_session_durtion: Time in Hours. If passed None, walk-in will be turned off
        :param check_in_time_limit: Time in Seconds. If passed None, Check-in required will be turned off
        :param max_days_in_advance: days 1 to 30
        :param reserve_remotely: bool
        :param group_path: Path of area, floor, building or site e.g. /site/building/floor/area or /site/building
        :return bool:
        """
        sync_env = global_variables.SYNC_ENV
        code = ""
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            token = raiden_helper.signin_method(global_variables.config, self.role)
            org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, token)
            code = self.sync_portal_hot_desks.update_desk_policy_settings(token=token, org_id=org_id,
                                                                          group_path=group_path,
                                                                          reserve_remotely=reserve_remotely,
                                                                          max_days_in_advance=max_days_in_advance,
                                                                          check_in_time_limit=check_in_time_limit,
                                                                          walk_in_session_duration=walk_in_session_duration,
                                                                          walk_in_notify_duration=walk_in_notify_duration,
                                                                          session_time_limit=session_time_limit,
                                                                          hardstop_from_reusing=hardstop_from_reusing,
                                                                          reserved_spot_visible=reserved_spot_visible,
                                                                          show_qr_code=show_qr_code)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env
        return code

    def get_ip_address_of_coily(self, site, building, floor, area, desk_name) -> str:
        """
        Method to get IP Address of Coily device associated with desk_name

        :param token:Sign in token
        :param org_id:
        :param site: Site of desk
        :param building: Building of desk
        :param floor: Floor of desk
        :param area: Area of desk
        :param desk_name: Name of desk
        :return ip_address:
        """
        sync_env = global_variables.SYNC_ENV
        ip_address = ""
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            ip_address = self.sync_portal_hot_desks.get_ip_address_of_coily_device(self.token, self.org_id, site,
                                                                                   building, floor, area, desk_name)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env
        return ip_address

    def get_room_agenda(self, room_name):
        """
        Method to get the current day’s agenda for a room.

        :param token:Sign in token
        :param org_id:
        :param room_name:
        :return ip_address:
        """
        sync_env = global_variables.SYNC_ENV
        try:
            global_variables.SYNC_ENV = 'raiden-prod-aladdin'
            self.token = raiden_helper.signin_method(global_variables.config, self.role)
            self.org_id = raiden_helper.parse_org_id_from_user_role(self.role, global_variables.config, self.token)
            #Below code is not complete - Placeholder
            # self.sync_portal_tap_scheduler.get_room_agenda(token=self.token, org_id=self.org_id, room_name=room_name)
        except Exception as e:
            Report.logException(str(e))
        global_variables.SYNC_ENV = sync_env


    def test_add_end_user_in_sync_portal(self):

        role = 'AladdinOwner'
        global_variables.SYNC_ENV = 'raiden-prod-aladdin'
        Report.logInfo(f'Adding end user: logging in as: {role}')
        self.token = raiden_helper.signin_method(global_variables.config, role)
        self.org_id = raiden_helper.parse_org_id_from_user_role(role, global_variables.config, self.token)
        adduser_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(self.org_id) + '/associate'
        print("adduser_url is:", adduser_url)
        emails = []
        for i in range(1):
            emails.append(f'mobile+qa+{i}@gmail.com')
        user_id, email = raiden_api_user_helper.add_enduser(role=role,
                                                            adduser_url=adduser_url,
                                                            token=self.token,
                                                            emails=emails)

        self.users_userid = user_id
        self.users_email = email

    def test_delete_end_user_in_sync_portal(self):

        role = 'AladdinOwner'
        global_variables.SYNC_ENV = 'raiden-prod-aladdin'
        user_email = 'mobile_qa_1@gmail.com'
        self.token = raiden_helper.signin_method(global_variables.config, role)
        self.org_id = raiden_helper.parse_org_id_from_user_role(role, global_variables.config, self.token)
        get_users_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + self.org_id + "/associate"

        delete_user_url = global_variables.config.BASE_URL + raiden_config.ORG_ENDPNT + str(self.org_id) + "/associate"

        emails = []
        for i in range(1):
            emails.append(f'mobile+qa+{i}@gmail.com')
        for user_email in emails:
            user_id = raiden_api_user_helper.get_end_user_id_from_email(user_email,
                                                                        get_users_url,
                                                                        self.token)
            response_delete_user = raiden_api_user_helper.delete_enduser_role(user_id, delete_user_url, self.token)

    def test_get_end_user_group(self):
        role = "AladdinOwner"
        email_id = "sanjeev.vc@gmail.com"
        global_variables.SYNC_ENV = 'raiden-prod-aladdin'

        self.token = raiden_helper.signin_method(global_variables.config, role)
        self.org_id = raiden_helper.parse_org_id_from_user_role(role, global_variables.config, self.token)
        user_groups = raiden_api_user_helper.get_groups_associated_with_end_user(global_variables.config, role,
                                                                                 self.org_id, self.token, email_id)
        print(user_groups)

    def test_update_end_user_group(self):
        role = "AladdinOwner"
        user_id = self.users_userid
        email_id = "sanjeev.vc@gmail.com"
        new_group_name = "Mobile QA"
        group_name = "Default"
        global_variables.SYNC_ENV = 'raiden-prod-aladdin'

        self.token = raiden_helper.signin_method(global_variables.config, role)
        self.org_id = raiden_helper.parse_org_id_from_user_role(role, global_variables.config, self.token)

        end_users_url = f"{global_variables.config.BASE_URL}{raiden_config.ORG_ENDPNT}{self.org_id}/associate"

        user_id = raiden_api_user_helper.get_end_user_id_from_email(email_id,
                                                                    end_users_url,
                                                                    self.token)

        cohort_id = raiden_api_user_helper.get_end_user_group_id_by_group_name(global_variables.config, self.org_id,
                                                                               self.token, new_group_name)

        status_update_endusergrp = raiden_api_user_helper.update_withnewgroupname_for_enduser(group_name,
                                                                                              cohort_id,
                                                                                              end_users_url,
                                                                                              user_id, self.token)


if __name__ == "__main__":
    unittest.main()
