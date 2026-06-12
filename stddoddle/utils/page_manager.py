import curses
from stddoddle.page import Page

"""
管理方式：
page 子类运行时注册(label)
切换页面：manager通过label查找
命令类型：
page manager命令：create switch
page 内部命令：通过page manager的parse调用执行


我打算给每个Page写一个虚拟屏幕，manager合并后输出到page_viewer中，
需要找一个字符来当空白字符（不是空格），用来表示非占用区域
"""

class PageManager:
    def __init__(self, page_viewer: curses.window):
        self._page_viewer = page_viewer
        self._registered_label: set[str] = set()
        self._head: Page|None = None
        self._tail: Page|None = None
        self._cur_page: Page|None = None 
    
    def switch_to(self, label: str):
        self._switch(label)

    def _switch(self, label: str|Page):
        # p = self.search_page(label) if type(label)==str else label
        if isinstance(label, str):
            p = self.search_page(label)
        else:
            p = label
        if not p:
            self._page_viewer.clear()
            self._page_viewer.refresh()
            # call warner
            return
        # assert(type(p)==Page)
        p.show()
        self._cur_page = p

    def show_next(self):
        if not self._cur_page or not self._head:
            # call warner
            return
        # assert(self._head)
        if self._cur_page == self._tail:
            self._switch(self._head)
        else:
            assert(self._cur_page.next)
            self._switch(self._cur_page.next)

    def _create(self, type: type[Page], label: str):
        if self._head and self._tail:
            # assert(self._tail)
            if not label in self._registered_label:
                p = type(self._page_viewer, self._tail, None, label)
                p.show()
                self._registered_label.add(label)
                self._tail.next = self._cur_page = p
                self._tail = self._tail.next
            else:
                # N: call warner
                pass
        else:
            p = type(self._page_viewer, None, None, label)
            p.show()
            self._registered_label.add(label)
            self._tail = self._head = self._cur_page = p


    def _parse(self, subcmd: str) -> bool:
        if self._cur_page:
            return self._cur_page.parse(subcmd)
        # N: call warner: command not found: "{subcmd}"
        return False

    def _destroy(self, label: str):
        if p:=self.search_page(label):
            if self._cur_page == p:
                if self._head == self._tail:
                    self._page_viewer.clear()
                    self._page_viewer.noutrefresh()
                    self._cur_page = None
                else:
                    self.show_next()
            if p.prev:
                p.prev.next = p.next
            else:
                self._head = p.next
            if p.next:
                p.next.prev = p.prev
            else:
                self._tail = p.prev
            self._registered_label.remove(label)
            p.destroy()
        else:
            # call warner: no page with label "{label}"
            return

    
    def search_page(self, label:str) -> Page|None:
        if not label in self._registered_label:
            return None
        p = self._head
        while p:
            if p.label == label:
                return p
            p = p.next