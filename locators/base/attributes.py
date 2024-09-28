from enum import Enum


class HtmlAttribute(Enum):
    class_ = '@class'
    data_testid = '@data-testid'
    draggable = '@draggable'
    id = '@id'
    name = 'name()'
    transform = '@transform'
    text = 'text()'
    data_theme = '@data-theme'
