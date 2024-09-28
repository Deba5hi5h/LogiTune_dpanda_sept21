from locators.base.elements import HtmlElement as El
from locators.base.attributes import HtmlAttribute as Attr
from locators.locators_templates import xpath_by_data_testid, xpath_by_text, xpath_by_multiple_attributes, \
    xpath_by_class


class TuneMeetingDetailsPageLocators:

    MEETING_TITLE = xpath_by_data_testid(El.p, "meetingDetail.meetingTitle")
    MEETING_SUBTITLE = xpath_by_data_testid(El.p, "meetingDetail.meetingSubTitle")
    ATTENDEE_ITEM = xpath_by_data_testid(El.div, "meetingDetail.attendeeItem", strict_check=False)
    ATTENDEES_INFO = xpath_by_data_testid(El.p, "meetingDetail.attendees.info")
    EXTERNAL_LINK = xpath_by_data_testid(El.div, "meetingDetail.link.goToExternal")
    COPY_LINK = xpath_by_data_testid(El.div, 'meetingDetail.link.copy')
    BACK_TO_DASHBOARD = xpath_by_data_testid(El.svg, 'meetingDetail.button.back')

