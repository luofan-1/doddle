import curses


FRED_BBLACK = 0

def style_init():
    curses.start_color()
    global FRED_BBLACK
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    FRED_BBLACK = curses.color_pair(1)