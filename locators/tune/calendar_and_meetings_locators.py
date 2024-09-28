from locators.base.elements import HtmlElement as El
from locators.locators_templates import xpath_by_data_testid, xpath_by_multiple_attributes_chained
from locators.base.attributes import HtmlAttribute


class TuneCalendarAndMeetingsLocators:
    BACK_BUTTON = xpath_by_data_testid(El.any, "screen.button.back")
    TITLE_LABEL = xpath_by_data_testid(El.p, "screen.title")

    SHOW_NON_VIDEO_MEETINGS_LABEL = xpath_by_data_testid(El.div,
                                                         "appSettings.calendarAgendaEnabledBody.checkbox.noVideo")
    SHOW_NON_VIDEO_MEETINGS_CHECKBOX = xpath_by_multiple_attributes_chained(
        (El.div, HtmlAttribute.data_testid, "appSettings.calendarAgendaEnabledBody.checkbox.noVideo"),
        (El.input, None, None)
    )
    SHOW_NON_VIDEO_MEETINGS_TOGGLE = xpath_by_multiple_attributes_chained(
        (El.div, HtmlAttribute.data_testid, "appSettings.calendarAgendaEnabledBody.checkbox.noVideo"),
        (El.any, HtmlAttribute.data_testid, 'checkbox.thumb')
    )

    SHOW_ALL_DAY_MEETINGS_LABEL = xpath_by_data_testid(El.div,
                                                         "appSettings.calendarAgendaEnabledBody.checkbox.allDayMeetings")
    SHOW_ALL_DAY_MEETINGS_CHECKBOX = xpath_by_multiple_attributes_chained(
        (El.div, HtmlAttribute.data_testid, "appSettings.calendarAgendaEnabledBody.checkbox.allDayMeetings"),
        (El.input, None, None)
    )
    SHOW_ALL_DAY_MEETINGS_TOGGLE = xpath_by_multiple_attributes_chained(
        (El.div, HtmlAttribute.data_testid, "appSettings.calendarAgendaEnabledBody.checkbox.allDayMeetings"),
        (El.any, HtmlAttribute.data_testid, 'checkbox.thumb')
    )

    SHOW_DECLINED_MEETINGS_LABEL = xpath_by_data_testid(El.div,
                                                         "appSettings.calendarAgendaEnabledBody.checkbox.declinedMeetings")
    SHOW_DECLINED_MEETINGS_CHECKBOX = xpath_by_multiple_attributes_chained(
        (El.div, HtmlAttribute.data_testid, "appSettings.calendarAgendaEnabledBody.checkbox.declinedMeetings"),
        (El.input, None, None)
    )
    SHOW_DECLINED_MEETINGS_TOGGLE = xpath_by_multiple_attributes_chained(
        (El.div, HtmlAttribute.data_testid, "appSettings.calendarAgendaEnabledBody.checkbox.declinedMeetings"),
        (El.any, HtmlAttribute.data_testid, 'checkbox.thumb')
    )

