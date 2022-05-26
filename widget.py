from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox


def but_plus(sc, x, y, xl, yl, str, rgb):
    but = Button(sc, x, y, xl, yl, text=str,
                 fontSize=25, margin=15,
                 textColour=(41, 49, 51),
                 inactiveColour=(rgb[0], rgb[1], rgb[2]),
                 shadowDistance=(2),
                 shadowColour=(41, 49, 51),
                 pressedColour=(227, 38, 54), radius=10
                 # ,onClick=lambda:
                 )
    return but


def but_whitetext(sc, x, y, xl, yl, str, rgb):
    but = Button(sc, x, y, xl, yl, text=str,
                 fontSize=25, margin=15,
                 textColour=(255, 255, 255),
                 inactiveColour=(rgb[0], rgb[1], rgb[2]),
                 shadowDistance=(2),
                 shadowColour=(41, 49, 51),
                 pressedColour=(227, 38, 54), radius=10
                 # ,onClick=lambda:
                 )
    return but


def textOutput(sc, x, y, xl, yl):
    text = TextBox(sc, x, y, xl, yl, colour=(255, 255, 255), fontSize=30, radius=15)
    return text
