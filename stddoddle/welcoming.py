from stddoddle.utils.page import Page
from stddoddle.utils.display import display_center
from doddleconfig.config import greeting_view


class Welcome_Page(Page):
    def __init__(self, doddle) -> None:
        super().__init__(doddle)
        # display_center(doddle.page_viewer, greeting_view)

    # 渲染虚拟屏幕
    def render(self):
        display_center(self.doddle.page_viewer, greeting_view)