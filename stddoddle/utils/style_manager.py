import curses

class StyleManager:
    def __init__(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        self.FRED_BBLACK = curses.color_pair(1)