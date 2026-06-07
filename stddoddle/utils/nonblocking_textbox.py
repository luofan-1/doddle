import curses
from curses import window

class NonblockingTextbox:
    def __init__(self, win: window):
        # super().__init__(win)
        self.win = win
        self.win.keypad(True)
        self.cursor_pos = 0
        self.buf = []
        self.input_text = ""

    # 放入循环内
    def nonblocking_edit(self):
        ch = self.win.getch()
        # if ch == -1:                                    # 无输入
        if ch in (10, 13):
            self.input_text = "".join(self.buf)
            self.buf.clear()
            self.cursor_pos = 0
            # self.win.move(0, 0)
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if self.cursor_pos>0:
                self.buf.pop(self.cursor_pos-1)
                self.cursor_pos -= 1
        elif ch==curses.KEY_LEFT:
            if self.cursor_pos>0:
                self.cursor_pos -= 1
        elif ch==curses.KEY_RIGHT:
            if self.cursor_pos<len(self.buf):
                self.cursor_pos += 1
        elif 32<=ch<=126:
            self.buf.insert(self.cursor_pos, chr(ch))
            self.cursor_pos += 1
        self.win.clear()
        self.win.addstr(0, 0, "".join(self.buf))
        self.win.move(0, self.cursor_pos)
        self.win.noutrefresh()

        return self.input_text if ch in (10, 13) else None