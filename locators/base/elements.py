from enum import Enum


class HtmlElement(Enum):
    any = '*'
    button = 'button'
    div = 'div'
    input = 'input'
    li = 'li'
    p = 'p'
    parent = '..'
    svg = "*[name()='svg']"
    defs = "*[name()='defs']"
    textarea = 'textarea'
    html = 'html'

    def __str__(self, *args, **kwargs):
        return self.value
