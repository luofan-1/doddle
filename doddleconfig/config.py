import curses

# welcome page
greeting_view = r"""
    ____        ____  ____  __       
   / __ \____  / __ \/ __ \/ /   ___ 
  / / / / __ \/ / / / / / / /   / _ \
 / /_/ / /_/ / /_/ / /_/ / /___/  __/
/_____/\____/_____/_____/_____/\___/ 
----——————————-————-———————————————=#
"""
# greeting_view = r"""
#   ____        ____  ____  _         
#  |  _ \  ___ |  _ \|  _ \| |    ___ 
#  | | | |/ _ \| | | | | | | |   / _ \
#  | |_| | (_) | |_| | |_| | |__|  __/
#  |____/ \___/|____/|____/|_____\___|
# """

# warner
warning_duration = 1.5

# cmd_bar
cmd_bar_prompt = "> ", curses.A_BOLD

# cmd_lib
def _launch_timer(doddle):
    """惰性导入 timer 模块，创建页面对象，加载到 page_viewer。"""
    from stddoddle.timer import Timer
    doddle.timer_page = Timer(doddle.page_viewer)
    doddle.timer_page.render()


cmd_lib = {
    "exit": lambda _: exit(0),
    "timer": _launch_timer,
}