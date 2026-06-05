import curses
from curses import wrapper

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    stdscr.clear()
    stdscr.refresh()
    pad = curses.newpad(10, curses.COLS)
    pad.addstr("1111111111111111111111111111111111111111111111afakfnfaekjnfaiaeefnefbaeiufaeoinaoiednafneiaefnoienaofnaeoifannaeoiffawoeihfeoifneoaifnoaiabgoiaeianeiofbaoiebfaofnea;ofna;oebfa;fa'fna'fna'oeifeni", curses.color_pair(1))
    pad.refresh(0, 0, 0, 0, 1, curses.COLS-1)
    stdscr.getch()

wrapper(main)

# import curses
# from curses import wrapper

# def main(stdscr):
#     stdscr.clear()
#     rows, cols = stdscr.getmaxyx()
#     pad = curses.newpad(10, cols)
#     pad.addstr(0, 0, "11111")
#     # 参数：pad_y,pad_x, scr_top, scr_left, scr_bottom, scr_right
#     pad.refresh(0, 0, 0, 0, 0, cols - 1)
#     stdscr.getch()

# wrapper(main)