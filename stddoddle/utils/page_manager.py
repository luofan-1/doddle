import curses
from stddoddle.page import Page

class PageManager:
    def __init__(self, page_viewer: curses.window):
        self._page_viewer = page_viewer
        self._history = []

    def show_page(self, page: Page):
        if self._history:
            self._history[-1]._hide()
        page._show()
        self._history.append(page)

    def hide_page(self, page):
        if self

    def new_page(self) -> Page:
        pass
    
    def search_page_by_label(self, label:str) -> list[int]:
        return [
            i 
            for i in range(len(self._history)) 
            if self._history[i].label==label
        ]

    def destroy_page(self, label: str=""):
        if self._history:
            