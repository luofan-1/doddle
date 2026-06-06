import time
import curses
import time
# from collections import deque
from doddleconfig.config import warning_duration
from stddoddle.utils import style_manager

PAD_CAPACITY = 10

class Warner:
    def __init__(self):
        self._msg_queue = []
        self._displayed_msg = []

        self._displayer = curses.newpad(PAD_CAPACITY, curses.COLS)
        self._pad_head = 0
        self._pad_tail = 0
        # self.nlines_on_display = 0 # 当前显示的行数

    def _pad_refresh(self):
        self._displayer.clear()
        if len(self._displayed_msg)==0:
            self._displayer.noutrefresh(0, 0, curses.LINES-11, 0, curses.LINES-2, curses.COLS-1)
            return

        cnt = 0
        for msgt in self._displayed_msg:
            self._displayer.addstr(cnt, 0, f'error: {msgt[0]}', style_manager.FRED_BBLACK)
            cnt += 1
        
        # self.nlines_on_display = cnt
        self._displayer.noutrefresh(0, 0, curses.LINES-1-cnt, 0, curses.LINES-2, curses.COLS-1)

    def add_msg(self, msg):
        self._msg_queue.append(msg)

    def update(self):
        
        # 获取当前时间
        now = time.time()

        # 显示
        while self._msg_queue:
            msg = self._msg_queue.pop(0)
            self._displayed_msg.append((msg, now+warning_duration))

        # 消除显示
        # while self._displayed_msg and now>=self._displayed_msg[0][1]:
        #     self._displayed_msg.pop(0)
        self._displayed_msg = [
            (msg, expire_time) for msg, expire_time in self._displayed_msg
            if expire_time > now
        ]

        self._pad_refresh()