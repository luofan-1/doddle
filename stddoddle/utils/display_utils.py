import curses

def display_center(win: curses.window, str: str, attr: int=0):
    max_y, max_x = win.getmaxyx()
    line_num = str.count("\n")+1
    start_y = (max_y-line_num)//2
    for i, line in enumerate(str.split("\n")):
        start_x = (max_x-len(line))//2
        # print(f"{start_x:=}, {start_y:=}")
        win.addstr(start_y+i, start_x, line, attr)