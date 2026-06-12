from curses import window
from collections.abc import Callable

class Page:
    _type = "BasePage"
    _commands: dict[str, Callable[[list[str]], bool]] = {}

    def __init__(self, page_viewer: window, prev, next, label:str="") -> None:
        self._page_viewer = page_viewer
        # doubly linked list
        self.next: Page|None = next
        self.prev: Page|None = prev
        self.label = label

    def parse(self, cmd: str) -> bool:
        args = cmd.split()
        if args[0] in self._commands:
            return self._commands[args[0]](args)
        return False

    def show(self):
        pass

    # abandoned
    def hide(self):
        pass

    def destroy(self):
        pass
    
    def render(self):
        pass