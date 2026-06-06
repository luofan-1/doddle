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

        # self.warning_pad = curses.newpad(10, curses.COLS)
        self.warner = Warner()

        self.cmd_bar = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.cmd_bar.addstr(*cmd_bar_prompt)
        self.cmd_bar.refresh()
        self.cmd_bar_input_win = self.cmd_bar.derwin(0, len(cmd_bar_prompt[0]))
        self.cmd_bar_input_win.nodelay(True)
        # self.cmd_input = Textbox(self.cmd_bar_input_win)
        self.cmd_input = NonblockingTextbox(self.cmd_bar_input_win)


def main(stdscr):
    doddle = App(stdscr)

    while True:
        # bug01: 错误提示只有在敲击键盘后才会消失
        input_text = doddle.cmd_input.nonblocking_edit()
        # curses.doupdate()

        if input_text:
            if input_text in cmd_lib:
                cmd_lib[input_text]()
            else:
                doddle.warner.add_msg(f"command not found: {input_text}")

        doddle.warner.update()

        doddle.page_viewer.noutrefresh()
        doddle.cmd_bar.noutrefresh()

        # curses.doupdate()

if __name__ == '__main__':
    wrapper(main)