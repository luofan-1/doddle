import curses
import time
from collections import deque
from ...doddleconfig.config import warning_duration

class Warner:
    def __init__(self):
        self.msgs = deque()
        self.displayer = curses.newpad(20, curses.COLS)
        self.on_display = 0 # 当前显示的行数
        