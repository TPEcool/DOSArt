from ttkbootstrap import *
from ttkbootstrap.scrolled import *
from typing import Callable
from tktooltip import ToolTip

def create(chars: tuple[str], parent: Labelframe, updatefunc: Callable, currentChar: str) -> ScrolledFrame:
    selchrs = tuple(i[0] for i in chars)

    charsel = ScrolledFrame(parent, autohide=True)
    WIDTH = 10 # characters

    class _ClickableLabel(Label):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            def charfunc(*args: object):
                updatefunc(charsel, self, kwargs['text'])

            self.bind('<Button-1>', charfunc)

    for ind, char in enumerate(selchrs):
        x = ind // WIDTH
        y = ind % WIDTH

        charframe = Frame(charsel, style=DARK, width=32, height=32)
        charframe.grid(row=x, column=y)

        charlabel = _ClickableLabel(charframe, text=char, font=('Modern DOS 9x16', 32), relief=SUNKEN if char == currentChar else FLAT)
        charlabel.pack(side=TOP)

        ToolTip(charlabel, chars[ind][3:-1])
        
    return charsel