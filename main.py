#! /d/projects/doddle/.doddleenv/Scripts/python

# 要实现的功能：
# 1. 异常警告系统
# 2. 导入系统

import curses
from curses import wrapper
from curses.textpad import Textbox

from stddoddle.utils.display import display_center
from stddoddle.utils.style_manager import StyleManager
from stddoddle.utils.warner import Warner
from doddleconfig.config import *

import time

class App:
    def __init__(self, stdscr):
        self.STYLE = StyleManager()

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
        self.cmd_input = Textbox(self.cmd_bar_input_win)


def main(stdscr):
    doddle = App(stdscr)

    while True:
        doddle.cmd_input.edit()

        input_text = doddle.cmd_input.gather().strip()
        # print(f"{input_text=}")
        doddle.cmd_bar_input_win.clear()
        if input_text in cmd_lib:
            cmd_lib[input_text]()
        else:
            doddle.warner.add_msg(f"command not found: {input_text}")

        doddle.warner.update()

        doddle.page_viewer.refresh()
        doddle.cmd_bar.refresh()

if __name__ == '__main__':
    wrapper(main)