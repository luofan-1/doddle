from doddleconfig.timer_config import *
from stddoddle.utils.page import Page

# figure_style = [
#     "  ___   \n / _ \\  \n| | | | \n| | | | \n| |_| | \n \\___/  \n        ",
#     "  __    \n /_ |   \n  | |   \n  | |   \n  | |   \n  |_|   \n        ",
#     " ___    \n|__ \\   \n   ) |  \n  / /   \n / /_   \n|____|  \n        ",
#     " ____   \n|___ \\  \n  __) | \n |__ <  \n ___) | \n|____/  \n        ",
#     " _  _   \n| || |  \n| || |_ \n|__   _|\n   | |  \n   |_|  \n        ",
#     " _____  \n| ____| \n| |__   \n|___ \\  \n ___) | \n|____/  \n        ",
#     "   __   \n  / /   \n / /_   \n| '_ \\  \n| (_) | \n \\___/  \n        ",
#     " ______ \n|____  |\n    / / \n   / /  \n  / /   \n /_/    \n        ",
#     "  ___   \n / _ \\  \n| (_) | \n > _ <  \n| (_) | \n \\___/  \n        ",
#     "  ___   \n / _ \\  \n| (_) | \n \\__, | \n   / /  \n  /_/   \n        "
# ]
# divider_style = "    \n _  \n(_) \n _  \n(_) \n    \n    "

# style_height = 7

# # 预计算，避免每次调用重复 split
# FIGURES = [s.split("\n") for s in figure_style]
# DIVIDER = divider_style.split("\n")

class Timer(Page):
    def __init__(self, doddle) -> None:
        super().__init__(doddle)
        self.time_counted = 0
        self.time_text = ""
        # self.summary_text = ""

    def render(self):
        pass

    def _gen_time_text(self):
        m, s = divmod(self.time_counted, 60)
        h, m = divmod(m, 60)

        # 边界保护，防止索引越界
        def _digits(n):
            tens, ones = divmod(n, 10)
            if tens>9:
                print("时间超出范围，停止中")
                tens = 9
            return FIGURES[tens], FIGURES[ones]

        hdigits = _digits(h)
        mdigits = _digits(m)
        sdigits = _digits(s)

        lines = []
        for i in range(style_height):
            line = (hdigits[0][i] + hdigits[1][i] + DIVIDER[i]
                  + mdigits[0][i] + mdigits[1][i] + DIVIDER[i]
                  + sdigits[0][i] + sdigits[1][i])
            lines.append(line)

        self.time_text = "\n".join(lines)

# tm = Timer()
# tm.time_counted = 211120
# tm._gen_time_text()
# print(tm.time_text)