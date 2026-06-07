#! /d/projects/doddle/.doddleenv/Scripts/python

import curses
from curses import wrapper
from curses.textpad import Textbox

from stddoddle.utils.display import display_center
from stddoddle.utils import style_manager
from stddoddle.utils.warner import Warner
from stddoddle.utils.nonblocking_textbox import NonblockingTextbox
from doddleconfig.config import *

import time

class App:
    def __init__(self, stdscr):
        style_manager.style_init()

        stdscr.clear()

        self.page_viewer = curses.newwin(curses.LINES-1, curses.COLS, 0, 0)
        display_center(self.page_viewer, greeting_view)
        self.page_viewer.refresh()
        
        self.warner = Warner()

        self.cmd_bar = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.cmd_bar.addstr(*cmd_bar_prompt)
        self.cmd_bar.refresh()
        self.cmd_bar_input_win = self.cmd_bar.derwin(0, len(cmd_bar_prompt[0]))
        self.cmd_bar_input_win.nodelay(True)
        self.cmd_input = NonblockingTextbox(self.cmd_bar_input_win)


def main(stdscr):
    doddle = App(stdscr)

    while True:
        
        doddle.cmd_bar.noutrefresh()
        doddle.page_viewer.noutrefresh()

        if doddle.warner.update():
            if not doddle.warner.is_active():
                doddle.page_viewer.touchwin()
                doddle.page_viewer.noutrefresh()
            curses.doupdate()

        input_text = doddle.cmd_input.nonblocking_edit()

        if input_text:
            if input_text in cmd_lib:
                cmd_lib[input_text]()
            else:
                # print(input_text)
                doddle.warner.add_msg(f"command not found: {input_text}")
        

if __name__ == '__main__':
    wrapper(main)