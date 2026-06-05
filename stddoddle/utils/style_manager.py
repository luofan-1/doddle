import curses

class StyleManager:
    FRED_BBLACK = 0

    def __init__(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        FRED_BBLACK = curses.color_pair(1)