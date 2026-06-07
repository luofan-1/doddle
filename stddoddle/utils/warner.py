import time
import curses
import time
# from collections import deque
from doddleconfig.config import warning_duration
from stddoddle.utils import style_manager

PAD_CAPACITY = 15

class Warner:
    def __init__(self):
        self._msg_queue = []
        self._displayed_msg = []
        # self._nlines_lastupdate = 0

        self._displayer = curses.newpad(PAD_CAPACITY, curses.COLS)
        # self._pad_head = 0
        # self._pad_tail = 0
        # self.nlines_on_display = 0 # 当前显示的行数

    def is_active(self):
        return len(self._displayed_msg)>0

    def _pad_refresh(self):
        self._displayer.clear()
        # print(self._displayed_msg)
        if len(self._displayed_msg)==0:
            self._displayer.noutrefresh(0, 0, curses.LINES-11, 0, curses.LINES-2, curses.COLS-1)
            # print("ok")
            return

        cnt = 0
        for msgt in self._displayed_msg:
            msg = f'error: {msgt[0]}'
            self._displayer.addstr(cnt, 0, msg, style_manager.FRED_BBLACK)
            cnt += 1
            self._displayer.noutrefresh(0, 0, curses.LINES-1-cnt, 0, curses.LINES-2, len(msg)-1)

    def add_msg(self, msg):
        self._msg_queue.append(msg)

    def update(self) -> bool:
        changed = False
        
        # 获取当前时间
        now = time.time()

        # 显示
        while self._msg_queue and (changed:=True):
            msg = self._msg_queue.pop(0)
            self._displayed_msg.append((msg, now+warning_duration))
        

        # 消除显示

        len_displayed_bf = len(self._displayed_msg)
        self._displayed_msg = [
            (msg, expire_time) 
            for msg, expire_time in self._displayed_msg 
            if expire_time>now
        ]
        if len(self._displayed_msg)!=len_displayed_bf:
            changed = True

        # if len(self._displayed_msg)<self._nlines_lastupdate:
            

        if changed:
            self._pad_refresh()
            # print(f"changed: {self._displayed_msg=}")

        return changed