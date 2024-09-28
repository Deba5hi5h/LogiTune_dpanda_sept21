from apps.tune.base.base_testcase import TuneBaseTestCase
from extentreport.report import Report
from apps.collabos.coily.utilities import (prepare_tune_calendar_account_credentials,
                                           prepare_work_account_credentials)
from base.base_settings import GOOGLE, MICROSOFT
from dataclasses import dataclass, asdict
from typing import Optional, Union
from collections.abc import Mapping


@dataclass
class BaseMapping(Mapping):
    """
    A class representing a base mapping.

    This class extends the `Mapping` class and provides methods for converting an instance
    to a dictionary, retrieving an iterable of keyword arguments,
    and implementing the iterable interface.

    Methods:
        - as_dict: Converts the instance to a dictionary.
        - kwargs_iterable: Returns an iterable of keyword arguments.
        - __iter__: Returns an iterator over the keyword arguments.
        - __len__: Returns the number of keyword arguments.
        - __getitem__: Retrieves the value associated with a keyword argument.

    Example usage:
        mapping = BaseMapping()
        assert mapping.as_dict == {}
        assert mapping.kwargs_iterable == []
        assert len(mapping) == 0
        assert mapping["item"] == None
    """
    @property
    def as_dict(self):
        return asdict(self)

    @property
    def kwargs_iterable(self):
        return [el for el in self.as_dict.keys() if el != "is_coily"]

    def __iter__(self):
        return iter(self.kwargs_iterable)

    def __len__(self):
        return len(self.kwargs_iterable)

    def __getitem__(self, item):
        return self.as_dict.__getitem__(item)


@dataclass
class SignInPayload(BaseMapping):
    name: str
    surname: str
    email: str
    password: str
    employee_id: Optional[str] = None
    identifier: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.surname or not self.email or not self.password:
            raise ValueError('Some values of the SignInPayload are empty!')


@dataclass
class Credentials(BaseMapping):
    signin_payload: SignInPayload
    coily_user: bool

    def __post_init__(self):
        self.signin_payload = SignInPayload(**self.signin_payload)


@dataclass
class Account(BaseMapping):
    provider: str
    credentials: Union[dict, Credentials]

    def __post_init__(self):
        self.credentials = Credentials(**self.credentials)


class DeskBookingBaseTestCase(TuneBaseTestCase):

    google_credentials_coily = Account(
        GOOGLE, {**prepare_work_account_credentials(GOOGLE), "coily_user": True}
    )
    microsoft_credentials_coily = Account(
        MICROSOFT, {**prepare_work_account_credentials(MICROSOFT), "coily_user": True}
    )
    google_credentials_calendar = Account(
        GOOGLE, {**prepare_tune_calendar_account_credentials(GOOGLE), "coily_user": False}
    )
    microsoft_credentials_calendar = Account(
        MICROSOFT, {**prepare_tune_calendar_account_credentials(MICROSOFT), "coily_user": False}
    )

    def setUp(self, *args, **kwargs) -> None:
        super().setUp()
        self.tune_app.reopen_tune_app()
        self.scenario.tune_pages.home.click_home_tab()
        try:
            for credentials in self.google_credentials_coily, self.microsoft_credentials_coily:
                Report.logInfo(f"Deleting Bookings and events for user: "
                               f"{credentials.credentials.signin_payload.email}")
                self.scenario.sync_api_methods.delete_reservations_for_user(
                    credentials.credentials.signin_payload.identifier)
                Report.logInfo(f"Deleting Reservations for desk: {self.scenario.desk_id}")
                self.scenario.sync_api_methods.delete_reservations_for_desk(self.scenario.desk_id)
                self.scenario.delete_calendar_events(**credentials)
            self.scenario.tune_pages.home.click_refresh_button_and_wait_for_refresh()
        except Exception as e:
            pass

    @classmethod
    def setUpClass(cls, *args, **kwargs) -> None:
        super().setUpClass(*args, **kwargs)
        cls.tune_app.connect_tune_app()
        cls.tune_app.driver.implicitly_wait(0)
        cls.scenario.disconnect_connected_account_if_needed()
        cls.scenario.sync_api_methods.set_desks_default_settings(cls.scenario.desk_id)
        cls.scenario.sync_api_methods.enable_map_for_desks_floor(
            cls.scenario.org_id,
            cls.scenario.desk_id,
            False
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.scenario.disconnect_connected_account_if_needed()
        super().tearDownClass()

    @staticmethod
    def clear_teammates(scenario):
        scenario.tune_pages.home.click_home_tab()
        scenario.tune_pages.home.click_people_tab()
        scenario.tune_pages.people.click_teammates_tab_button()
        scenario.tune_pages.people.click_all_teammates_button()
        if scenario.tune_pages.people_team.verify_edit_button():
            scenario.tune_pages.people_team.click_edit_button()
            scenario.tune_pages.people_team_edit.delete_all_teammates()
            scenario.tune_pages.people_team_edit.click_done_button()
        scenario.tune_pages.people_team.click_back_button()
        scenario.tune_pages.home.click_home_tab()

    @staticmethod
    def delete_remaining_teams(scenario):
        scenario.tune_pages.home.click_home_tab()
        scenario.tune_pages.home.click_people_tab()
        scenario.tune_pages.people.click_teammates_tab_button()
        if scenario.tune_pages.people.verify_edit_teams_button():
            scenario.tune_pages.people.click_edit_teams_button()
            scenario.tune_pages.people_teams_edit.delete_all_teams()
            assert scenario.tune_pages.people_teams_edit.verify_no_teams_found(), \
                "Teams Delete Failed"
            scenario.tune_pages.people_teams_edit.click_done_button()
