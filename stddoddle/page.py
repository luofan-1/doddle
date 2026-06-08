class Page:
    def __init__(self, doddle, label:str="") -> None:
        self.doddle = doddle
        self.label = label
        self._type = "BasePage"

    def _show(self):
        pass

    def _hide(self):
        pass        

    def _destroy(self):
        pass
    
    def render(self):
        pass